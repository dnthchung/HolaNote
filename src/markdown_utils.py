import markdown

def convert_markdown_to_html(md_text):
    html = markdown.markdown(md_text, extensions=["fenced_code", "tables"])
    return html

def extract_checkbox_tasks(md_text):
    tasks = []
    lines = md_text.splitlines()
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("- [ ]"):
            tasks.append((False, stripped[5:].strip()))
        elif stripped.startswith("- [x]"):
            tasks.append((True, stripped[5:].strip()))
    return tasks
