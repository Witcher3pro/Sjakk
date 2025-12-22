
import tkinter as tk
import BrikkerogLogikk as bl
import copy
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
        
        self.white_turn = True
        self.root = root
        self.root.title("Sjakk i Tkinter (Canvas)")
        self.square_size = square_size
        self.board = [row[:] for row in (board or START_BOARD)]
        self.selected = None  # (row, col) for valgt brikke
        self.highlight = []   # ruter som markeres
        self.N = 8
        self.status_label = tk.Label(self.root,text="Velkommen Til Fredriks Sjakk; Hvit sin tur",font=("Arial",17))
        self.status_label.pack(pady=10)
        self.game_over = False
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
                                    fill="#D1B1FC", outline="")

        # Tegn brikker
        for r in range(self.N):
            for c in range(self.N):
                piece = bl.get_piece(self.board,rc_til_xy([r,c]))
                if not(isinstance(piece,bl.None_Piece)) and piece is not None:
                    glyph = bl.piecetranslate_canvas[type(piece)][piece.color]
                    x, y = c * s + s // 2, r * s + s // 2
                    # Velg font-størrelse etter rute-størrelse
                    font_size = int(s * 0.6)
                    self.canvas.create_text(x, y, text=glyph, font=("DejaVu Sans", font_size),fill="black")

    def on_click(self, event):
        if self.game_over:
            return 0 
        s = self.square_size
        c = event.x // s
        r = event.y // s
        if not (0 <= r < self.N and 0 <= c < self.N):
            return
        if self.selected is None:
            brikke = bl.get_piece(self.board,rc_til_xy([r,c]))
            is_white = True if brikke.color =="white" else False
            if not(isinstance(brikke,bl.None_Piece)) and is_white == self.white_turn:
                self.selected = (r, c)
                for move in brikke.get_legal_moves(self.board):
                    self.highlight.append(xy_til_rc(move))
        else:
            # Flytt (kun visuell – ingen regelkontroll her)
            r0, c0 = self.selected
            brikke = bl.get_piece(self.board,rc_til_xy([r0,c0]))
            is_white = True if brikke.color =="white" else False
            if (r, c) != (r0, c0) and (rc_til_xy([r,c]) in brikke.get_legal_moves(self.board)) and is_white == self.white_turn:
                lovlige_trekk_kopi = copy.deepcopy(brikke.get_moves(self.board))
                onsket_trekk_copy = copy.deepcopy([r,c])
                bl.move_piece(self.board,brikke,rc_til_xy([r,c]))
                ## Sjekk for sjakk og Remi
                if bl.remi_sjekk_canvas(self.board,brikke.color):
                    self.status_label.config(text=f"{brikke.color} har satt motstanderen i patt")
                
                
                brett_streng = bl.board_to_string(self.board)
                bl.board_history.append(brett_streng)
                
                if bl.tre_trekks_remi(bl.board_history):
                    self.status_label.config(text="Det er tre trekks remi", font=("Arial", 12))
                    self.game_over = True
                temp_color = "black" if is_white else "white"
                if bl.kan_kongen_daue(self.board,temp_color):
                    not_sjakkmatt = False
                    for u in range(8):
                        for v in range(8):
                            temp_brikke = bl.get_piece(self.board,[u,v])
                            if temp_brikke.color !=temp_color:
                                continue

                            
                            if len(temp_brikke.get_legal_moves(self.board)) != 0:
                                self.status_label.config(text=f"Det er sjakk mot {temp_color}, men ikke sjakk matt")
                                not_sjakkmatt=True
                    if not(not_sjakkmatt):
                        self.status_label.config(text=f"Det er sjakkmatt mot {temp_color} bra spilt")
                        self.game_over = True 
                
                if bl.remi_sjekk_canvas(self.board,brikke.color):
                    self.status_label.config(text=f"{brikke.color} har satt motstanderen i patt")
                    self.game_over = True
                self.white_turn = not(self.white_turn)

                print(bl.board_history)
                brikke.has_moved = True
                if isinstance(brikke,bl.King):
                    x,y = rc_til_xy(onsket_trekk_copy)
                    if [x,y] not in lovlige_trekk_kopi:
                        if x < 4:
                            bl.move_piece(self.board,bl.get_rook(self.board,"venstre",brikke.color),[x+1,y])
                        else:
                            bl.move_piece(self.board,bl.get_rook(self.board,"høyre",brikke.color),[x-1,y])
                for u in range(8):
                    for v in [3,4]:
                        
                        pawn = bl.get_piece(self.board,[u,v])
                        
                        is_white = pawn.color == "white"
                        direction = -1 if is_white else 1
                       
                        if bl.on_board([u,v+direction]):
                            enemy_pawn = bl.get_piece(self.board,[u,v+direction])
                        else:
                            continue
                        if pawn.is_passantable and isinstance(enemy_pawn,bl.Pawn) and enemy_pawn.color != pawn.color:
                           
                            self.board[7-v][u] = bl.None_Piece([u,v])
                        else:
                            pawn.is_passantable = False
                if brikke.has_moved:
                    if isinstance(brikke,bl.Pawn):
                        is_white = brikke.color == "white"
                        direction = 2 if is_white else -2
                        
                        if rc_til_xy([r,c])[1] == rc_til_xy([r0,c0])[1] + direction:
                            
                            brikke.is_passantable = True
                            
            
            self.selected = None
            self.highlight = []
            if self.white_turn:
                self.status_label.config(text="Hvit sin tur")
            else:
                self.status_label.config(text="Svart sin tur")
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
    app = ChessGUI(root,board)
    root.mainloop()
