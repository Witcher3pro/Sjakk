
import tkinter as tk
import BrikkerogLogikk as bl

# Unicode sjakktegn (hvite/svarte)
PIECE_GLYPHS = {
    "K": "♔", "Q": "♕", "R": "♖", "B": "♗", "N": "♘", "P": "♙",
    "k": "♚", "q": "♛", "r": "♜", "b": "♝", "n": "♞", "p": "♟",
}

# Startposisjon (FEN-lignende til liste): tom = "."
START_BOARD = [
    list("rnbqkbnr"),
    list("pppppppp"),
    list("........"),
    list("........"),
    list("........"),
    list("........"),
    list("PPPPPPPP"),
    list("RNBQKBNR"),
]



class ChessGUI:
    def __init__(self, root, board=None, square_size=80):
        self.root = root
        self.root.title("Sjakk i Tkinter (Canvas)")
        self.square_size = square_size
        self.board = [row[:] for row in (board or START_BOARD)]
        self.selected = None  # (row, col) for valgt brikke
        self.highlight = []   # ruter som markeres
        self.N = 8

        w = h = self.N * self.square_size
        self.canvas = tk.Canvas(root, width=w, height=h)
        self.canvas.pack()

        self.canvas.bind("<Button-1>", self.on_click)

        self.draw_board()

    def draw_board(self):
        self.canvas.delete("all")
        s = self.square_size

        # Tegn ruter
        for r in range(self.N):
            for c in range(self.N):
                x0, y0 = c * s, r * s
                x1, y1 = x0 + s, y0 + s
                # Lys/mørk farge på ruter
                fill = "#EEEED2" if (r + c) % 2 == 0 else "#769656"
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=fill, outline="")

        # Marker ev. valgt rute
        if self.selected:
            r, c = self.selected
            x0, y0 = c * s, r * s
            x1, y1 = x0 + s, y0 + s
            self.canvas.create_rectangle(x0, y0, x1, y1, outline="#FFD700", width=4)

        # (valgfritt) marker mulige trekk – her bare eksempler/placeholder
        for (r, c) in self.highlight:
            x0, y0 = c * s + s//2, r * s + s//2
            radius = s//8
            self.canvas.create_oval(x0 - radius, y0 - radius, x0 + radius, y0 + radius,
                                    fill="#00000033", outline="")

        # Tegn brikker
        for r in range(self.N):
            for c in range(self.N):
                piece = self.board[r][c]
                if piece != '.':
                    glyph = PIECE_GLYPHS.get(piece, "?")
                    x, y = c * s + s // 2, r * s + s // 2
                    # Velg font-størrelse etter rute-størrelse
                    font_size = int(s * 0.6)
                    self.canvas.create_text(x, y, text=glyph, font=("DejaVu Sans", font_size),
                                            fill="black")

    def on_click(self, event):
        s = self.square_size
        c = event.x // s
        r = event.y // s
        if not (0 <= r < self.N and 0 <= c < self.N):
            return

        if self.selected is None:
            # Velg brikke hvis det finnes en brikke på r,c
            if self.board[r][c] != '.':
                self.selected = (r, c)
                # (placeholder) highlight – her kunne du kalle din get_legal_moves(...)
                self.highlight = []  # f.eks. fylles med lovlige mål
        else:
            # Flytt (kun visuell – ingen regelkontroll her)
            r0, c0 = self.selected
            if (r, c) != (r0, c0):
                self.board[r][c] = self.board[r0][c0]
                self.board[r0][c0] = '.'
            self.selected = None
            self.highlight = []

        self.draw_board()



board_string = (
    "rnbqkbnr"
    "pppppppp"
    "........"
    "........"
    "........"
    "........"
    "PPPPPPPP"
    "RNBQKBNR"
)
def rc_til_xy(rc):
    return [rc[1],7-rc[0]]
def xy_til_rc(xy):
    return [7-xy[1],xy[0]]

board = bl.make_board(board_string)
bl.print_board(board)
if __name__ == "__main__":
    root = tk.Tk()
    app = ChessGUI(root)
    root.mainloop()
