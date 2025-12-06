
import tkinter as tk

#from sjakk.BrikkerogLogikk import Pawn,King,Queen,None_Piece,Rook,Bishop,Knight


# Farger for sjakkbrettet
LIGHT = "#F0D9B5"
DARK = "#B58863"
HIGHLIGHT_SEL = "#32a852"
HIGHLIGHT_MOVE = "#333333"  # mørk prikk/ramme for trekk
BTN_FONT = ("Segoe UI", 12)
TILE_SIZE = 80 


def create_board(root):
    frame = tk.Frame(root)
    frame.pack(padx=10, pady=10)

    # Lag 8x8 grid med knapper
    for row in range(8):
        for col in range(8):
            color = LIGHT if (row + col) % 2 == 0 else DARK
            btn = tk.Button(frame, width=6, height=3, bg=color)
            btn.grid(row=row, column=col, padx=1, pady=1)

class VisuellBrett:
    def __init__(self,root,board,current_player="white"):
        self.root = root
        self.board = board
        self.current_player = current_player

        self.root.title("Fredriks Veldig brae sjakk")
        self.frame = tk.Frame(root)
        self.frame.pack(padx = 8, pady = 8)

        self.buttons = [[None for _ in range(8)] for _ in range(8)]

        self.selected = None
        self.selected_koords = None
        self.legal_moves = []

        self.status = tk.StringVar(value=f"Tur: {self.current_player}")
        tk.Label(self.frame, textvariable=self.status, font=("segoe UI",12,"bold")).grid(row=0,column=0,columnspan=8,pady=(0,6))
root = tk.Tk()
board = VisuellBrett(root,create_board(root))
board.root.mainloop()


