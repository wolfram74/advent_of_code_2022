'''
split line in half
find duplicate item in second half
score item
sum all scores
'''

def parse_group(sacks):
	set_sacks = [set(sack) for sack in sacks]

	for item in set_sacks[0]:
		badge = True
		for sack in set_sacks[1:]:
			if item not in sack:
				badge =False
				break
		if badge:
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