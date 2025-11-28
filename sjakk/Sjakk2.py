import copy

#Brikker
class Piece:
    def __init__(self,color,koords):
        self.color = color
        self.koords = koords
        self.has_moved = False

    def get_moves(self,board):
        return []
    def get_legal_moves(self,board):
        return []
    def is_enemy(self,board,target_koords):
        target = get_piece(board,target_koords)
        if on_board(target_koords):

            if not(isinstance(target,None_Piece)) and self.color != target.color:
                return True
            else:
                return False
    def get_legal_moves(self, board,blirdsjakk=True):
        moves = self.get_moves(board)
        if blirdsjakk:
            moves = [m for m in moves if not(blir_det_sjakk_for_meg(board,self,m))] 
        return moves

class None_Piece(Piece):
    def __init__(self,koords,color = None):
        self.color = None
        self.koords = koords
    
    
class Pawn(Piece):
    def get_moves(self,board):
        is_white = self.color =="white"
        direction = 1 if is_white else -1
        start_rank = 1 if is_white else 6
        x,y = self.koords
      

        moves = []
        #fremover
        if is_empty(board,[x, y + direction]):
            moves.append([x, y + direction])
        # Double move from starting rank
            if y == start_rank and is_empty(board,[x, y + 2 * direction]):
                moves.append([x, y + 2 * direction])
        
        for dx in (-1, 1):
            nx, ny = x + dx, y + direction
            if on_board([nx,ny]):
                if self.is_enemy(board,[nx, ny]):
                    moves.append([nx, ny])
        return moves
    
    
    
class Rook(Piece):
    def get_moves(self, board):
        
        moves = []
        x,y = self.koords
       
        #chat herregud så mye renere
        directions = [(1,0),(-1,0),(0,1),(0,-1)]

        for dx,dy in directions:
            nx,ny = x + dx, y + dy
            while on_board([nx,ny]):
                if is_empty(board,[nx,ny]):
                    moves.append([nx,ny])
                elif self.is_enemy(board,[nx,ny]):
                    moves.append([nx,ny])
                    break
                else:
                    break
                nx += dx
                ny += dy
        return moves

class Bishop(Piece):
    def get_moves(self, board):
        
        moves = []
        x,y = self.koords
      
        directions = [(1,1),(-1,-1),(-1,1),(1,-1)]
        for dx,dy in directions:
            nx,ny = x+ dx,y+dy
            while on_board([nx,ny]):
                if is_empty(board,[nx,ny]):
                    moves.append([nx,ny])
                elif self.is_enemy(board,[nx,ny]):
                    moves.append([nx,ny])
                    break
                else:
                    break
                nx += dx
                ny += dy
        return moves



class Queen(Piece):
    def get_moves(self, board):
        
        moves = []
        x,y = self.koords
        
        directions = [(1,1),(-1,-1),(-1,1),(1,-1)] + [(1,0),(-1,0),(0,1),(0,-1)]
        for dx,dy in directions:
            nx,ny = x+ dx,y+dy
            while on_board([nx,ny]):
                if is_empty(board,[nx,ny]):
                    moves.append([nx,ny])
                elif self.is_enemy(board,[nx,ny]):
                    moves.append([nx,ny])
                    break
                else:
                    break
                nx += dx
                ny += dy
        return moves

