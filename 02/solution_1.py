def parse_round(moves):
	#X -> rock, Y-> Paper, Z-> scissors
	move_score = {'X':1, 'Y':2, 'Z':3, }
	vict_score = {'L':0, 'T':3, 'W':6, }
	opp_map = {'A':'X', 'B':'Y', 'C':'Z'}
	results = ["T", "W", "L"]
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

if __name__ == '__main__':
	total_score = 0
	with open('input.txt', 'r') as rounds:
		for line in rounds:
			moves = line.rstrip().split(' ')
			total_score+= parse_round(moves)
	print(total_score)