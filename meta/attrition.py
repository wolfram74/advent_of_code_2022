stats = [
(13, 25670, 1389),
(12, 38450, 903),
(11, 49382, 7264),
(10, 63493, 4037),
(9, 63033, 8843),
(8, 83588, 5923),
(7, 89483, 1861),
(6, 124460, 1119),
(5, 126465, 2199),
(4, 148391, 2535),
(3, 160934, 7959),
(2, 187099, 8457),
(1, 223555, 9350),
]

def part_two_drop_off():
    print('drop off from part 2')
    for pair in stats:
        print(pair[0], pair[2]/pair[1])

def day_to_day():
    print('drop off from day to day')
    for index, day in enumerate(stats[:-2]):
        print(day[0], day[1]/stats[index+1][1])

if __name__ == '__main__':

    part_two_drop_off()
    day_to_day()
