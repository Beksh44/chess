import tkinter as tk
import tkmacosx
from PIL import Image, ImageTk
from tkinter import ttk

# class Chess:
#
#     window = tk.Tk()
#     ROWS = {"A", "B", "C", "D", "E", "F", "G", "H"}
#     COLUMNS = {1, 2, 3, 4, 5, 6, 7, 8}
#     def __init__(self):
#         pass
#

Pieces = ["rook", "knight", "bishop", "queen", "king", "bishop", "knight", "rook",
          "pawn", "pawn"  , "pawn"  , "pawn" , "pawn", "pawn"  , "pawn"  , "pawn"]
whitePiecesPath = []
tmpWhite = []
blackPiecesPath = []
tmpBlack = []
j = 15
for i in range(16):
    tmpWhite.append("images/pieces-png/white-" + Pieces[i] + ".png")
    tmpBlack.append("images/pieces-png/black-" + Pieces[j] + ".png")
    if i == 7 or i == 15:
        whitePiecesPath.append(tmpWhite.copy())
        blackPiecesPath.append(tmpBlack.copy())
        tmpWhite.clear()
        tmpBlack.clear()
    j -= 1

print(whitePiecesPath)
print(blackPiecesPath)
ROWS = ["A", "B", "C", "D", "E", "F", "G", "H"]
COLUMNS = [8, 7, 6, 5, 4, 3, 2, 1]

def drawBoard():

    for i in range(10):
        root.grid_columnconfigure(i, minsize=95)
        root.grid_rowconfigure(i, minsize=95)

    for i in range(8):
        for j in range(8):
            canvas = tk.Canvas(root, width=95, height=95, bg="white" if (i + j) % 2 == 0 else "#187F30")
            canvas.grid(row=i, column=j + 3, sticky=tk.NSEW)
            if i == 0 or i == 1:  # if it is the 1 or 2 rows, where the starting white pieces should be located
                tmp = Image.open(whitePiecesPath[i][j]).resize((80, 80), Image.LANCZOS)
                # Convert the resized image to a format Tkinter can use
                tmp = tmp.convert("RGBA")
                image = ImageTk.PhotoImage(tmp)
                canvas.create_image(50, 50, image=image)
                canvas.image = image

            if i == 6 or i == 7:  # if it is the 7 or 8 rows, where the starting black pieces should be located
                tmp = Image.open(blackPiecesPath[i-6][j]).resize((80, 80), Image.LANCZOS)
                # Convert the resized image to a format Tkinter can use
                tmp = tmp.convert("RGBA")
                image = ImageTk.PhotoImage(tmp)
                canvas.create_image(50, 50, image=image)
                canvas.image = image

            if i == 0 and j == 0:  # if it is top left cell where we need to put both 8 and A
                canvas.create_text(95 - 10, 95 - 10, anchor="se", text="A", font=("Arial", 20), fill="black")
                canvas.create_text(10, 10, anchor="nw", text=8, font=("Arial", 20), fill="black")
            elif i == 0:  # if it is first row
                canvas.create_text(95 - 10, 95 - 10, anchor="se", text=ROWS[j], font=("Arial", 20), fill="black")
            elif j == 0:  # if it is first column
                canvas.create_text(10, 10, anchor="nw", text=COLUMNS[i], font=("Arial", 20), fill="black")

def menuLabels():
    texts = ["Play","Tutorial","Settings"]
    j = 0
    for i in texts:
        lab = tk.Label(root,
                       text=i,
                       bg="white",
                       fg="black",  # Set text color to make it visible on black background
                       font=("Arial", 30, "bold"))
        lab.grid(row=j, column=1)
        j += 1


# Main window setup

root = tk.Tk()
root.title("Chess")
root.geometry("500x500+400+150")  # Set initial size and position
root.minsize(500, 500)  # Minimum size of the window
icon = tk.PhotoImage(file="images/icon.png")
root.iconphoto(False, icon)  # Set the window icon
root.config(bg="black")
drawBoard()
menuLabels()
# Run the main loop
root.mainloop()