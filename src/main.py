from tkinter import *
from markdown_utils import convert_markdown_to_html, extract_checkbox_tasks
from widgets import CheckBoxRenderer

NOTE_FILE = "../note.md"

class HolaNote:
    def __init__(self, root):
        self.root = root
        self.root.title("HolaNote")
        self.root.geometry("800x400")
        self.root.attributes("-topmost", True)

        self.left_frame = Frame(self.root)
        self.left_frame.pack(side=LEFT, fill=BOTH, expand=True)

        self.right_frame = Frame(self.root, bg="#f7f7f7")
        self.right_frame.pack(side=RIGHT, fill=BOTH, expand=True)

        self.text = Text(self.left_frame, font=("Consolas", 12))
        self.text.pack(fill=BOTH, expand=True)
        self.text.bind("<KeyRelease>", self.update_preview)
        self.root.bind("<Control-s>", self.save_note)

        self.checkbox_frame = Frame(self.right_frame, bg="#f7f7f7")
        self.checkbox_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

        try:
            with open(NOTE_FILE, "r", encoding="utf-8") as f:
                content = f.read()
                self.text.insert("1.0", content)
                self.render_checkboxes(content)
        except FileNotFoundError:
            pass

    def update_preview(self, event=None):
        content = self.text.get("1.0", END)
        self.render_checkboxes(content)

    def render_checkboxes(self, content):
        for widget in self.checkbox_frame.winfo_children():
            widget.destroy()

        tasks = extract_checkbox_tasks(content)
        if tasks:
            cb_renderer = CheckBoxRenderer(self.checkbox_frame, tasks, self.update_markdown_from_checkboxes)
            cb_renderer.pack(fill=BOTH, expand=True)

    def update_markdown_from_checkboxes(self, updated_lines):
        lines = self.text.get("1.0", END).splitlines()
        new_lines = []
        task_index = 0
        for line in lines:
            if line.strip().startswith("- [ ]") or line.strip().startswith("- [x]"):
                new_lines.append(updated_lines[task_index])
                task_index += 1
            else:
                new_lines.append(line)
        new_content = "\n".join(new_lines)
        self.text.delete("1.0", END)
        self.text.insert("1.0", new_content)
        self.save_note()

    def save_note(self, event=None):
        with open(NOTE_FILE, "w", encoding="utf-8") as f:
            f.write(self.text.get("1.0", END).strip())

if __name__ == "__main__":
    root = Tk()
    app = HolaNote(root)
    root.mainloop()
