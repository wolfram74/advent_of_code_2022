'''
root has two trees, one which will resolve completely, one that has my term in it
I need to resolve the full tree (already done essentially)
and invert mine so I know what to produce
'''

def parse_file(file_name):
    output = {}
    seen = set()
    with open(file_name, 'r') as encrypted:
        for line in encrypted.readlines():
            monk_id, operation = line.rstrip().split(': ')
            try:
                number = int(operation)
                output[monk_id] = number
                if monk_id == 'humn':
                    output[monk_id] = monk_id
            except:
                left_monk = operation[:4]
                right_monk = operation[-4:]
                action = operation[5]
                output[monk_id] = [left_monk, action, right_monk]
            if monk_id in seen:
                print(monk_id, 'is repeated')
            seen.add(monk_id)
    return output

def expand_list(input_list, expression_dict):
    output_list = [0 for el in input_list]
    lookups = False
    layer_lookups = False
    for index, term in enumerate(input_list):
        if type(term)==list:
            results = expand_list(term, expression_dict)
            output_list[index], layer_lookups = results[0], (layer_lookups or results[1])
            # print('found sublist', term, layer_lookups)
            # print('found sublist', term)
            continue
        if term == 'humn':
            output_list[index] = term
            continue            
        if not term in expression_dict:
            output_list[index] = term
            continue
        output_list[index] = expression_dict[term]
        lookups = True
    # print('call status')
    # print(input_list)
    # print(output_list)
    # print(lookups, layer_lookups, '|', (lookups or layer_lookups))
    return output_list, (lookups or layer_lookups)

operations = {
    '+': (lambda x,y: x+y),
    '-': (lambda x,y: x-y),
    '*': (lambda x,y: x*y),
    '/': (lambda x,y: int(x/y)),
}

inverse_ops = {
    '+':'-',
    '-':'+',
    '*':'/',
    '/':'*'
}
def collapse_tree(expression_tree):
    output = 0
    x = expression_tree[0]
    y = expression_tree[2]
    op = expression_tree[1]
    weirdness = False
    # if x == 2:
    #     print('hey, its happening', expression_tree)
    #     weirdness = True
    if x == 'humn' or y == 'humn':
        print(expression_tree, 'turned into \n', x, op, y)
        return expression_tree
    if type(x)==list:
        x = collapse_tree(x)
    if type(y)==list:
        y = collapse_tree(y)
    if type(x)==list or type(y)==list:
        return expression_tree
    try:
        return operations[op](x, y)
    except:
        if weirdness:
            print('weird', x, y)
        print(expression_tree, 'turned into \n', x, op, y)
        return([x, op, y])
        exit()

def trim_dowel(left_exp, right_exp):
    if type(left_exp) == int:
        output = left_exp
        dowel = right_exp
    else:
        output = right_exp
        dowel = left_exp
    # any given layer of dowel is a number, an operation and a list
    while type(dowel) == list:
        operation = dowel[1]
        # print(dowel)
        if type(dowel[0])==int:
            number = dowel[0]
            dowel = dowel[2]
        else:
            number = dowel[2]
            dowel = dowel[0]
        print(output, number)
        output = operations[inverse_ops[operation]](output, number)
    print(output,dowel)

    return output

def solution(file_name):
    expression_dict = parse_file(file_name)
    # for key in expression_dict.keys():
    #     print(key, expression_dict[key])
    # for index, term in enumerate(expression_dict['root']):
    #     print(term, index)
    #     if type(term)==list:
    #         continue
    #     if not term in expression_dict:
    #         continue
    #     expression_dict['root'][index] = expression_dict[term]
    lookups = True
    # for i in range(6):
    while lookups:
        expression_dict['root'], lookups = expand_list(expression_dict['root'], expression_dict)
        print(lookups)
    # print(len(expression_dict['root']))
    # print(expression_dict['root'])
    left_value = collapse_tree(expression_dict['root'][0])
    right_value = collapse_tree(expression_dict['root'][2])
    print(left_value, 'L')
    print(right_value, 'R')
    result = trim_dowel(left_value, right_value)
    return result

if __name__ == '__main__':
    
    if not solution('test_input.txt') == 301:
        print('test failed, stopping')
        exit()

    print('test passing, onto full')
    # exit()
    print(solution('input.txt'))
    # part 1 4310
    # 4040 too high
