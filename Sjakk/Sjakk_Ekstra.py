def make_board(board_string):
    board_grid = []
    i = 0 
    for y in range(8):
        rad = []
        for x in range(8):
            char = board_string[i]
            rad.append(char_to_piece(char if char !="." else None))
            i +=1
        board_grid.append(rad)
    return board_grid

def get_piece(board_grid,x,y):
    return board_grid[8-y][x-1]

def on_board(x,y):
    return  1 <= x <= 8 and 1 <= y <= 8

def is_empty(board_grid,x, y):
    return on_board(x, y) and get_piece(board_grid, x, y) is None



def print_board(board_grid):
    piecetranslate = {
        Pawn: {"white": "♟", "black": "♙"}, Rook: {"white":"♜","black":"♖"}, Bishop:{"white":"♝","black":"♗"}, Queen:{"white":"♛","black":"♕"},King:{"white":"♚","black":"♔"},Knight:{"white":"♞","black":"♘"},
        None: " "
    }
    for row in board_grid:
        visual_row = []
        for piece in row:
            if piece is None:
                visual_row.append(piecetranslate[None])
            else:
                visual_row.append(piecetranslate[type(piece)][piece.color])
        print(visual_row)


def char_to_piece(char):
    if char is None:
        return None
    color = "white" if char.isupper() else "black"
    piece_type = char.lower()
    if piece_type == "p":
        return Pawn(color)
    if piece_type =="r":
        return Rook(color)
    if piece_type =="b":
        return Bishop(color)
    if piece_type =="q":
        return Queen(color)
    if piece_type =="k":
        return King(color)
    if piece_type =="n":
        return Knight(color)
    #FORTSETT HER
    return None

