import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
import json, os, hashlib
from datetime import datetime, date, timedelta
from PIL import Image, ImageTk


DATA_FILE = "aoi_data.enc"
SECRET_KEY = b"AoiTodoSuperSecretKey_ChangeMe"

CONQUEST_IMG = "conquest.png"
AOT_FLASH_IMG = "aot_flash.png"


def _keystream(length: int):
    # builds a repeating SHA-256 keystream long enough to XOR against the data
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
    return bytes(a ^ b for a, b in zip(raw, ks))  # XOR is reversible, same op decrypts


def decrypt(data: bytes) -> str:
    ks = _keystream(len(data))
    raw = bytes(a ^ b for a, b in zip(data, ks))
    return raw.decode("utf-8", errors="ignore")


def load_data():
    if not os.path.exists(DATA_FILE):
        return {"users": {}}  # first run, no save file yet
    try:
        with open(DATA_FILE, "rb") as f:
            enc = f.read()
        raw = decrypt(enc)
        data = json.loads(raw)
        if "users" not in data:
            data["users"] = {}
        return data
    except Exception:
        return {"users": {}}  # corrupted or unreadable file, don't crash on launch


def save_data(data):
    raw = json.dumps(data)
    enc = encrypt(raw)
    with open(DATA_FILE, "wb") as f:
        f.write(enc)


def apply_theme(root, theme: str):
    # called on every window/dialog so dark and light mode stay consistent app-wide
    style = ttk.Style(root)
    if theme in ("dark", "wallpaper"):
        root.configure(bg="#1e1e1e")
        style.theme_use("clam")  # clam lets us actually override colours, default theme ignores them
        style.configure("TFrame", background="#1e1e1e")
        style.configure("TLabel", background="#1e1e1e", foreground="white", font=("Segoe UI", 11))
        style.configure("TButton", background="#3a3a3a", foreground="white",
                        font=("Segoe UI", 11), padding=6)
        style.map("TButton", background=[("active", "#505050")])  # hover colour
        style.configure("Treeview",
                        background="#2b2b2b",
                        foreground="white",
                        fieldbackground="#2b2b2b",
                        rowheight=26,
                        font=("Segoe UI", 10))
        style.configure("Treeview.Heading",
                        background="#3a3a3a",
                        foreground="white",
                        font=("Segoe UI", 10, "bold"))
        style.map("Treeview", background=[("selected", "#5a5a5a")])  # selected row colour
    else:  # light theme
        root.configure(bg="#f5f5f5")
        style.theme_use("clam")
        style.configure("TFrame", background="#f5f5f5")
        style.configure("TLabel", background="#f5f5f5", foreground="#222", font=("Segoe UI", 11))
        style.configure("TButton", background="#ffffff", foreground="#222",
                        font=("Segoe UI", 11), padding=6)
        style.map("TButton", background=[("active", "#e0e0e0")])
        style.configure("Treeview",
                        background="#ffffff",
                        foreground="#222",
                        fieldbackground="#ffffff",
                        rowheight=26,
                        font=("Segoe UI", 10))
        style.configure("Treeview.Heading",
                        background="#e0e0e0",
                        foreground="#222",
                        font=("Segoe UI", 10, "bold"))
        style.map("Treeview", background=[("selected", "#c0ddff")])


class Task:
    def __init__(self, title, due_date=None, priority=1, tags=None, completed=False,
                 created_at=None, completed_at=None, notified=False,
                 time_block=None):
        self.title = title
        self.due_date = due_date
        self.priority = priority
        self.tags = tags or []  # avoids the mutable default argument trap
        self.completed = completed
        self.created_at = created_at or datetime.now().isoformat()
        self.completed_at = completed_at
        self.notified = notified
        self.time_block = time_block

    def to_dict(self):
        # flattens the task into a plain dict so it can be JSON serialised
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
        # .get() with defaults so older save files missing newer fields still load fine
        return Task(
            d["title"],
            d.get("due_date"),
            d.get("priority", 1),
            d.get("tags", []),
            d.get("completed", False),
            d.get("created_at"),
            d.get("completed_at"),
            d.get("notified", False),
            d.get("time_block"),
        )


