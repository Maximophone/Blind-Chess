import pdb

class MovePattern(object):

	def __init__(self,pattern,propagates):
		self.propagates = propagates
		self.pattern = pattern

	def compute(self,init_pos,white,board):
		if not self.propagates:
			#get all possible pos
			hypo = [[init_pos[0]+move[0],init_pos[1]+move[1]] for move in self.pattern]
			#remove the ones that are out of the board
			hypo_in_range = [[x,y] for x,y in hypo if x in range(8) and y in range(8)]
			final = []
			#remove the ones that clash on a friendly piece
			for pos in hypo_in_range:
				keeping = True
				for piece in board.pieces:
					if not piece.dead and piece.white == white and piece.pos == pos:
						keeping = False
				if keeping: final.append(pos)
			return final
		else:
			hypo = []
			for move in self.pattern:
				#for each possible move
				#create a buffer position, initiated at the piece's position
				buffer_pos = init_pos
				while buffer_pos[0] in range(8) and buffer_pos[1] in range(8):
					#while the buffer is still inside the board
					#if the buffer is at the original position, move it
					if buffer_pos == init_pos: 
						buffer_pos = [buffer_pos[0]+move[0],buffer_pos[1]+move[1]]
						continue
					breaking = False
					for piece in board.pieces:
						#if buffer arrives at a friendly piece's location, stop
						if piece.pos == buffer_pos and piece.white==white and not piece.dead: 
							breaking=True
							break
					if breaking: break
					#add this position to the list
					hypo.append(buffer_pos)
					for piece in board.pieces:
						#if buffer arrives at an opponent's piece location, stop
						if piece.pos == buffer_pos and piece.white!=white: 
							breaking=True
							break
					if breaking: break
					#otherwise, iterate buffer
					buffer_pos = [buffer_pos[0]+move[0],buffer_pos[1]+move[1]]
			return hypo





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

	def isCheck(self):
		#returns true if there is check, false otherwise

		#get the king
		for piece in self.pieces:
			if piece.white == self.whitePlaying and piece.name == 'king':
				king_pos = piece.pos
				break

		#then cycle through every opponent's piece and find if one can get the king
		for piece in self.pieces:
			if piece.white != self.whitePlaying and not piece.dead:
				possible_moves = piece.getMoves(self)
				for move in possible_moves:
					if move==king_pos: return True
		return False

	def expandMoves(self):
		#implement rocke, small rocke and en passant
		return []


	def restrictMoves(self,piece,hypo):
		#If there is check, restrict moves
		restricted_moves = []
		origin = piece.pos
		for move in hypo:
			piece.fake_move(move,self)
			if not self.isCheck(): restricted_moves.append(move)
			piece.cancel_fake_move(self)
		return restricted_moves


	def promote(self):
		#promote pawns that have reached the last line
		for i,piece in enumerate(self.pieces):
			if piece.name == 'pawn' and piece.pos[1] in (0,7):	self.pieces[i] = Queen(piece.pos,piece.white)



	def isLegit(self,pos_from,pos_to):
		wrongStart = True
		for piece in self.pieces:
			#If that's an opponent's piece
			if piece.pos == pos_from and piece.white!=self.whitePlaying and not piece.dead: return False
			#If that's one of the player's piece
			elif piece.pos == pos_from and not piece.dead: 
				wrongStart = False
				break
		#If this place is empty
		if wrongStart: return False
		possible_moves = piece.getMoves(self)
		extended_moves = self.expandMoves()
		#pdb.set_trace()
		restricted_moves = self.restrictMoves(piece,possible_moves+extended_moves)
		#Implement "roque" exception here? If piece is a king extend its moves
		#Also we need to check if we are in a check situation
		return pos_to in restricted_moves

	def execute(self,pos_from,pos_to):
		#here we assume move is legit
		for piece in self.pieces:
			if piece.pos == pos_from and not piece.dead: break
		piece.move(pos_to,self)
		self.promote()
		self.whitePlaying = not self.whitePlaying

	def checkSyntax(self,command):
		if command[0].lower() not in ['a','b','c','d','e','f','g','h']: return False
		if command[1] not in ['1','2','3','4','5','6','7','8']: return False
		if command[2].lower() not in ['a','b','c','d','e','f','g','h']: return False
		if command[3] not in ['1','2','3','4','5','6','7','8']: return False
		return True

	def parse(self,command):
		if not self.checkSyntax(command): return False

		pos_from = [self.letterToInt[command[0]],int(command[1])-1]
		pos_to = [self.letterToInt[command[2]],int(command[3])-1]

		legit = self.isLegit(pos_from,pos_to)

		if not legit: return False

		self.execute(pos_from,pos_to)
		return True

	def genDisplayString(self):
		nameToSymbol = {
		'king':'k',
		'queen':'q',
		'bishop':'b',
		'knight':'h',
		'tower':'t',
		'pawn':'p'
		}
		dispMat=[[' ' for x in range(8)] for y in range(8)]
		for piece in self.pieces:
			if not piece.dead:
				dispMat[piece.pos[1]][piece.pos[0]] = nameToSymbol[piece.name]
		return '---------------------------------\n| '+' |\n---------------------------------\n| '.join([' | '.join(x) for x in dispMat]) + ' |\n---------------------------------\n'


