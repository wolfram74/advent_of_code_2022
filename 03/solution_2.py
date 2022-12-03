'''
split line in half
find duplicate item in second half
score item
sum all scores
'''

def parse_group(sacks):
	sack0 = set(sacks[0])
	sack1 = set(sacks[1])
	sack2 = set(sacks[2])
	for item in sack0:
		if item in sack1 and item in sack2:
			print(item)
			return item

def score_item(letter):
	ord_val = ord(letter)
	if ord_val>96:
		return ord_val-96
	return ord_val-64+26

if __name__ == '__main__':
	total_score = 0
	group_size = 3
	group = []
	with open('input.txt', 'r') as sacks:
		for line in sacks:
			sack = line.rstrip()
			group.append(sack)
			if len(group) < group_size:
				continue
			duped_item = parse_group(group)
			total_score+= score_item(duped_item)
			group = []
	print(total_score)