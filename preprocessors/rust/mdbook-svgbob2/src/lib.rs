use mdbook_preprocessor::{
    book::{Book, BookItem},
    errors::Error,
    Preprocessor, PreprocessorContext,
};
use pulldown_cmark::{CodeBlockKind, Event, Options, Parser, Tag, TagEnd};
use pulldown_cmark_to_cmark::cmark;
use std::collections::BTreeMap;
use svgbob::Settings;

pub struct Bob;

impl Bob {
    pub fn new() -> Self {
        Self
    }
}

impl Default for Bob {
    fn default() -> Self {
        Self::new()
    }
}

impl Preprocessor for Bob {
    fn name(&self) -> &str {
        "svgbob2"
    }

    fn run(&self, ctx: &PreprocessorContext, mut book: Book) -> Result<Book, Error> {
        // first load the configuration from the book.toml
        // also apply some default settings that are good for mdbook
        let mut settings = svgbob::Settings {
            background: "transparent".to_owned(),
            stroke_color: "var(--fg)".to_owned(),
            ..Default::default()
        };

        let mut font_color = "var(--fg)".to_owned();

        // Read config from [preprocessor.svgbob2] table
        if let Ok(Some(cfg)) = ctx.config.get::<BTreeMap<String, toml::Value>>("preprocessor.svgbob2") {
            for (key, val) in &cfg {
                match key.as_str() {
                    "font_size" => if let Some(v) = val.as_integer() { settings.font_size = v as usize },
                    "font_family" => if let Some(v) = val.as_str() { settings.font_family = v.to_owned() },
                    "fill_color" => if let Some(v) = val.as_str() { settings.fill_color = v.to_owned() },
                    "background" => if let Some(v) = val.as_str() { settings.background = v.to_owned() },
                    "stroke_color" => if let Some(v) = val.as_str() { settings.stroke_color = v.to_owned() },
                    "stroke_width" => if let Some(v) = val.as_float() { settings.stroke_width = v as f32 },
                    "scale" => if let Some(v) = val.as_float() { settings.scale = v as f32 },
                    "enhance_circuitries" => if let Some(v) = val.as_bool() { settings.enhance_circuitries = v },
                    "include_backdrop" => if let Some(v) = val.as_bool() { settings.include_backdrop = v },
                    "include_styles" => if let Some(v) = val.as_bool() { settings.include_styles = v },
                    "include_defs" => if let Some(v) = val.as_bool() { settings.include_defs = v },
                    "merge_line_with_shapes" => if let Some(v) = val.as_bool() { settings.merge_line_with_shapes = v },
                    "font_color" => if let Some(v) = val.as_str() { font_color = v.to_owned() },
                    _ => (),
                }
            }
        }

        book.for_each_mut(|item| {
            if let BookItem::Chapter(chapter) = item {
                // saved to check if we are currently inside a codeblock
                let mut in_block = false;

                // if Windows crlf line endings are used, a code block will consist
                // of many different Text blocks, thus we need to buffer them in here
                // see https://github.com/raphlinus/pulldown-cmark/issues/507
                let mut diagram = String::new();
                let events =
                    Parser::new_ext(&chapter.content, Options::all()).filter_map(|event| {
                        match (&event, in_block) {
                            // check if we are entering a svgbob codeblock
                            (
                                Event::Start(Tag::CodeBlock(CodeBlockKind::Fenced(info))),
                                false,
                            ) if info.as_ref() == "svgbob" => {
                                in_block = true;
                                diagram.clear();
                                None
                            }
                            // check if we are currently inside an svgbob block
                            (Event::Text(content), true) => {
                                diagram.push_str(content);
                                None
                            }
                            // check if we are exiting an svgbob block
                            (
                                Event::End(TagEnd::CodeBlock),
                                true,
                            ) => {
                                in_block = false;
                                let html = create_svg_html(&diagram, &settings, &font_color);
                                Some(Event::Html(
                                    html.into(),
                                ))
                            }
                            // if nothing matches, change nothing
                            _ => Some(event),
                        }
                    });

                // create a buffer in which we can place the markdown
                let mut buf = String::with_capacity(chapter.content.len() + 128);

                // convert it back to markdown and replace the original chapter's content
                cmark(events, &mut buf).unwrap();
                
                chapter.content = buf;
            }
        });

        Ok(book)
    }

    fn supports_renderer(&self, renderer: &str) -> Result<bool, Error> {
        Ok(renderer == "html")
    }
}

fn create_svg_html(s: &str, settings: &Settings, font_color: &str) -> String {
    let svg = svgbob::to_svg_with_settings(s, settings);
    // Collapse newlines to prevent mdBook's markdown parser from splitting
    // the HTML block into multiple events and stripping SVG content
    let svg_oneline = svg.replace('\n', "");

    format!(
        "<pre class=\"svgbob\"><style>text{{fill:{}}}</style>{}</pre>",
        font_color, svg_oneline
    )
}
