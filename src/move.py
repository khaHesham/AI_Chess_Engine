

class Move:

    def __init__(self,initial,final):  #initial and final are both squares
        self.initial=initial
        self.final=final

    def final_square(self): return self.final

    def __eq__(self, other):
        return self.initial==other.initial and self.final==other.final
