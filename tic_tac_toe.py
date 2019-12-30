from enum import Enum

class Type(Enum):
	NEUTRAL = 0
	CROSS = 1
	CIRCLE = 2

tic_tac = [
    [0,0,0],
    [0,0,0],
    [0,0,0],
]



def printGrid(grid):
	for i in range(len(grid) + 1):
		print("")
		string = ""
		line = ""
		for x in range(len(grid) + 1):
			# enumerate the axis
			if i == 0:
				string = "  0 1 2"
				break
			if x == 0:
				string += str(i-1) + " "
				continue
			

			# Add value to fields 
			if grid[i-1][x-1] == Type.NEUTRAL.value:
				string += "-"
			else:
				board_value = grid[i-1][x-1]
				if board_value == Type.CIRCLE.value:
					string += "O"
				else: 
					string += "X"
			string += " "
			
			#if((i-1+1)%3 == 0):
			#	line += "__"
			#if((x-1+1)%3 == 0 ):
			#	string += "| "

		print(string)
		#if(line != ""):
		#	print(line+"_____")	

def check_legal_change(data, turn_counter, sign):
	# Format of data: (to_line to_col from_line from_col). Only the first two if turn_counter < 5
	# Check that data is of right sizes in respect to input
	size = len(data)

	if turn_counter > 5 and size != 4: 
		return False
	if turn_counter <= 5 and size != 2: 
		return False

	# Check valid input - input is in range [0;2]
	for num in data:
		if num > 2 or num < 0:
			return False
	
	# Check that there is not already a piece where we will move
	to_line = data[0]
	to_col = data[1]
	board_value = tic_tac[to_line][to_col]
	if board_value != 0:
		return False
	
	# Check that there is a piece of correct type on from coordinate. 
	if size > 2:	
		from_line = data[2]
		from_col = data[3]
		board_value = tic_tac[from_line][from_col]
		if board_value != sign:
			return False
	
	return True


def do_move(data, sign):
	to_line = data[0]
	to_col = data[1]	
	tic_tac[to_line][to_col] = sign
	
	# in case we have from poins as well that needs to be handled. 
	if len(data) > 2:
		from_line = data[2]
		from_col = data[3]
		tic_tac[from_line][from_col] = Type.NEUTRAL.value

def check_for_winner(player, sign):
	valid_sequences = [
		[(0,0), (0,1), (0,2)], # Choice of lines
		[(1,0), (1,1), (1,2)],
		[(2,0), (2,1), (2,2)],
		[(0,0), (1,0), (2,0)], # Choice of columns
		[(0,1), (1,1), (2,1)],
		[(0,2), (1,2), (2,2)],
		[(0,0), (1,1), (2,2)], # Cross
		[(0,2), (1,1), (2,0)]
	]

	for seq in valid_sequences:
		number_of_sequentiel_signs = 0
		for (line, col) in seq:
			board_value = tic_tac[line][col]
			if board_value == sign:
				number_of_sequentiel_signs += 1
		
		if(number_of_sequentiel_signs == 3):
			return True
	
	return False

if __name__ == "__main__":
	players = ["player 1", "player 2"]
	signs = [Type.CROSS.value, Type.CIRCLE.value]

	turn_counter = 0
	while True:
		printGrid(tic_tac)
		player = players[turn_counter % 2]
		sign = signs[turn_counter % 2]
		
		input_format = "(to_line to_col from_line from_col)"; 
		if turn_counter <= 5:
			input_format = "(to_line to_col)"

		data = input("The turn belongs to " + player +"\nInsert a coordinate with space in between in format" + input_format + "\n")
		data = list(map(int, data.strip().split()))

		# Check if legal insert
		is_legal = check_legal_change(data, turn_counter, sign)
		if not is_legal:
			print("Invalid input - try again")
			continue

		# Do the change to the board
		do_move(data, sign)

		turn_counter += 1

		# Stop condition. Check if all is lines possible is owned by same type
		if check_for_winner(player, sign):
			print("!!!!!!", player, "is the WINNER !!!!!!")
			printGrid(tic_tac)
			break
