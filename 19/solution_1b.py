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

observation: the way I'm deciding time points it should be impossible to have a state with 0 of any resource that has robots
the fact that my best out come violates that implies my build function is using resources that are gathered while building is happening
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
        '''
        factory state is completely described by a 9-vector
        t, res_4, rob_4
        '''
        self.parent_factory = parent_factory
        self.bp_ID = bp_ID
        self.costs = recipes
        # self.turn = 0
        # self.robots = [1,0,0,0]
        # self.resources = [0,0,0,0]
        self.visited_states = set()
        self.terminal_states = set()
        self.frontier = set()
        self.frontier.add((
            0,
            0,0,0,0,
            1,0,0,0,
            ))
        self.next_steps = []

    def options(self, state):
        possible = []
        robots = list(state[-4:])
        for name in self.costs.keys():
            # print(name)
            if name == 'orebot':
                if robots[0]>=4:
                    continue
            needs = self.costs[name]
            buildable = True
            for index in range(len(needs)):
                if needs[index]==0:
                    continue
                if robots[index]==0:
                    buildable = False
                    break
            if buildable:
                possible.append(name)
        return possible

    def minimum_build_time(self, target, state):
        cost = self.costs[target]
        limiting_time = 0
        resources = state[1:5]
        robots = state[-4:]
        for index in range(len(cost)):
            # print(cost)
            if cost[index]==0:
                continue
            if robots[index]==0:
                print('should have run options first, cant build %s' % target)
                raise ValueError
            deficit = cost[index]-resources[index]
            if deficit < 0:
                continue
            possible_limit = ceil(deficit/robots[index])
            if possible_limit > limiting_time:
                limiting_time = possible_limit
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
        present = self.frontier.pop()
        self.visited_states.add(present)
        next_moves = self.options(present)
        time = present[0]
        robots = present[-4:]
        resources = present[1:5]

        for option in next_moves:
            move_duration = self.minimum_build_time(option, present)
            # print(option, move_duration)
            turn_value = time+move_duration
            if turn_value > 24:
                self.terminal_states.add(present)
                continue

            resource_delta = vector_scale(robots, move_duration)
            resource_delta = vector_diff(resource_delta, self.costs[option])
            # how many resources does it have
            next_resources = vector_add(resources, resource_delta)
            # how many robots does it have
            next_robots = vector_add(robots, Factory.robot_outputs[option])
            next_state = tuple(
                [turn_value]+
                list(next_resources)+
                list(next_robots))
            if next_state in self.visited_states:
                continue
            if next_state[1]==0:
                print(present, next_state)
                exit()
            self.frontier.add(next_state)

            # for turn in range(move_duration):
            #     resource_delta = vector_add(resource_delta, self.robots)

    def max_geode_production(self,state):
        # if self.robots[3]==0:
        #     return 0
        time_left = 24-state[0]
        return state[-1]*time_left+state[4]


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
    present = test_factory.frontier.pop()
    targets = test_factory.options(present)
    for target in targets:
        print(test_factory.minimum_build_time(target, present))

def test_generate_next_options(test_factory):
    # present = test_factory.frontier.pop()
    test_factory.generate_next_options()
    # for state in test_factory.next_steps:
    #     print(state)
    # print(test_factory.frontier)
    # print(test_factory.visited_states)
    # test_factory.generate_next_options()
    # for state in test_factory.frontier:
    #     print(state)
    # print(test_factory.frontier)
    # print(test_factory.visited_states)
    while test_factory.frontier:
        test_factory.generate_next_options()
        if len(test_factory.visited_states)%10000==0:
            print(
                len(test_factory.visited_states),
                len(test_factory.frontier),
                len(test_factory.terminal_states)
                )
    best = 0
    for end_state in test_factory.terminal_states:
        results = test_factory.max_geode_production(end_state)
        if results > best:
            best = results
            print(end_state, best)
    expected_states = [
        (0,0,0,0,0,1,0,0,0),
        # (0,0,0,0,0,1,0,0,0),
        (15,1,5,4,0,1,4,2,0),
        (18,2,17,3,0,1,4,2,1),
        (21,3,29,2,3,1,4,2,2),
    ]
    for check in expected_states:
        print(check,
            check in test_factory.visited_states,
            check in test_factory.terminal_states)

def find_best_result(factory):
    while factory.frontier:
        factory.generate_next_options()
        if len(factory.visited_states)%1000000==0:
            print(
                len(factory.visited_states),
                len(factory.frontier),
                len(factory.terminal_states)
                )
    best = 0
    for end_state in factory.terminal_states:
        results = factory.max_geode_production(end_state)
        if results > best:
            best = results
            # print(end_state, best)
    return best

def solution(file_name):
    blueprints = parse_file(file_name)
    # print(blueprints)
    # resource vector ore, clay, obsidian, geode
    # bots = [1,0,0,0]
    # test_factory = Factory(blueprints[0][0], blueprints[0][1])
    # # test_factory_options(test_factory)
    # test_generate_next_options(test_factory)
    quality_scores = 0
    for design in blueprints:
        candidate_factory = Factory(design[0], design[1])
        geodes = find_best_result(candidate_factory)
        print(design[0], geodes)
        quality_scores+= geodes*design[0]
    return quality_scores

if __name__ == '__main__':
    
    # if not solution('test_input.txt') == 33:
    #     print('test failed, stopping')
    #     exit()

    print('test passing, onto full')
    # exit()
    print(solution('input.txt'))
    # part 1 4310
    # 4040 too high
    # 2441 too low
    # 2341
    # 3985 too high