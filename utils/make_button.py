import tkinter as tk

# Biến toàn cục để lưu nút đang active
active_button = None

def make_button(parent, text, icon=None, cmd=None, padx=20):
    """
    Tạo một button sidebar với icon, highlight khi click.
    """
    global active_button

    def on_click():
        global active_button
        # reset nút cũ
        if active_button:
            active_button.config(bg="#FFFFFF", font=("Arial", 12))
        # set nút mới
        btn.config(bg="#e0f7fa", font=("Arial", 12, "bold"))
        active_button = btn
        if cmd:
            cmd()

    btn = tk.Button(
        parent,
        text=text,
        image=icon,
        compound="left",
        anchor="w",
        padx=padx,
        font=("Arial", 12),
        bg="#FFFFFF",
        relief="flat",
        bd=1,
        activebackground="#e0f7fa",
        command=on_click
    )
    return btn
