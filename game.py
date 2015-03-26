

class MovePattern(object):

	def __init__(self,pattern,propagates):
		self.propagates = propagates
		self.pattern = pattern

	def compute(self,init_pos,white,board):
		if not self.propagates:
			hypo = [[init_pos[0]+move[0],init_pos[1]+move[1]] for move in self.pattern]
			return [[x,y] for x,y in hypo if x in range(8) and y in range(8)]
		else:
			hypo = []
			for move in self.pattern:
				buffer_pos = init_pos
				while buffer_pos[0] in range(8) and buffer_pos[1] in range(8):
					if buffer_pos[0] == init_pos[0] and buffer_pos[1] == init_pos[1]: 
						buffer_pos = [buffer_pos[0]+move[0],buffer_pos[1]+move[1]]
						continue
					for piece in board.pieces:
						if piece.pos[0]==buffer_pos[0] and piece.pos[1]==buffer_pos[1] and piece.white==white: break
					hypo.append(buffer_pos)
					for piece in board.pieces:
						if piece.pos[0]==buffer_pos[0] and piece.pos[1]==buffer_pos[1] and piece.white!=white: break
					buffer_pos = [buffer_pos[0]+move[0],buffer_pos[1]+move[1]]





class Board(object):

	letterToInt = {
	'a':0,
	'b':1,
	'c':2,
	'd':3,
	'e':4,
	'f':5,
	'g':6,
	'h':7
	}

	def __init__(self,pieces = None):
		self.pieces = self.initiate()
		self.turns_elapsed = 0
		self.whitePlaying = True

	def initiate(self):
		#White player (south)
		wking = King([4,0],True)
		wqueen = Queen([3,0],True)
		wbishop1 = Bishop([2,0],True)
		wbishop2 = Bishop([5,0],True)
		wknight1 = Knight([1,0],True)
		wknight2 = Knight([6,0],True)
		wtower1 = Tower([0,0],True)
		wtower2 = Tower([7,0],True)
		wpawn1 = Pawn([0,1],True,False)
		wpawn2 = Pawn([1,1],True,False)
		wpawn3 = Pawn([2,1],True,False)
		wpawn4 = Pawn([3,1],True,False)
		wpawn5 = Pawn([4,1],True,False)
		wpawn6 = Pawn([5,1],True,False)
		wpawn7 = Pawn([6,1],True,False)
		wpawn8 = Pawn([7,1],True,False)

		#Black player (north)
		bking = King([3,7],False)
		bqueen = Queen([4,7],False)
		bbishop1 = Bishop([2,7],False)
		bbishop2 = Bishop([5,7],False)
		bknight1 = Knight([1,7],False)
		bknight2 = Knight([6,7],False)
		btower1 = Tower([0,7],False)
		btower2 = Tower([7,7],False)
		bpawn1 = Pawn([0,6],False,True)
		bpawn2 = Pawn([1,6],False,True)
		bpawn3 = Pawn([2,6],False,True)
		bpawn4 = Pawn([3,6],False,True)
		bpawn5 = Pawn([4,6],False,True)
		bpawn6 = Pawn([5,6],False,True)
		bpawn7 = Pawn([6,6],False,True)
		bpawn8 = Pawn([7,6],False,True)

		return [wking,wqueen,wbishop1,wbishop2,wknight2,wknight1,wtower2,wtower1,wpawn8,wpawn7,wpawn6,wpawn5,wpawn4,wpawn3,wpawn2,wpawn1,bking,bqueen,bbishop2,bbishop1,bknight2,bknight1,btower2,btower1,bpawn8,bpawn7,bpawn6,bpawn5,bpawn4,bpawn3,bpawn2,bpawn1]

	def isLegit(self,pos_from,pos_to):
		wrongStart = True
		for piece in self.pieces:
			if piece.pos == pos_from and piece.white!=self.whitePlaying: return False
			elif piece.pos == pos_from: 
				wrongStart = False
				break
		if wrongStart: return False
		possibleMoves = piece.getMoves(self)
		#Implement "roque" exception here? If piece is a king extend its moves
		#Also we need to check if we are in a check situation
		return pos_to in possibleMoves

	def execute(self,pos_from,pos_to):
		#here we assume move is legit
		for piece in self.pieces:
			if piece.pos == pos_from: break
		piece.move(pos_to)
		self.whitePlaying = not self.whitePlaying

	def parse(self,command):
		pos_from = [self.letterToInt[command[0]],int(command[1])]
		pos_to = [self.letterToInt[command[2]],int(command[3])]

		legit = self.isLegit(pos_from,pos_to)

		if not legit: return False

		self.execute(pos_from,pos_to)
		return True


