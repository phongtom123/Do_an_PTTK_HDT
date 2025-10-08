# utils.py
import tkinter as tk

def make_button(parent, text, icon=None, cmd=None, padx=20, anchor="w"):
    """
    Trả về tk.Button có behavior highlight (dùng chung).
    Lưu trạng thái button đang active ở make_button.active_button
    """
    def on_click():
        if getattr(make_button, "active_button", None) and make_button.active_button != btn:
            make_button.active_button.config(bg="#FFFFFF", font=("Arial", 12))
        btn.config(bg="#e8f4ff", font=("Arial", 12, "bold"))
        make_button.active_button = btn
        if cmd:
            cmd()

    btn = tk.Button(
        parent,
        image=icon,
        text=f"  {text}" if icon else text,
        compound="left",
        command=on_click,
        font=("Arial", 12),
        fg="black",
        bg="#FFFFFF",
        activebackground="#f0f0f0",
        bd=0,
        anchor=anchor,
        padx=padx
    )
    return btn

# biến lưu nút đang active
make_button.active_button = None