class Piece(object):

	def __init__(self,pos,white,move_pattern = None):
		self.move_pattern = move_pattern
		self.pos = pos
		self.white = white
		self.dead = False
		self.killed = None

	def move(self,pos,board):
		for piece in board.pieces:
			if piece.pos == pos and not piece.dead: 
				piece.dead=True
				break
		self.pos = pos

	def fake_move(self,pos,board):
		for piece in board.pieces:
			if piece.pos == pos and piece.white != self.white and not piece.dead: 
				piece.dead=True
				self.killed = piece
				break
		self.prevPos = self.pos
		self.pos = pos

	def cancel_fake_move(self,board):
		self.pos = self.prevPos
		if self.killed is not None:
			self.killed.dead = False
			self.killed = None



class King(Piece):

	move_pattern = MovePattern([[1,1],[1,0],[1,-1],[0,-1],[-1,-1],[-1,0],[-1,1],[0,1]],False)

	def __init__(self,pos,white):
		self.name='king'
		super(King,self).__init__(pos,white,self.move_pattern,)

	def getMoves(self,board):
		return self.move_pattern.compute(self.pos,self.white,board)

class Queen(Piece):

	move_pattern = MovePattern([[1,1],[1,0],[1,-1],[0,-1],[-1,-1],[-1,0],[-1,1],[0,1]],True)

	def __init__(self,pos,white):
		self.name='queen'
		super(Queen,self).__init__(pos,white,self.move_pattern)

	def getMoves(self,board):
		return self.move_pattern.compute(self.pos,self.white,board)

class Bishop(Piece):

	move_pattern = MovePattern([[1,1],[1,-1],[-1,-1],[-1,1]],True)

	def __init__(self,pos,white):
		self.name='bishop'
		super(Bishop,self).__init__(pos,white,self.move_pattern)

	def getMoves(self,board):
		return self.move_pattern.compute(self.pos,self.white,board)

class Tower(Piece):

	move_pattern = MovePattern([[1,0],[0,-1],[-1,0],[0,1]],True)

	def __init__(self,pos,white):
		self.name='tower'
		super(Tower,self).__init__(pos,white,self.move_pattern)

	def getMoves(self,board):
		return self.move_pattern.compute(self.pos,self.white,board)

class Knight(Piece):

	move_pattern = MovePattern([[1,2],[1,-2],[2,1],[2,-1],[-1,2],[-1,-2],[-2,1],[-2,-1]],False)

	def __init__(self,pos,white):
		self.name='knight'
		super(Knight,self).__init__(pos,white,self.move_pattern)

	def getMoves(self,board):
		return self.move_pattern.compute(self.pos,self.white,board)

class Pawn(Piece):

	def __init__(self,pos,white,north):
		self.name='pawn'
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
		print board.genDisplayString()
		x = raw_input()
		result = board.parse(x)
		print "Legit" if result else "not Legit"

if __name__ == '__main__':
	run()
