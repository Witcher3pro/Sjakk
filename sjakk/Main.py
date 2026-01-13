
import BrikkerogLogikk as bl
import SjakkGui as gui
import tkinter as tk
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



def main_terminal():
   vinner = None
   print("velkommen til fredriks sjakk")
   board = bl.make_board(board_string)
   while game_not_finished:
        bl.print_board(board) 
        print("Hvit sin tur")
        bl.handle_move(board,"white")
        bl.print_board(board)
        #print(board_to_string(board))
        white_move = bl.board_to_string(board)
        bl.board_history.append(white_move)
        bl.tre_trekks_remi(bl.board_history)
        if not(game_not_finished):
            if not(bl.remi):
                vinner = "white"
                break
            break
        print("svart sin tur")
        bl.handle_move(board,"black")
        black_move = bl.board_to_string(board)
        bl.board_history.append(black_move)
        bl.tre_trekks_remi(bl.board_history)
        if not(game_not_finished):
            if not(bl.remi):
                vinner = "black"
                break
            break
   if vinner:        
    print(f"vinneren er {vinner} gratulerer!")
   else:
       print("Det ble remi,wow") 
   


def main():
    vinner = None 
    root = tk.Tk()
    board = gui.ChessGUI(root,bl.make_board(gui.board_string))
    board.root.mainloop()

print("sigma sigma boi")
main_terminal()