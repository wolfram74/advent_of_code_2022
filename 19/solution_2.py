import re
from math import ceil
import numpy
'''
given possible builds we need to explore our decision tree and figure out how to maximize 4th resource (geodes) in fixed time
every turn robots increase their respective supply by 1 per bot
every turn we have a choice to spend resources to increase our bot supply by one next turn
we could model trajectories turn by turn, or we could model them based on what options are available
ie: at turn 0 we could decide to wait 4 turns to start on an ore bot or wait 2 turns to start on a claybot
tree structure, nodes are factory states, branching factor at most 4,

hanging at ~half a billion numbers (56million visits, 9 numbers per visit), maybe I'm having ram issues?
the visit and frontier spaces could be a list of sets 
'''
def vector_add(v1, v2):
    return tuple([sum(el) for el in zip(v1, v2)])

def vector_diff(v1, v2):
    return tuple([el[0]-el[1] for el in zip(v1, v2)])

def vector_scale(v1, c):
    return tuple([el*c for el in v1])


class Factory:
    robot_outputs = {
        'orebot': numpy.array((1,0,0,0)),
        'claybot': numpy.array((0,1,0,0 )),
        'obsibot': numpy.array((0,0,1,0)),
        'geodbot': numpy.array((0,0,0,1)),
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
        self.most_geode = 0

    def options(self, state):
        possible = []
        robots = state[-4:]
        for name in self.costs.keys():
            # print(name)
            if name == 'orebot':
                if robots[0]>=3:
                    continue
            if name == 'claybot':
                if robots[1]>=11:
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
        return self.optimize_options(state, possible)

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

    def optimize_options(self, state, options):
        trimmed_options = options
        # if you could buy an obsi before geode, ignore buying a geode
        # if you could buy a clay before obsi
        # print('raw', options)
        if len(options) == 1:
            return options
        if options == ['orebot', 'claybot']:
            return options
        time_to_clay = self.minimum_build_time('claybot', state)
        time_to_obsi = self.minimum_build_time('obsibot', state)
        if options[-1]=='geodbot':
            # return options
            time_to_geode = self.minimum_build_time('geodbot', state)
            # time_to_obsi = self.minimum_build_time(options[-2], state)
            delta = time_to_geode-time_to_obsi
            # delta_clay = time_to_obsi-time_to_clay
            if delta == 0:
                return options
            if delta*state[5]>3:
                trimmed_options.pop()
        delta_clay = time_to_obsi-time_to_clay
        if delta_clay == 0:
            return trimmed_options
        if delta_clay*state[5]>3:
            trimmed_options.pop()
    
        # if delta_clay
            # print('trimmed')
            # return trimmed_options

        # print('----------', options, state, delta)
        # print(self.costs['obsibot'])
        # print(self.costs['geodbot'])
        return options


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
        fantasy_output = self.fantasy_geode_production(present)
        if fantasy_output < self.most_geode:
            return
        present = numpy.array(present)
        next_moves = self.options(present)
        # print('optimized', next_moves)
        time = present[0]
        robots = present[-4:]
        resources = present[1:5]

        for option in next_moves:
            move_duration = self.minimum_build_time(option, present)
            # print(option, move_duration)
            turn_value = time+move_duration
            if turn_value > 32:
                self.terminal_states.add(tuple(present))
                continue

            resource_delta = robots*move_duration
            resource_delta = resource_delta - self.costs[option]
            # how many resources does it have
            next_resources = resources+resource_delta
            # how many robots does it have
            next_robots = robots+Factory.robot_outputs[option]
            next_state = (turn_value,) + tuple(next_resources) + tuple(next_robots)
            if next_state in self.visited_states:
                continue

            if next_state in self.frontier:
                # print('front dupe')
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
        time_left = 32-state[0]
        return state[-1]*time_left+state[4]

    def fantasy_geode_production(self, state):
        time_left = 32-state[0]
        triangle = int(time_left*(time_left+1)/2)
        return state[4]*time_left+state[-1]+triangle

    def trim_finals(self):
        # print(len(self.terminal_states))
        while self.terminal_states:
            end_state = self.terminal_states.pop()
            geodes = self.max_geode_production(end_state)
            if geodes > self.most_geode:
                self.most_geode = geodes

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
                'orebot': numpy.array((values[1],0,0,0)),
                'claybot': numpy.array((values[2],0,0,0 )),
                'obsibot': numpy.array((values[3],values[4],0,0)),
                'geodbot': numpy.array((values[5],0,values[6],0)),
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
                factory.most_geode
                )
        factory.trim_finals()
    # best = 0
    # for end_state in factory.terminal_states:
    #     results = factory.max_geode_production(end_state)
    #     if results > best:
    #         best = results
    #         # print(end_state, best)
    return factory.most_geode

def solution(file_name):
    blueprints = parse_file(file_name)
    # print(blueprints)
    # resource vector ore, clay, obsidian, geode
    # bots = [1,0,0,0]
    # test_factory = Factory(blueprints[0][0], blueprints[0][1])
    # # test_factory_options(test_factory)
    # test_generate_next_options(test_factory)
    quality_scores = 1
    for design in blueprints:
        if design[0] > 3:
            break
        candidate_factory = Factory(design[0], design[1])
        geodes = find_best_result(candidate_factory)
        print(design[0], geodes)
        quality_scores *= geodes
    return quality_scores

if __name__ == '__main__':
    
    # if not solution('test_input.txt') == 62*56:
    #     print('test failed, stopping')
    #     exit()

    print('test passing, onto full')
    # exit()
    print(solution('input.txt')) 
    # 1760, 4, 44, 10 # too low
