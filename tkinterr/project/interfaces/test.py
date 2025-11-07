import tkinter as tk

def highlight_selection():
    try:
        start = text.index("sel.first")
        end = text.index("sel.last")
        text.tag_add("highlight", start, end)
    except tk.TclError:
        pass  # không có vùng chọn

def remove_highlight():
    text.tag_remove("highlight", "1.0", "end")

def show_context_menu(event):
    # Hiển thị menu tại vị trí chuột
    context_menu.tk_popup(event.x_root, event.y_root)

root = tk.Tk()
root.title("Right-click Highlight Demo")

text = tk.Text(root, wrap="word", font=("Arial", 14))
text.pack(expand=True, fill="both", padx=10, pady=10)
text.insert("1.0", "👉 Hãy bôi đen một đoạn văn, rồi nhấn chuột phải để highlight hoặc xóa highlight.\n\nBạn có thể tô nhiều đoạn khác nhau.")

# Cấu hình tag highlight
text.tag_configure("highlight", background="#FFF176")

# Tạo menu chuột phải
context_menu = tk.Menu(root, tearoff=0)
context_menu.add_command(label="✨ Highlight vùng chọn", command=highlight_selection)
context_menu.add_command(label="❌ Bỏ highlight", command=remove_highlight)

# Gán sự kiện chuột phải cho Text
text.bind("<Button-3>", show_context_menu)

root.mainloop()
