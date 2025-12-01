use mdbook::BookItem;
use mdbook::book::{Book, Chapter};
use mdbook::errors::Result;
use mdbook::preprocess::{CmdPreprocessor, Preprocessor, PreprocessorContext};
use nanoid::nanoid;
use pulldown_cmark::{CodeBlockKind, Event, Options, Parser, Tag, TagEnd};
use regex::Regex;
use std::io;
use std::sync::LazyLock;

fn main() {
    let mut args = std::env::args().skip(1);
    match args.next().as_deref() {
        Some("supports") => {
            // Supports all renderers.
            return;
        }
        Some(arg) => {
            eprintln!("unknown argument: {arg}");
            std::process::exit(1);
        }
        None => {}
    }

    if let Err(e) = handle_preprocessing() {
        eprintln!("{e}");
        std::process::exit(1);
    }
}

pub fn handle_preprocessing() -> Result<()> {
    let pre = CodeBlockTabsPreprocessor;
    let (ctx, book) = CmdPreprocessor::parse_input(io::stdin())?;

    let processed_book = pre.run(&ctx, book)?;
    serde_json::to_writer(io::stdout(), &processed_book)?;

    Ok(())
}

struct CodeBlockTabsPreprocessor;

fn process_codeblock_event<'a>(lang: &str, code: &str) -> Vec<Event<'a>> {
    static FILE_PATTERN: LazyLock<Regex> = LazyLock::new(|| {
        Regex::new(
            r#"(?msx)
        ^[^\n]*?FILE:\s+(?P<filename>[\w\d.-_]+?)(?:\s.+?)??$
        \n
        (?P<code>.*?)
        \n
        ^[^\n]*?FILE_END(?:\s.+?)??$"#,
        )
        .unwrap()
    });

    let mut result = Vec::new();
    let mut filenames = Vec::new();
    let codeblock_id = format!("{}{}", nanoid!(2, &('a'..='z').into_iter().collect::<Vec<_>>()), nanoid!(10)); // first character is a letter to ensure valid HTML id

    for (i, capture) in FILE_PATTERN.captures_iter(&code).enumerate() {
        let filename = capture.name("filename").unwrap().as_str();
        let file_code = capture.name("code").unwrap().as_str();

        filenames.push(filename.to_string());

        // eprintln!("Found file block: {} with code:\n{}", filename, file_code);

        let custom_lang = format!(
            "{},codeblock-id-{},codeblock-file-num-{}",
            lang, codeblock_id, i
        );

        result.push(Event::Start(Tag::HtmlBlock));
        result.push(Event::Html(format!(
            r#"<section id="codeblock-{codeblock_id}-file-{i}" role="tabpanel" data-codeblock-id="{codeblock_id}" data-file-num="{i}" {}>
                <strong class="codeblock-tabs-title-print">{filename}</strong>{}"#,
            if i == 0 { r#"aria-hidden="false""# } else { r#"aria-hidden="true" hidden"# }, "\n")
         .into()));
        result.push(Event::End(TagEnd::HtmlBlock));
        result.push(Event::Start(Tag::CodeBlock(CodeBlockKind::Fenced(
            custom_lang.to_string().into(),
        ))));
        result.push(Event::Text(file_code.to_string().into()));
        result.push(Event::End(TagEnd::CodeBlock));
        result.push(Event::Start(Tag::HtmlBlock));
        result.push(Event::Html("</section>\n".into()));
        result.push(Event::End(TagEnd::HtmlBlock));
    }

    if !result.is_empty() {
        let mut html_header = "\n".to_string();
        html_header.push_str(&format!(
            r#"<div class="codeblock-tabs" id="{}"><ul class="codeblock-tabs-titles">"#,
            codeblock_id
        ));

        for (i, filename) in filenames.iter().enumerate() {
            html_header.push_str(&format!(
                r##"<li role="presentation">
                <a href="#codeblock-{codeblock_id}-file-{i}" role="tab" aria-controls="codeblock-{codeblock_id}-file-{i}" data-codeblock-id="{codeblock_id}" data-file-num="{i}" {}>
                {filename}
                </a>
                </li>"##,
                if i == 0 { r#"aria-selected="true" tabindex="0""# } else { r#"aria-selected="false" tabindex="-1""# },
            ));
        }

        html_header.push_str("</ul>");
        html_header.push_str(r#"<div class="codeblock-tabs-contents">"#);
        html_header.push_str("\n");

        result.insert(0, Event::Start(Tag::HtmlBlock));
        result.insert(1, Event::Html(html_header.into()));
        result.insert(2, Event::End(TagEnd::HtmlBlock));

        result.push(Event::Start(Tag::HtmlBlock));
        result.push(Event::Html("</div></div>\n".into()));
        result.push(Event::End(TagEnd::HtmlBlock));

        return result;
    }

    vec![
        Event::Start(Tag::CodeBlock(CodeBlockKind::Fenced(
            lang.to_string().into(),
        ))),
        Event::Text(code.to_string().into()),
        Event::End(TagEnd::CodeBlock),
    ]
}

fn create_tabbed_codeblocks(chapter: &mut Chapter) {
    let mut buf = String::with_capacity(chapter.content.len());
    let mut current_codeblock_lang = None;

    let mut opts = Options::empty();
    opts.insert(Options::ENABLE_TABLES);
    opts.insert(Options::ENABLE_FOOTNOTES);
    opts.insert(Options::ENABLE_STRIKETHROUGH);
    opts.insert(Options::ENABLE_TASKLISTS);
    let parser = Parser::new_ext(&chapter.content, opts);
    
    let mut text_buf = String::new();

    let parser = parser.flat_map(|event| match &event {
        Event::Start(Tag::CodeBlock(CodeBlockKind::Fenced(lang))) => {
            current_codeblock_lang = Some(lang.to_string());
            vec![]
        }
        Event::Text(text) => match &current_codeblock_lang {
            Some(_) => {
                // eprintln!("Got code block with lang = {}", lang);
                text_buf.push_str(text);
                vec![]
            }
            None => vec![event],
        },
        Event::End(TagEnd::CodeBlock) => match &current_codeblock_lang {
            Some(lang) => {
                let code_block = process_codeblock_event(lang, &text_buf);
                current_codeblock_lang = None;
                text_buf.clear();
                code_block
            }
            None => vec![event],
        },
        _ => vec![event],
    });

    match pulldown_cmark_to_cmark::cmark(parser, &mut buf) {
        Ok(_) => chapter.content = buf,
        Err(e) => eprintln!("Error converting markdown: {}", e),
    }
}

impl Preprocessor for CodeBlockTabsPreprocessor {
    fn name(&self) -> &str {
        "codeblock-tabs"
    }

    fn run(&self, _ctx: &PreprocessorContext, mut book: Book) -> Result<Book> {
        book.for_each_mut(|item| match item {
            BookItem::Chapter(ch) => create_tabbed_codeblocks(ch),
            _ => {}
        });
        Ok(book)
    }
}
