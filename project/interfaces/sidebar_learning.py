import tkinter as tk

def create_sidebar_learning(root, mode="Reading"):
    sidebar = tk.Frame(
        root,
        bg="#FFFFFF",
        width=250,
        highlightbackground="#d0d0d0",
        highlightthickness=2,
        bd=0
    )
    sidebar.pack(side="right", fill="y", padx=(10, 20), pady=10)
    sidebar.pack_propagate(False)

    # Canvas + Scrollbar
    canvas = tk.Canvas(sidebar, bg="#FFFFFF", highlightthickness=0)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar = tk.Scrollbar(sidebar, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")
    canvas.configure(yscrollcommand=scrollbar.set)

    scrollable_frame = tk.Frame(canvas, bg="#FFFFFF")
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    def on_frame_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))
    scrollable_frame.bind("<Configure>", on_frame_configure)

    # Scroll wheel chỉ dành cho canvas này
    def _on_mousewheel(event):
     canvas.yview_scroll(int(-1*(event.delta/120)), "units")

# Khi chuột vào canvas, scroll wheel chỉ điều khiển canvas này
    canvas.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", _on_mousewheel))
    canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))


    # -----------------------------
    # Custom radiobutton tròn
    # -----------------------------
    def create_circle_radiobutton(parent, text, var, value):
        frame = tk.Frame(parent, bg="white")
        frame.pack(fill="x", padx=10, pady=3)

        canvas = tk.Canvas(frame, width=18, height=18, bg="white", highlightthickness=0)
        canvas.pack(side="left", padx=(0, 8))
        circle = canvas.create_oval(2, 2, 16, 16, outline="#888", width=1.5, fill="white")

        label = tk.Label(frame, text=text, font=("Arial", 10), bg="white", anchor="w")
        label.pack(side="left", fill="x", expand=True)

        def update_circle():
            if var.get() == value:
                canvas.itemconfig(circle, fill="#000000", outline="#000000")
            else:
                canvas.itemconfig(circle, fill="white", outline="#888")

        def on_click(event=None):
            var.set(value)
            update_all()

        def on_hover(event=None):
            if var.get() != value:
                canvas.itemconfig(circle, outline="#3498db")

        def on_leave(event=None):
            if var.get() != value:
                canvas.itemconfig(circle, outline="#888")

        frame.bind("<Button-1>", on_click)
        label.bind("<Button-1>", on_click)
        canvas.bind("<Button-1>", on_click)
        frame.bind("<Enter>", on_hover)
        frame.bind("<Leave>", on_leave)
        label.bind("<Enter>", on_hover)
        label.bind("<Leave>", on_leave)
        canvas.bind("<Enter>", on_hover)
        canvas.bind("<Leave>", on_leave)

        def update_all():
            for w in parent.winfo_children():
                if hasattr(w, "update_circle_func"):
                    w.update_circle_func()

        frame.update_circle_func = update_circle
        update_circle()

        return frame

    # -----------------------------
    # Card câu hỏi
    # -----------------------------
    def create_question_card(parent, q_num, question, options):
        outer = tk.Frame(parent, bg="#FFFFFF", highlightbackground="#e0e0e0")
        outer.pack(pady=8, padx=8, fill="x")

        card = tk.Frame(outer, bg="white")
        card.pack(padx=4, pady=4, fill="x")

        tk.Label(card, text=f"Question {q_num}:", font=("Arial", 11, "bold"), bg="white", anchor="w").pack(fill="x", padx=10, pady=(6, 0))
        tk.Label(card, text=question, font=("Arial", 10), bg="white", wraplength=220, justify="left", anchor="w").pack(padx=10, pady=5, fill="x")

        selected_option = tk.StringVar(value="")
        for opt in options:
            create_circle_radiobutton(card, opt, selected_option, opt)

    # -----------------------------
    # Danh sách câu hỏi
    # -----------------------------
    if mode == "Reading":
        questions = [
        {"q": "What is the main idea of the passage?", "opts": ["A. Travel", "B. Food", "C. Sports", "D. Technology"]},
        {"q": "How many animals were mentioned in this paragraph?", "opts": ["A. 1", "B. 2", "C. 3", "D. None"]},
        {"q": "Which color symbolizes peace and is often used in flags?", "opts": ["A. Red", "B. Green", "C. White", "D. Black"]},
    ]
    elif mode == "Listening":
            questions = [
        {"q": "What did the speaker mention first?", "opts": ["A. The weather", "B. His work", "C. A trip", "D. A song"]},
        {"q": "Where does the conversation take place?", "opts": ["A. At school", "B. At a cafe", "C. On a bus", "D. At home"]},
        {"q": "What is the tone of the speaker?", "opts": ["A. Angry", "B. Happy", "C. Sad", "D. Surprised"]},
    ]
    else:
        questions = []


    for i, q in enumerate(questions, start=1):
        create_question_card(scrollable_frame, i, q["q"], q["opts"])

    # -----------------------------
    # Nút Hoàn thành
    # -----------------------------
    def on_complete():
        print("✅ Bài làm đã hoàn thành!")

    complete_btn = tk.Button(
        scrollable_frame,
        text="Hoàn thành",
        command=on_complete,
        bg="#2ecc71",
        fg="white",
        font=("Arial", 11, "bold"),
        relief="flat",
        activebackground="#27ae60",
        activeforeground="white",
        cursor="hand2",
        pady=6,
        highlightthickness = 1
    )
    complete_btn.pack(fill="x", padx=40, pady=20)

    return sidebar

# -----------------------------
# Test nhanh
# -----------------------------
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x600")
    create_sidebar_learning(root)
    root.mainloop()
