move_score = {'X':1, 'Y':2, 'Z':3, }
vict_score = {'L':0, 'T':3, 'W':6, }
opp_map = {'A':'X', 'B':'Y', 'C':'Z'}
results = ["T", "W", "L"]


def parse_round(moves):
	#X -> rock, Y-> Paper, Z-> scissors
	opp = opp_map[moves[0]]
	mine = moves[1]
	
	# if opp==mine:
	# 	result= "T"
	
	score_delta = move_score[mine]-move_score[opp]

	result = results[
		( score_delta )%3
		]
	print(mine, opp, score_delta, result)

	return move_score[mine]+vict_score[result]

def solve_round(round_data):
	victory = {'A':'Y', 'B':'Z', 'C':'X'}
	loss = {'A':'Z', 'B':'X', 'C':'Y'}
	opp = round_data[0]
	result = round_data[1] #X-> lose Y->draw z->win
	# opp = opp_map[round_data[0]]
	result_number = {"X":2, "Y":0, "Z":1}
	if result == 'Y':
		choice = opp_map[opp]
	if result == 'Z':
		choice = victory[opp]
	if result == 'X':
		choice = loss[opp]

	return [opp, choice]

if __name__ == '__main__':
	total_score = 0
	with open('input.txt', 'r') as rounds:
		for line in rounds:
			round_data = line.rstrip().split(' ')
			moves = solve_round(round_data)
			total_score+= parse_round(moves)
	print(total_score)