def load_tree_grid(tree_map):
    output = []
    for line in tree_map.readlines():
        output.append(
            [int(el) for el in list(line.rstrip())]
            )
        print(output[-1])
    return output


if __name__ == '__main__':
    with open('input.txt', 'r') as tree_map:

        tree_grid = load_tree_grid(tree_map)

        # include_directory_size(folder_dict)
        # print(folder_dict['/'].size)
        # files_under_threshold(folder_dict, 100000)

