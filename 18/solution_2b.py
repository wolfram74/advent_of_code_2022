'''
given a set of voxel coordinates, what is the total exposed area
is it safe to assume the blob is contiguous?
every cube starts with 6 faces
probably best to make a 3-d list and just do neighbor occupancy checks
void detection:
get the bounds of obsidian, suspect only positive numbers
second pass on blob generation, iterate over all space and if there's an existent blob nearby, add it to void list
take 2 on void detection:
while generating blob, also generate voids
do the same algorithm to get rid of voids with no neighbors
then do bfs to get others and do something like the surface area calculation
'''
def vector_add(v1, v2):
    return tuple([sum(el) for el in zip(v1, v2)])

directions  = [
    (1,0,0),
    (-1,0,0),
    (0,1,0),
    (0,-1,0),
    (0,0,1),
    (0,0,-1),
]

def parse_file(file_name):
    blob = {}
    bounds = [0,0,0]
    with open(file_name, 'r') as vectors:
        for vector in vectors.readlines():
            location = tuple(int(el) for el in vector.rstrip().split(','))
            blob[location] = [True, 0]
            for ind, val in enumerate(location):
                compare = bounds[ind]
                if val < 0:
                    print('well carp')
                if val > compare:
                    bounds[ind] = val+1
            # print(location)
    return blob, bounds



def out_of_bounds(point, bounds):
    # mins = [100,100,100]
    # maxs = [0,0,0]
    if point[0] in (-2, bounds[0]+2):
        return True
    if point[1] in (-2, bounds[1]+2):
        return True
    if point[2] in (-2, bounds[2]+2):
        return True
        # for i in range(3):
        #     if point[i] > maxs[i]:
        #         maxs[i] = point[i]
        #     if point[i] < mins[i]:
        #         mins[i] = point[i]
    # print('bounds of big void', mins, maxs)
    return False

def solution(file_name):
    blob, bounds = parse_file(file_name)
    tally = 0
    print(len(blob.keys()), bounds[0]*bounds[1]*bounds[2])
    print(bounds)
    # frontier = [(-1,-1,-1)]
    frontier = set()
    frontier.add((-1,-1,-1))
    # print(frontier)
    external_void = set()
    blob_hits = {}
    while frontier:
        focus = frontier.pop()
        # print(len(frontier), tally)
        # print
        if focus in external_void:
            continue
        # if focus in blob:
        #     print(focus)
        #     tally+=1
        #     blob[focus][1]+=1
        #     continue
        if out_of_bounds(focus, bounds):
            continue
        for direction in directions:
            future = vector_add(focus, direction)
            if future in blob:
                tally+=1
                blob[future][1]+=1
                continue
            if future in external_void:
                continue
            if future in frontier:
                continue
            frontier.add(future)
        external_void.add(focus)
            # pass
    print(len(external_void), tally)
    # print(blob)
    return tally


if __name__ == '__main__':
    
    if not solution('test_input2.txt') == 6*5:
        print('test failed, stopping')
        exit()

    if not solution('test_input.txt') == 58:
        print('test failed, stopping')
        exit()

    print('test passing, onto full')
    # exit()
    print(solution('input.txt'))
    # part 1 4310
    # 4040 too high
    # 2441 too low
    # 2341
    # 3985 too high
    # 2466