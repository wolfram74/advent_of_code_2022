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
        # step 2 modification is 4 elements, 2nd set is where stampy is
        self.plans = [[(0, 'AA', 0, 'AA')]]
        self.total_time = 26
        self.valves = valves
        self.flowing = {}
        self.finished_plans = []
        for key in self.valves.keys():
            valve = self.valves[key]
            if valve.flow > 0:
                self.flowing[key] = valve.flow

    def best_next(self, branching_factor, plan):
        # first pass at trying to have bart and stampy team up

        bart = self.valves[plan[-1][1]]
        stampy = self.valves[plan[-1][3]]
        bart_time = self.total_time-plan[-1][0]
        stampy_time = self.total_time-plan[-1][0]
        unvisited = (
            set(self.flowing.keys()) 
            - set([el[1] for el in plan]) # bart's valves
            - set([el[3] for el in plan]) # stampy's valves
            )
        # in 1 player options were a 2-item pressure value, destination, 
        # maybe 2 player is a 3 item, pressure value, bart destination, stampy destination
        # only one of which is changed? so each candidate generates two options
        options = []
        for candidate in unvisited:
            # for index, actor in enumerate([bart, stampy]):
            #     # print(candidate)
            #     # print(origin.paths[candidate])
            delta_t_b = 1+len(bart.paths[candidate])
            delta_t_s = 1+len(stampy.paths[candidate])
            value_b = self.flowing[candidate]*(bart_time-delta_t_b)
            value_s = self.flowing[candidate]*(stampy_time-delta_t_s)
            if value_b > 0:
                options.append([value_b, candidate, stampy.ID])
            if value_s > 0:
                options.append([value_s, bart.ID, candidate])
        options = list(sorted(options, key=lambda x: x[0], reverse=True))
        # print(options)
        return options[:branching_factor]

    def advance_step(self, branching_factor):
        new_plans = []
        for plan in self.plans:
            bart = self.valves[plan[-1][1]]
            stampy = self.valves[plan[-1][3]]
            time_passed_b = plan[-1][0]
            time_passed_s = plan[-1][2]

            options = self.best_next(branching_factor=branching_factor, plan=plan)
            if len(options) == 0:
                self.finished_plans.append(plan)
            for option in options:
                # print(option)
                delta_t_b = 1 + len(bart.paths[option[1]])
                delta_t_s = 1 + len(stampy.paths[option[2]])

                if option[1]==bart.ID:
                    step = [(
                        time_passed_b,bart.ID, 
                        delta_t_s+time_passed_s, option[2],
                        )]
                if option[2]==stampy.ID:
                    step = [(
                        delta_t_b+time_passed_b, option[1],
                        time_passed_s,stampy.ID, 
                        )]
                
                new_plans.append(plan+step)
                if new_plans[-1][-1][0] >= 28:
                    self.finished_plans.append(new_plans.pop())
        self.plans = new_plans

    def rank_plans(self):
        self.plans = list(sorted(self.plans, reverse=True, key=self.evaluate_plan))
        self.finished_plans = list(sorted(self.finished_plans, reverse=True, key=self.evaluate_plan))

    def evaluate_plan(self, plan):
        pressure = 0
        accounted = {}
        for step in plan:
            delta_t_b = self.total_time-step[0]
            valve_b = step[1]
            delta_t_s = self.total_time-step[2]
            valve_s = step[3]
            if not valve_b in accounted:
                pressure += delta_t_b*self.valves[valve_b].flow
                accounted[valve_b] = pressure
            if not valve_s in accounted:
                pressure += delta_t_s*self.valves[valve_s].flow
                accounted[valve_s] = pressure
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
    # while plan_coordinator.plans:
    for i in range(7):
        plan_coordinator.advance_step(branching_factor=3)
        steps += 1
        print(steps, len(plan_coordinator.plans))
    plan_coordinator.rank_plans()
    print('time left')
    # for plan in plan_coordinator.plans:
    #     # print(plan_coordinator.evaluate_plan(plan), plan)
    #     print(plan_coordinator.evaluate_plan(plan))
    # print(plan_coordinator.plans)
    print('time up')
    # for plan in plan_coordinator.finished_plans:
    #     # print(plan_coordinator.evaluate_plan(plan), plan)
    #     print(plan_coordinator.evaluate_plan(plan))
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
    
    if not solution('test_input.txt') == 1707:
        print('test failed, stopping')
        exit()
    print('test passing, onto full')
    # exit()
    print(solution('input.txt'))

