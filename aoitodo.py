import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime, date


class Task:
    def __init__(self, title, due_date=None, priority=1, tags=None):
        self.title = title
        self.due_date = due_date
        self.priority = priority
        self.tags = tags or []
        self.completed = False
        self.created_at = datetime.now().isoformat()
        self.completed_at = None

    def to_dict(self):
        return {
            "title": self.title,
            "due_date": self.due_date,
            "priority": self.priority,
            "tags": self.tags,
            "completed": self.completed,
            "created_at": self.created_at,
            "completed_at": self.completed_at,
        }

    @staticmethod
    def from_dict(d):
        t = Task(
            d["title"],
            d.get("due_date"),
            d.get("priority", 1),
            d.get("tags", []),
        )
        t.completed = d.get("completed", False)
        t.created_at = d.get("created_at", datetime.now().isoformat())
        t.completed_at = d.get("completed_at")
        return t


class AoiTodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Aoi Todo")
        self.root.geometry("900x550")
        self.tasks = []
        self.filter_mode = "all"
        self.build_ui()

    def build_ui(self):
        header = tk.Frame(self.root, bg="#252525", height=50)
        header.pack(fill="x")
        tk.Label(header, text="Aoi Todo", bg="#252525", fg="white",
                 font=("Segoe UI", 16, "bold")).pack(side="left", padx=15)

        sidebar = tk.Frame(self.root, bg="#202020", width=200)
        sidebar.pack(side="left", fill="y")

        tk.Label(sidebar, text="Views", bg="#202020", fg="white",
                 font=("Segoe UI", 11, "bold")).pack(anchor="w", padx=15, pady=(15, 5))
        tk.Button(sidebar, text="All tasks", command=lambda: self.set_filter("all"),
                  bg="#2a2a2a", fg="white", relief="flat").pack(fill="x", padx=10, pady=2)
        tk.Button(sidebar, text="Today", command=lambda: self.set_filter("today"),
                  bg="#2a2a2a", fg="white", relief="flat").pack(fill="x", padx=10, pady=2)
        tk.Button(sidebar, text="Completed", command=lambda: self.set_filter("completed"),
                  bg="#2a2a2a", fg="white", relief="flat").pack(fill="x", padx=10, pady=2)

        tk.Label(sidebar, text="Actions", bg="#202020", fg="white",
                 font=("Segoe UI", 11, "bold")).pack(anchor="w", padx=15, pady=(15, 5))
        tk.Button(sidebar, text="Add Task", command=self.add_task_dialog,
                  bg="#2a2a2a", fg="white", relief="flat").pack(fill="x", padx=10, pady=2)

        main = tk.Frame(self.root, bg="#1e1e1e")
        main.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        btn_row = tk.Frame(main, bg="#1e1e1e")
        btn_row.pack(fill="x", pady=(0, 5))
        tk.Button(btn_row, text="Delete", command=self.delete_task,
                  bg="#3a3a3a", fg="white", relief="flat").pack(side="left", padx=2)
        tk.Button(btn_row, text="Complete", command=self.mark_complete,
                  bg="#3a3a3a", fg="white", relief="flat").pack(side="left", padx=2)

        cols = ("title", "due", "priority", "tags", "status")
        self.tree = ttk.Treeview(main, columns=cols, show="headings")
        for c in cols:
            self.tree.heading(c, text=c.capitalize())
        self.tree.pack(fill="both", expand=True)
        self.refresh_task_list()

    def set_filter(self, mode):
        self.filter_mode = mode
        self.refresh_task_list()

    def refresh_task_list(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        def passes(t):
            if self.filter_mode == "today":
                return t.due_date == date.today().isoformat()
            if self.filter_mode == "completed":
                return t.completed
            return True

        for t in sorted(self.tasks, key=lambda x: (x.completed, x.priority, x.due_date or "9999")):
            if not passes(t):
                continue
            status = "Done" if t.completed else "Pending"
            self.tree.insert("", "end", values=(t.title, t.due_date or "", t.priority,
                                                ", ".join(t.tags), status))

    def add_task_dialog(self):
        title = simpledialog.askstring("Task", "Task title:")
        if not title:
            return
        due = simpledialog.askstring("Due date", "YYYY-MM-DD or blank:") or None
        priority = simpledialog.askinteger("Priority", "1=High 3=Low:", minvalue=1, maxvalue=3, initialvalue=2)
        if priority is None:
            priority = 2
        tags_str = simpledialog.askstring("Tags", "Comma separated tags:") or ""
        tags = [t.strip() for t in tags_str.split(",") if t.strip()]
        self.tasks.append(Task(title, due or None, priority, tags))
        self.refresh_task_list()

    def get_selected_task(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showerror("Error", "No task selected")
            return None
        vals = self.tree.item(sel[0], "values")
        for t in self.tasks:
            if t.title == vals[0] and (t.due_date or "") == vals[1]:
                return t
        return None

    def delete_task(self):
        task = self.get_selected_task()
        if not task:
            return
        if messagebox.askyesno("Delete", f"Delete '{task.title}'?"):
            self.tasks.remove(task)
            self.refresh_task_list()

    def mark_complete(self):
        task = self.get_selected_task()
        if not task:
            return
        task.completed = True
        task.completed_at = datetime.now().isoformat()
        self.refresh_task_list()


if __name__ == "__main__":
    root = tk.Tk()
    root.configure(bg="#1e1e1e")
    app = AoiTodoApp(root)
    root.mainloop()