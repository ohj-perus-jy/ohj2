use mdbook::BookItem;
use mdbook::book::{Book, Chapter};
use mdbook::errors::Result;
use mdbook::preprocess::{CmdPreprocessor, Preprocessor, PreprocessorContext};
use nanoid::nanoid;
use pulldown_cmark::{CodeBlockKind, Event, Parser, Tag, TagEnd};
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
    let codeblock_id = nanoid!(10);

    for (i, capture) in FILE_PATTERN.captures_iter(&code).enumerate() {
        let filename = capture.name("filename").unwrap().as_str();
        let file_code = capture.name("code").unwrap().as_str();

        filenames.push(filename.to_string());

        eprintln!("Found file block: {} with code:\n{}", filename, file_code);

        let custom_lang = format!(
            "{},codeblock-id-{},codeblock-file-num-{}",
            lang, codeblock_id, i
        );
        result.push(Event::Start(Tag::CodeBlock(CodeBlockKind::Fenced(
            custom_lang.to_string().into(),
        ))));
        result.push(Event::Text(file_code.to_string().into()));
        result.push(Event::End(TagEnd::CodeBlock));
    }

    if !result.is_empty() {
        let mut html_header = "\n".to_string();
        html_header.push_str(&format!(
            r#"<div class="codeblock-tabs" id="{}"><ul class="codeblock-tabs-titles">"#,
            codeblock_id
        ));

        for (i, filename) in filenames.iter().enumerate() {
            html_header.push_str(&format!(
                r#"<li class="codeblock-tab-title" data-codeblock-file-num="{}">{}</li>"#,
                i, filename
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
    let parser = Parser::new(&chapter.content);
    let mut current_codeblock_lang = None;

    let parser = parser.flat_map(|event| match &event {
        Event::Start(Tag::CodeBlock(CodeBlockKind::Fenced(lang))) => {
            current_codeblock_lang = Some(lang.to_string());
            vec![]
        }
        Event::Text(text) => match &current_codeblock_lang {
            Some(lang) => {
                eprintln!("Got code block with lang = {}", lang);
                process_codeblock_event(lang, text)
            }
            None => vec![event],
        },
        Event::End(TagEnd::CodeBlock) => match &current_codeblock_lang {
            Some(_) => {
                current_codeblock_lang = None;
                vec![]
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
