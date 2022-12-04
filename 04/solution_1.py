def parse_pair(pair):
    assignment = []
    left, right = pair.split(',')
    left_ints = [int(el) for el in left.split('-')]
    right_ints = [int(el) for el in right.split('-')]
    assignment.append(left_ints)
    assignment.append(right_ints)
    return assignment

def is_enclosed(pair):
    if pair[0][0] <= pair[1][0] and pair[0][1] >= pair[1][1]:
        return True
    if pair[0][0] >= pair[1][0] and pair[0][1] <= pair[1][1]:
        return True        
    return False

if __name__ == '__main__':
    total_score = 0
    with open('input.txt', 'r') as assignment_pairs:
        for line in assignment_pairs:
            pair = line.rstrip()
            pair_ranges = parse_pair(pair)
            if is_enclosed(pair_ranges):
                total_score+=1
            # print(pair_ranges)
            # total_score+= score_item(duped_item)

    print(total_score) # not 330