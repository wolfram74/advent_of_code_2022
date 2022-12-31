import solution_1
import unittest

class HorizontalCase(unittest.TestCase):
    @unittest.skip("not complicated enough")
    def test_horizontal(self):
        elf_list = solution_1.parse_file('test_input3.txt')
        elf_list, movers = solution_1.take_turn(elf_list, 0)
        self.assertEqual(movers, 2)
        self.assertEqual(set([(0,0),(1,0)]), solution_1.settify_elves(elf_list))
        elf_list, movers = solution_1.take_turn(elf_list,1)
        self.assertEqual(movers, 2)
        self.assertEqual(set([(0,1),(1,1)]), solution_1.settify_elves(elf_list))
        elf_list, movers = solution_1.take_turn(elf_list,2)
        self.assertEqual(movers, 2)
        self.assertEqual(set([(-1,1),(2,1)]), solution_1.settify_elves(elf_list))
        elf_list, movers = solution_1.take_turn(elf_list,3)
        self.assertEqual(movers, 0)
        self.assertEqual(set([(-1,1),(2,1)]), solution_1.settify_elves(elf_list))

class Horizontal3Case(unittest.TestCase):
    @unittest.skip("not complicated enough")
    def test_horizontal3(self):
        elf_list = solution_1.parse_file('test_input8.txt') # initial set 0,1 | 1,1 | 2,1
        elf_list, movers = solution_1.take_turn(elf_list, 0)
        self.assertEqual(movers, 3)
        self.assertEqual(set([(0,0),(1,0),(2,0)]), solution_1.settify_elves(elf_list))
        elf_list, movers = solution_1.take_turn(elf_list,1)
        self.assertEqual(movers, 3)
        self.assertEqual(set([(0,1),(1,1),(2,1)]), solution_1.settify_elves(elf_list))
        elf_list, movers = solution_1.take_turn(elf_list,2)
        self.assertEqual(movers, 3)
        self.assertEqual(set([(-1,1),(1,0),(3,1)]), solution_1.settify_elves(elf_list))
        elf_list, movers = solution_1.take_turn(elf_list,3)
        self.assertEqual(movers, 0)
        # self.assertEqual(True, False)
        self.assertEqual(set([(-1,1),(1,0),(3,1)]), solution_1.settify_elves(elf_list))

class VerticalCase(unittest.TestCase):
    @unittest.skip("not complicated enough")
    def test_vertical(self):
        elf_list = solution_1.parse_file('test_input4.txt') # initially 1,0| 1,1

        elf_list, movers = solution_1.take_turn(elf_list, 0)
        self.assertEqual(movers, 2)
        self.assertEqual(set([(1,-1),(1,2)]), solution_1.settify_elves(elf_list))

        elf_list, movers = solution_1.take_turn(elf_list,1)
        self.assertEqual(movers, 0)
        self.assertEqual(set([(1,-1),(1,2)]), solution_1.settify_elves(elf_list))

class Vertical3Case(unittest.TestCase):
    @unittest.skip("not complicated enough")
    def test_vertical3(self):
        elf_list = solution_1.parse_file('test_input7.txt') # initially 1,0| 1,1 | 1,2

        elf_list, movers = solution_1.take_turn(elf_list, 0)
        self.assertEqual(movers, 3)
        self.assertEqual(set([(1,-1),(0,1),(1,3)]), solution_1.settify_elves(elf_list))

        elf_list, movers = solution_1.take_turn(elf_list,1)
        self.assertEqual(movers, 0)
        self.assertEqual(set([(1,-1),(0,1),(1,3)]), solution_1.settify_elves(elf_list))

class Diag1Case(unittest.TestCase):
    @unittest.skip("not complicated enough")
    def test_diag_1(self):
        elf_list = solution_1.parse_file('test_input5.txt') # initiall 0,0| 1,1

        elf_list, movers = solution_1.take_turn(elf_list, 0)
        self.assertEqual(movers, 2)
        self.assertEqual(set([(0,-1),(1,2)]), solution_1.settify_elves(elf_list))

        elf_list, movers = solution_1.take_turn(elf_list,1)
        self.assertEqual(movers, 0)
        self.assertEqual(set([(0,-1),(1,2)]), solution_1.settify_elves(elf_list))

class Diag2Case(unittest.TestCase):
    @unittest.skip("not complicated enough")
    def test_diag_2(self):
        elf_list = solution_1.parse_file('test_input6.txt') # initiall 1,0| 0,1

        elf_list, movers = solution_1.take_turn(elf_list, 0)
        self.assertEqual(movers, 2)
        self.assertEqual(set([(1,-1),(0,2)]), solution_1.settify_elves(elf_list))

        elf_list, movers = solution_1.take_turn(elf_list,1)
        self.assertEqual(movers, 0)
        self.assertEqual(set([(1,-1),(0,2)]), solution_1.settify_elves(elf_list))

class FiveElfCase(unittest.TestCase):
    def test_bulk_movement(self):
        turn_0 = solution_1.parse_file('test_input2.txt') 
        after1_turn, movers = solution_1.take_turn(turn_0, 0)
        # self.assertEqual(True, False)

        print('turn 0', solution_1.settify_elves(turn_0))
        turn_1 = solution_1.parse_file('test_input2b.txt') 
        set_1 = solution_1.settify_elves(turn_1)
        self.assertEqual(solution_1.settify_elves(after1_turn), set_1)


        print('turn 1', solution_1.settify_elves(after1_turn), movers)
        after2_turn, movers = solution_1.take_turn(after1_turn, 1)
        # 2,2 tries to south, scared, so checks west
        print('turn 2', solution_1.settify_elves(after2_turn), movers)

        turn_2 = solution_1.parse_file('test_input2c.txt') 
        set_2 = solution_1.settify_elves(turn_2)
        self.assertEqual(solution_1.settify_elves(after2_turn), set_2)

        after3_turn, movers = solution_1.take_turn(after2_turn, 2)
        after4_turn, movers = solution_1.take_turn(after3_turn, 3)

        turn_3 = solution_1.parse_file('test_input2d.txt') 
        set_3 = solution_1.settify_elves(turn_3)
        self.assertEqual(solution_1.settify_elves(after3_turn), set_3)
        self.assertEqual(solution_1.settify_elves(after4_turn), set_3)


if __name__ == '__main__':
    unittest.main()
