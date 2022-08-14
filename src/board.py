

from const import *
from square import Square
from piece import *
from move import Move
import copy
from sound import Sound
import os
import random


class Board:

    def __init__(self):
        self.squares = []
        self._create()
        self._add_pieces('white')
        self._add_pieces('black')
        self.last_move = None

    # def is_Game_Over(self):
    #     temp_board=copy.deepcopy(self)
    #     for row in range(ROWS):
    #         for col in range(COLUMNS):
    #             if not temp_board.squares[row][col].isempty():
    #                 p=temp_board.squares[row][col].piece
    #                 temp_board.calc_move(p,row,col,bool=False)
    #                 if len(p.moves) != 0:
    #                     return False
    #     return True

    def in_check(self,piece,move):
        temp_piece=copy.deepcopy(piece)
        temp_board=copy.deepcopy(self)
        temp_board.move(temp_piece,move,testing=True)

        for row in range(ROWS):
            for col in range(COLUMNS):
                if temp_board.squares[row][col].has_enemy_piece(piece.color):
                    p=temp_board.squares[row][col].piece
                    temp_board.calc_move(p,row,col,bool=False)
                    for m in p.moves:
                        if isinstance(m.final.piece, King):
                            print('checkmate')
                            return True
        return False


    def random_move(self):
        temp_board=copy.deepcopy(self)
        for row in range(ROWS):
            for col in range(COLUMNS):
                if not temp_board.squares[row][col].isempty:
                    p=temp_board.squares[row][col].piece
                    temp_board.calc_move(p,row,col,False)
        while True:
            if not temp_board.squares[random.randrange(0,7)][random.randrange(0,7)].isempty():
                p = temp_board.squares[random.randrange(0,7)][random.randrange(0,7)].piece 
                if p.moves != []:
                    return p.moves[random.randrange(0,len(p.moves))]          



    def calc_move(self, piece, row, col,bool=True):
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
                        final_piece=self.squares[possible_row][possible_col].piece
                        final = Square(possible_row, possible_col,final_piece)

                        move = Move(initial, final)

                        if bool:
                            if not self.in_check(piece,move):
                                piece.add_move(move)
                            # else: break
                        else:
                            piece.add_move(move)

        def Pawn_moves():  
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

                        if bool:
                            if not self.in_check(piece,move):
                                piece.add_move(move)
                        else:
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
                        final_piece=self.squares[possible_move_row][move_col].piece
                        final = Square(possible_move_row, move_col,final_piece)
                        move = Move(initial, final)

                        if bool:
                            if not self.in_check(piece,move):
                                piece.add_move(move)
                        else:
                            piece.add_move(move)

            #en passant moves
            r=3 if piece.color=='white' else 4
            fr=2 if piece.color == 'white' else 5
            #left en passant
            if Square.in_range(col-1) and row==r:
                if self.squares[row][col-1].has_enemy_piece(piece.color):
                    p=self.squares[row][col-1].piece
                    if isinstance(p,Pawn):
                        if p.en_passant:
                            initial = Square(row, col)
                            final = Square(fr, col-1,p)
                            move = Move(initial, final)

                            if bool:
                                if not self.in_check(piece,move):
                                    piece.add_move(move)
                            else:
                                piece.add_move(move)

            #right en passant
            if Square.in_range(col+1) and row==r:
                if self.squares[row][col+1].has_enemy_piece(piece.color):
                    p=self.squares[row][col+1].piece
                    if isinstance(p,Pawn):
                        if p.en_passant:
                            initial = Square(row, col)
                            final = Square(fr, col+1,p)
                            move = Move(initial, final)

                            if bool:
                                if not self.in_check(piece,move):
                                    piece.add_move(move)
                            else:
                                piece.add_move(move)


        def straight_moves(incrs):
            for inc in incrs:
                row_increment, col_increment = inc
                possible_move_row = row+row_increment
                possible_move_col = col+col_increment

                while True:
                    if Square.in_range(possible_move_row, possible_move_col):
                        initial = Square(row, col)
                        final_piece=self.squares[possible_move_row][possible_move_col].piece
                        final = Square(possible_move_row, possible_move_col,final_piece)
                        move = Move(initial, final)

                        # continue looping
                        if self.squares[possible_move_row][possible_move_col].isempty():
                            # append new move
                            if bool:
                                if not self.in_check(piece,move):
                                    piece.add_move(move)
                            else:
                                piece.add_move(move)
                        # stop where you see the enemy
                        elif self.squares[possible_move_row][possible_move_col].has_enemy_piece(piece.color):
                            if bool:
                                if not self.in_check(piece,move):
                                    piece.add_move(move)
                            else: 
                                piece.add_move(move)

                            break
                                
                        # friendly fire lol
                        elif self.squares[possible_move_row][possible_move_col].has_team_piece(piece.color):
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
                        if bool:
                            if not self.in_check(piece,move):
                                piece.add_move(move)
                            # else :break
                        else:
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
                                moveR=Move(initial,final)
                               
                                #create king move
                                initial=Square(row,col)
                                final=Square(row,2)
                                moveK=Move(initial,final)


                                if bool:
                                    if not self.in_check(left_rook,moveR) and not self.in_check(piece,moveK):
                                        piece.add_move(moveK)
                                        left_rook.add_move(moveR)
                                else:
                                    piece.add_move(moveK)
                                    left_rook.add_move(moveR)

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
                                moveR=Move(initial,final)

                                
                                #create king move
                                initial=Square(row,col)
                                final=Square(row,6)
                                moveK=Move(initial,final)

                                
                                if bool:
                                    if not self.in_check(right_rook,moveR) and not self.in_check(piece,moveK):
                                        piece.add_move(moveK)
                                        right_rook.add_move(moveR)
                                else:
                                    piece.add_move(moveK)
                                    right_rook.add_move(moveR)


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

    
    def set_true_en_passant(self,piece):
        if not isinstance(piece,Pawn):
            return
        for row in range(ROWS):
            for col in range(COLUMNS):
                if isinstance(self.squares[row][col].piece,Pawn):
                    self.squares[row][col].piece.en_passant=False
        piece.en_passant= True


    def move(self, piece, move,testing=False):
        initial = move.initial
        final = move.final
        en_passant_empty=self.squares[final.row][final.col].isempty()
        # update the board
        self.squares[initial.row][initial.col].piece = None
        self.squares[final.row][final.col].piece = piece

        #pawn pormotion & en passant
        if isinstance(piece,Pawn):
            diff=final.col-initial.col
            if diff != 0 and en_passant_empty:
                self.squares[initial.row][initial.col+diff].piece = None
                self.squares[final.row][final.col].piece = piece
                if not testing:
                    sound = Sound(os.path.join('../assets/sounds/capture.wav'))
                    sound.play()

            else:
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
