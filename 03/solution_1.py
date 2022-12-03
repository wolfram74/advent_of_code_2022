'''
split line in half
find duplicate item in second half
score item
sum all scores
'''

def parse_sack(sack):
	total_items = len(sack)
	print(sack, total_items)
	middle = int(total_items/2)
	
	left = set(sack[:middle])
	right = set(sack[middle:])
	for item in left:
		if item in right:
			print(item)
			return item

def score_item(letter):
	ord_val = ord(letter)
	if ord_val>96:
		return ord_val-96
	return ord_val-64+26

if __name__ == '__main__':
	total_score = 0
	with open('input.txt', 'r') as sacks:
		for line in sacks:
			sack = line.rstrip()
			duped_item = parse_sack(sack)
			total_score+= score_item(duped_item)
	print(total_score)