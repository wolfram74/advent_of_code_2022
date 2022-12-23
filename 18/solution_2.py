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
            blob[location] = [True, 6]
            for ind, val in enumerate(location):
                compare = bounds[ind]
                if val < 0:
                    print('well carp')
                if val > compare:
                    bounds[ind] = val+1
            # print(location)
    return blob, bounds

def void_check(blob, bounds):
    print(bounds)
    empty_cubes = set()
    for x in range(bounds[0]):
        for y in range(bounds[1]):
            for z in range(bounds[2]):
                location = (x,y,z)
                if location in blob:
                    continue
                empty_cubes.add(location)
    clusters = form_clusters(empty_cubes)
    internal_penalties = []
    for cluster in clusters:
        if (0,0,0) in cluster:
            print('rejected len %d cluster, obviously outside' % len(cluster))
            area_check(blob, cluster)
            continue
        if len(cluster) > 4:
            if bound_check(cluster, bounds):
                print('rejected len %d cluster' % len(cluster))
                continue
        # if tuple(bounds) in cluster:
        #     continue
        # if vector_add(bounds,(-1,-1,-1)) in cluster:
        #     continue
        # print(cluster)
        internal_penalties.append(area_check(blob, cluster))
    # print(empty_cubes)
    # print(enclosed_voids)
    return internal_penalties

def form_clusters(spaces):
    '''
    choose a node at random, make a 
    generate list of guesses
    work on 
    '''
    # print(len(spaces))
    visited_spaces = set()
    clusters = []
    while len(spaces) > 0:
        start = spaces.pop()
        if start in visited_spaces:
            continue

        cluster = set()
        frontier = [start]
        while len(frontier) > 0:
            # print(len(frontier))
            inspect = frontier.pop(0)
            if inspect in visited_spaces:
                continue
            for direction in directions:
                new_point = vector_add(inspect, direction)
                if not new_point in spaces:
                    continue
                if new_point in visited_spaces:
                    continue
                if new_point in frontier:
                    continue
                frontier.append(new_point)
                # visited_spaces.add(new_point)
            cluster.add(inspect)
            visited_spaces.add(inspect)
        clusters.append(cluster)
    # for cluster in clusters:
        # print(cluster, len(cluster))
        # print(len(cluster))
    return clusters

def area_check(blob, void):
    penalty = 0
    for point in void:
        for direction in directions:
            check = vector_add(direction, point)
            if check in blob:
                penalty+=1
    print('void size, penalty', len(void), penalty)
    return penalty

def bound_check(blob, bounds):
    mins = [100,100,100]
    maxs = [0,0,0]
    for point in blob:
        if point[0] in (0, bounds[0]-1):
            return True
        if point[1] in (0, bounds[1]-1):
            return True
        if point[2] in (0, bounds[2]-1):
            return True
        for i in range(3):
            if point[i] > maxs[i]:
                maxs[i] = point[i]
            if point[i] < mins[i]:
                mins[i] = point[i]
    print('bounds of big void', mins, maxs)
    return False

def solution(file_name):
    blob, bounds = parse_file(file_name)
    tally = 0
    print(len(blob.keys()), bounds[0]*bounds[1]*bounds[2])
    for vector in blob.keys():
        # print(vector)
        for direction in directions:
            check = vector_add(direction,vector)
            if check in blob:
                blob[vector][1] -= 1
        tally += blob[vector][1]
    void_census = void_check(blob, bounds)
    # void_clusters = find_voids(blob, bounds)
    tally -= sum(void_census)
    # failing on larger input, guess was too high
    # if anything, I feel like mine would under shoot in case where two void voxels were adjacent
    # that's exactly what it's missing, multi-voxel voids would register as external space by this check
    print(tally)
    return tally


if __name__ == '__main__':
    
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