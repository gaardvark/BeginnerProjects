import random

def loadfile(filename):
    with open(filename, "r") as open_file:
        return [line.strip() for line in open_file]
 
class Bunny(object):
	pos = (-1,-1)
	def __init__(self):
		self.age = 0
		self.sex = random.choice(("M", "F"))
		self.name = random.choice(male_names if self.sex == "M" else female_names)
		self.radioactive = random.randrange(1,100) <= 2
		self.color = random.choice(colors)

	def isdead(self):
		if not self.radioactive:
			return self.age > 10
		return self.age > 50

	def breedable(self):
		return self.sex == "F" and self.age >= 2 and not self.radioactive

	def getstats(self):
		return "{name:10}\t{age}\t{sex}\t{color:20}\t{radioactive}".format(name = self.name,
																		age = self.age,
																		sex = self.sex,
																		color = self.color,
																		radioactive = "Healthy" if not self.radioactive else "Radioactive")

def makebaby(mother):
	newbaby = Bunny()
	newbaby.color = mother.color
	return newbaby

def printgrid(board):
	for i in range(10):
		for j in range(10):
			if not board[i][j] == 0 and not board[i][j].radioactive:
				print board[i][j].sex,
			elif not board[i][j] == 0 and board[i][j].radioactive:
				print "X",
			else:
				print 0,
		print ""
	print "-" * 72

#Maybe use filter with function that compares  == 0
def getemptycoords(board):
	emptycoord = list()
	for i in range(10):
		for j in range(10):
			if board[i][j] == 0:
				emptycoord.append((i,j))
	return emptycoord

def move((x,y), bunny, board):
	a, b = bunny.pos
	board[a][b] = 0
	bunny.pos = (x,y)
	board[x][y] = bunny

def cycle(bunnies, board):
	with open("bunnyinfo.txt", "a") as f:
		for bunny in bunnies[:]: #This creates a copy of bunnies, so can change bunnies in the iterations
			bunny.age += 1
			
			if bunny.isdead():
				bunnies.remove(bunny)
				x,y = bunny.pos
				board[x][y] = 0
				continue

			if bunny.breedable():
				male_bunnies = filter(lambda x: x.sex == "M", bunnies)
				if male_bunnies:
					bunnies.append(makebaby(bunny))

			if bunny.radioactive:
				normal_bunnies = list(filter(lambda x: not x.radioactive, bunnies))
				if normal_bunnies:
					unlucky_bunny = random.choice(normal_bunnies)
					bunnies[bunnies.index(unlucky_bunny)].radioactive = True

			print bunny.getstats()

			if bunny.pos == (-1,-1) and len(getemptycoords(board)) != 0:
				pos = random.choice(getemptycoords(board))
				move(pos, bunny, board)

		for bunny in bunnies:
			f.write(str(bunny.getstats()) + "\n")

def main():
	#Initialize bunny list
	bunnies = [Bunny() for i in range(5)]
	
	#Initialize a 3 by 3 board filled with 0's
	board = [[0 for col in range(10)]for row in range(10)]

	with open("bunnyinfo.txt", "w") as f:
		f.write("")

	while bunnies:
		cycle(bunnies, board)
		if len(bunnies) > 1000:
			random.shuffle(bunnies)
			bunnies = bunnies[:len(bunnies) // 2]

		printgrid(board)

if __name__ == '__main__':
	male_names = loadfile("names_male.txt")
	female_names = loadfile("names_female.txt")
	colors = loadfile("colorlist.txt")
	main()

male_names = loadfile("names_male.txt")
female_names = loadfile("names_female.txt")
colors = loadfile("colorlist.txt")