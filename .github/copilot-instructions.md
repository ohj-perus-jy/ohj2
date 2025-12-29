# Copilot Instructions for ohj2

## Project Overview

This is an **mdBook-based course material** for "Ohjelmointi 2" (Programming 2), a Finnish university course teaching Java object-oriented programming. The site is built with Rust's mdBook static site generator with custom preprocessors and extensions.

## Architecture

- **Content**: Markdown files in [src/](../src/) organized by course sections (osa1-osa6, meaning "parts" 1-6)
- **Build output**: Generated HTML in [book/](../book/) (git-tracked for GitHub Pages)
- **Custom preprocessors**: 
  - Python: [preprocessors/python/accordion.py](../preprocessors/python/accordion.py) for tabbed content
  - Rust: [preprocessors/rust/mdbook-codeblock-tabs/](../preprocessors/rust/mdbook-codeblock-tabs/) for multi-file code blocks
- **Theme customizations**: JavaScript and CSS in [theme/](../theme/) for interactive features

## Development Workflow

### Quick start
```bash
bash ./start.sh  # Installs dependencies and serves on localhost:3000
```

### Manual setup
```bash
bash ./update-mdbook.sh  # Install mdbook + plugins via Cargo
mdbook serve --hostname 0.0.0.0 --port 3000 --open
```

The mdBook server auto-reloads on file changes. The task "mdbook: serve" runs on port 36742 in the dev container.

## Custom Markdown Extensions

### Multi-file code blocks
Use `// FILE:` and `// FILE_END` markers to create tabbed code examples:

```java
// FILE: main.java
public class Ohjelma {
    // code here
}
// FILE_END
// FILE: Kissa.java
public class Kissa {
    // code here
}
// FILE_END
```

Processed by the Rust preprocessor into interactive tabs.

### Code highlighting
Add color highlights with marker comments (removed from display):

```java
// HIGHLIGHT_GREEN_BEGIN
public Kissa(String name) {
// HIGHLIGHT_GREEN_END
```

Colors: `GREEN`, `YELLOW`, `RED`, `BLUE`. Defined in [theme/code-highlights.css](../theme/code-highlights.css), processed by [theme/code-highlights.js](../theme/code-highlights.js).

### Accordion tabs
Platform-specific instructions use accordion syntax:

```markdown
### [Windows](#tab/win)
Content for Windows
***
### [macOS](#tab/macos)
Content for macOS
***
### [Valitse](#tab/default)
Default visible tab
***
```

Processed by [preprocessors/python/accordion.py](../preprocessors/python/accordion.py).

### Task blocks
Exercise assignments use custom HTML tags:

```markdown
<task>
<task-title>Tehtävä 1.1: Oma ohjelma <points>1 p.</points></task-title>
<handout>
Exercise instructions here...
</handout>
<task-link><a href="...">Tee tehtävä TIMissa</a></task-link>
</task>
```

## Content Conventions

- **Language**: All content is in **Finnish**
- **Course structure**: Six main parts (osa1-osa6) covering Java basics to advanced topics
- **Exercises**: Linked to external TIM platform, handout files in [src/exercises/](../src/exercises/)
- **Navigation**: Defined in [src/SUMMARY.md](../src/SUMMARY.md)

## Configuration

- [book.toml](../book.toml): mdBook config, preprocessors, custom themes (jyu-light/jyu-dark)
- Preprocessors: `alerts`, `mermaid`, `katex`, `codeblock-tabs`, `accordion`, `plantuml`, `inline-highlighting`
- Edit links point to `github.com/ohj-perus-jy/ohj2/edit/main/{path}`

## When Editing Content

1. Modify markdown files in [src/](../src/), not generated HTML in [book/](../book/)
2. Follow existing patterns for FILE markers, HIGHLIGHT comments, and task blocks
3. mdBook auto-rebuilds on save - check browser for errors
4. Ensure code examples use Java syntax with proper indentation
5. Maintain Finnish language consistency

## Dependencies

Install via [update-mdbook.sh](../update-mdbook.sh):
- mdbook 0.4.52
- mdbook-mermaid 0.16.2
- mdbook-alerts 0.8.0
- mdbook-katex 0.9.4
- mdbook-plantuml 0.8.0
- mdbook-inline-highlighting 1.0.0
- Custom: mdbook-codeblock-tabs (local Rust crate)

Requires Rust/Cargo and Python 3.
