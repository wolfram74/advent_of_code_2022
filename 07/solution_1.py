class Directory:
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
        self.size = 0
        self.level = 0
        self.sub_directories = {}
        self.files = []

    def add_file(self, new_file):
        self.files.append(new_file)
        self.size += new_file.size

    def add_directory(self, new_directory):
        new_directory.level = self.level+1
        self.sub_directories[new_directory.name] = new_directory


class File:
    def __init__(self, name, parent, size):
        self.name = name
        self.parent = parent
        self.size = size


def generate_file_tree(command_log):
    file_tree = {}
    folder_dict = {}
    pwd_name = '/'
    deepest_level = 0
    folder_dict[pwd_name] = Directory(pwd_name, parent = None)
    pwd = folder_dict[pwd_name]
    print(folder_dict[pwd_name].name)
    while True:
        line_feed = command_log.readline().rstrip().split(' ')
        # print(line_feed)
        # starts with either $, dir or an int
        # int is easy, add file directory
        # dir is also easy, add blank directory to directory
        # cd
        if line_feed[0] == '':
            break
        if line_feed[0] == 'dir':
            new_folder = Directory(
                name=line_feed[1], parent=pwd_name
                )
            if new_folder.name in folder_dict:
                print('oh fuck')
            folder_dict[new_folder.name] = new_folder
            pwd.add_directory(new_folder)
            continue
        if line_feed[0] == '$':
            if line_feed[1] == 'ls':
                continue
            pwd_name = line_feed[2]
            if pwd_name == '..':
                pwd_name = pwd.parent
            pwd = folder_dict[pwd_name]
            if pwd.level > deepest_level:
               deepest_level = pwd.level 
            continue
        file_size = int(line_feed[0])
        file_name = line_feed[1]
        new_file = File(
            name=file_name, size=file_size, parent=pwd_name
            )
        pwd.add_file(new_file)
    print(pwd.files)
    print(pwd.size)
    print(pwd.level)
    print(deepest_level)
    # print(folder_dict.keys())
    return folder_dict

def include_directory_size(folder_dict):
    # identify what level directories are in
    # start from lowest adding their size to directory size
    # 
    directories_by_level = [[] for el in range(8)]
    for dir_name in folder_dict.keys():
        directory = folder_dict[dir_name]
        directories_by_level[directory.level].append(directory.name)
    for level in directories_by_level:
        print(level)

        
if __name__ == '__main__':
    with open('input.txt', 'r') as command_log:
        # goal: sum every directory with size <= 100000
        command_log.readline()
        command_log.readline() # get into / and start reading contents
        folder_dict = generate_file_tree(command_log)
        print(folder_dict['/'].size)
        include_directory_size(folder_dict)
        print(folder_dict['/'].size)



