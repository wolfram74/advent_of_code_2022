'''
given a set of voxel coordinates, what is the total exposed area
is it safe to assume the blob is contiguous?
every cube starts with 6 faces
probably best to make a 3-d list and just do neighbor occupancy checks
void detection:
get the bounds of obsidian, suspect only positive numbers
second pass on blob generation, iterate over all space and if there's an existent blob nearby, add it to void list
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
    enclosed_voids = 0
    compound_candidates = [{} for i in range(7)]
    for x in range(bounds[0]):
        for y in range(bounds[1]):
            for z in range(bounds[2]):
                location = (x,y,z)
                if location in blob:
                    continue
                void_neighbors = find_connected_voids(blob, location)
                # print(location, void_neighbors, len(void_neighbors))
                if len(void_neighbors) == 0:
                    enclosed_voids += 1
                    continue
                compound_candidates[len(void_neighbors)][location]=void_neighbors
                # if is_enclosed(blob, location):
    examine_compouds(compound_candidates)
    # print(enclosed_voids)
    return [enclosed_voids, 0]

def find_connected_voids(blob, location):
    void_neighbors = []
    for direction in directions:
        check = vector_add(direction,location)
        if -1 in check:
            continue
        if not check in blob:
            # print(location,check)
            void_neighbors.append(check)
            continue
            # return False
    # if len(void_neighbors) == 6:
    #     return False, []
    # print(location, void_neighbors)
    return void_neighbors

def examine_compouds(void_groups):
    voids_in_clusters = set()
    void_clusters = []
    for ind, level in enumerate(void_groups):
        print(ind, len(level.keys()))
        # if ind >4:
        #     continue
        for void in level.keys():
            if void in voids_in_clusters:
                continue
            new_cluster = set()
            new_cluster.add(void)
            for neighbor in level[void]:
                if neighbor in voids_in_clusters:
                    continue
                new_cluster.add(neighbor)
                voids_in_clusters.add(neighbor)
            void_clusters.append(new_cluster)
            # if ind == 3:

            if len(new_cluster) > 3:
                continue
            print('new cluster', len(new_cluster), '\n', new_cluster)

        #     print(ind, void)
    print('compounds', len(void_clusters))

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
    tally -= (6*void_census[0]+5*void_census[1])
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
