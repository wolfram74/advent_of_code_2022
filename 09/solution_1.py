# input is series of steps taken by the head
# desired output is number of unique squares visited by tail
# provided are rules for how tail follows head
# 
# plan: generate entire path of head
# step by step generate path of tail

from math import ceil

def vector_add(v1, v2):
    return tuple([sum(el) for el in zip(v1, v2)])

def vector_diff(v1, v2):
    return tuple([el[0]-el[1] for el in zip(v1, v2)])

def mag2(v1):
    return sum([el**2 for el in v1])

def half_size(v1):
    return tuple([ceil(el/2) for el in v1])


def reconstruct_head_path(head_moves):
    # format is : direction quantity
    direction = {"U":(0,1), "D":(0,-1), "R":(1,0), "L":(-1,0)}
    path = [(0,0)]
    operation = head_moves.readline().rstrip()
    while operation:
        way, quantity = operation.split(' ')
        for step in range(int(quantity)):
            path.append(
                vector_add(path[-1], direction[way])
                )
        operation = head_moves.readline().rstrip()

    return path

def tail_response(head_now, previous_tail):
    displacement = vector_diff(head_now, previous_tail)
    # if the tail is touching or overlapping, do nothing
    # for example the head could move in a circle around the tail and nothing would happen
    if mag2(displacement)<4:
        return previous_tail

    # if the tail is two steps away in a cardinal direction, it will close the distance
    if mag2(displacement)==4:
        return vector_add(
            previous_tail,
            half_size(displacement)
            )

    # if the head is a rooks move away the tail will do a bishop move to regain contact
    # so there are 8 possible places the head could be, but only 4 possible moves the tail could take
    # ceiling divide by 2
    if mag2(displacement) > 4:
        return vector_add(
            previous_tail,
            half_size(displacement)
            )
    pass

def construct_tail_path(head_path):
    tail_path = [(0,0),]
    # print(tail_path)
    for step in range(1,len(head_path)):
        # print(head_path[step], tail_path[-1])
        tail_path.append(
            tail_response(head_path[step], tail_path[-1])
            )
    return tail_path

if __name__ == '__main__':
    with open('input.txt', 'r') as head_moves:

        # print(vector_add((1,2), (4,3)))
        head_path = reconstruct_head_path(head_moves)
        # print(head_path[:15])
        tail_path = construct_tail_path(head_path)
        # print(tail_path[:15])
        # for step in range(15):
        #     print(head_path[step], tail_path[step], vector_diff(head_path[step], tail_path[step]))
        print(len(head_path), len(tail_path), len(set(tail_path)))
        # 6252 is too high