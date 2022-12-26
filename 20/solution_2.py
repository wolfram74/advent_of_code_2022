'''
input text has repeated values
and some very large values
some kind of linked list solution where each node knows
    it's value
    it's original position
    it's current position
    and how to move from it's current position to where it should be
would take ~5000^2 operations. 25 million isn't too bad compared with the valve problem
a node object that knows it's neighbors and current index as well as a having methods for editing those
and a list that has the original order, iterate through that list in order should work


iteratively moving step by step is having some tricky behavior at cycle over points
would probably go away if we switched to just calculating new index and teleporting

ok multiplying all the values by a ~billion will make a tolerable compute time impossibly long.
of course we can expedite the steps by taking the modulus of %list size

not going quite like I would prefer
maybe look around for data structures that will help
need to be able to quickly find specific elements
and move them a certain number of spaces
option1: elements in a list are (original_index, value), use pop(location) and insert()
    have an unchanging list that keeps the original order intact for coordination purposes

'''
class MapCell:
    def __init__(self, value, index, size):
        self.value = value
        self.index = index
        self.list_size = size
        self.left_cell = None
        self.right_cell = None

    def set_left(self, left):
        self.left_cell = left

    def set_right(self, right):
        self.right_cell = right

    def mix(self):
        if self.value == 0:
            return 0 
        if self.value < 0:
            # self.go_right(left=True)
            return self.go_left()
        return self.go_right()

    def go_left(self):
        steps = abs(self.value)
        steps %= self.list_size
        underflow = False
        if self.index + self.value < 0:
            underflow = True
        # old_index = self.index
        # new_index = (old_index + self.value)%self.list_size

        # # establish hole
        # old_right = self.right_cell
        # old_left = self.left_cell
        # next_left = old_left
        # for loop in range(steps):
        #     if next_left.index == new_index:
        #         break
        #     next_left = next_left.left_cell
        # print(next_left.index, new_index)

        for loop in range(steps):
            old_index = self.index
            new_index = self.left_cell.index

            old_right = self.right_cell
            old_left = self.left_cell
            new_right = old_left
            new_left = old_left.left_cell

            old_right.set_left(old_left)
            
            old_left.set_right(old_right)
            old_left.set_left(self)

            new_left.set_right(self)

            self.set_left(new_left)
            self.set_right(new_right)

            self.right_cell.index = old_index
            self.index = new_index

        if underflow:
            return -1
        return 0
        # print(self.left_cell, (self.index, self.value), self.right_cell)

    def go_right(self, left = False):
        steps = abs(self.value)
        steps %= self.list_size
        overflow = False
        if self.index + self.value >= self.list_size:
            overflow = True

        if left:
            steps = self.value % self.list_size
        for loop in range(steps):
            old_index = self.index
            new_index = self.right_cell.index

            old_right = self.right_cell
            old_left = self.left_cell

            new_left = old_right
            new_right = old_right.right_cell

            old_left.set_right(old_right)
            
            old_right.set_left(old_left)
            old_right.set_right(self)

            new_right.set_left(self)

            self.set_left(new_left)
            self.set_right(new_right)

            self.left_cell.index = old_index
            self.index = new_index
        # print(self.left_cell, (self.index, self.value), self.right_cell)
        if overflow:
            return 1
        return 0

    def __str__(self):
        return '%d, %d' % (self.index, self.value)

def parse(file_name):
    output = []
    seen = set()
    with open(file_name, 'r') as encrypted:
        for value in encrypted.readlines():
            output.append(int(value))
            if value in seen:
                print(value, 'is repeated')
            seen.add(value)
    return output

def reconstruct(map_code, shift=0):
    size = len(map_code)
    output = [0 for el in range(size)]
    for cell in map_code:
        output[(cell.index+shift)%size] = cell.value
    return output

def solution(file_name):
    output = 0
    code = parse(file_name)
    decryption_key = 811589153
    print(code)
    size = len(code)
    map_code = [MapCell(code[0]*decryption_key, 0, size)]
    for index in range(1, len(code)):
        new_cell = MapCell(code[index]*decryption_key, index, size)
        map_code.append(new_cell)

        map_code[-1].set_left(map_code[-2])
        map_code[-2].set_right(map_code[-1])
    # return output
    map_code[0].set_left(map_code[-1])
    map_code[-1].set_right(map_code[0])


    # map_code[2].mix()
    # map_code[1].mix()
    # head = map_code[0]
    # for loop in range(len(map_code)*2):
    #     print(head.left_cell, head, head.right_cell)
    #     head = head.right_cell
    print('begin')
    shift = 0
    print(reconstruct(map_code, shift))
    for mix_cycle in range(10):
        for loop in range(len(map_code)):
            # print(head.left_cell, head, head.right_cell)
            # head = head.right_cell
            if loop %500==499:
                print(loop)
            shift += map_code[loop].mix()
        print(reconstruct(map_code, shift), shift)

    # for cell in map_code:
    #     print(cell)
    decrypted = reconstruct(map_code, shift)
    start_index = decrypted.index(0)
    key_vals = (
        decrypted[(start_index+1000)%size],
        decrypted[(start_index+2000)%size],
        decrypted[(start_index+3000)%size]
        )
    print(key_vals, sum(key_vals))
    return sum(key_vals)
    # print([1, 2, -3, 4, 0, 3, -2], 'wanted')


if __name__ == '__main__':
    
    if not solution('test_input.txt') == 1623178306:
        print('test failed, stopping')
        exit()

    print('test passing, onto full')
    exit()
    print(solution('input.txt'))
    # part 1 4310
    # 4040 too high
    # 2441 too low
    # 2341
    # 3985 too high