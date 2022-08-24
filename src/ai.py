
import copy 
# import tensorflow as tf
import numpy as np

from const import *
from board import *
from square import Square
from piece import *
from move import Move




class Ai:
    '''
        main class for chess brain
    '''
    def __init__(self,color):
        self.color=color   # Ai player color
       


    def BestMove(self,depth,bd,color, alpha,beta, maximizingPlayer,pos):
        # print(f'another call depth : {depth}')

        if depth == 0 :  
            # print('finished the tree Backtracking now')
            c='white' if color=='black' else 'black'
            score=Board.evaluate(bd,c)     #return static evaluation of the board
            if maximizingPlayer:
                return (score,pos,pos.initial.piece)
            else:
                return (-score,pos,pos.initial.piece)
        
        if maximizingPlayer:

            maxEval=-9999999
            best_move=None
            piece=None

            positions=Board.get_ValidMoves(bd,color)
            for pos in positions:     #move-> initial final 
                    p = pos.initial.piece 
                    # print(f'initial : {pos.initial.row},{pos.initial.col}  final : {pos.final.row},{pos.final.col} name: {p.name} color {color}')
                    bd.move(p,pos,True)

                    c='white' if color=='black' else 'black'
                    eval,move,pe= self.BestMove(depth-1,bd,c,alpha,beta,False,pos)

                    # undo=Move(pos.final,pos.initial)
                
                    # bd.move(p,undo,True)

                    #undo here this move iam the most stuped person on earth
                    if eval>=maxEval: #calling maximizes score
                        maxEval=eval
                        alpha=eval
                        best_move=move
                        piece=pe
                    if alpha >= beta: # alpha-beta cutoff
                        break
            # print(f'alpha : {alpha}')
            return (maxEval,best_move,piece)

        else:  # minimizing player

            minEval=9999999
            best_move=None
            piece=None

            positions=Board.get_ValidMoves(bd,color)
            for pos in positions:
                p =pos.initial.piece

                # print(f'initial : {pos.initial.row},{pos.initial.col}  final : {pos.final.row},{pos.final.col} name: {p.name} color {color}')
                
                bd.move(p,pos,True)  

                c='white' if color=='black' else 'black'
                eval,move,pe=self.BestMove(depth-1,bd,c,alpha,beta,True,pos)

                # undo=Move(pos.final,pos.initial)
                # bd.move(p,undo,True) 
                
                if eval <= minEval: #other minimizes his score
                    beta = eval
                    minEval=eval
                    best_move=move
                    piece=pe
                if alpha >= beta:
                    break 
            # print(f'beta : {beta}')       
            return (minEval,best_move,piece)


    def MinMax(self,board):
        temp_board=copy.deepcopy(board)
        e,m,p=self.BestMove(3,temp_board,self.color,-999999999,999999999, True,None)
        print(e)
        return (e,m,p)

   