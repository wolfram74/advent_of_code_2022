import re
from math import ceil

snaf_map = {'0':0, '1':1, '2':2, '-':-1, '=':-2}
arab_map = {0:'0', 1:'1', 2:'2', -1:'-', -2:'='}

def snaf_to_arab(string):
    total = 0
    power = len(string)
    for i in range(power):
        total+= 5**(power-i-1)*snaf_map[string[i]]
    return total

def arab_to_snaf(number):
    base_5 = []
    power = 1
    while number:
        unit = 5**power
        place = number % unit
        base_5.insert(0, int(5* place/unit))
        number -= place
        power += 1
        print(base_5, number)
    output = ""
    changing = True
    while changing:
        changing = False
        for i in reversed(range(len(base_5))):
            print(i, base_5[i])
            if base_5[i]>2:
                changing = True
                base_5[i]-=5
                if i==0:
                    base_5.insert(0, 1)
                    break
                base_5[i-1]+=1
        print(base_5)
    string = [arab_map[el] for el in base_5]
    # print(string, ''.join(string))

    return ''.join(string)
    # print(base_5)
    # pass

def solution(file_name):
    running_total = 0
    with open(file_name, 'r') as fuel_loads:
        for snafu_string in fuel_loads.readlines():
            value = snaf_to_arab(snafu_string.rstrip())
            print(snafu_string, value)
            running_total += value
    print(running_total)
    output = arab_to_snaf(running_total)
    print(output)
    return output

if __name__ == '__main__':
    
    if not solution('test_input.txt') == '2=-1=0':
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