class King(Piece):
    def get_moves(self, board):
        
        moves = []
        x,y = self.koords
        directions = [(1,1),(-1,-1),(-1,1),(1,-1)] + [(1,0),(-1,0),(0,1),(0,-1)]
        for dx,dy in directions:
            nx,ny = x+ dx,y+dy
            if on_board([nx,ny]):
                if is_empty(board,[nx,ny]):
                    moves.append([nx,ny])
                elif self.is_enemy(board,[nx,ny]):
                    moves.append([nx,ny])
        return moves
    
    def rokade_lov(self,board):
        retninger = [(-1,0,4),(1,0,3)]
        x,y = self.koords
        if kan_kongen_daue(board,self.color):
            return [False,False]
        result = []
        for dx,dy,lengde in retninger:
            nx = x + dx
            ny = y + dy
            end_piece = get_piece(board,[x+lengde*dx,y+lengde*dy])
            if isinstance(end_piece,Rook) and not(end_piece.has_moved):
                for i in range(lengde):
                    if blir_ruten_angripe(board,[nx,ny]) or not(is_empty(board,[nx,ny])):
                        result.append(False)
                        break
                    nx += dx
                    ny += dy
                result.append(True)
            else:
                result.append(False)
        return result

class Knight(Piece):
     def get_moves(self, board):
        
        moves = []
        x,y = self.koords
        directions = [(1,2),(-1,2),(1,-2),(-1,-2)]
        for dx,dy in directions:
            nx,ny = x+ dx,y+dy
            if on_board([nx,ny]): 
                if is_empty(board,[nx,ny]):
                    moves.append([nx,ny])
                elif self.is_enemy(board,[nx,ny]):
                    moves.append([nx,ny])
        return moves
     

#Spill_Logikk


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
board_string2 = (
    "........"
    "R......."
    "........" 
    "Q......."
    "........"
    "........"
    "........"
    "R...K..R"
)
bokstaver = ["A","B","C","D","E","F","G","H"]
taller = ["1","2","3","4","5","6","7","8"]


def char_to_piece(char,koords):
    if char ==".":
        return None_Piece(koords)
    color = "white" if char.isupper() else "black"
    piece_type = char.lower()
    if piece_type == "p":
        return Pawn(color,koords)
    if piece_type =="r":
        return Rook(color,koords)
    if piece_type =="b":
        return Bishop(color,koords)
    if piece_type =="q":
        return Queen(color,koords)
    if piece_type =="k":
        return King(color,koords)
    if piece_type =="n":
        return Knight(color,koords)
    #FORTSETT HER



def make_board(board_string):
    board_grid = []
    i = 0
    for y in range(8):
        rad = []
        for x in range(8):
            char = board_string[i]
            rad.append(char_to_piece(char,[x,7-y]))
            i +=1
        board_grid.append(rad)
        
    return board_grid

def get_piece(board,koords):
    x,y = koords
    return board[7-y][x]


def A1_til_xy(string):
    bokstav = string[0]
    tall = string[1]
    return [bokstaver.index(bokstav),taller.index(tall)]

def xy_til_A1(koords):
    x,y = koords
    return "".join([bokstaver[x],taller[y]])

def on_board(koords):
    x,y = koords
    return 0 <= x <= 7 and 0 <= y <= 7

def is_empty(board,koords):
    if isinstance(get_piece(board,koords),None_Piece):
        return True
    else:
        return False 

def print_board(board_grid):
    piecetranslate = {
        Pawn: {"white": "♟", "black": "♙"}, Rook: {"white":"♜","black":"♖"}, Bishop:{"white":"♝","black":"♗"}, Queen:{"white":"♛","black":"♕"},King:{"white":"♚","black":"♔"},Knight:{"white":"♞","black":"♘"},
        None_Piece: " "
    }
    i = -1
    for row in board_grid:
        visual_row = []
        
        for piece in row:
            if isinstance(piece,None_Piece):
                visual_row.append(piecetranslate[None_Piece])
            else:
                visual_row.append(piecetranslate[type(piece)][piece.color])
        i += 1
        print(8-i,visual_row)
    print("    A    B    C    D    E    F    G    H")

def konge_koords(board,farge):
    for x in range(8):
        for y in range(8):
            konge = get_piece(board,[x,y])
            if isinstance(konge,King) and konge.color == farge:
                return [x,y]
    return None

def move_piece(board,brikke,brikke_til):
    nx,ny = brikke_til
    x,y = brikke.koords
    brikke.koords = brikke_til
    board[7-ny][nx] = brikke
    board[7-y][x] = None_Piece([x,y])

