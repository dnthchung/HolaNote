from tkinter import Checkbutton, IntVar, Frame

class CheckBoxRenderer(Frame):
    def __init__(self, parent, tasks, on_update):
        super().__init__(parent)
        self.vars = []
        self.tasks = tasks
        self.on_update = on_update

        for index, (checked, text) in enumerate(tasks):
            var = IntVar(value=1 if checked else 0)
            cb = Checkbutton(self, text=text, variable=var, command=self.update_state)
            cb.pack(anchor="w")
            self.vars.append((var, text))

    def update_state(self):
        updated = []
        for var, text in self.vars:
            updated.append(("- [x] " if var.get() else "- [ ] ") + text)
        self.on_update(updated)
