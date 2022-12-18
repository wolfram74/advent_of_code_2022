'''
so the path can't be longer than 30 steps regardless, and any openings shortens it
the branching factor in the actual input is pretty always at least 2, sometimes much higher
also a lot of the nodes have no output so the paths will be on the long side
don't think we can naively generate every path see what works best
'''
import re


class Valve:
    def __init__(self, string):
        id_reg = re.compile('([A-Z][A-Z])')
        flow_reg = re.compile(r'rate=(\d+)')
        ids = re.findall(id_reg, string)
        
        self.ID = ids[0]
        self.flow = int(re.findall(flow_reg, string)[0])
        self.neighbors = ids[1:]
        self.paths = {self.ID:[]}
        for val in self.neighbors:
            self.paths[val] = [val]

    def find_new_paths(self, valves):
        newbies = []
        for found in self.paths.keys():
            frontier = valves[found]
            for candi in frontier.neighbors:
                if candi in self.paths.keys():
                    continue
                step = (found, candi)
                newbies.append(step)
        for newbie in newbies:
            self.paths[newbie[1]] = self.paths[newbie[0]] + [newbie[1]]
        return len(self.paths.keys())

class Plan:
    def __init__(self, valves):
        #list of lists, each base element has time to get to place, and ID of place
        self.plans = [[(0, 'AA')]]
        self.total_time = 30
        self.valves = valves
        self.flowing = {}
        self.finished_plans = []
        for key in self.valves.keys():
            valve = self.valves[key]
            if valve.flow > 0:
                self.flowing[key] = valve.flow

    def best_next(self, branching_factor, plan):
        options = []
        origin = self.valves[plan[-1][1]]
        time_left = self.total_time-plan[-1][0]
        unvisited = set(self.flowing.keys()) - set([el[1] for el in plan])
        for candidate in unvisited:
            # print(candidate)
            # print(origin.paths[candidate])
            delta_t = 1+len(origin.paths[candidate])
            value = self.flowing[candidate]*(time_left-delta_t)
            if value < 0:
                continue
            options.append([value, candidate])
        options = list(sorted(options, key=lambda x: x[0], reverse=True))
        # print(options)
        return options[:branching_factor]

    def advance_step(self):
        new_plans = []
        for plan in self.plans:
            head = self.valves[plan[-1][1]]
            time_passed = plan[-1][0]

            options = self.best_next(branching_factor=13, plan=plan)
            if len(options) == 0:
                self.finished_plans.append(plan)
            for option in options:
                delta_t = 1 + len(head.paths[option[1]])
                new_plans.append(plan+[(time_passed + delta_t, option[1])])
                if new_plans[-1][-1][0] >= 28:
                    self.finished_plans.append(new_plans.pop())
        self.plans = new_plans

    def rank_plans(self):
        self.plans = list(sorted(self.plans, reverse=True, key=self.evaluate_plan))
        self.finished_plans = list(sorted(self.finished_plans, reverse=True, key=self.evaluate_plan))

    def evaluate_plan(self, plan):
        pressure = 0
        for step in plan:
            delta_t = self.total_time-step[0]
            pressure += delta_t*self.valves[step[1]].flow
        return pressure


def parse_file(file_name):
    valves = {}
    with open(file_name, 'r') as text:
        for line in text.readlines():
            new_valve = Valve(line.rstrip())
            valves[new_valve.ID] = new_valve
    return valves

def distance_calc(valves, origin, destination):
    paths = [[origin]]
    pathing = True
    while pathing:
        new_paths = []
        # candidates = []
        for path in paths:
            head = path[-1]
        #     next_steps = 
        # candidates+= 

def path_caching2(valves):
    valve_count = len(valves.keys())
    flowing = True
    while flowing:
        done = True
        for v_id in valves.keys():
            valve = valves[v_id]
            if len(valve.paths.keys())==valve_count:
                continue
            paths = valve.find_new_paths(valves)
            if len(valve.paths.keys())==valve_count:
                continue
            done = False
            # if not done:
                # print(valve.ID)
                # print(valve.paths.keys())
        flowing = not done
    # print(valve.ID)
    # print(valve.paths)

def solution(file_name):
    valves = parse_file(file_name)
    path_caching2(valves)
    plan_coordinator = Plan(valves)
    # print(print_distance_matrix(valves))
    # if len(valves.keys())> 20:
    #     exit()
    # print(plan.best_next(branching_factor = 3, path = plan.paths[0]))
    steps = 0
    while plan_coordinator.plans:
        plan_coordinator.advance_step()
        steps += 1
        print(steps, len(plan_coordinator.plans))
    plan_coordinator.rank_plans()
    # print('time left')
    # for plan in plan_coordinator.plans:
    #     print(plan_coordinator.evaluate_plan(plan), plan)
    # print(plan_coordinator.plans)
    # print('time up')
    # for plan in plan_coordinator.finished_plans:
    #     print(plan_coordinator.evaluate_plan(plan), plan)
    # print(len(plan_coordinator.plans), len(plan_coordinator.finished_plans))

    return plan_coordinator.evaluate_plan(plan_coordinator.finished_plans[0])

def print_distance_matrix(valves):
    keys = list(valves.keys())
    print(keys)
    for key in keys:
        row_valve = valves[key]
        # print(type(row_valve.paths))
        travels = [len(row_valve.paths[key2]) for key2 in keys ]
        print(travels)


if __name__ == '__main__':
    
    if not solution('test_input.txt') == 1651:
        print('test failed, stopping')
        exit()
    print('test passing, onto full')
    # exit()
    print(solution('input.txt'))

