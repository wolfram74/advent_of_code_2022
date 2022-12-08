class Directory:
    def __init__(self, name, parent_address):
        self.name = name
        self.parent_address = parent_address
        if parent_address:
            self.address = '-'.join([parent_address, name])
        else:
            self.address = name
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
    def __init__(self, name, parent_address, size):
        self.name = name
        self.parent_address = parent_address
        self.size = size


def generate_file_tree(command_log):
    file_tree = {}
    folder_dict = {}
    pwd_name = '/'
    deepest_level = 0
    folder_dict[pwd_name] = Directory(pwd_name, parent_address = None)
    pwd = folder_dict[pwd_name]
    # print(folder_dict[pwd_name].name)
    total_file_size = 0
    while True:
        line_feed = command_log.readline().rstrip().split(' ')
        # print(line_feed)
        # starts with either $, dir or an int
        # int is easy, add file directory
        # dir is also easy, add blank directory to directory
        # directory names are not unique
        # cd
        if line_feed[0] == '':
            break
        if line_feed[0] == 'dir':
            new_folder = Directory(
                name=line_feed[1],
                parent_address=pwd.address
                )
            if new_folder.address in folder_dict:
                print('oh fuck')
            folder_dict[new_folder.address] = new_folder
            pwd.add_directory(new_folder)
            continue
        if line_feed[0] == '$':
            if line_feed[1] == 'ls':
                continue
            pwd_name = line_feed[2]
            if pwd_name == '..':
                pwd_name = pwd.parent_address
                pwd = folder_dict[pwd_name]
                continue

            # print(pwd.name, pwd_name)
            # print(pwd.name, pwd.sub_directories.keys(), pwd_name)
            # print(pwd.sub_directories[pwd_name].address)

            # print(folder_dict.keys())
            target_address = pwd.sub_directories[pwd_name].address

            pwd = folder_dict[target_address]
            if pwd.level > deepest_level:
               deepest_level = pwd.level 
            continue
        file_size = int(line_feed[0])
        total_file_size += file_size
        file_name = line_feed[1]
        new_file = File(
            name=file_name, size=file_size, parent_address=pwd.address
            )
        pwd.add_file(new_file)
    print(pwd.files)
    print(pwd.size)
    print(pwd.level)
    print(deepest_level, total_file_size)
    # print(folder_dict.keys())
    return folder_dict

def include_directory_size(folder_dict):
    # identify what level directories are in
    # start from lowest adding their size to directory size
    # 
    directories_by_level = [[] for el in range(8)]
    for dir_name in folder_dict.keys():
        directory = folder_dict[dir_name]
        directories_by_level[directory.level].append(directory.address)
    for level in range(7, 0, -1):
        directory_tier = directories_by_level[level]
        for address in directory_tier:
            folder = folder_dict[address]
            parent = folder_dict[folder.parent_address]
            parent.size+=folder.size

def files_under_threshold(folder_dict, threshold):
    total_size = 0
    for address in folder_dict.keys():
        folder = folder_dict[address]
        if folder.size <= threshold:
            total_size+= folder.size
    print(total_size)
        
if __name__ == '__main__':
    with open('input.txt', 'r') as command_log:
        # goal: sum every directory with size <= 100000
        command_log.readline()
        command_log.readline() # get into / and start reading contents
        folder_dict = generate_file_tree(command_log)
        print(folder_dict['/'].size)
        include_directory_size(folder_dict)
        print(folder_dict['/'].size)
        files_under_threshold(folder_dict, 100000)


