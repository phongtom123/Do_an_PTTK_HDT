import tkinter as tk

def create_header(root, part_text="Phần 9", title_text="Bài mới mỗi ngày", color="#1da9fe"):
    """Tạo thanh tiêu đề tự mở rộng ngang (giống lesson_cards)."""
    wrapper = tk.Frame(root, bg="#f9f9f9")
    wrapper.pack(fill="x", padx=20, pady=15)  

    header = tk.Frame(wrapper, bg=color, height=80)
    header.pack(fill="x")                     
    header.pack_propagate(False)              

    tk.Label(
        header, text=f"← {part_text}", bg=color,
        fg="white", font=("Arial", 10, "bold"), anchor="w"
    ).pack(anchor="w", padx=20, pady=(10, 0))

    tk.Label(
        header, text=title_text, bg=color,
        fg="white", font=("Arial", 14, "bold"), anchor="w"
    ).pack(anchor="w", padx=20, pady=(2, 10))

    return header


def create_lesson_cards(root, lessons):
    """Danh sách thẻ học phần (không bo tròn)."""
    container = tk.Frame(root, bg="#f9f9f9")
    container.pack(fill="both", expand=True, padx=20, pady=10)

    def create_card(parent, title, status_text, button_text="ÔN TẬP"):
        outer = tk.Frame(parent, bg="white", highlightbackground="#e0e0e0", highlightthickness=1)
        outer.pack(pady=10, fill="x")

        inner = tk.Frame(outer, bg="white")
        inner.pack(fill="x", padx=20, pady=15)

        left = tk.Frame(inner, bg="white")
        left.pack(side="left", fill="x", expand=True)

        tk.Label(left, text=title, font=("Arial", 13, "bold"), bg="white", fg="#333").pack(anchor="w")
        tk.Label(left, text=f"✅ {status_text}", font=("Arial", 11, "bold"), bg="white", fg="#00AA00").pack(anchor="w", pady=(5,0))

        tk.Button(inner, text=button_text,
                  font=("Arial", 11, "bold"),
                  fg="#1da9fe", bg="white",
                  bd=1, relief="solid",
                  activebackground="#ecf5ff",
                  cursor="hand2",
                  width=10, height=1).pack(side="right")

        return outer

    for lesson in lessons:
        create_card(container, lesson["title"], lesson["status"])

    return container

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("600x550")
    root.title("Danh sách học phần")

    create_header(root, part_text="Phần 9", title_text="Bài mới mỗi ngày", color="#1da9fe")

    sample_lessons = [
        {"title": "Unit 1", "status": "HOÀN THÀNH!"},
        {"title": "Unit 2", "status": "HOÀN THÀNH!"},
        {"title": "Unit 3", "status": "HOÀN THÀNH!"},
        {"title": "Unit 4", "status": "HOÀN THÀNH"},
    ]

    create_lesson_cards(root, sample_lessons)

    root.mainloop()