class AoiTodoApp:
    def __init__(self, root):
        self.root = root
        self.themes = ["dark", "light", "wallpaper"]
        self.theme_index = 0
        self.theme = self.themes[self.theme_index]
        apply_theme(root, self.theme)
        self.root.title("Aoi Todo")
        self.root.geometry("1000x600")
        self.root.minsize(900, 550)

        self.data = load_data()  # whole encrypted user database lives in memory while running
        self.current_user = None
        self.tasks = []
        self.templates = []
        self.filter_mode = "all"

        self.bg_image = None  # needs a reference held or tkinter garbage collects the image
        self.bg_label = None

        self.login_window()

    def login_window(self):
        self.clear_root()  # wipe whatever was on screen before (logout, theme switch, etc.)
        apply_theme(self.root, self.theme)
        self.setup_wallpaper_background()

        frame = ttk.Frame(self.root, padding=20)
        frame.place(relx=0.5, rely=0.5, anchor="center")  # centres the login box regardless of window size

        ttk.Label(frame, text="Aoi Todo", font=("Segoe UI", 22, "bold")).pack(pady=(0, 10))
        ttk.Label(frame, text="Login or create an account").pack(pady=(0, 15))

        ttk.Label(frame, text="Username:").pack(anchor="w")
        self.username_entry = ttk.Entry(frame, width=30)
        self.username_entry.pack()

        ttk.Label(frame, text="Password:").pack(anchor="w", pady=(10, 0))
        self.password_entry = ttk.Entry(frame, show="*", width=30)  # show="*" masks the typed password
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
        if username in self.data["users"]:  # block duplicate accounts
            messagebox.showerror("Error", "User already exists")
            return
        self.data["users"][username] = {
            "password": password,
            "tasks": [],
            "logins": [],
            "templates": []
        }
        save_data(self.data)
        messagebox.showinfo("Success", "Account created. You can now log in.")

    def load_user_data(self):
        user = self.data["users"][self.current_user]
        user["logins"].append(datetime.now().isoformat())  # track login for analytics later
        self.tasks = [Task.from_dict(t) for t in user.get("tasks", [])]
        self.templates = user.get("templates", [])
        save_data(self.data)

    def save_user_data(self):
        if not self.current_user:  # nothing to save if nobody's logged in
            return
        user = self.data["users"][self.current_user]
        user["tasks"] = [t.to_dict() for t in self.tasks]
        user["templates"] = self.templates
        save_data(self.data)  # re-encrypts and writes the whole file every save, not just this user

    def main_window(self):
        self.clear_root()
        apply_theme(self.root, self.theme)
        self.setup_wallpaper_background()

        # File menu for JSON import/export
        menubar = tk.Menu(self.root)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Import JSON", command=self.import_json)
        file_menu.add_command(label="Export JSON", command=self.export_json)
        menubar.add_cascade(label="File", menu=file_menu)
        self.root.config(menu=menubar)

        header_bg = "#252525" if self.theme in ("dark", "wallpaper") else "#e0e0e0"
        header_fg = "white" if self.theme in ("dark", "wallpaper") else "#222"

        # top header bar with app name, current user, theme toggle, logout
        header = tk.Frame(self.root, bg=header_bg, height=50)
        header.pack(fill="x")

        tk.Label(header,
                 text="Aoi Todo",
                 bg=header_bg,
                 fg=header_fg,
                 font=("Segoe UI", 16, "bold")
                 ).pack(side="left", padx=15)

        tk.Label(header,
                 text=f"{self.current_user}",
                 bg=header_bg,
                 fg="#bbbbbb" if self.theme in ("dark", "wallpaper") else "#555",
                 font=("Segoe UI", 10)
                 ).pack(side="left")

        ttk.Button(header, text=f"Theme: {self.theme}", command=self.toggle_theme).pack(side="right", padx=5)
        ttk.Button(header, text="Logout", command=self.logout).pack(side="right", padx=5)

        sidebar_bg = "#202020" if self.theme in ("dark", "wallpaper") else "#f0f0f0"
        sidebar_fg = "white" if self.theme in ("dark", "wallpaper") else "#222"

        # left sidebar with view filters and action shortcuts
        sidebar = tk.Frame(self.root, bg=sidebar_bg, width=220)
        sidebar.pack(side="left", fill="y")

        tk.Label(sidebar,
                 text="Views",
                 bg=sidebar_bg,
                 fg=sidebar_fg,
                 font=("Segoe UI", 11, "bold")
                 ).pack(anchor="w", padx=15, pady=(15, 5))

        ttk.Button(sidebar, text="All tasks", command=lambda: self.set_filter("all")).pack(fill="x", padx=10, pady=2)
        ttk.Button(sidebar, text="Today", command=lambda: self.set_filter("today")).pack(fill="x", padx=10, pady=2)
        ttk.Button(sidebar, text="Completed", command=lambda: self.set_filter("completed")).pack(fill="x", padx=10, pady=2)

        tk.Label(sidebar,
                 text="Actions",
                 bg=sidebar_bg,
                 fg=sidebar_fg,
                 font=("Segoe UI", 11, "bold")
                 ).pack(anchor="w", padx=15, pady=(15, 5))

        ttk.Button(sidebar, text="Add Task", command=self.add_task_dialog).pack(fill="x", padx=10, pady=2)
        ttk.Button(sidebar, text="Templates", command=self.open_templates_window).pack(fill="x", padx=10, pady=2)
        ttk.Button(sidebar, text="Analytics", command=self.show_analytics).pack(fill="x", padx=10, pady=2)
        ttk.Button(sidebar, text="Pomodoro", command=self.pomodoro_dialog).pack(fill="x", padx=10, pady=2)

        main = ttk.Frame(self.root)
        main.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        # search bar + edit/delete/complete buttons sit above the task table
        search_frame = ttk.Frame(main)
        search_frame.pack(fill="x", pady=(0, 5))

        ttk.Label(search_frame, text="Search / Filter:").pack(side="left")
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *args: self.refresh_task_list())  # live filtering as you type
        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        self.search_entry.pack(side="left", fill="x", expand=True, padx=5)

        ttk.Button(search_frame, text="Edit", command=self.edit_task_dialog).pack(side="left", padx=2)
        ttk.Button(search_frame, text="Delete", command=self.delete_task).pack(side="left", padx=2)
        ttk.Button(search_frame, text="Complete", command=self.mark_complete).pack(side="left", padx=2)

        # main task table
        columns = ("title", "due", "priority", "tags", "status")
        self.tree = ttk.Treeview(main, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col.capitalize())
        self.tree.pack(fill="both", expand=True)

        self.refresh_task_list()

    def setup_wallpaper_background(self):
        if self.bg_label:  # remove any previous background before drawing a new one
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
                self.bg_label.lower()  # push behind every other widget
            except Exception:
                self.bg_label = None  # todo.png missing, just skip the background silently

    def toggle_theme(self, event=None):
        self.theme_index = (self.theme_index + 1) % len(self.themes)  # cycles through the theme list
        self.theme = self.themes[self.theme_index]
        if self.current_user:
            self.main_window()  # rebuild whichever screen is currently showing
        else:
            self.login_window()

    def logout(self):
        self.save_user_data()  # persist before wiping the in-memory session
        self.current_user = None
        self.tasks = []
        self.templates = []
        self.login_window()

    def clear_root(self):
        for w in self.root.winfo_children():  # destroy every widget so the next screen starts fresh
            w.destroy()
        self.bg_label = None

    def set_filter(self, mode):
        self.filter_mode = mode
        self.refresh_task_list()

    def parse_simple_filters(self, query, task: Task):
        parts = query.split()
        for p in parts:
            if ":" in p:  # key:value filters like priority:1 or tag:school
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
        words = [w for w in parts if ":" not in w]  # everything left over is a plain text search
        for w in words:
            if w.lower() not in task.title.lower() and not any(w.lower() in t.lower() for t in task.tags):
                return False
        return True

    def refresh_task_list(self):
        if not hasattr(self, "tree"):  # tree doesn't exist outside the main window
            return
        query = self.search_var.get().strip() if hasattr(self, "search_var") else ""
        for i in self.tree.get_children():  # clear the table before redrawing it
            self.tree.delete(i)

        def passes_filter(t: Task):
            if self.filter_mode == "all":
                return True
            if self.filter_mode == "today":
                if not t.due_date:
                    return False
                return t.due_date == date.today().isoformat()
            if self.filter_mode == "completed":
                return t.completed
            return True

        sorted_tasks = sorted(self.tasks, key=lambda t: (t.completed, t.priority, t.due_date or "9999-12-31"))  # incomplete tasks first, then priority, then soonest due
        for t in sorted_tasks:
            if not passes_filter(t):
                continue
            if query:
                if not self.parse_simple_filters(query, t):
                    continue
            status = "Done" if t.completed else "Pending"
            tags_str = ", ".join(t.tags)
            tb = ""
            if t.time_block:
                tb = f"{t.time_block.get('date','')} {t.time_block.get('time','')}"  # display string for the time block column
            self.tree.insert("", "end",
                             values=(t.title, t.due_date or "", t.priority, tags_str, status, tb))

    def add_task_dialog(self, template=None):
        if template:  # pre-fill the dialog fields from a template if one was passed in
            base_title = template.get("title", "")
            base_priority = template.get("priority", 2)
            base_tags = ", ".join(template.get("tags", []))
        else:
            base_title = ""
            base_priority = 2
            base_tags = ""

        title = simpledialog.askstring("Task", "Task title:", initialvalue=base_title)
        if not title:  # cancel/empty input aborts the whole flow
            return
        due = simpledialog.askstring("Due date", "YYYY-MM-DD or blank:", initialvalue="")
        if due == "":
            due = None
        priority = simpledialog.askinteger("Priority", "1=High, 3=Low:",
                                           minvalue=1, maxvalue=3,
                                           initialvalue=base_priority)
        if priority is None:  # user dismissed the dialog, fall back to default
            priority = base_priority
        tags_str = simpledialog.askstring("Tags", "Comma separated tags:", initialvalue=base_tags) or ""
        tags = [t.strip() for t in tags_str.split(",") if t.strip()]
        new_task = Task(title, due, priority, tags)
        self.tasks.append(new_task)
        self.save_user_data()
        self.refresh_task_list()
        self.check_easter_egg(new_task)  # check if the title/date combo triggers a hidden feature

    def get_selected_task(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showerror("Error", "No task selected")
            return None
        values = self.tree.item(sel[0], "values")
        for t in self.tasks:
            if t.title == values[0] and (t.due_date or "") == values[1]:  # match title + due date, not just title
                return t
        return None

    def edit_task_dialog(self):
        task = self.get_selected_task()
        if not task:
            return
        title = simpledialog.askstring("Task", "Task title:", initialvalue=task.title)  # pre-fills with current values
        if not title:
            return
        due = simpledialog.askstring("Due date", "YYYY-MM-DD or blank:", initialvalue=task.due_date or "")
        if due == "":
            due = None
        priority = simpledialog.askinteger("Priority", "1=High, 3=Low:",
                                           initialvalue=task.priority, minvalue=1, maxvalue=3)
        if priority is None:
            priority = task.priority
        tags_str = simpledialog.askstring("Tags", "Comma separated tags:", initialvalue=", ".join(task.tags))
        tags = [t.strip() for t in tags_str.split(",") if t.strip()]
        task.title = title  # mutate the existing Task object directly rather than creating a new one
        task.due_date = due
        task.priority = priority
        task.tags = tags
        self.save_user_data()
        self.refresh_task_list()
        self.check_easter_egg(task)

    def delete_task(self):
        task = self.get_selected_task()
        if not task:
            return
        if messagebox.askyesno("Delete", f"Delete task '{task.title}'?"):  # confirm before destructive action
            self.tasks.remove(task)
            self.save_user_data()
            self.refresh_task_list()

    def mark_complete(self):
        task = self.get_selected_task()
        if not task:
            return
        task.completed = True
        task.completed_at = datetime.now().isoformat()  # timestamp used later for analytics duration calcs
        self.save_user_data()
        self.refresh_task_list()
        self.show_conquest_popup()  # reward popup on every completion

    def show_analytics(self):
        completed = [t for t in self.tasks if t.completed and t.completed_at]
        if not completed:
            messagebox.showinfo("Analytics", "No completed tasks yet.")
            return
        durations = []
        for t in completed:
            try:
                start = datetime.fromisoformat(t.created_at)
                end = datetime.fromisoformat(t.completed_at)
                durations.append((end - start).total_seconds() / 3600)  # convert to hours
            except Exception:
                continue
        avg_hours = sum(durations) / len(durations) if durations else 0
        user = self.data["users"][self.current_user]
        login_count = len(user.get("logins", []))  # total logins recorded for this account
        messagebox.showinfo(
            "Analytics",
            f"Completed tasks: {len(completed)}\n"
            f"Average completion time: {avg_hours:.2f} hours\n"
            f"Total logins: {login_count}"
        )


    def pomodoro_dialog(self):
        work = simpledialog.askinteger("Pomodoro", "Work minutes:", minvalue=1, maxvalue=120, initialvalue=25)
        if work is None:  # user cancelled, don't start a timer
            return
        rest = simpledialog.askinteger("Pomodoro", "Break minutes:", minvalue=1, maxvalue=60, initialvalue=5)
        if rest is None:
            return
        self.start_pomodoro(work, rest)

    def start_pomodoro(self, work_minutes, break_minutes):
        win = tk.Toplevel(self.root)  # separate popup window so it can run alongside the main app
        win.title("Pomodoro Timer")
        bg = "#1e1e1e" if self.theme in ("dark", "wallpaper") else "#f5f5f5"
        fg = "white" if self.theme in ("dark", "wallpaper") else "#222"
        win.configure(bg=bg)

        label = tk.Label(win, text="", font=("Segoe UI", 20), bg=bg, fg=fg)
        label.pack(padx=20, pady=20)

        state = {"phase": "work", "remaining": work_minutes * 60}  # seconds remaining in the current phase

        def tick():
            r = state["remaining"]
            mins = r // 60
            secs = r % 60
            label.config(text=f"{state['phase'].capitalize()} — {mins:02d}:{secs:02d}")
            if r <= 0:
                if state["phase"] == "work":
                    messagebox.showinfo("Pomodoro", "Work session done! Break time.")
                    state["phase"] = "break"  # switch phase and restart the countdown
                    state["remaining"] = break_minutes * 60
                else:
                    messagebox.showinfo("Pomodoro", "Break finished!")
                    win.destroy()
                    return
            else:
                state["remaining"] -= 1
            win.after(1000, tick)  # reschedule itself every second

        tick()  # kick off the first tick immediately

    def export_json(self):
        if not self.tasks:
            messagebox.showinfo("Export", "No tasks to export.")
            return
        path = filedialog.asksaveasfilename(defaultextension=".json",
                                            filetypes=[("JSON files", "*.json")])
        if not path:  # user cancelled the save dialog
            return
        data = [t.to_dict() for t in self.tasks]
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)  # exported as plain unencrypted JSON, unlike the save file
            messagebox.showinfo("Export", "Tasks exported successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export.\n{e}")

    def import_json(self):
        path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if not path:
            return
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            imported = [Task.from_dict(d) for d in data]
            self.tasks.extend(imported)  # adds to existing tasks rather than replacing them
            self.save_user_data()
            self.refresh_task_list()
            messagebox.showinfo("Import", f"Imported {len(imported)} tasks.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to import.\n{e}")

    def open_templates_window(self):
        win = tk.Toplevel(self.root)
        win.title("Task Templates")
        apply_theme(win, self.theme)
        win.geometry("400x350")

        frame = ttk.Frame(win)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.template_listbox = tk.Listbox(frame)
        self.template_listbox.pack(fill="both", expand=True)

        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill="x", pady=5)

        ttk.Button(btn_frame, text="Add", command=self.add_template).pack(side="left", padx=2)
        ttk.Button(btn_frame, text="Edit", command=self.edit_template).pack(side="left", padx=2)
        ttk.Button(btn_frame, text="Delete", command=self.delete_template).pack(side="left", padx=2)
        ttk.Button(btn_frame, text="Use", command=self.use_template).pack(side="right", padx=2)

        self.refresh_template_listbox()

        if not self.templates:  # give new users a few starter templates instead of an empty list
            self.templates.extend([
                {"title": "School assignment", "tags": ["school"], "priority": 2},
                {"title": "Workout routine", "tags": ["health"], "priority": 2},
                {"title": "Daily review", "tags": ["reflection"], "priority": 1},
            ])
            self.save_user_data()
            self.refresh_template_listbox()

    def refresh_template_listbox(self):
        if not hasattr(self, "template_listbox"):
            return
        self.template_listbox.delete(0, "end")
        for t in self.templates:
            title = t.get("title", "Untitled")
            tags = ", ".join(t.get("tags", []))
            pr = t.get("priority", 2)
            self.template_listbox.insert("end", f"{title} [p{pr}] ({tags})")  # single-line summary per template

    def add_template(self):
        title = simpledialog.askstring("Template", "Template name:")
        if not title:
            return
        tags_str = simpledialog.askstring("Template", "Default tags (comma separated):") or ""
        tags = [t.strip() for t in tags_str.split(",") if t.strip()]
        priority = simpledialog.askinteger("Template", "Default priority (1-3):",
                                           minvalue=1, maxvalue=3, initialvalue=2)
        if priority is None:
            priority = 2
        tmpl = {"title": title, "tags": tags, "priority": priority}  # templates are plain dictionaries not Task objects
        self.templates.append(tmpl)
        self.save_user_data()
        self.refresh_template_listbox()

    def get_selected_template(self):
        if not hasattr(self, "template_listbox"):
            return None
        sel = self.template_listbox.curselection()
        if not sel:
            messagebox.showerror("Error", "No template selected")
            return None
        idx = sel[0]
        if idx < 0 or idx >= len(self.templates):  # guards against a stale index after the list changes
            return None
        return self.templates[idx], idx

    def edit_template(self):
        res = self.get_selected_template()
        if not res:
            return
        tmpl, idx = res
        title = simpledialog.askstring("Template", "Template name:", initialvalue=tmpl.get("title", ""))
        if not title:
            return
        tags_str = simpledialog.askstring("Template", "Default tags (comma separated):",
                                          initialvalue=", ".join(tmpl.get("tags", []))) or ""
        tags = [t.strip() for t in tags_str.split(",") if t.strip()]
        priority = simpledialog.askinteger("Template", "Default priority (1-3):",
                                           minvalue=1, maxvalue=3,
                                           initialvalue=tmpl.get("priority", 2))
        if priority is None:
            priority = tmpl.get("priority", 2)
        tmpl["title"] = title
        tmpl["tags"] = tags
        tmpl["priority"] = priority
        self.templates[idx] = tmpl
        self.save_user_data()
        self.refresh_template_listbox()

    def delete_template(self):
        res = self.get_selected_template()
        if not res:
            return
        tmpl, idx = res
        if messagebox.askyesno("Delete", f"Delete template '{tmpl.get('title','')}'?"):
            del self.templates[idx]
            self.save_user_data()
            self.refresh_template_listbox()

    def use_template(self):
        res = self.get_selected_template()
        if not res:
            return
        tmpl, _ = res
        self.add_task_dialog(template=tmpl)  # reuses the normal add flow, just pre-filled

    def check_easter_egg(self, task):
        title_upper = task.title.strip().upper()  # case-insensitive matching against the trigger words

        if title_upper == "AOITODO" and task.due_date == "2024-09-23":  # secret combo for the launch date egg
            try:
                img = Image.open("todo.png")
                img = img.resize((300, 300))
                img_tk = ImageTk.PhotoImage(img)
                win = tk.Toplevel(self.root)
                win.title("Aoi Todo Easter Egg")
                bg = "#1e1e1e" if self.theme in ("dark", "wallpaper") else "#f5f5f5"
                win.configure(bg=bg)
                lbl = tk.Label(win, image=img_tk, bg=bg)
                lbl.image = img_tk  # keep a reference or tkinter discards the image
                lbl.pack(padx=20, pady=20)
            except Exception as e:
                messagebox.showerror("Error", f"Easter egg image not found.\n{e}")

        if title_upper == "VILTRUMITE":
            self.show_conquest_popup()

        if title_upper == "CONQUEST":
            self.show_conquest_popup()

        if title_upper == "AOT":
            self.flash_aot()

    def show_conquest_popup(self):
        img_path = CONQUEST_IMG

        win = tk.Toplevel(self.root)
        win.title("Conquest")
        win.overrideredirect(True)  # removes window borders/title bar for a fullscreen-style popup

        win.update_idletasks()
        w, h = 400, 400
        sw = win.winfo_screenwidth()
        sh = win.winfo_screenheight()
        x = (sw - w) // 2  # centres the popup on screen
        y = (sh - h) // 2
        win.geometry(f"{w}x{h}+{x}+{y}")

        bg = "#000000"
        win.configure(bg=bg)

        try:
            img = Image.open(img_path)
            img = img.resize((350, 350))
            img_tk = ImageTk.PhotoImage(img)
            lbl = tk.Label(win, image=img_tk, bg=bg)
            lbl.image = img_tk
            lbl.pack(padx=10, pady=10)
        except Exception:
            tk.Label(win, text="CONQUEST", fg="white", bg=bg,  # fallback text if the image file is missing
                     font=("Segoe UI", 20, "bold")).pack(expand=True)

        win.after(5000, win.destroy)  # auto-closes after 5 seconds

    def flash_aot(self):
        win = tk.Toplevel(self.root)
        win.overrideredirect(True)
        win.configure(bg="black")
        win.update_idletasks()
        w, h = 500, 300
        sw = win.winfo_screenwidth()
        sh = win.winfo_screenheight()
        x = (sw - w) // 2
        y = (sh - h) // 2
        win.geometry(f"{w}x{h}+{x}+{y}")

        if os.path.exists(AOT_FLASH_IMG):
            try:
                img = Image.open(AOT_FLASH_IMG)
                img = img.resize((w, h))
                img_tk = ImageTk.PhotoImage(img)
                lbl = tk.Label(win, image=img_tk, bg="black")
                lbl.image = img_tk
                lbl.pack(fill="both", expand=True)
            except Exception:
                tk.Label(win, text="AOT", fg="white", bg="black",
                         font=("Segoe UI", 24, "bold")).pack(expand=True)
        else:  # image file not found at all  skip straight to the text fallback
            tk.Label(win, text="AOT", fg="white", bg="black",
                     font=("Segoe UI", 24, "bold")).pack(expand=True)

        win.after(1500, win.destroy)  # shorter flash than the conquest popup


if __name__ == "__main__":
    root = tk.Tk()
    app = AoiTodoApp(root)
    root.mainloop()