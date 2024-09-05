import tkinter as tk
from PIL import Image, ImageTk
import tkmacosx

# Initialize data for pieces
blackPieces = ["rook", "knight", "bishop", "queen", "king", "bishop", "knight", "rook",
               "pawn", "pawn", "pawn", "pawn", "pawn", "pawn", "pawn", "pawn"]

whitePieces = ["pawn", "pawn", "pawn", "pawn", "pawn", "pawn", "pawn", "pawn",
               "rook", "knight", "bishop", "queen", "king", "bishop", "knight", "rook"]

whitePiecesPath = []
tmpWhite = []
blackPiecesPath = []
tmpBlack = []


# Prepare paths for pieces
for i in range(16):
    tmpWhite.append("images/pieces-png/white-" + whitePieces[i] + ".png")
    tmpBlack.append("images/pieces-png/black-" + blackPieces[i] + ".png")
    if i == 7 or i == 15:
        whitePiecesPath.append(tmpWhite.copy())
        blackPiecesPath.append(tmpBlack.copy())
        tmpWhite.clear()
        tmpBlack.clear()

ROWS = ["A", "B", "C", "D", "E", "F", "G", "H"]
COLUMNS = [8, 7, 6, 5, 4, 3, 2, 1]


class MyButton(tkmacosx.Button):
    def __init__(self, parent, image=None, path=None, cell_id=None, row=None, column=None, bg_color=None, **kwargs):
        self.cell_id = cell_id
        self.path = path
        if self.path is not None:
            self.piece = path.removeprefix("images/pieces-png/").removesuffix(".png")
            self.color = self.piece.split("-")[0]  # color of a piece
        else:
            self.piece = None
            self.color = None
        self.image = image
        self.row = row
        self.column = column
        self.bg_color = bg_color  # background color of a cell

        super().__init__(parent, image=image, **kwargs)

    def __repr__(self):
        return f"MyButton(piece={self.piece}, cell_id={self.cell_id})"


class Board:
    def __init__(self):
        self.cells = {}
        self.images = {}
        self.button_count = 0
        self.pressed = None

    def initialize_board(self):
        for i in range(8):
            for j in range(8):
                cell_id = ROWS[j] + str(COLUMNS[i])
                piece_image = None
                if i == 7 or i == 6:
                    piece_image = whitePiecesPath[i - 6][j]
                elif i == 0 or i == 1:
                    piece_image = blackPiecesPath[i][j]

                bg_color = "white" if (i + j) % 2 == 0 else "#187F30"

                # Schedule button creation with a delay
                frame2.after(self.button_count * 50, self.create_and_store_button, cell_id, piece_image, bg_color, i, j)
                self.button_count += 1

    def create_and_store_button(self, cell_id, path, bg_color, row, column):
        button = self.make_button(path=path, bg_color=bg_color, cell_id=cell_id,row=row,column=column)
        button.grid(row=row, column=column + 3, stick=tk.NSEW)
        self.cells[cell_id] = button

    def pressed_btn(self, cell_id):
        current_button = self.cells[cell_id]

        if self.pressed is None:  # if player didn't select any piece
            # No piece has been selected yet
            if current_button.image:  # Select the piece if it exists
                self.pressed = self.cells[cell_id]
                print(f"Selected {self.pressed.piece} at {cell_id}")
            else:
                print("No piece in this cell.")
        else:  # if player did select a piece
            if current_button.image is None:  # if the cell player's trying to move is empty
                self.move_piece(current_button)
            else:  # if the cell player's trying to move is not empty
                if current_button.color == self.pressed.color:  # if player's trying to eat teammate piece
                    self.pressed = current_button
                    print("can not eat its own teammate")
                else:  # if player's trying to eat enemy piece
                    self.move_piece(current_button)

    def move_piece(self, current_button):
        btn = self.pressed
        # Move the image from the pressed button to the target button
        self.create_and_store_button(cell_id=current_button.cell_id,
                                     path=btn.path,
                                     bg_color=current_button.bg_color,
                                     row=current_button.row,
                                     column=current_button.column)

        # Clear the image and path in the source button
        btn.config(image="")
        self.cells[btn.cell_id] = self.remove_piece(cell_id=btn.cell_id,
                                                    row=btn.row,
                                                    column=btn.column,
                                                    bg_color=btn.bg_color)
        # Reset the pressed button
        self.pressed = None

    def make_button(self, path, bg_color, cell_id, row, column):
        if path:
            image = open_and_resize(80, 80, path)
        else:
            image = None

        return MyButton(frame2,
                        cell_id=cell_id,
                        image=image,
                        path=path,
                        command=lambda: self.pressed_btn(cell_id),
                        row=row,
                        column=column,
                        bg=bg_color,
                        bg_color=bg_color)

    def remove_piece(self, cell_id, row, column, bg_color):
        return MyButton(frame2,
                        cell_id=cell_id,
                        image=None,
                        path=None,
                        command=lambda: self.pressed_btn(cell_id),
                        row=row,
                        column=column,
                        bg=bg_color,
                        bg_color=bg_color,
                        color=None)


    # method to get value from a cell
    def get_cellvalue(self, cell_id):
        if self.cells[cell_id].image:
            return self.cells[cell_id].piece

        return None


def open_and_resize(width, height, path):
    tmp = Image.open(path).resize((width, height), Image.LANCZOS).convert("RGBA")
    return ImageTk.PhotoImage(tmp)


def create_canvaimage(canvas, i, j, piecesPath):
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
                create_canvaimage(canvas=canvas,i=i,j=j,piecesPath=blackPiecesPath)
            if i == 6 or i == 7:  # if it is the 7 or 8 rows, where the starting black pieces should be located
                create_canvaimage(canvas=canvas, i=i-6, j=j, piecesPath=whitePiecesPath)

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
        b = Board()
        b.initialize_board()


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

# Run the main loop
root.mainloop()