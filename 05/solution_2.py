def init_stack_state(crane_plan):
    raw_lines = []
    crates_state = [[] for el in range(9)]
    content = True
    while content:
        line = crane_plan.readline()
        if line.rstrip()=='':
            break
        if line[0] == ' ':
            continue
        raw_lines.append(line.rstrip())

    for line in raw_lines:
        for index, stack in enumerate(crates_state):
            slot = index*4+1 #letter value is always in same column of text
            if slot >= len(line):
                continue
            if line[slot] == ' ':
                continue
            stack.append(line[slot])

    return crates_state

def parse_instruction(line):
    output = []
    values = [1,3,5]
    words = line.split(' ')
    output = [int(words[el]) for el in values]
    # print(output)
    return output

def crane_operation(state, instruction):
    #move 3 from 8 to 9
    #crate indices are 0 indexed instead of 1 indexed, so a minus 1 will happen

    #pop(0) from crate 8-1, insert(0) resulting element onto crate 9-1, do so 3 times
    crates = instruction[0]
    origin = instruction[1]-1
    destination = instruction[2]-1
    intermediate = []
    for i in range(crates):
        intermediate.append(state[origin].pop(0))
    for i in range(crates):
        state[destination].insert(0, intermediate.pop())
    return state

def print_crates(state):
    for stack in state:
        print(stack)
    print()

def top_stack(state):
    top_row = []
    for stack in state:
        top_row.append(stack[0])
    print(''.join(top_row))


if __name__ == '__main__':
    top_boxs = []
    with open('input.txt', 'r') as crane_plan:
        crates_state = init_stack_state(crane_plan)
        print_crates(crates_state)
        raw_instruction = crane_plan.readline()
        # instruction = parse_instruction(raw_instruction)
        # crates_state = crane_operation(crates_state, instruction)
        # print_crates(crates_state)

        while raw_instruction:
            instruction = parse_instruction(raw_instruction)
            crates_state = crane_operation(crates_state, instruction)
            raw_instruction = crane_plan.readline()

        print_crates(crates_state)
        top_stack(crates_state)


    # print(total_score) # not 330