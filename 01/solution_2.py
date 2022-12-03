
if __name__ == '__main__':
	running_tally = 0
	totals = []
	with open('input.txt', 'r') as rations:
		for line in rations:
			if line =='\n':
				totals.append(running_tally)
				running_tally = 0
				continue
			running_tally += int(line)
	ranked_totals = sorted(totals)
	print(ranked_totals[-3:])
	print(sum(ranked_totals[-3:]))
# 670451 is wrong