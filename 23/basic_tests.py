import solution_1
import unittest
class HorizontalCase(unittest.TestCase):
    def test_horizontal(self):
        elf_list = solution_1.parse_file('test_input3.txt')
        elf_list, movers = solution_1.take_turn(elf_list)
        self.assertEqual(movers, 2)
        self.assertEqual(set([(0,0),(1,0)]), solution_1.settify_elves(elf_list))
        elf_list, movers = solution_1.take_turn(elf_list)
        self.assertEqual(movers, 2)
        self.assertEqual(set([(0,1),(1,1)]), solution_1.settify_elves(elf_list))
        elf_list, movers = solution_1.take_turn(elf_list)
        self.assertEqual(movers, 2)
        self.assertEqual(set([(-1,1),(2,1)]), solution_1.settify_elves(elf_list))
        elf_list, movers = solution_1.take_turn(elf_list)
        self.assertEqual(movers, 0)
        self.assertEqual(set([(-1,1),(2,1)]), solution_1.settify_elves(elf_list))


if __name__ == '__main__':
    unittest.main()
