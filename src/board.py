

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
        self.last_move = None

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
                row_increment, col_increment = inc
                possible_move_row = row+row_increment
                possible_move_col = col+col_increment

                while True:
                    if Square.in_range(possible_move_row, possible_move_col):
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)
                        move = Move(initial, final)

                        # continue looping
                        if self.squares[possible_move_row][possible_move_col].isempty():
                            # append new move
                            piece.add_move(move)
                        # stop where you see the enemy
                        if self.squares[possible_move_row][possible_move_col].has_enemy_piece(piece.color):
                            piece.add_move(move)
                            break
                        # friendly fire lol
                        if self.squares[possible_move_row][possible_move_col].has_team_piece(piece.color):
                            break
                    # not in range
                    else:
                        break

                    possible_move_row += row_increment
                    possible_move_col += col_increment

        def king_moves():

            adjacents = [
                (row, col+1),
                (row, col-1),
                (row+1, col),
                (row-1, col),
                (row+1, col+1),
                (row+1, col-1),
                (row-1, col+1),
                (row-1, col-1)
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
            #castling
            if not piece.moved:
                left_rook=self.squares[row][0].piece
                if isinstance(left_rook,Rook):
                    if not left_rook.moved:
                        for column in range(1,4):
                            if self.squares[row][column].has_piece(): #castling cant be done
                                break
                            if column==3:
                                piece.left_rook=left_rook

                                #create rook move

                                initial=Square(row,0)
                                final=Square(row,3)
                                move=Move(initial,final)
                                left_rook.add_move(move)

                                #create king move

                                initial=Square(row,col)
                                final=Square(row,2)
                                move=Move(initial,final)

                                piece.add_move(move)

                right_rook=self.squares[row][7].piece
                if isinstance(right_rook,Rook):
                    if not right_rook.moved:
                        for column in range(5,7):
                            if self.squares[row][column].has_piece(): #castling cant be done
                                break
                            if column==6:
                                piece.right_rook=right_rook

                                #create rook move
                                initial=Square(row,7)
                                final=Square(row,5)
                                move=Move(initial,final)
                                right_rook.add_move(move)
                                #create king move
                                initial=Square(row,col)
                                final=Square(row,6)
                                move=Move(initial,final)
                                
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

        
    def castling(self,initial,final):
        return abs(initial.col-final.col) == 2


    def move(self, piece, move):
        initial = move.initial
        final = move.final

        # update the board
        self.squares[initial.row][initial.col].piece = None
        self.squares[final.row][final.col].piece = piece

        #pawn pormotion 
        if isinstance(piece,Pawn):
            self.check_pormotion(piece,final)

        if isinstance(piece,King):
            if self.castling(initial,final):
                diff=final.col-initial.col
                rook=piece.left_rook if (diff < 0) else piece.right_rook
                self.move(rook,rook.moves[-1])


        piece.moved = True

        # clear valid moves  --> because we changed position
        piece.clear_moves()

        self.last_move = move

    def valid_move(self, piece, move):
        return move in piece.moves

    def check_pormotion(self,piece,final):
        if final.row==0 or final.row==7:
            self.squares[final.row][final.col].piece=Queen(piece.color)
