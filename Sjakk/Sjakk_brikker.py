class Piece:
    def __init__(self,color):
        self.color = color

    def get_legal_moves(self,board_grid,x,y):
        return []
    
    def is_enemy(self,board_grid,x,y):
            if not(on_board(x,y)):
                return False
            target = get_piece(board_grid,x,y)
            return target is not None and target.color != self.color
    def move_piece(self,board_grid,from_x,from_y,to_x,to_y):
        if not(on_board(from_x,from_y)) or not(on_board(to_x,to_y)):
            return False
        possibleMoves = self.get_legal_moves(board_grid,from_x,from_y)
        


class Pawn(Piece):
    def get_legal_moves(self, board_grid, x, y):
        is_white = self.color =="white"
        direction = 1 if is_white else -1
        start_rank = 2 if is_white else 7
        
        moves = []
        #fremover
        if is_empty(board_grid,x, y + direction):
            moves.append((x, y + direction))
        # Double move from starting rank
            if y == start_rank and is_empty(board_grid,x, y + 2 * direction):
                moves.append((x, y + 2 * direction))
        
        for dx in (-1, 1):
            nx, ny = x + dx, y + direction
            if self.is_enemy(board_grid,nx, ny):
                moves.append((nx, ny))
        return moves

class Rook(Piece):
    def get_legal_moves(self, board_grid, x, y):
        
        moves = []
        #chat herregud så mye renere
        directions = [(1,0),(-1,0),(0,1),(0,-1)]

        for dx,dy in directions:
            nx,ny = x + dx, y + dy
            while on_board(nx,ny):
                if is_empty(board_grid,nx,ny):
                    moves.append([nx,ny])
                elif self.is_enemy(board_grid,nx,ny):
                    moves.append([nx,ny])
                    break
                else:
                    break
                nx += dx
                ny += dy
        return moves

class Bishop(Piece):
    def get_legal_moves(self, board_grid, x, y):
        
        moves = []
        directions = [(1,1),(-1,-1),(-1,1),(1,-1)]
        for dx,dy in directions:
            nx,ny = x+ dx,y+dy
            while on_board(nx,ny):
                if is_empty(board_grid,nx,ny):
                    moves.append([nx,ny])
                elif self.is_enemy(board_grid,nx,ny):
                    moves.append([nx,ny])
                    break
                else:
                    break
                nx += dx
                ny += dy
        return moves



class Queen(Piece):
    def get_legal_moves(self, board_grid, x, y):
        
        moves = []
        directions = [(1,1),(-1,-1),(-1,1),(1,-1)] + [(1,0),(-1,0),(0,1),(0,-1)]
        for dx,dy in directions:
            nx,ny = x+ dx,y+dy
            while on_board(nx,ny):
                if is_empty(board_grid,nx,ny):
                    moves.append([nx,ny])
                elif self.is_enemy(board_grid,nx,ny):
                    moves.append([nx,ny])
                    break
                else:
                    break
                nx += dx
                ny += dy
        return moves

class King(Piece):
    def get_legal_moves(self, board_grid, x, y):
        
        moves = []
        directions = [(1,1),(-1,-1),(-1,1),(1,-1)] + [(1,0),(-1,0),(0,1),(0,-1)]
        for dx,dy in directions:
            nx,ny = x+ dx,y+dy
            if is_empty(board_grid,nx,ny):
                moves.append([nx,ny])
            elif self.is_enemy(board_grid,nx,ny):
                moves.append([nx,ny])
                break
            else:
                break
            nx += dx
            ny += dy
        return moves

class Knight(Piece):
     def get_legal_moves(self, board_grid, x, y):
        
        moves = []
        directions = [(1,2),(-1,2),(1,-2),(-1,-2)]
        for dx,dy in directions:
            nx,ny = x+ dx,y+dy
            if is_empty(board_grid,nx,ny):
                moves.append([nx,ny])
            elif self.is_enemy(board_grid,nx,ny):
                moves.append([nx,ny])
                break
            else:
                break
            nx += dx
            ny += dy
        return moves
