import tkinter as tk
from PIL import Image, ImageTk
import tkmacosx

# Initialize data for pieces
Pieces = ["rook", "knight", "bishop", "queen", "king", "bishop", "knight", "rook",
          "pawn", "pawn", "pawn", "pawn", "pawn", "pawn", "pawn", "pawn"]
whitePiecesPath = []
tmpWhite = []
blackPiecesPath = []
tmpBlack = []
j = 15

# Prepare paths for pieces
for i in range(16):
    tmpWhite.append("images/pieces-png/white-" + Pieces[i] + ".png")
    tmpBlack.append("images/pieces-png/black-" + Pieces[j] + ".png")
    if i == 7 or i == 15:
        whitePiecesPath.append(tmpWhite.copy())
        blackPiecesPath.append(tmpBlack.copy())
        tmpWhite.clear()
        tmpBlack.clear()
    j -= 1

ROWS = ["A", "B", "C", "D", "E", "F", "G", "H"]
COLUMNS = [8, 7, 6, 5, 4, 3, 2, 1]


def create_canvaImage(canvas, i, j, piecesPath):
    # Load, resize, and convert image for Tkinter
    tmp = Image.open(piecesPath[i][j]).resize((80, 80), Image.LANCZOS).convert("RGBA")
    image = ImageTk.PhotoImage(tmp)
    canvas.create_image(50, 50, image=image)
    canvas.image = image  # Keep reference to avoid garbage collection


def drawBoard():

    for i in range(10):
        root.grid_columnconfigure(i, minsize=95)
        root.grid_rowconfigure(i, minsize=95)

    for i in range(8):
        for j in range(8):
            canvas = tk.Canvas(root, width=95, height=95, bg="white" if (i + j) % 2 == 0 else "#187F30")
            canvas.grid(row=i, column=j + 3, sticky=tk.NSEW)
            if i == 0 or i == 1:  # if it is the 1 or 2 rows, where the starting white pieces should be located
                create_canvaImage(canvas=canvas,i=i,j=j,piecesPath=whitePiecesPath)
            if i == 6 or i == 7:  # if it is the 7 or 8 rows, where the starting black pieces should be located
                create_canvaImage(canvas=canvas, i=i-6, j=j, piecesPath=blackPiecesPath)

            if i == 0 and j == 0:  # if it is top left cell where we need to put both 8 and A
                canvas.create_text(95 - 5, 95 - 5, anchor="se", text="A", font=("Arial", 20), fill="black")
                canvas.create_text(10, 10, anchor="nw", text=8, font=("Arial", 20), fill="black")
            elif i == 0:  # if it is first row
                canvas.create_text(95 - 5, 95 - 5, anchor="se", text=ROWS[j], font=("Arial", 20), fill="black")
            elif j == 0:  # if it is first column
                canvas.create_text(10, 10, anchor="nw", text=COLUMNS[i], font=("Arial", 20), fill="black")

def on_pressedBtn(text):
    print(f"Button pressed: {text}")


def menuLabels():
    texts = ["Play vs a friend", "Play vs AI\n(In process)", "Tutorial"]
    for j, text in enumerate(texts):
        btn = tkmacosx.Button(root,
                              text=text,
                              fg="black",
                              bg="white",
                              font=("Arial", 30),
                              command=lambda t=text: on_pressedBtn(t),
                              bd=8)
        btn.grid(row=j, column=1, sticky=tk.EW)


# Main window setup
root = tk.Tk()
root.title("Chess")
root.geometry("500x500+400+150")  # Set initial size and position
root.minsize(500, 500)  # Minimum size of the window
icon = tk.PhotoImage(file="images/icon.png")
root.iconphoto(False, icon)  # Set the window icon
root.config(bg="#360D0D")

drawBoard()
menuLabels()

# Run the main loop
root.mainloop()
