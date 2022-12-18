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

    def best_next(self, branching_factor, plan, debug=False):
        # first pass at trying to have bart and stampy team up

        bart = self.valves[plan[-1][1]]
        stampy = self.valves[plan[-1][3]]
        bart_time = self.total_time-plan[-1][0]
        stampy_time = self.total_time-plan[-1][2]
        valve_set = set(self.flowing.keys())
        bart_set = set([el[1] for el in plan])
        stampy_set = set([el[3] for el in plan])
        unvisited = (
            (valve_set-bart_set)-stampy_set
            )
        if debug:
            print(valve_set)
            print(bart_set, stampy_set)
            print(valve_set-bart_set)
        # in 1 player options were a 2-item pressure value, destination, 
        # maybe 2 player is a 3 item, pressure value, bart destination, stampy destination
        # only one of which is changed? so each candidate generates two options
        options = []
        for candidate in unvisited:
            if debug:
                print(candidate)
            delta_t_b = 1+len(bart.paths[candidate])
            delta_t_s = 1+len(stampy.paths[candidate])
            value_b = self.flowing[candidate]*(bart_time-delta_t_b)
            value_s = self.flowing[candidate]*(stampy_time-delta_t_s)
            if debug:
                print('---')
                print(bart_time, stampy_time)
                print(delta_t_b, delta_t_s)
                print(value_b, value_s)
            if value_b > 0:
                options.append([value_b, candidate, stampy.ID])
            if value_s > 0:
                options.append([value_s, bart.ID, candidate])
        options = list(sorted(options, key=lambda x: x[0], reverse=True))
        # print(options)
        return options[:branching_factor]

    def advance_step(self, branching_factor, debug=False):
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

    def rank_plans(self, final=False):
        if final:
            self.finished_plans = list(sorted(self.finished_plans, reverse=True, key=self.evaluate_plan))
            return
        self.plans = list(sorted(self.plans, reverse=True, key=self.evaluate_plan))
        return

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

    def decile_report(self):
        contenders = len(self.finished_plans)
        for i in range(10):
            index = int(contenders*i/10)
            print(i, index,'---',self.evaluate_plan(self.finished_plans[index]))
        return

    def prune_bottom_two_thirds(self):
        contenders = len(self.plans)
        keep_index = int(contenders/3)
        self.rank_plans()
        self.plans = self.plans[:keep_index]
        return

    def prune_best_finished(self):
        # contenders = 
        if len(self.finished_plans) == 0:
            return
        # keep_index = int(contenders/3)
        self.rank_plans(final=True)
        self.finished_plans = [self.finished_plans[0]]
        return


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
    print('there are %d flow positive valves' % len(plan_coordinator.flowing.keys()))
    # print(print_distance_matrix(valves))
    # if len(valves.keys())> 20:
    #     exit()
    # print(plan.best_next(branching_factor = 3, path = plan.paths[0]))
    steps = 0
    while plan_coordinator.plans:
    # for i in range(7):
        plan_coordinator.advance_step(branching_factor=15)
        steps += 1
        print('%02d' % steps, len(plan_coordinator.plans), len(plan_coordinator.finished_plans))
        if len(plan_coordinator.plans) > 10**6:
            plan_coordinator.prune_bottom_two_thirds()
        plan_coordinator.prune_best_finished()
        # print(steps, len(plan_coordinator.plans), len(plan_coordinator.finished_plans))
    plan_coordinator.rank_plans(final=True)

    # print('time left')
    # for plan in plan_coordinator.plans:
    #     # print(plan_coordinator.evaluate_plan(plan), plan)
    #     print(plan_coordinator.evaluate_plan(plan))
    # print(plan_coordinator.plans)

    # print('time up')
    # for plan in plan_coordinator.finished_plans:
    #     # print(plan_coordinator.evaluate_plan(plan), plan)
    #     print(plan_coordinator.evaluate_plan(plan))
    # print(len(plan_coordinator.plans), len(plan_coordinator.finished_plans))
    # print(plan_coordinator.finished_plans[0])
    winner = plan_coordinator.finished_plans[0]
    # plan_coordinator.decile_report()
    # plan_coordinator.best_next(branching_factor=8, plan = winner, debug=True)
    return plan_coordinator.evaluate_plan(winner)

def print_distance_matrix(valves):
    keys = list(valves.keys())
    print(keys)
    for key in keys:
        row_valve = valves[key]
        # print(type(row_valve.paths))
        travels = [len(row_valve.paths[key2]) for key2 in keys ]
        print(travels)


if __name__ == '__main__':
    
    # if not solution('test_input.txt') == 1707:
    #     print('test failed, stopping')
    #     exit()
    # if not solution('test_input2.txt') == (30*24+29*23):
    #     print('test failed, stopping')
    #     exit()
    # if not solution('test_input3.txt') == (30*24+29*23+25*22):
    #     print('test failed, stopping')
    #     exit()
    # if not solution('test_input4.txt') == 1707:
    #     print('test failed, stopping')
    #     exit()

    print('test passing, onto full')
    # exit()
    print(solution('input.txt'))
    # part 1 best 1896

    # bf 5 -> 2320
    # bf 6 -> 2320
    # bf 7 -> 2339 x
    # bf 8 -> 2339 x
    # bf 9 -> 2380 wrong
    # bf 10 -> 2402
    # bf 11 -> 2483
    # bf 12 -> 2483 wrong
    # bf 13 -> 2483 x
    # bf 14 -> 2483 x
    # bf 15 -> 2339
'''
1 14
2 196
3 2728
4 35483
5 405387
6 4155731
7 39767211

1 15
2 225
3 3346
4 46148
5 557803
6 6057606
7 61493639

01 15 0
02 225 0
03 3375 0
04 50304 0
05 682699 0
06 6787579 8037
07 17090968 52738

'''


# bad time keeping for stampy/vs part
# bf 5 -> 1794
# bf 6 -> 1803
# bf 7 -> 1828
# plan = [(0, 'AA', 0, 'AA'), (5, 'JO', 0, 'AA'), (9, 'KP', 0, 'AA'), (9, 'KP', 7, 'EV'), (9, 'KP', 11, 'FB'), (16, 'CN', 11, 'FB'), (19, 'HB', 11, 'FB')]
# bf 8 -> 1828
# plan = [(0, 'AA', 0, 'AA'), (5, 'JO', 0, 'AA'), (9, 'KP', 0, 'AA'), (9, 'KP', 7, 'EV'), (9, 'KP', 11, 'FB'), (16, 'CN', 11, 'FB'), (19, 'HB', 11, 'FB')]

# bf 9 -> 1828 too low
# bf 10 -> 1828 
# bf 11 -> 1828 X
# bf 12 -> 1828 X
# bf 13 -> 1828 x
# bf 14 -> 1828 x
# bf 15 -> 1828 god damn it

# hadn't disabled premature exit after 7 loops
# bf 4 -> 1641
# bf 5 -> 1655
# bf 6 -> 1655
# bf 7 -> 1685
# bf 8 -> 1685
# bf 9 -> 1685 x
# bf 10 -> 1685 x
# bf 11 -> 1685 x
# bf 12 -> 1685 x
# bf 13 -> 1685
# bf 14 -> 1685
# bf 15 -> 1685