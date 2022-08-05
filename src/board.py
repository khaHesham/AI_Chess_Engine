

from const import *
from square import Square
from piece import *
from move import Move


class Board:

    def __init__(self):
        self.squares = []
        self._create()
        self._add_pieces('white')
        self._add_pieces('black')

    def calc_move(self, piece, row, col):
        '''
            Calculate all valid move of this piece at this position
        '''
        def Knight_moves():

            possible_moves = [
                (row-2, col+1),
                (row-2, col-1),
                (row+2, col+1),
                (row+2, col-1),
                (row-1, col+2),
                (row-1, col-2),
                (row+1, col+2),
                (row+1, col-2),
            ]

            for possibleMove in possible_moves:
                possible_row, possible_col = possibleMove

                if Square.in_range(possible_row, possible_col):
                    if self.squares[possible_row][possible_col].isempty_or_enemy(piece.color):
                        # create a new move here
                        initial = Square(row, col)
                        final = Square(possible_row, possible_col)

                        move = Move(initial, final)
                        piece.add_move(move)

        def Pawn_moves():  # missing pormotion
            steps = 1 if piece.moved else 2

            # vertical moves
            start = row+piece.dir
            end = row + (piece.dir*(1+steps))
            for move_row in range(start, end, piece.dir):
                if Square.in_range(move_row):
                    if self.squares[move_row][col].isempty():

                        # create initial and final squares
                        initial = Square(row, col)
                        final = Square(move_row, col)
                        # new move
                        move = Move(initial, final)
                        piece.add_move(move)
                    # we are blocked
                    else:
                        break
                # not in range
                else:
                    break

            # diagonal moves
            possible_move_row = row+piece.dir
            possible_move_cols = [col-1, col+1]
            for move_col in possible_move_cols:
                if Square.in_range(possible_move_row, move_col):
                    if self.squares[possible_move_row][move_col].has_enemy_piece(piece.color):
                        initial = Square(row, col)
                        final = Square(possible_move_row, move_col)
                        move = Move(initial, final)
                        piece.add_move(move)

        def straight_moves(incrs):
            for inc in incrs:
                row_increment,col_increment=inc
                possible_move_row=row+row_increment
                possible_move_col=col+col_increment

                while True:
                    if Square.in_range(possible_move_row,possible_move_col):
                        initial=Square(row,col)
                        final=Square(possible_move_row,possible_move_col)
                        move=Move(initial,final)

                        #continue looping
                        if self.squares[possible_move_row][possible_move_col].isempty():
                            #append new move 
                            piece.add_move(move)
                        #stop where you see the enemy
                        if self.squares[possible_move_row][possible_move_col].has_enemy_piece(piece.color):
                            piece.add_move(move)
                            break
                        #friendly fire lol
                        if self.squares[possible_move_row][possible_move_col].has_team_piece(piece.color):
                            break
                    #not in range
                    else : 
                        break

                    possible_move_row+=row_increment
                    possible_move_col+=col_increment

        def king_moves():

            adjacents=[
                (row,col+1),
                (row,col-1),
                (row+1,col),
                (row-1,col),
                (row+1,col+1),
                (row+1,col-1),
                (row-1,col+1),
                (row-1,col-1)
            ]

            for possibleMove in adjacents:
                possible_row, possible_col = possibleMove

                if Square.in_range(possible_row, possible_col):
                    if self.squares[possible_row][possible_col].isempty_or_enemy(piece.color):
                        # create a new move here
                        initial = Square(row, col)
                        final = Square(possible_row, possible_col)

                        move = Move(initial, final)
                        piece.add_move(move)


        if isinstance(piece, Pawn):
            Pawn_moves()
        if isinstance(piece, Knight):
            Knight_moves()
        if isinstance(piece, Bishop):
            straight_moves([
                (-1, 1),  # up right
                (-1, -1),  # up left
                (1, 1),  # down right
                (1, -1)  # down left
            ])
        if isinstance(piece, Rook):
            straight_moves([
                (-1, 0),  # up
                (0, 1),  # left
                (1, 0),  # down
                (0, -1)  # left
            ])
        if isinstance(piece, Queen):
            straight_moves([
                    (-1, 1),  # up right
                    (-1, -1),  # up left
                    (1, 1),  # down right
                    (1, -1),  # down left
                    (-1, 0),  # up
                    (0, 1),  # left
                    (1, 0),  # down
                    (0, -1)  # left
                ]
            )
        if isinstance(piece, King):
            king_moves()

    def _create(self):
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0] for col in range(COLUMNS)]
        for row in range(ROWS):
            for col in range(COLUMNS):
                self.squares[row][col] = Square(row, col)

    def _add_pieces(self, color):
        # actually white is at bottom row index (6 and 7) ,Black (0,1)
        row_pawn, row_other = (6, 7) if color == 'white' else (1, 0)

        # pawns
        for col in range(COLUMNS):
            self.squares[row_pawn][col] = Square(row_pawn, col, Pawn(color))

        # knights
        self.squares[row_other][1] = Square(row_other, 1, Knight(color))
        self.squares[row_other][6] = Square(row_other, 6, Knight(color))
        # self.squares[3][3]=Square(3,3,Knight(color))

        # bishops
        self.squares[row_other][2] = Square(row_other, 2, Bishop(color))
        self.squares[row_other][5] = Square(row_other, 5, Bishop(color))
       

        # rooks
        self.squares[row_other][0] = Square(row_other, 0, Rook(color))
        self.squares[row_other][7] = Square(row_other, 7, Rook(color))

    
        # queen & king
        self.squares[row_other][3] = Square(row_other, 3, Queen(color))
        self.squares[row_other][4] = Square(row_other, 4, King(color))

        self.squares[5][4] = Square(5, 4, King(color))

