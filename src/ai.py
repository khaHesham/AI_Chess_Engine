
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
       


    def BestMove(self,depth,bd,color, alpha,beta, maximizingPlayer):
        print(f'another call depth : {depth}')

        if depth == 0 :
            # positions=Board.get_ValidMoves(bd,color)
            # piece,move_random=positions[0].initial.piece,positions[0]
            print('finished the tree Backtracking now')
            score=Board.evaluate(bd,color)
            if maximizingPlayer:
                return (score,None,None)
            else:
                return (-score,None,None)
        
        if maximizingPlayer:

            # maxEval=-9999999
            best_move=None
            piece=None

            positions=Board.get_ValidMoves(bd,color)
            for pos in positions:     #move-> initial final 
                    p = pos.initial.piece 
                    print(f'initial : {pos.initial.row},{pos.initial.col}  final : {pos.final.row},{pos.final.col} name: {p.name} color {color}')
                    bd.move(p,pos,True)

                    c='white' if color=='black' else 'black'
                    eval,move,pe= self.BestMove(depth-1,bd,c,alpha,beta,False)
                    
                    if eval>=alpha: #calling maximizes score
                        alpha=eval
                        best_move=move
                        piece=pe
                    if alpha >= beta: # alpha-beta cutoff
                        break
            print(f'alpha : {alpha}')
            return (alpha,best_move,piece)

        else:  # minimizing player

            # maxEval=9999999
            best_move=None
            piece=None

            positions=Board.get_ValidMoves(bd,color)
            for pos in positions:
                p =pos.initial.piece

                print(f'initial : {pos.initial.row},{pos.initial.col}  final : {pos.final.row},{pos.final.col} name: {p.name} color {color}')
                
                bd.move(p,pos,True)  

                c='white' if color=='black' else 'black'
                eval,move,pe=self.BestMove(depth-1,bd,c,alpha,beta,True)
                
                if eval <= beta: #other minimizes his score
                    beta = eval
                    best_move=move
                    piece=pe
                if alpha >= beta:
                    break 
            print(f'beta : {beta}')       
            return (beta,best_move,piece)


    def MinMax(self,board):
        temp_board=copy.deepcopy(board)
        e,m,p=self.BestMove(1,temp_board,self.color,-999999999,999999999, True)
        print(e)
        return (e,m,p)

   