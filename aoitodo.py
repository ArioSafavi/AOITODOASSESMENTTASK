import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json, os, hashlib
from datetime import datetime, date
from PIL import Image, ImageTk


DATA_FILE = "aoi_data.enc"
SECRET_KEY = b"AoiTodoSuperSecretKey_ChangeMe"
CONQUEST_IMG = "conquest.png"
AOT_FLASH_IMG = "aot_flash.png"


def _keystream(length: int):
    stream = b""
    counter = 0
    while len(stream) < length:
        h = hashlib.sha256(SECRET_KEY + counter.to_bytes(4, "big")).digest()
        stream += h
        counter += 1
    return stream[:length]


def encrypt(data: str) -> bytes:
    raw = data.encode("utf-8")
    ks = _keystream(len(raw))
    return bytes(a ^ b for a, b in zip(raw, ks))


def decrypt(data: bytes) -> str:
    ks = _keystream(len(data))
    raw = bytes(a ^ b for a, b in zip(data, ks))
    return raw.decode("utf-8", errors="ignore")


def load_data():
    if not os.path.exists(DATA_FILE):
        return {"users": {}}
    try:
        with open(DATA_FILE, "rb") as f:
            enc = f.read()
        raw = decrypt(enc)
        data = json.loads(raw)
        if "users" not in data:
            data["users"] = {}
        return data
    except Exception:
        return {"users": {}}


def save_data(data):
    enc = encrypt(json.dumps(data))
    with open(DATA_FILE, "wb") as f:
        f.write(enc)


def apply_theme(root, theme):
    style = ttk.Style(root)
    if theme in ("dark", "wallpaper", "watermark"):
        root.configure(bg="#1e1e1e")
        style.theme_use("clam")
        style.configure("TFrame", background="#1e1e1e")
        style.configure("TLabel", background="#1e1e1e", foreground="white", font=("Segoe UI", 11))
        style.configure("TButton", background="#3a3a3a", foreground="white", font=("Segoe UI", 11), padding=6)
        style.map("TButton", background=[("active", "#505050")])
        style.configure("Treeview", background="#2b2b2b", foreground="white",
                        fieldbackground="#2b2b2b", rowheight=26, font=("Segoe UI", 10))
        style.configure("Treeview.Heading", background="#3a3a3a", foreground="white",
                        font=("Segoe UI", 10, "bold"))
        style.map("Treeview", background=[("selected", "#5a5a5a")])
    else:
        root.configure(bg="#f5f5f5")
        style.theme_use("clam")
        style.configure("TFrame", background="#f5f5f5")
        style.configure("TLabel", background="#f5f5f5", foreground="#222", font=("Segoe UI", 11))
        style.configure("TButton", background="#ffffff", foreground="#222", font=("Segoe UI", 11), padding=6)
        style.map("TButton", background=[("active", "#e0e0e0")])
        style.configure("Treeview", background="#ffffff", foreground="#222",
                        fieldbackground="#ffffff", rowheight=26, font=("Segoe UI", 10))
        style.configure("Treeview.Heading", background="#e0e0e0", foreground="#222",
                        font=("Segoe UI", 10, "bold"))
        style.map("Treeview", background=[("selected", "#c0ddff")])


class Task:
    def __init__(self, title, due_date=None, priority=1, tags=None, completed=False,
                 created_at=None, completed_at=None, notified=False, time_block=None):
        self.title = title
        self.due_date = due_date
        self.priority = priority
        self.tags = tags or []
        self.completed = completed
        self.created_at = created_at or datetime.now().isoformat()
        self.completed_at = completed_at
        self.notified = notified
        self.time_block = time_block

    def to_dict(self):
        return {
            "title": self.title,
            "due_date": self.due_date,
            "priority": self.priority,
            "tags": self.tags,
            "completed": self.completed,
            "created_at": self.created_at,
            "completed_at": self.completed_at,
            "notified": self.notified,
            "time_block": self.time_block,
        }

    @staticmethod
    def from_dict(d):
        return Task(
            d["title"], d.get("due_date"), d.get("priority", 1),
            d.get("tags", []), d.get("completed", False),
            d.get("created_at"), d.get("completed_at"),
            d.get("notified", False), d.get("time_block"),
        )


