from tkinter import ttk, Text, Frame, Label, Button

class ReadingView:
    def __init__(self, root, main_frame, app):
        self.root = root
        self.main_frame = main_frame
        self.app = app
        self._build_ui()

    def _build_ui(self):
        Label(self.main_frame, text="📖 Reading Practice", font=("Arial", 16, "bold"), bg="white").pack(pady=10)
        text = Text(self.main_frame, wrap="word", font=("Arial", 12))
        text.insert("1.0", "The elephant is the largest land animal...")
        text.pack(fill="both", expand=True, padx=20, pady=20)
        Button(self.main_frame, text="← Quay lại", command=self.app.show_lesson_list).pack(pady=10)
