# no division is happening now
# the passing test only depends on what factors a number has
# truncate numbers into product of each test_num to keep sizes manageable?
class Monkey():
    def __init__(self, 
        ID_num, items, operation, test_num, recipients
        ):
        self.ID_num = ID_num
        self.items = items
        self.operation = operation
        self.test_num = test_num
        self.recipients = recipients
        self.monkey_level = 0

    def evaluate_items(self):
        self.truthy = []
        self.falsey = []
        self.monkey_level+= len(self.items)
        while self.items:
            current = self.items.pop(0)
            # new_val = int( self.operation(current)/3 )
            new_val = int( self.operation(current) )
            if new_val%self.test_num == 0:
                self.truthy.append(new_val)
                continue
            self.falsey.append(new_val)

def build_monkeys(census):
    line = census.readline()
    monkey_entry = []
    monkeys = []
    while line:
        monkey_entry.append(line.rstrip())
        # print(line)
        line = census.readline()
        if line == '\n':
            monkeys.append(parse_entry(monkey_entry))
            line = census.readline()
            monkey_entry = []
    monkeys.append(parse_entry(monkey_entry))
    return monkeys

def parse_entry(lines):
    ID_num = lines[0][-2]
    
    items = lines[1].split(':')[1].split(',')
    items = [int(el) for el in items]

    if '+' in lines[2]:
        delta = int(lines[2].split('+')[-1])
        print('+', delta)
        operation = lambda x: x + delta
    else:
        if lines[2][-3:] == 'old':
            # print(ID_num, '**')
            operation = lambda x: x**2
        else:
            factor = int(lines[2].split('*')[-1])
            # print('*', factor)

            operation = lambda x: x * factor


    test_num = int(lines[3].split('by')[-1])

    recipients = [
        int(lines[4][-1]),
        int(lines[5][-1]),
        ]

    # for line in lines:
    #     print(line)
    # print(ID_num, items, operation, test_num, recipients)
    # print('----')
    return Monkey(ID_num=ID_num, items=items, operation=operation, test_num=test_num, recipients=recipients)

def do_round(monkeys):
    for monkey in monkeys:
        monkey.evaluate_items()
        monkeys[monkey.recipients[0]].items += monkey.truthy
        monkeys[monkey.recipients[1]].items += monkey.falsey
    return monkeys

def clean_items(monkeys, space):
    for monkey in monkeys:
        monkey.items = [item%space for item in monkey.items]
    return monkeys

def inspect_items(monkeys):
    for monkey in monkeys:
        print(monkey.items)
    print('----')

def find_monkey_business(monkeys):
    monkey_levels = sorted([monkey.monkey_level for monkey in monkeys])
    print(monkey_levels[-1]*monkey_levels[-2])


if __name__ == '__main__':
    with open('input.txt', 'r') as monkey_census: #
    # with open('test_input.txt', 'r') as monkey_census: #

        monkeys = build_monkeys(monkey_census)
        # monkeys[0].evaluate_items()
        # print(monkeys[0].truthy)
        # print(monkeys[0].falsey)
        inspect_items(monkeys)
        test_nums = [monkey.test_num for monkey in monkeys]
        space = 1
        for num in test_nums:
            space *= num

        for loop in range(10000):
            monkeys = do_round(monkeys)
            monkeys = clean_items(monkeys, space)
            if loop%1000 ==0:
                inspect_items(monkeys)
                find_monkey_business(monkeys) 
        inspect_items(monkeys)
        find_monkey_business(monkeys) # 

