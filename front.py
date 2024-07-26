import tkinter as tk

root = tk.Tk()

root.title("chess")  # giving our application a title
root.geometry("500x500+400+150")  # giving our application starting screen resolution and starting position
root.minsize(500, 500)  # user can't change resolution lesser than 500x500
icon = tk.PhotoImage(file="images/icon.png")
root.iconphoto(False, icon)  # setting our icon image

root.mainloop()
