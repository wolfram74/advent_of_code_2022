if __name__ == '__main__':
	running_tally = 0
	high_tally = 0
	with open('input.txt', 'r') as rations:
		for line in rations:
			if line =='\n':
				if running_tally > high_tally:
					high_tally = running_tally
				running_tally = 0
				print(high_tally)
				continue
			running_tally += int(line)
# 670451 is wrong