def blir_det_sjakk_for_meg(board,brikke,brikke_til):
    brett_kopi = copy.deepcopy(board)
    brikke_kopi = copy.deepcopy(brikke)
    brikke_til_kopi = copy.deepcopy(brikke_til)
    move_piece(brett_kopi,brikke_kopi,brikke_til_kopi)
    kingdeath = kan_kongen_daue(brett_kopi,brikke_kopi.color)
    return kingdeath

def blir_ruten_angripe(board,koords):
    for x in range(8):
        for y in range(8):
            brikke = get_piece(board,[x,y])
            if koords in brikke.get_moves(board):
                return True
    return False


    
    
def kan_kongen_daue(board,kongefarge):
    k_koords = konge_koords(board,kongefarge)
    return blir_ruten_angripe(board,k_koords)
   


def handle_move(board,farge):
    gyldig_brikke = False
    while not(gyldig_brikke):
        valgt_brikke = input("Hvilken brikke vil du flytte feks <A3> ")
        valgt_brikke = A1_til_xy(valgt_brikke)
        valgt_brikke = get_piece(board,valgt_brikke)
        gyldig_brikke = valgt_brikke.color == farge and valgt_brikke.get_legal_moves(board)
    gyldig_trekk = False
    readable_moves = []
    if not(isinstance(valgt_brikke,None_Piece)) and (valgt_brikke.get_legal_moves(board) is not None):
        for move in valgt_brikke.get_legal_moves(board):
            readable_moves.append(xy_til_A1(move))
    while not(gyldig_trekk):
        print(readable_moves)
        onsket_trekk = input(f"Hvor vil du flytte din {type(valgt_brikke).__name__} ")
        onsket_trekk = A1_til_xy(onsket_trekk)
        if onsket_trekk in valgt_brikke.get_legal_moves(board):
            gyldig_trekk = True
    move_piece(board,valgt_brikke,onsket_trekk)

    #Has moved checks
    if not(valgt_brikke.has_moved):
        valgt_brikke.has_moved = True

    if valgt_brikke.color == "white":
        enemy_king = "black"
    else:
        enemy_king = "white"
    if kan_kongen_daue(board,enemy_king):
        print(f"det er sjakk til {enemy_king}")
        for x in range(8):
            for y in range(8):
                ally_brikke = get_piece(board,[x,y])
                if ally_brikke.color != enemy_king:
                    continue
                if len(ally_brikke.get_legal_moves(board)) != 0:
                    return 0
        print("det er sjakkmatt")
        global game_not_finished
        game_not_finished = False
    elif remi_sjekk(board,enemy_king):
        print("det er remi!")
        game_not_finished = False
        global remi 
        remi = True
 
                    
        
def remi_sjekk(board,color):
    for x in range(8):
        for y in range(8):
            brikke = get_piece(board,[x,y])
            if brikke.color != color:
                continue
            if len(brikke.get_legal_moves(board)) != 0:
                return False
    return True


game_not_finished = True


def main():
   vinner = None
   print("velkommen til fredriks sjakk")
   board = make_board(board_string)
   while game_not_finished:
        print_board(board)
        print("Hvit sin tur")
        handle_move(board,"white")
        print_board(board)
        if not(game_not_finished):
            if not(remi):
                vinner = "white"
                break
            break
        print("svart sin tur")
        handle_move(board,"black")
        if not(game_not_finished):
            if not(remi):
                vinner = "black"
                break
            break
   if vinner:        
    print(f"vinneren er {vinner} gratulerer!")
   else:
       print("Det ble remi,wow") 
   

    
    
    
def test():
    board = make_board(board_string2)
    print_board(board)
    hvit_konge = get_piece(board,konge_koords(board,"white"))
    print(hvit_konge.rokade_lov(board,))

test()
