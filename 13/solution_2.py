from functools import cmp_to_key

def extract_pairs(stream):
    output = []
    pair = []
    line = data_stream.readline()
    while line:
        if line == '\n':
            output.append(pair)
            pair = []
            line = data_stream.readline()    
            continue
        # print(line)
        # print(eval(line))
        pair.append(eval(line))
        line = data_stream.readline()    
        # print(parse_string(list(line)))
    output.append(pair)
    return output    
  
def is_ordered(list0, list1):
    '''
    ways to return True:
        two intgers are compared and I0 < I1
            I0 > I1 -> return False
        list0 runs out of items before list1 
    '''
    # print(pair)
    # print(pair[1])
    for index in range(len(list1)): #second list should be longer
        try:
            item0 = list0[index]
            item1 = list1[index]
        except IndexError as e:
            # print('L0 is shorter than L1, should be truthy')
            # print(e)
            return True
        type0 = type(item0)
        type1 = type(item1)
        # print(type0, type1)
        if (type0, type1) == (int, int):        
            if item0 < item1:
                return True
            if item0 > item1:
                return False
            # third case equal, keep checking
            continue

        if (type0, type1) == (list, list):
            next_pair = (item0, item1)
        if (type0, type1) == (int, list):
            next_pair = ([item0], item1)
        if (type0, type1) == (list, int):
            next_pair = (item0, [item1])
            # print('fart', item0, item1)
        
        result = is_ordered(next_pair[0], next_pair[1])
        if result == 'continue':
            continue
        return result

    if len(list1)<len(list0):
        # print('L1 shorter than L0, should be falsey')
        return False
    # print('same length unresolved')
    return 'continue'

def stream_diagnostic(pairs):
    index_sum = 0
    for index, pair in enumerate(pairs):

        # print(pair[0])  
        # print(pair[1])
        ordered = is_ordered(pair[0], pair[1])
        print(ordered)
        if ordered:
            index_sum+=(index+1)
        # print('-----')
    print(index_sum)

def order_wrap(el0, el1):
    if is_ordered(el0, el1):
        return 1
    return -1

def flatten_stream(pairs):
    output = [[[2]], [[6]]]
    for pair in pairs:
        output.append(pair[0])
        output.append(pair[1])
    return output

if __name__ == '__main__':
    with open('input.txt', 'r') as data_stream: # 
    # with open('test_input.txt', 'r') as data_stream: # expect 13, part2 140
        pairs = extract_pairs(data_stream)
        # stream_diagnostic(pairs) #5922 is too low
        flat_stream = flatten_stream(pairs)
        ordered_stream = sorted(flat_stream, key=cmp_to_key(order_wrap), reverse=True)
        # print(ordered_stream)
        print((ordered_stream.index([[2]])+1)*(ordered_stream.index([[6]])+1))
        # for packet in ordered_stream:
        #     print(packet) 
