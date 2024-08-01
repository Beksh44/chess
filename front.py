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
    tmpWhite.append("images/pieces-png/white-" + Pieces[j] + ".png")
    tmpBlack.append("images/pieces-png/black-" + Pieces[i] + ".png")
    if i == 7 or i == 15:
        whitePiecesPath.append(tmpWhite.copy())
        blackPiecesPath.append(tmpBlack.copy())
        tmpWhite.clear()
        tmpBlack.clear()
    j -= 1

ROWS = ["A", "B", "C", "D", "E", "F", "G", "H"]
COLUMNS = [8, 7, 6, 5, 4, 3, 2, 1]


class MyButton(tkmacosx.Button):
    def __init__(self, parent, image=None, piece="none", **kwargs):
        super().__init__(parent, image=image, **kwargs)
        self.piece = piece

    def __repr__(self):
        return f"MyButton(piece={self.piece})"


class Board:
    def __init__(self):
        self.cells = {}
        self.images = {}

    def initialize_board(self):
        count = 0
        for i in range(8):
            for j in range(8):
                if i == 7 or i == 6:  # Place Black pieces on rows 8 and 7
                    self.cells[ROWS[j] + str(COLUMNS[i])] = self.make_button(whitePiecesPath[i-6][j],
                                                                             bg_color="white" if (i + j) % 2 == 0 else "#187F30")
                    count += 1
                    self.cells[ROWS[j] + str(COLUMNS[i])].grid(row=i, column=j + 2, sticky=tk.NSEW)
                elif i == 0 or i == 1:  # Place White pieces on rows 1 and 2
                    if j == 'A' and i == 1:
                        count = 0
                    self.cells[ROWS[j] + str(COLUMNS[i])] = self.make_button(blackPiecesPath[i][j],
                                                                             bg_color="white" if (i + j) % 2 == 0 else "#187F30")
                    count += 1
                    self.cells[ROWS[j] + str(COLUMNS[i])].grid(row=i, column=j + 2, sticky=tk.NSEW)
                else:  # any other cells with no pieces at starting
                    self.cells[ROWS[j] + str(COLUMNS[i])] = self.make_button(None,
                                                                             bg_color="white" if (i + j) % 2 == 0 else "#187F30")
                    self.cells[ROWS[j] + str(COLUMNS[i])].grid(row=i, column=j + 2, sticky=tk.NSEW)
        print(self.cells)

    def make_button(self, value, bg_color):
        if value:
            image = open_and_resize(80, 80, value)
        else:
            image = None
        return MyButton(frame2,
                        image=image,
                        piece=value if value else "none",
                        bg=bg_color)

    # method to get value from a cell
    def get_cellvalue(self,position):
        if position in self.cells:
            return self.cells[position]

        return None



def open_and_resize(width, height, path):
    tmp = Image.open(path).resize((width, height), Image.LANCZOS).convert("RGBA")
    return ImageTk.PhotoImage(tmp)

def create_canvaImage(canvas, i, j, piecesPath):
    # Load, resize, and convert image for Tkinter
    tmp = Image.open(piecesPath[i][j]).resize((80, 80), Image.LANCZOS).convert("RGBA")
    image = ImageTk.PhotoImage(tmp)
    canvas.create_image(50, 50, image=image)
    canvas.image = image  # Keep reference to avoid garbage collection


def raw_board():

    for i in range(10):
        frame1.grid_columnconfigure(i, minsize=95)
        frame1.grid_rowconfigure(i, minsize=95)
        frame2.grid_columnconfigure(i, minsize=95)
        frame2.grid_rowconfigure(i, minsize=95)

    for i in range(8):
        for j in range(8):
            canvas = tk.Canvas(frame1, width=95, height=95, bg="white" if (i + j) % 2 == 0 else "#187F30")
            canvas.grid(row=i, column=j + 3, sticky=tk.NSEW)
            if i == 0 or i == 1:  # if it is the 1 or 2 rows, where the starting white pieces should be located
                create_canvaImage(canvas=canvas,i=i,j=j,piecesPath=blackPiecesPath)
            if i == 6 or i == 7:  # if it is the 7 or 8 rows, where the starting black pieces should be located
                create_canvaImage(canvas=canvas, i=i-6, j=j, piecesPath=whitePiecesPath)

            if i == 0 and j == 0:  # if it is top left cell where we need to put both 8 and A
                canvas.create_text(95 - 4, 95 - 4, anchor="se", text="A", font=("Arial", 20), fill="black")
                canvas.create_text(10, 10, anchor="nw", text=8, font=("Arial", 20), fill="black")
            elif i == 0:  # if it is first row
                canvas.create_text(95 - 4, 95 - 4, anchor="se", text=ROWS[j], font=("Arial", 20), fill="black")
            elif j == 0:  # if it is first column
                canvas.create_text(10, 10, anchor="nw", text=COLUMNS[i], font=("Arial", 20), fill="black")

def on_pressedBtn(text):
    print(f"Button pressed: {text}")
    if text == "Play vs a friend":
        frame2.tkraise()


def menuLabels():
    texts = ["Play vs a friend", "Play vs AI\n(In process)", "Tutorial"]
    for j, text in enumerate(texts):
        btn = tkmacosx.Button(frame1,
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

frame1 = tk.Frame(root)
frame1.config(bg="#360D0D")
frame2 = tk.Frame(root)
frame2.config(bg="#360D0D")
frame1.grid(row=0, column=0, stick=tk.NSEW)
frame2.grid(row=0, column=0, stick=tk.NSEW)
frame1.tkraise()

raw_board()
menuLabels()
b = Board()
b.initialize_board()

# Run the main loop
root.mainloop()

# class App:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("Frame Switching Example")
#         self.root.geometry("400x300")
#
#         # Create two frames
#         self.frame1 = tk.Frame(root, bg="lightblue")
#         self.frame2 = tk.Frame(root, bg="lightgreen")
#
#         # Add content to frame1
#         tk.Label(self.frame1, text="This is Frame 1", font=("Arial", 20)).pack(pady=20)
#         tk.Button(self.frame1, text="Go to Frame 2", command=self.show_frame2).pack(pady=10)
#
#         # Add content to frame2
#         tk.Label(self.frame2, text="This is Frame 2", font=("Arial", 20)).pack(pady=20)
#         tk.Button(self.frame2, text="Go to Frame 1", command=self.show_frame1).pack(pady=10)
#
#         # Initially show frame1
#         self.show_frame1()
#
#     def show_frame1(self):
#         self.frame1.pack(fill=tk.BOTH, expand=True)
#         self.frame2.pack_forget()
#
#     def show_frame2(self):
#         self.frame2.pack(fill=tk.BOTH, expand=True)
#         self.frame1.pack_forget()
#
# # Main window setup
# root = tk.Tk()
# app = App(root)
