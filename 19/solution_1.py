import re
from math import ceil

'''
given possible builds we need to explore our decision tree and figure out how to maximize 4th resource (geodes) in fixed time
every turn robots increase their respective supply by 1 per bot
every turn we have a choice to spend resources to increase our bot supply by one next turn
we could model trajectories turn by turn, or we could model them based on what options are available
ie: at turn 0 we could decide to wait 4 turns to start on an ore bot or wait 2 turns to start on a claybot
tree structure, nodes are factory states, branching factor at most 4,

new tack avoiding recursion:
 just treat them like 9 dimensional points in configuration space, do a normal frontier set/candidate set thing
 iterative, cuts out redundant checks that are path agnostic
'''
def vector_add(v1, v2):
    return tuple([sum(el) for el in zip(v1, v2)])

def vector_diff(v1, v2):
    return tuple([el[0]-el[1] for el in zip(v1, v2)])

def vector_scale(v1, c):
    return tuple([el*c for el in v1])


class Factory:
    robot_outputs = {
        'orebot': (1,0,0,0),
        'claybot': (0,1,0,0 ),
        'obsibot': (0,0,1,0),
        'geodbot': (0,0,0,1),
    }
    def __init__(self,bp_ID, recipes, parent_factory=None):
        self.parent_factory = parent_factory
        self.bp_ID = bp_ID
        self.costs = recipes
        self.turn = 0
        self.robots = [1,0,0,0]
        self.resources = [0,0,0,0]
        self.next_steps = []

    def options(self):
        possible = []
        for name in self.costs.keys():
            # print(name)
            needs = self.costs[name]
            buildable = True
            for index in range(len(needs)):
                if needs[index]==0:
                    continue
                if self.robots[index]==0:
                    buildable = False
                    break
            if buildable:
                possible.append(name)
        return possible

    def minimum_build_time(self, target):
        cost = self.costs[target]
        limiting_time = 0
        for index in range(len(cost)):
            # print(cost)
            if cost[index]==0:
                continue
            if self.robots[index]==0:
                print('should have run options first, cant build %s' % target)
                raise ValueError
            deficit = cost[index]-self.resources[index]
            if deficit < 0:
                continue
            limiting_time = ceil(deficit/self.robots[index])
        return limiting_time+1

    def generate_next_options(self):
        '''
        1) find the possible next builds
        2) for each option
            find time to build
            if time>24, skip it
            find resources at time of completion
            set up new factory with parent, finished time, resources, new robots
            add to next steps
        '''
        next_moves = self.options()
        for option in next_moves:
            new_factory = Factory(self.bp_ID, self.costs, parent_factory=self)
            move_duration = self.minimum_build_time(option)
            # print(option, move_duration)
            turn_value = self.turn+move_duration
            if turn_value > 24:
                continue

            new_factory.turn = turn_value #what time does this factory state exist at
            resource_delta = vector_scale(self.robots, move_duration)
            resource_delta = vector_diff(resource_delta, self.costs[option])
            # how many resources does it have
            new_factory.resources = vector_add(self.resources, resource_delta)
            # how many robots does it have
            new_factory.robots = vector_add(self.robots, Factory.robot_outputs[option])

            self.next_steps.append(new_factory)

            # for turn in range(move_duration):
            #     resource_delta = vector_add(resource_delta, self.robots)

    def max_geode_production(self):
        # if self.robots[3]==0:
        #     return 0
        time_left = 24-self.turn
        return self.robots[3]*time_left+self.resources[3]


def parse_file(file_name):
    cost = re.compile(r'(\d+)')
    options = []
    with open(file_name, 'r') as blueprints:
        for plan in blueprints.readlines():
            # print(plan)
            values = re.findall(cost, plan)
            values = [int(el) for el in values]
            # print(values)
            recipes = {
                # 'bp_ID': values[0],
                # resource vector ore, clay, obsidian, geode
                'orebot': (values[1],0,0,0),
                'claybot': (values[2],0,0,0 ),
                'obsibot': (values[3],values[4],0,0),
                'geodbot': (values[5],0,values[6],0),
            }
            options.append([values[0], recipes])
    return options

def test_factory_options(test_factory):
    targets = test_factory.options()
    for target in targets:
        print(test_factory.minimum_build_time(target))

def test_generate_next_options(test_factory):
    test_factory.generate_next_options()
    print(test_factory.next_steps[0].resources)
    print(test_factory.next_steps[0].robots)
    print(test_factory.next_steps[1].resources)
    print(test_factory.next_steps[1].robots)
    print(test_factory.next_steps[1].turn)
    follow = test_factory.next_steps[1]
    follow.generate_next_options()
    print(follow.next_steps[0].robots)
    print(follow.next_steps[1].robots)
    print(follow.next_steps[1].resources)
    print(follow.next_steps[1].turn)
    # print(follow.next_steps[2].robots)

def recurse_factory(factory):
    # print('inside recursion', factory.turn)
    best_value = factory.max_geode_production()
    if factory.turn == 24:
        if best_value > 8:
            print(factory.turn, factory.robots, best_value)
        return best_value
    factory.generate_next_options()
    # print(factory.turn, [nex.turn for nex in factory.next_steps])
    for option in factory.next_steps:
        result = recurse_factory(option)
        if result > best_value:
            best_value = result

            # print(option.turn, option.robots, best_value)

    return best_value

def solution(file_name):
    blueprints = parse_file(file_name)
    # print(blueprints)
    # resource vector ore, clay, obsidian, geode
    bots = [1,0,0,0]
    test_factory = Factory(blueprints[0][0], blueprints[0][1])
    # test_factory_options(test_factory)
    test_generate_next_options(test_factory)
    # print(recurse_factory(test_factory))


if __name__ == '__main__':
    
    if not solution('test_input.txt') == 33:
        print('test failed, stopping')
        exit()

    print('test passing, onto full')
    # exit()
    print(solution('input.txt'))
    # part 1 4310
    # 4040 too high
    # 2441 too low
    # 2341
    # 3985 too high