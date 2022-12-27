
def parse_file(file_name):
    output = {}
    seen = set()
    with open(file_name, 'r') as encrypted:
        for line in encrypted.readlines():
            monk_id, operation = line.rstrip().split(': ')
            try:
                number = int(operation)
                output[monk_id] = number
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
def collapse_tree(expression_tree):
    output = 0
    x = expression_tree[0]
    y = expression_tree[2]
    op = expression_tree[1]
    if type(x)==list:
        x = collapse_tree(x)
    if type(y)==list:
        y = collapse_tree(y)
    try:
        return operations[op](x, y)
    except:
        print(x, op, y)
        exit()


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
    root_value = collapse_tree(expression_dict['root'])
    print(root_value)
    return root_value

if __name__ == '__main__':
    
    if not solution('test_input.txt') == 152:
        print('test failed, stopping')
        exit()

    print('test passing, onto full')
    # exit()
    print(solution('input.txt'))
    # part 1 4310
    # 4040 too high
