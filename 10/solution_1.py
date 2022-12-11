def reconstruct_reg_history(commands):
    register = [1]
    command = commands.readline().rstrip()
    while command:
        command = command.split(' ')
        if command[0] == "noop":
            register.append(register[-1])
        if command[0] == 'addx':
            change = int(command[1])
            register.append(register[-1])
            register.append(register[-1]+change)
        command = commands.readline().rstrip()
    return register


def signal_strength_calculator(x_reg):
    total = 0
    check = 0
    sample_index = check*40+20-1
    while sample_index < len(x_reg):
        total += x_reg[sample_index]*(sample_index+1)
        print(check, sample_index, total)
        print()
        check+=1
        sample_index = check*40+20-1
    print(total)
    pass

if __name__ == '__main__':
    with open('input.txt', 'r') as command_log:
    # with open('test_input.txt', 'r') as command_log: #13140 result

        x_reg_history = reconstruct_reg_history(command_log)
        print(x_reg_history[:10])
        print(len(x_reg_history))
        signal_strength_calculator(x_reg_history) #3740 is too low