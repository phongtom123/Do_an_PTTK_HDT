import tkinter as tk
from ui.LoginForm import LoginForm 

def main():
    window = tk.Tk()
    app = LoginForm(window)
    window.mainloop()

if __name__ == "__main__":
    main()