class AoiTodoApp:
    def __init__(self, root):
        self.root = root
        self.themes = ["dark", "light", "wallpaper", "watermark"]
        self.theme_index = 0
        self.theme = self.themes[self.theme_index]
        apply_theme(root, self.theme)
        self.root.title("Aoi Todo")
        self.root.geometry("1000x600")
        self.root.minsize(900, 550)

        self.data = load_data()
        self.current_user = None
        self.tasks = []
        self.filter_mode = "all"
        self.bg_image = None
        self.bg_label = None
        self.watermark_image = None
        self.watermark_label = None

        self.login_window()

    def login_window(self):
        self.clear_root()
        apply_theme(self.root, self.theme)
        self.setup_wallpaper_background()

        frame = ttk.Frame(self.root, padding=20)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        ttk.Label(frame, text="Aoi Todo", font=("Segoe UI", 22, "bold")).pack(pady=(0, 10))
        ttk.Label(frame, text="Login or create an account").pack(pady=(0, 15))

        ttk.Label(frame, text="Username:").pack(anchor="w")
        self.username_entry = ttk.Entry(frame, width=30)
        self.username_entry.pack()

        ttk.Label(frame, text="Password:").pack(anchor="w", pady=(10, 0))
        self.password_entry = ttk.Entry(frame, show="*", width=30)
        self.password_entry.pack()

        btn_row = ttk.Frame(frame)
        btn_row.pack(pady=15)
        ttk.Button(btn_row, text="Login", command=self.login).pack(side="left", padx=5)
        ttk.Button(btn_row, text="Register", command=self.register).pack(side="left", padx=5)
        ttk.Button(frame, text=f"Theme: {self.theme}", command=self.toggle_theme).pack()

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        users = self.data["users"]
        if username not in users or users[username]["password"] != password:
            messagebox.showerror("Error", "Invalid login")
            return
        self.current_user = username
        self.load_user_data()
        self.main_window()

    def register(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        if not username or not password:
            messagebox.showerror("Error", "Enter username and password")
            return
        if username in self.data["users"]:
            messagebox.showerror("Error", "User already exists")
            return
        self.data["users"][username] = {"password": password, "tasks": [], "logins": [], "templates": []}
        save_data(self.data)
        messagebox.showinfo("Success", "Account created. You can now log in.")

    def load_user_data(self):
        user = self.data["users"][self.current_user]
        user["logins"].append(datetime.now().isoformat())
        self.tasks = [Task.from_dict(t) for t in user.get("tasks", [])]
        save_data(self.data)

    def save_user_data(self):
        if not self.current_user:
            return
        self.data["users"][self.current_user]["tasks"] = [t.to_dict() for t in self.tasks]
        save_data(self.data)

    def main_window(self):
        self.clear_root()
        apply_theme(self.root, self.theme)
        self.setup_wallpaper_background()

        header_bg = "#252525" if self.theme in ("dark", "wallpaper", "watermark") else "#e0e0e0"
        header_fg = "white" if self.theme in ("dark", "wallpaper", "watermark") else "#222"
        header = tk.Frame(self.root, bg=header_bg, height=50)
        header.pack(fill="x")
        tk.Label(header, text="Aoi Todo", bg=header_bg, fg=header_fg,
                 font=("Segoe UI", 16, "bold")).pack(side="left", padx=15)
        tk.Label(header, text=self.current_user, bg=header_bg,
                 fg="#bbb" if self.theme in ("dark", "wallpaper", "watermark") else "#555",
                 font=("Segoe UI", 10)).pack(side="left")
        ttk.Button(header, text=f"Theme: {self.theme}", command=self.toggle_theme).pack(side="right", padx=5)
        ttk.Button(header, text="Logout", command=self.logout).pack(side="right", padx=5)

        sidebar_bg = "#202020" if self.theme in ("dark", "wallpaper", "watermark") else "#f0f0f0"
        sidebar_fg = "white" if self.theme in ("dark", "wallpaper", "watermark") else "#222"
        sidebar = tk.Frame(self.root, bg=sidebar_bg, width=220)
        sidebar.pack(side="left", fill="y")

        tk.Label(sidebar, text="Views", bg=sidebar_bg, fg=sidebar_fg,
                 font=("Segoe UI", 11, "bold")).pack(anchor="w", padx=15, pady=(15, 5))
        ttk.Button(sidebar, text="All tasks", command=lambda: self.set_filter("all")).pack(fill="x", padx=10, pady=2)
        ttk.Button(sidebar, text="Today", command=lambda: self.set_filter("today")).pack(fill="x", padx=10, pady=2)
        ttk.Button(sidebar, text="Completed", command=lambda: self.set_filter("completed")).pack(fill="x", padx=10, pady=2)

        tk.Label(sidebar, text="Actions", bg=sidebar_bg, fg=sidebar_fg,
                 font=("Segoe UI", 11, "bold")).pack(anchor="w", padx=15, pady=(15, 5))
        ttk.Button(sidebar, text="Add Task", command=self.add_task_dialog).pack(fill="x", padx=10, pady=2)

        main = ttk.Frame(self.root)
        main.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        if self.theme == "watermark":
            self.apply_watermark(main)

        search_frame = ttk.Frame(main)
        search_frame.pack(fill="x", pady=(0, 5))
        ttk.Label(search_frame, text="Search / Filter:").pack(side="left")
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *args: self.refresh_task_list())
        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        self.search_entry.pack(side="left", fill="x", expand=True, padx=5)
        ttk.Button(search_frame, text="Edit", command=self.edit_task_dialog).pack(side="left", padx=2)
        ttk.Button(search_frame, text="Delete", command=self.delete_task).pack(side="left", padx=2)
        ttk.Button(search_frame, text="Complete", command=self.mark_complete).pack(side="left", padx=2)

        cols = ("title", "due", "priority", "tags", "status")
        self.tree = ttk.Treeview(main, columns=cols, show="headings")
        for c in cols:
            self.tree.heading(c, text=c.capitalize())
        self.tree.pack(fill="both", expand=True)
        self.refresh_task_list()

    def setup_wallpaper_background(self):
        if self.bg_label:
            self.bg_label.destroy()
            self.bg_label = None
        if self.theme == "wallpaper":
            try:
                img = Image.open("todo.png")
                w = self.root.winfo_screenwidth()
                h = self.root.winfo_screenheight()
                img = img.resize((w, h))
                self.bg_image = ImageTk.PhotoImage(img)
                self.bg_label = tk.Label(self.root, image=self.bg_image)
                self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
                self.bg_label.lower()
            except Exception:
                self.bg_label = None

    def apply_watermark(self, parent):
        try:
            img = Image.open("todo.png").convert("RGBA")
            img = img.resize((300, 300))
            img.putalpha(80)
            self.watermark_image = ImageTk.PhotoImage(img)
            self.watermark_label = tk.Label(parent, image=self.watermark_image,
                                            bg=parent.cget("background"), borderwidth=0, highlightthickness=0)
            self.watermark_label.place(relx=0.5, rely=0.5, anchor="center")
            self.watermark_label.lower()
        except Exception as e:
            print("Watermark failed:", e)

    def toggle_theme(self):
        self.theme_index = (self.theme_index + 1) % len(self.themes)
        self.theme = self.themes[self.theme_index]
        if self.current_user:
            self.main_window()
        else:
            self.login_window()

    def logout(self):
        self.save_user_data()
        self.current_user = None
        self.tasks = []
        self.login_window()

    def clear_root(self):
        for w in self.root.winfo_children():
            w.destroy()
        self.bg_label = None
        self.watermark_label = None

    def set_filter(self, mode):
        self.filter_mode = mode
        self.refresh_task_list()

    def parse_simple_filters(self, query, task: Task):
        parts = query.split()
        for p in parts:
            if ":" in p:
                key, val = p.split(":", 1)
                key = key.lower()
                val = val.lower()
                if key == "priority":
                    try:
                        if task.priority != int(val):
                            return False
                    except ValueError:
                        return False
                elif key == "tag":
                    if not any(val in t.lower() for t in task.tags):
                        return False
                elif key == "due":
                    if val == "today":
                        if task.due_date != date.today().isoformat():
                            return False
                    else:
                        if task.due_date != val:
                            return False
        words = [w for w in parts if ":" not in w]
        for w in words:
            if w.lower() not in task.title.lower() and not any(w.lower() in t.lower() for t in task.tags):
                return False
        return True

    def refresh_task_list(self):
        if not hasattr(self, "tree"):
            return
        query = self.search_var.get().strip() if hasattr(self, "search_var") else ""
        for i in self.tree.get_children():
            self.tree.delete(i)

        def passes(t):
            if self.filter_mode == "today":
                return t.due_date == date.today().isoformat()
            if self.filter_mode == "completed":
                return t.completed
            return True

        for t in sorted(self.tasks, key=lambda x: (x.completed, x.priority, x.due_date or "9999-12-31")):
            if not passes(t):
                continue
            if query and not self.parse_simple_filters(query, t):
                continue
            tb = ""
            if t.time_block:
                tb = f"{t.time_block.get('date','')} {t.time_block.get('time','')}"
            self.tree.insert("", "end", values=(t.title, t.due_date or "", t.priority,
                                                ", ".join(t.tags),
                                                "Done" if t.completed else "Pending", tb))

    def add_task_dialog(self, template=None):
        base_title = template.get("title", "") if template else ""
        base_priority = template.get("priority", 2) if template else 2
        base_tags = ", ".join(template.get("tags", [])) if template else ""

        title = simpledialog.askstring("Task", "Task title:", initialvalue=base_title)
        if not title:
            return
        due = simpledialog.askstring("Due date", "YYYY-MM-DD or blank:") or None
        priority = simpledialog.askinteger("Priority", "1=High 3=Low:", minvalue=1, maxvalue=3, initialvalue=base_priority)
        if priority is None:
            priority = base_priority
        tags_str = simpledialog.askstring("Tags", "Comma separated tags:", initialvalue=base_tags) or ""
        tags = [t.strip() for t in tags_str.split(",") if t.strip()]
        task = Task(title, due or None, priority, tags)
        self.tasks.append(task)
        self.save_user_data()
        self.refresh_task_list()
        self.check_easter_egg(task)

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

    def edit_task_dialog(self):
        task = self.get_selected_task()
        if not task:
            return
        title = simpledialog.askstring("Task", "Task title:", initialvalue=task.title)
        if not title:
            return
        due = simpledialog.askstring("Due date", "YYYY-MM-DD or blank:", initialvalue=task.due_date or "")
        priority = simpledialog.askinteger("Priority", "1=High 3=Low:", initialvalue=task.priority, minvalue=1, maxvalue=3)
        if priority is None:
            priority = task.priority
        tags_str = simpledialog.askstring("Tags", "Comma separated tags:", initialvalue=", ".join(task.tags)) or ""
        tags = [t.strip() for t in tags_str.split(",") if t.strip()]
        task.title = title
        task.due_date = due or None
        task.priority = priority
        task.tags = tags
        self.save_user_data()
        self.refresh_task_list()
        self.check_easter_egg(task)

    def delete_task(self):
        task = self.get_selected_task()
        if not task:
            return
        if messagebox.askyesno("Delete", f"Delete '{task.title}'?"):
            self.tasks.remove(task)
            self.save_user_data()
            self.refresh_task_list()

    def mark_complete(self):
        task = self.get_selected_task()
        if not task:
            return
        task.completed = True
        task.completed_at = datetime.now().isoformat()
        self.save_user_data()
        self.refresh_task_list()
        self.show_conquest_popup(mode="normal")

    def check_easter_egg(self, task):
        t = task.title.strip().upper()
        if t == "AOITODO" and task.due_date == "2024-09-23":
            try:
                img = Image.open("todo.png").resize((300, 300))
                img_tk = ImageTk.PhotoImage(img)
                win = tk.Toplevel(self.root)
                win.title("Aoi Todo Easter Egg")
                bg = "#1e1e1e" if self.theme in ("dark", "wallpaper", "watermark") else "#f5f5f5"
                win.configure(bg=bg)
                lbl = tk.Label(win, image=img_tk, bg=bg)
                lbl.image = img_tk
                lbl.pack(padx=20, pady=20)
            except Exception as e:
                messagebox.showerror("Error", f"Easter egg image not found.\n{e}")
        if t == "VILTRUMITE":
            self.show_conquest_popup(mode="jumpscare")
        if t == "CONQUEST":
            self.show_conquest_popup(mode="special")
        if t == "AOT":
            self.flash_aot()

    def show_conquest_popup(self, mode="normal"):
        img_path = CONQUEST_IMG
        if mode == "special" and os.path.exists(CONQUEST_IMG):
            img_path = CONQUEST_IMG
        if mode == "jumpscare" and os.path.exists(CONQUEST_IMG):
            img_path = CONQUEST_IMG

        win = tk.Toplevel(self.root)
        win.title("Conquest")
        win.overrideredirect(True)
        win.update_idletasks()
        w, h = 400, 400
        x = (win.winfo_screenwidth() - w) // 2
        y = (win.winfo_screenheight() - h) // 2
        win.geometry(f"{w}x{h}+{x}+{y}")
        win.configure(bg="#000000")

        try:
            img = Image.open(img_path).resize((350, 350))
            img_tk = ImageTk.PhotoImage(img)
            lbl = tk.Label(win, image=img_tk, bg="#000000")
            lbl.image = img_tk
            lbl.pack(padx=10, pady=10)
        except Exception:
            tk.Label(win, text="CONQUEST", fg="white", bg="#000000",
                     font=("Segoe UI", 20, "bold")).pack(expand=True)



        win.after(5000, win.destroy)



    def flash_aot(self):
        win = tk.Toplevel(self.root)
        win.overrideredirect(True)
        win.configure(bg="black")
        win.update_idletasks()
        w, h = 500, 300
        x = (win.winfo_screenwidth() - w) // 2
        y = (win.winfo_screenheight() - h) // 2
        win.geometry(f"{w}x{h}+{x}+{y}")
        if os.path.exists(AOT_FLASH_IMG):
            try:
                img = Image.open(AOT_FLASH_IMG).resize((w, h))
                img_tk = ImageTk.PhotoImage(img)
                lbl = tk.Label(win, image=img_tk, bg="black")
                lbl.image = img_tk
                lbl.pack(fill="both", expand=True)
            except Exception:
                tk.Label(win, text="AOT", fg="white", bg="black",
                         font=("Segoe UI", 24, "bold")).pack(expand=True)
        else:
            tk.Label(win, text="AOT", fg="white", bg="black",
                     font=("Segoe UI", 24, "bold")).pack(expand=True)
        win.after(1500, win.destroy)


if __name__ == "__main__":
    root = tk.Tk()
    app = AoiTodoApp(root)
    root.mainloop()
