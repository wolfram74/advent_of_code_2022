
def vector_add(v1, v2):
    return tuple([sum(el) for el in zip(v1, v2)])

def vector_diff(v1, v2):
    return tuple([el[0]-el[1] for el in zip(v1, v2)])

def mag2(v1):
    return sum([el**2 for el in v1])

def half_size(v1):
    trunk = lambda x: x if x%2>0 else int(x/2)
    return tuple([trunk(el) for el in v1])



def build_terrain(map_data):
    terrain = []
    values = {}
    # termini = ['S', 'E']
    starts = []
    terminus = (0,0)
    for val in range(26):
        values[chr(val+97)] = val
    values['S']=0
    values['E']=25
    # print(values)
    for ind, line in enumerate(map_data.readlines()):
        if 'S' in line:
            # print(ind, line.index('S'))
            # termini[0] = (ind, line.index('S'))
            starts.append( (ind, line.index('S')) )
        if 'E' in line:
            # print(ind, line.index('E'))
            terminus = (ind, line.index('E'))
        terrain.append(
            [values[el] for el in line.rstrip()]
            )
        for x_val, elev in enumerate(terrain[-1]):
            if elev > 0:
                continue
            starts.append( (ind, x_val) )

        # print(terrain[-1])
    return terrain, terminus, starts

def navigate(terrain, termini):
    '''
    probably kind of a storage intensive breadth first search
        iterate over paths via pop(0)
        for each path identify valid next steps and generate new candidate paths from there
        check next steps against dict of steps already in paths
        if next step is new, add to path and append to list of paths
        if next step is already visited, see if new path get's there faster than previous path.
            take shorter path, put other path in rejects
    '''
    visited_points = {termini[0]:True}
    paths = [[termini[0]]]
    finished_paths = []
    dead_paths = []
    attempts = 0
    while paths:
        if attempts > 50000:
            print('panic escape-------------------')
            break
        attempts += 1
        next_path = paths.pop(0)
        # print(next_path)
        next_steps = valid_steps(terrain, next_path[-1])
        for option in next_steps:
            if option == termini[1]:
                finished_paths.append(next_path+[option])
                continue
            if not option in visited_points:
                paths.append(next_path+[option])
                visited_points[option] = True
                continue
            if option in next_path:
                continue

            next_len = len(next_path)+1
            dupes = []
            done = False
            for path_ind, old_path in enumerate(paths):
                if not option in old_path: #not relevant
                    continue
                if old_path.index(option) < next_len: #already got there
                    dead_paths.append(next_path)
                    done = True
                    break
                dupes.append((path_ind, old_path)) # new path would get to a point on these old paths faster
            if not dupes:
                done = True
            if done:
                continue

            print('should have accounted for shortcuts--')
            print(next_path+[option])
            for dupe in dupes:
                print(dupe)
            for dead in dead_paths:
                print(dead)
            print('--')
            # old_lens = list(map((lambda pat: pat.index(option) if option in pat else None), paths))
            # print(old_lens)
            # paths.append(next_path+[option])
    if len(finished_paths)==0:
        # print('finished with no paths')
        return 10**6
    if len(finished_paths)>1:
        print('finished with extra paths---------')
        return [len(path)-1 for path in finished_paths]

    # print('finished with %d paths' % len(finished_paths))

    # for path in paths:
    #     print(path)
    # for path in finished_paths:
    #     print(len(path)-1)
    #     print(path)
    return len(finished_paths[0])-1

def valid_steps(terrain, location):
    elevation = terrain[location[0]][location[1]]
    max_Y, max_X = len(terrain), len(terrain[0])
    def in_bounds(vector):
        if vector[0]<0 or vector[0]>=max_Y:
            return False
        if vector[1]<0 or vector[1]>=max_X:
            return False
        return True

    def height_gain(vector):
        # print(elevation-terrain[vector[0]][vector[1]])
        # print(terrain[vector[0]][vector[1]]-elevation)
        return (terrain[vector[0]][vector[1]]-elevation)<=1

    up = (1,0)
    right = (0,1)
    candidates = [
        vector_add(location, up),
        vector_add(location, right),
        vector_diff(location, up),
        vector_diff(location, right)
        ]
    candidates = list(filter(in_bounds, candidates))
    candidates = list(filter(height_gain, candidates))
    return list(candidates)


if __name__ == '__main__':
    with open('input.txt', 'r') as map_data: # should beat 380
    # with open('test_input.txt', 'r') as map_data: # expect 6 starts, shortest 29

        terrain, end_point, start_points = build_terrain(map_data)
        lengths = []
        for start in start_points:
            print(start)
            path = navigate(terrain, (start, end_point))
            if path < 400:
                lengths.append(path)
        print(lengths)
        print(sorted(lengths))
        # print(valid_steps(terrain, (0,2))) # should have two elements in it for test input