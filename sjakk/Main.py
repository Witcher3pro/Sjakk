
import Logikk as l

game_not_finished = True




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

def main():
   vinner = None
   print("velkommen til fredriks sjakk")
   board = l.make_board(board_string)
   while game_not_finished:
        l.print_board(board) 
        print("Hvit sin tur")
        l.handle_move(board,"white")
        l.print_board(board)
        #print(board_to_string(board))
        white_move = l.board_to_string(board)
        l.board_history.append(white_move)
        l.tre_trekks_remi(l.board_history)
        if not(game_not_finished):
            if not(l.remi):
                vinner = "white"
                break
            break
        print("svart sin tur")
        l.handle_move(board,"black")
        black_move = l.board_to_string(board)
        l.board_history.append(black_move)
        l.tre_trekks_remi(l.board_history)
        if not(game_not_finished):
            if not(l.remi):
                vinner = "black"
                break
            break
   if vinner:        
    print(f"vinneren er {vinner} gratulerer!")
   else:
       print("Det ble remi,wow") 
   


main()