class Piece(object):

	def __init__(self,pos,white,move_pattern = None):
		self.move_pattern = move_pattern
		self.pos = pos
		self.white = white

	def move(self,pos):
		self.pos = pos



class King(Piece):

	move_pattern = MovePattern([[1,1],[1,0],[1,-1],[0,-1],[-1,-1],[-1,0],[-1,1],[0,1]],False)

	def __init__(self,pos,white):
		super(King,self).__init__(pos,white,self.move_pattern)

	def getMoves(self,board):
		return self.move_pattern.compute(self.pos,self.white,board)

class Queen(Piece):

	move_pattern = MovePattern([[1,1],[1,0],[1,-1],[0,-1],[-1,-1],[-1,0],[-1,1],[0,1]],True)

	def __init__(self,pos,white):
		super(Queen,self).__init__(pos,white,self.move_pattern)

	def getMoves(self,board):
		return self.move_pattern.compute(self.pos,self.white,board)

class Bishop(Piece):

	move_pattern = MovePattern([[1,1],[1,-1],[-1,-1],[-1,1]],True)

	def __init__(self,pos,white):
		super(Bishop,self).__init__(pos,white,self.move_pattern)

	def getMoves(self,board):
		return self.move_pattern.compute(self.pos,self.white,board)

class Tower(Piece):

	move_pattern = MovePattern([[1,0],[0,-1],[-1,0],[0,1]],True)

	def __init__(self,pos,white):
		super(Tower,self).__init__(pos,white,self.move_pattern)

	def getMoves(self,board):
		return self.move_pattern.compute(self.pos,self.white,board)

class Knight(Piece):

	move_pattern = MovePattern([[1,2],[1,-2],[2,1],[2,-1],[-1,2],[-1,-2],[-2,1],[-2,-1]],False)

	def __init__(self,pos,white):
		super(Knight,self).__init__(pos,white,self.move_pattern)

	def getMoves(self,board):
		return self.move_pattern.compute(self.pos,self.white,board)

class Pawn(Piece):

	def __init__(self,pos,white,north):
		self.north = north
		super(Pawn,self).__init__(pos,white)

	def isStart(self):
		return (self.north and self.pos[1] == 6) or (not self.north and self.pos[1] == 1)

	def getMoves(self,board):
		hypo = []
		firstNext = [self.pos[0],self.pos[1] + (-1 if self.north else 1)]
		secondNext = [self.pos[0],self.pos[1] + (-2 if self.north else 2)]
		firstDiag = [self.pos[0]+1,self.pos[1] + (-1 if self.north else 1)]
		secondDiag = [self.pos[0]-1,self.pos[1] + (-1 if self.north else 1)]
		firstNextEmpty = True
		secondNextEmpty = True
		for piece in board.pieces:
			if piece.pos == firstNext: firstNextEmpty=False
			if piece.pos == secondNext: secondNextEmpty=False
			if piece.pos == firstDiag and piece.white != self.white: hypo.append(firstDiag)
			if piece.pos == secondDiag and piece.white != self.white: hypo.append(secondDiag)
		if firstNextEmpty: hypo.append(firstNext)
		if self.isStart() and firstNextEmpty and secondNextEmpty: hypo.append(secondNext)
		return hypo 

def run():
	board = Board()
	while(True):
		x = raw_input()
		result = board.parse(x)
		print "Legit" if result else "not Legit"

if __name__ == '__main__':
	run()
