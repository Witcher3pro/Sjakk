#Brikker
import Logikk as l


class Piece:
    def __init__(self,color,koords):
        self.color = color
        self.koords = koords
        self.has_moved = False
        self.is_passantable = False

    def get_moves(self,board):
        return []
    def get_legal_moves(self,board):
        return []
    def is_enemy(self,board,target_koords):
        target = l.get_piece(board,target_koords)
        if l.on_board(target_koords):

            if not(isinstance(target,None_Piece)) and self.color != target.color:
                return True
            else:
                return False
    def get_legal_moves(self, board,blirdsjakk=True):
        moves = self.get_moves(board)
        if blirdsjakk:
            moves = [m for m in moves if not(l.blir_det_sjakk_for_meg(board,self,m))] 
        return moves

class None_Piece(Piece):
    def __init__(self,koords,color = None):
        self.color = None
        self.koords = koords
        self.is_passantable = False
    
    
class Pawn(Piece):
    def get_moves(self,board):
        is_white = self.color =="white"
        direction = 1 if is_white else -1
        start_rank = 1 if is_white else 6
        x,y = self.koords
      

        moves = []
        #fremover
        if l.is_empty(board,[x, y + direction]):
            moves.append([x, y + direction])
        # Double move from starting rank
            if y == start_rank and l.is_empty(board,[x, y + 2 * direction]):
                moves.append([x, y + 2 * direction])
        
        for dx in (-1, 1):
            nx, ny = x + dx, y + direction
            if l.on_board([nx,ny]):
                if self.is_enemy(board,[nx, ny]):
                    moves.append([nx, ny])
        return moves
    
    def get_legal_moves(self, board, blirdsjakk=True):
        moves = self.get_moves(board)
        if blirdsjakk:
            moves = [m for m in moves if not(l.blir_det_sjakk_for_meg(board,self,m))]
        x,y = self.koords
        is_white = self.color == "white"
        directions = [(1,1),(-1,1)] if is_white else [(1,-1),(-1,-1)]
        passant_directions = [(1,0),(-1,0)]
        passant_line = 4 if is_white else 3
        if y == passant_line: 
            for direction in passant_directions:
                nx = x + direction[0]
                ny = y + direction[1]
                ax = x + directions[passant_directions.index(direction)][0]
                ay = y + directions[passant_directions.index(direction)][1]
                if l.on_board([nx,ny]):
                    target = l.get_piece(board,[nx,ny])
                    if isinstance(target, Pawn) and target.is_passantable and not(l.blir_det_sjakk_for_meg(board,self,[ax,ay])):
                        moves.append([ax,ay])
                else:
                    continue
                
        return moves
    def promote(self,board,newpiece):
        x,y = self.koords
        board[7-y][x] = newpiece(self.color,self.koords)



        

    
    
    
class Rook(Piece):
    def get_moves(self, board):
        
        moves = []
        x,y = self.koords
       
        #chat herregud så mye renere
        directions = [(1,0),(-1,0),(0,1),(0,-1)]

        for dx,dy in directions:
            nx,ny = x + dx, y + dy
            while l.on_board([nx,ny]):
                if l.is_empty(board,[nx,ny]):
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
            while l.on_board([nx,ny]):
                if l.is_empty(board,[nx,ny]):
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
            while l.on_board([nx,ny]):
                if l.is_empty(board,[nx,ny]):
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
        directions = [(1,1),(-1,-1),(-1,1),(1,-1),(1,0),(-1,0),(0,1),(0,-1)]
        for dx,dy in directions:
            nx,ny = x+ dx,y+dy
            if l.on_board([nx,ny]):
                if l.is_empty(board,[nx,ny]):
                    moves.append([nx,ny])
                elif self.is_enemy(board,[nx,ny]):
                    print(f"{l.xy_til_A1([nx,ny])} er en fiende")
                    moves.append([nx,ny])
        return moves
    
    def rokade_lov(self,board):
        retninger = [(-1,0,4),(1,0,3)]
        x,y = self.koords
        if l.kan_kongen_daue(board,self.color) or self.has_moved:
            return [False,False]
        result = []
        for dx,dy,lengde in retninger:
            nx = x + dx
            ny = y + dy
            end_piece = l.get_piece(board,[x+lengde*dx,y+lengde*dy])
            if isinstance(end_piece,Rook) and not(end_piece.has_moved):
                rokade = True
                for i in range(lengde-1):
                    if l.blir_ruten_angripe(board,[nx,ny],self.color) or not(l.is_empty(board,[nx,ny])):
                        rokade = False
                        break
                    nx += dx
                    ny += dy
                result.append(rokade)
            else:
                result.append(False)
        return result
    
    def get_legal_moves(self, board, blirdsjakk=True):
        moves = self.get_moves(board)
        x,y = self.koords
        if blirdsjakk:
            moves = [m for m in moves if not(l.blir_det_sjakk_for_meg(board,self,m))] 
        blabla = [self.rokade_lov(board)[0],[x-2,y]],[self.rokade_lov(board)[1],[x+2,y]]
        for boolean,koords in blabla:
            if boolean:
                moves.append(koords)
        return moves            
    

class Knight(Piece):
     def get_moves(self, board):
        
        moves = []
        x,y = self.koords
        directions = [(1,2),(-1,2),(1,-2),(-1,-2)]
        for dx,dy in directions:
            nx,ny = x+ dx,y+dy
            if l.on_board([nx,ny]): 
                if l.is_empty(board,[nx,ny]):
                    moves.append([nx,ny])
                elif self.is_enemy(board,[nx,ny]):
                    moves.append([nx,ny])
        return moves
     
