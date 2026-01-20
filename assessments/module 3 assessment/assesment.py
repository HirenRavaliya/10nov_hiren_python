import tkinter as tk
from tkinter import messagebox
import os

class User:
    def __init__(self, username):
        self.username = username

class Post:
    def __init__(self, user, title, content):
        self.user = user
        self.title = title
        self.content = content

    def save_to_file(self):
        filename = f"{self.user.username}_{self.title}.txt"
        try:
            with open(filename, "w") as file:
                file.write(self.content)
            return True, filename
        except Exception as e:
            return False, str(e)

class MiniBlogApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("MiniBlog Application")
        self.geometry("1100x650")
        self.configure(bg="#f0f2f5")

        self.sidebar_color = "#2c3e50"
        self.main_bg = "#ecf0f1"
        self.button_color = "#34495e"
        self.accent_color = "#1abc9c"
        self.text_color = "white"

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.create_sidebar()

        self.container = tk.Frame(self, bg=self.main_bg)
        self.container.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (CreatePostPage, ViewPostsPage):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("CreatePostPage")

    def create_sidebar(self):
        sidebar = tk.Frame(self, bg=self.sidebar_color, width=200)
        sidebar.grid(row=0, column=0, sticky="ns")
        sidebar.grid_propagate(False)

        app_title = tk.Label(sidebar, text="MiniBlog", bg=self.sidebar_color, fg=self.text_color, font=("Arial", 20, "bold"))
        app_title.pack(pady=(30, 50))

        self.create_nav_button(sidebar, "New Post", "CreatePostPage")
        self.create_nav_button(sidebar, "View Posts", "ViewPostsPage")

        btn_exit = tk.Label(sidebar, text="Exit", bg="#c0392b", fg=self.text_color, font=("Arial", 12), cursor="hand2", pady=10)
        btn_exit.pack(fill="x", pady=5, padx=10, side="bottom", anchor="s")
        btn_exit.bind("<Button-1>", lambda e: self.quit())

        watermark = tk.Label(sidebar, text="Designed by\nHiren Ravaliya", bg=self.sidebar_color, fg="#95a5a6", font=("Arial", 9, "italic"))
        watermark.pack(side="bottom", pady=20)

    def create_nav_button(self, parent, text, page_name):
        btn = tk.Label(parent, text=text, bg=self.button_color, fg=self.text_color, font=("Arial", 12), cursor="hand2", pady=10)
        btn.pack(fill="x", pady=5, padx=10)
        btn.bind("<Button-1>", lambda e: self.show_frame(page_name))
        
        def on_enter(e):
            btn.config(bg=self.accent_color)
        def on_leave(e):
            btn.config(bg=self.button_color)
            
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()
        if page_name == "ViewPostsPage":
            frame.refresh_file_list()

class CreatePostPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=controller.main_bg)
        self.controller = controller

        header = tk.Label(self, text="Write a New Story", font=("Arial", 24, "bold"), bg=controller.main_bg, fg="#2c3e50")
        header.pack(pady=(20, 30))

        form_frame = tk.Frame(self, bg=controller.main_bg)
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="Author Name", font=("Arial", 11, "bold"), bg=controller.main_bg, fg="#7f8c8d").grid(row=0, column=0, sticky="w", padx=10)
        self.entry_user = tk.Entry(form_frame, width=50, font=("Arial", 12), bd=2, relief="flat", bg="white", fg="black", insertbackground="black")
        self.entry_user.grid(row=1, column=0, padx=10, pady=(5, 15))

        tk.Label(form_frame, text="Post Title", font=("Arial", 11, "bold"), bg=controller.main_bg, fg="#7f8c8d").grid(row=2, column=0, sticky="w", padx=10)
        self.entry_title = tk.Entry(form_frame, width=50, font=("Arial", 12), bd=2, relief="flat", bg="white", fg="black", insertbackground="black")
        self.entry_title.grid(row=3, column=0, padx=10, pady=(5, 15))

        tk.Label(form_frame, text="Content", font=("Arial", 11, "bold"), bg=controller.main_bg, fg="#7f8c8d").grid(row=4, column=0, sticky="w", padx=10)
        self.text_content = tk.Text(form_frame, width=50, height=12, font=("Arial", 12), bd=2, relief="flat", bg="white", fg="black", insertbackground="black")
        self.text_content.grid(row=5, column=0, padx=10, pady=(5, 20))

        save_btn = tk.Label(self, text="Publish Post", bg="#27ae60", fg="white", font=("Arial", 12, "bold"), padx=20, pady=10, cursor="hand2")
        save_btn.pack()
        save_btn.bind("<Button-1>", lambda e: self.save_post())

    def save_post(self):
        username = self.entry_user.get().strip()
        title = self.entry_title.get().strip()
        content = self.text_content.get("1.0", tk.END).strip()

        if not username or not title or not content:
            messagebox.showwarning("Missing Info", "Please fill in all fields.")
            return

        user = User(username)
        post = Post(user, title, content)
        success, message = post.save_to_file()

        if success:
            messagebox.showinfo("Published", f"Post saved successfully!\nFile: {message}")
            self.clear_fields()
        else:
            messagebox.showerror("Error", f"Could not save: {message}")

    def clear_fields(self):
        self.entry_user.delete(0, tk.END)
        self.entry_title.delete(0, tk.END)
        self.text_content.delete("1.0", tk.END)

class ViewPostsPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=controller.main_bg)
        self.controller = controller
        
        header = tk.Label(self, text="Saved Posts Archive", font=("Arial", 24, "bold"), bg=controller.main_bg, fg="#2c3e50")
        header.pack(pady=(20, 20))

        content_frame = tk.Frame(self, bg=controller.main_bg)
        content_frame.pack(expand=True, fill="both", padx=30, pady=10)

        left_pane = tk.Frame(content_frame, bg=controller.main_bg)
        left_pane.pack(side="left", fill="y", padx=(0, 20))

        tk.Label(left_pane, text="Select File:", font=("Arial", 11, "bold"), bg=controller.main_bg, fg="#7f8c8d").pack(anchor="w")
        self.post_listbox = tk.Listbox(left_pane, width=35, height=20, font=("Arial", 11), bd=0, highlightthickness=0, bg="white", fg="black")
        self.post_listbox.pack(pady=5, fill="y", expand=True)
        self.post_listbox.bind('<<ListboxSelect>>', self.display_post_content)

        right_pane = tk.Frame(content_frame, bg=controller.main_bg)
        right_pane.pack(side="left", fill="both", expand=True)

        tk.Label(right_pane, text="Preview:", font=("Arial", 11, "bold"), bg=controller.main_bg, fg="#7f8c8d").pack(anchor="w")
        self.display_text = tk.Text(right_pane, width=40, height=20, font=("Arial", 12), bd=0, highlightthickness=0, bg="white", fg="black", padx=10, pady=10)
        self.display_text.pack(pady=5, fill="both", expand=True)
        self.display_text.config(state="disabled")

    def refresh_file_list(self):
        self.post_listbox.delete(0, tk.END)
        self.display_text.config(state="normal")
        self.display_text.delete("1.0", tk.END)
        self.display_text.config(state="disabled")

        try:
            files = [f for f in os.listdir() if f.endswith(".txt")]
            for f in files:
                self.post_listbox.insert(tk.END, f)
        except:
            pass

    def display_post_content(self, event):
        selection = self.post_listbox.curselection()
        if not selection:
            return
        
        filename = self.post_listbox.get(selection[0])
        
        try:
            with open(filename, "r") as file:
                content = file.read()
                self.display_text.config(state="normal")
                self.display_text.delete("1.0", tk.END)
                self.display_text.insert(tk.END, content)
                self.display_text.config(state="disabled")
        except Exception as e:
            messagebox.showerror("Read Error", str(e))

if __name__ == "__main__":
    app = MiniBlogApp()
    app.mainloop()