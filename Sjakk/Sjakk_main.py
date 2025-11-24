

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


#HER KOMMER CLASSES MAAAASSE COPILOT!!

def main():
    board = make_board(board_string)
    print_board(board)
    piece = get_piece(board,2,1)
    print(piece.get_legal_moves(board,2,1))



main()