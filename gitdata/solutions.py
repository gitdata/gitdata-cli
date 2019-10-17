"""
    gitdata.solutions

    solution finders
"""

import logging

class StopException(Exception):
    """Stop solving"""
    pass

def stop(data):
    raise StopException()


#--------------------------------------------------------
def apply(rule, data):
    def apply_rule(rule, data):
        for row in data:
            new_row = rule(row)
            if new_row:
                if new_row == True:
                    yield row
                else:
                    try:
                        for i in new_row:
                            yield i
                    # except StopException:
                    #     yield row
                    except:
                        yield new_row
    if callable(rule):
        return apply_rule(rule, data)
    # else do some sort of outer join if what was passed is another list of
    # items

def _solve(data, rule=None, *rest):
    if rule:
        return _solve(apply(rule, data), *rest)
    else:
        return data

def solve(data, *rules):
    return list(_solve(data, *rules))


# generic predicates
#--------------------------------------------------------
def is_not(rule):
    return lambda a: not rule(a)

# output
def emit(person):
    print(person)
    return person


class Pathfinder(object):
    """Find paths in sets of edges"""

    logger = logging.getLogger(__name__)

    def __init__(self, facts=None, cost=None):
        self.facts = {}
        self.cost = cost
        self.learn(facts)

    def learn(self, facts):
        if facts:
            self.facts.update({(t, h): self.cost(t, h) for t, h in facts})

    def find(self, start, target):
        """Find multiple paths from start to target"""

        facts = self.facts.copy()
        solutions = []
        markers = []
        path = []

        def push(start, target, cost):
            """Save a segment to the path"""
            path.append((start, target, cost))

        def pick(start):
            """Pick a successor"""
            for (tail, head), cost in facts.items():
                if start == tail and head not in markers:
                    markers.append(head)
                    return head, cost

        def match(start, target):
            """Test for a match and return cost if a match is found"""
            if (start, target) in facts:
                return facts[(start, target)]

        def retract(fact):
            """Retract a fact from the database to look for alternate paths"""
            if fact in facts:
                self.logger.debug('retracting %s', fact)
                del facts[fact]

        def clear_markers():
            """Clear the markers"""
            markers.clear()

        def describe(to):
            """return a route as a english phrase"""
            result = []
            total = 0
            for tail, head, cost in path:
                result.append('{} to'.format(tail))
                total += cost
            result.append('{} - cost {}\n'.format(to, total))
            return ' '.join(result)

        def emit(*msg):
            """log a message indented to the length of the current path"""
            return self.logger.debug(' '*len(path) + ' '.join(map(str, msg)))

        def solved(start, target):
            """Solve for a path"""

            cost = match(start, target)
            if cost != None:
                emit('matched', start, target, cost, path)
                push(start, target, cost)
                return tuple(path)

            step = pick(start)
            if step:
                anywhere, cost = step
                push(start, anywhere, cost)
                emit('trying', anywhere, path)
                return solved(anywhere, target)
            elif path:
                emit('out of options on', start)
                start, _, _ = path.pop()
                emit('reattempting', start, target)
                return solved(start, target)

        while True:
            solution = solved(start, target)
            if solution:
                self.logger.debug('found solution: %s', describe(target))
                solutions.append(solution)
                markers.clear()
                tail, head, _ = path.pop()
                path.clear()
                retract((tail, head))
            else:
                self.logger.debug('no more solutions')
                break

        return solutions
