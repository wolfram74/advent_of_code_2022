def vector_add(v1, v2):
    return tuple([sum(el) for el in zip(v1, v2)])

def vector_diff(v1, v2):
    return tuple([el[0]-el[1] for el in zip(v1, v2)])

def mh_metric(p1, p2):
    diff = vector_diff(p1, p2)
    return sum([abs(el) for el in diff])

def parse_input(file):
    output = []
    bounds = [[10**6,0],[10**6,0]]
    for line in file.readlines():
        sensor, beacon = line.split(':')
        s_pieces = sensor.split(' ')
        b_pieces = beacon.split(' ')
        sensor_pos = [
            int(s_pieces[-2].split('=')[-1][:-1]),
            int(s_pieces[-1].split('=')[-1]),
            ]
        beacon_pos = [
            int(b_pieces[-2].split('=')[-1][:-1]),
            int(b_pieces[-1].split('=')[-1]),
            ]
        # print([sensor_pos, beacon_pos])
        output.append([sensor_pos, beacon_pos])
        for point in output[-1]:
            x,y = point
            if x > bounds[0][1]:
                bounds[0][1] = x
            if x < bounds[0][0]:
                bounds[0][0] = x
            if y > bounds[1][1]:
                bounds[1][1] = y
            if y < bounds[1][0]:
                bounds[1][0] = y

    return output, bounds

def rule_outs(beacon_pairs, x_bounds, row_check):
    row = set(range(x_bounds[0],x_bounds[1]+1))
    print(len(row))
    # print(row)
    rejects = []
    # print(row)
    for pair in beacon_pairs:
        sens = pair[0]
        beac = pair[1]
        distance = mh_metric(sens,beac)
        delta_y = abs(sens[1]-row_check)
        if delta_y > distance:
            # print(sens, 'too far to matter')
            continue
        # print(sens, 'care about it')
        x_budget = distance - delta_y
        print(sens, distance ,x_budget)
        print(sens[0]-x_budget, sens[0]+x_budget+1)
        for check in range(sens[0]-x_budget, sens[0]+x_budget+1):
            # print(check)
            # if check%1000 == 0:
            #     print(check, sens)
            if not check in row:
                continue
            row.remove(check)
            rejects.append(check)
    #     print(len(rejects), rejects)
    # print(len(rejects), sorted(rejects))

    # return 5
    return len(rejects)

def composite_range_builder(beacon_pairs, x_bounds, row_check):
    ranges = []
    for pair in beacon_pairs:
        sens = pair[0]
        beac = pair[1]
        distance = mh_metric(sens,beac)
        delta_y = abs(sens[1]-row_check)
        if delta_y > distance:
            # print(sens, 'too far to matter')
            continue
        # print(sens, 'care about it')
        x_budget = distance - delta_y
        # print(sens, distance ,x_budget)
        # print(sens[0]-x_budget, sens[0]+x_budget)
        sensor_range = [sens[0]-x_budget, sens[0]+x_budget]
        stitched = False
        for index, bounds in enumerate(ranges):
            if not overlap_check(bounds, sensor_range):
                continue
            ranges[index] = stitch_ranges(bounds, sensor_range)
            stitched = True
            break
        if not stitched:
            ranges.append(sensor_range)
    output = []
    while not len(output)==1:
        for range0 in ranges:
            stitched = False
            for index, bounds in enumerate(output):
                if not overlap_check(bounds, range0):
                    continue
                output[index] = stitch_ranges(bounds, range0)
                stitched = True
                break
            if not stitched:
                output.append(range0)
        ranges = output
        print(ranges)
        if len(output) == 1:
            break
        output = []

    print(ranges)

def inside_range(bounds, value):
    if bounds[0] > value:
        return False
    if bounds[1] < value:
        return False
    return True

def overlap_check(range1, range2):
    if inside_range(range1, range2[0]):
        return True
    if inside_range(range1, range2[1]):
        return True
    if inside_range(range2, range1[1]):
        return True
    return False

def stitch_ranges(range1, range2):
    return [min(range1[0],range2[0]), max(range1[1],range2[1])]

def beacon_check(pairs, row):
    output = 0
    found = set()
    conflict = set()
    for pair in pairs:
        beac = tuple(pair[1])
        if beac in found:
            continue
        found.add(beac)
        if beac[1] == row:
            print(pair[1])
            output+=1
    print(found, output)
    return output

if __name__ == '__main__':
    with open('test_input.txt', 'r') as sensor_positions: # expect 26
        sensor_beacon_pairs, space = parse_input(sensor_positions)
        row_query = 10
        # print(space)
        # width = space[0][1]-space[0][0]
        # print(mh_metric(sensor_beacon_pairs[0][0], sensor_beacon_pairs[0][1]))
        rejects = rule_outs(sensor_beacon_pairs, space[0], row_query)
        beacons_in_row = beacon_check(sensor_beacon_pairs, row_query)
        composite_range_builder(sensor_beacon_pairs, space[0], row_query)
        # print(rejects, beacons_in_row)
        total = rejects-beacons_in_row
        # total = 7
        # print(total, total==26)
        if not total==26:
            exit()
    # exit()
    with open('input.txt', 'r') as sensor_positions: # 
        print('going to the big leagues')
        sensor_beacon_pairs, space = parse_input(sensor_positions)
        print(space)
        row_query = 2000000
        composite_range_builder(sensor_beacon_pairs, space[0], row_query)

        # rejects = rule_outs(sensor_beacon_pairs, space[0], row_query)
        # beacons_in_row = beacon_check(sensor_beacon_pairs, row_query)
        # print(rejects, beacons_in_row)
        # total = rejects-beacons_in_row
        # print(total) #4406715 is too low
        # synthetic bound approach also yields 4406715
        # not limiting space to places where things already are gets 5367037 and the right answer


