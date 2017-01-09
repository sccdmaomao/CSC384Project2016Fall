#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete the Sokoban warehouse domain.

#   You may add only standard python imports---i.e., ones that are automatically
#   available on TEACH.CS
#   You may not remove any imports.
#   You may not import or otherwise source any of your own files

#import os for time functions
from search import * #for search engines
from sokoban import SokobanState, Direction, PROBLEMS, sokoban_goal_state #for Sokoban specific classes and problems
import time

#SOKOBAN HEURISTICS
def heur_displaced(state):
  '''trivial admissible sokoban heuristic'''
  '''INPUT: a sokoban state'''
  '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''
  count = 0
  for box in state.boxes:
    if box not in state.storage:
      count += 1
    return count

def heur_manhattan_distance(state):
#IMPLEMENT
    '''admissible sokoban heuristic: manhattan distance'''
    '''INPUT: a sokoban state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''
    #We want an admissible heuristic, which is an optimistic heuristic.
    #It must always underestimate the cost to get from the current state to the goal.
    #The sum Manhattan distance of the boxes to their closest storage spaces is such a heuristic.
    #When calculating distances, assume there are no obstacles on the grid and that several boxes can fit in one storage bin.
    #You should implement this heuristic function exactly, even if it is tempting to improve it.
    #Your function should return a numeric value; this is the estimate of the distance to the goal.

    # 1. find paris of all shorest distance
    all_pairs = []   # a list of pair of nearest box to storage, duplicate storage may exsists
    for box in state.boxes:
        min_distance = float("inf")
        for storage in state.storage:
            distance = calc_distance(box, storage)
            if distance < min_distance:
                min_distance = distance
        pair = (box, min_distance)  # i.e. ((boxX,boxY), (storageX, storageY), distance)
        all_pairs.append(pair)

    # 2. add up the distances in all_pairs, after cleaned up duplicate storages
    manhattan_distance = 0
    for pair in all_pairs:
        manhattan_distance += pair[1]
    return manhattan_distance


'''
    A helper function to calculate the absolute distance from start to end on a 2D grid.
'''
def calc_distance(start, end):
    return abs(abs(start[0]) - abs(end[0])) + abs(abs(start[1]) - abs(end[1]))

'''
    heur_alternate(state) will return the sum of best estimte distance between a box and empty storage
    Improvements:
        1. storage can only be taken once
        2. 'Dead ends' have infinit distance value so its not preferable
        Dead-ends are:
            1. storage that can't store box. i.e. box can't be pushed into storage. 2 units of space is required
                to push a box to storage
            2. box in corner

'''
def heur_alternate(state):
#IMPLEMENT
    '''a better sokoban heuristic'''
    '''INPUT: a sokoban state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''
    #heur_min_moves has flaws.
    #Write a heuristic function that improves upon heur_manhattan_distance to estimate distance between the current state and the goal.
    #Your function should return a numeric value for the estimate of the distance to the goal.


    # use greedy strategy, the duplicate with shortest distance wins. others need to find alternative
    # 1. find paris of all shorest distance
    all_pairs = []   # a list of pair of nearest box to storage, no duplicate storage exsists
    avaliable_storage = list(state.storage or [])
    for box in state.boxes or []:
        min_distance = float("inf")
        nearest_storage = None
        for storage in avaliable_storage:
            distance = calc_heuristic_distance(state, box, storage, avaliable_storage)
            if distance < min_distance:
                min_distance = distance
                nearest_storage = storage
        if (min_distance == float("inf")):
            # there is no solution
            return min_distance
        pair = (box, nearest_storage, min_distance)  # i.e. ((boxX,boxY), (storageX, storageY), distance)
        all_pairs.append(pair)
        avaliable_storage.remove(nearest_storage)   # remove the stroage from avaliable_storage
    # 2. add up the distances in all_pairs, after cleaned up duplicate storages
    heuristic_value = 0
    for pair in all_pairs:
        heuristic_value += pair[2]
    return heuristic_value

'''
    A helper function to refine distance calculation
    Distance is infinit if any of the following condition is satisfied.
        1. storage that can't store box. i.e. box can't be pushed into storage. 2 units of space is required
            to push a box to storage
        2. box in corner
'''
def calc_heuristic_distance(state, box, storage, avaliable_storage):

    # best case
    if box == storage:
        return 0
    # Check for box in corner (height, width, obstacles taken into account)
    x = box[0]
    y = box[1]
    if (x + 1 == state.width or (x + 1, y) in state.obstacles):  # right side of box is stuck
        if (y == 0 or (x, y - 1) in state.obstacles):    # top is stuck
            return float("inf")
        if (y + 1 == state.height or (x, y + 1) in state.obstacles): # bottom is stuck
            return float("inf")
    elif (x == 0 or (x - 1, y) in state.obstacles): # left side of box is stuck
        if (y == 0 or (x, y - 1) in state.obstacles):    # top is stuck
            return float("inf")
        if (y + 1 == state.height or (x, y + 1) in state.obstacles): # bottom is stuck
            return float("inf")

    # Check for invalid storage
    x = storage[0]
    y = storage[1]
    # a storage is invalid when all four directions are blocked
    # left side of storage is blocked. i.e. can't push in a box
    if (x - 1 <= 0 or (x - 1, y) in state.obstacles or (x - 2, y) in state.obstacles):
        # top side of storage is blocked.
        if (y - 1 <= 0 or (x, y - 1) in state.obstacles or (x, y - 2) in state.obstacles):
            # right side of storage is blocked.
            if (x + 1 >= state.width or (x + 1, y) in (state.obstacles) or (x + 2, y) in state.obstacles):
                # bottom is also blocked
                if (y + 1 >= state.height or (x, y + 1) in (state.obstacles) or (x, y + 2) in state.obstacles):
                    avaliable_storage.remove((x,y))   # remove invalid storage from avaliable storage
                    return float("inf")
    return abs(abs(box[0]) - abs(storage[0])) + abs(abs(box[1]) - abs(storage[1]))

def fval_function(sN, weight):
#IMPLEMENT
    """
    Provide a custom formula for f-value computation for Anytime Weighted A star.
    Returns the fval of the state contained in the sNode.

    @param sNode sN: A search node (containing a SokobanState)
    @param float weight: Weight given by Anytime Weighted A star
    @rtype: float
    """

    #Many searches will explore nodes (or states) that are ordered by their f-value.
    #For UCS, the fvalue is the same as the gval of the state. For best-first search, the fvalue is the hval of the state.
    #You can use this function to create an alternate f-value for states; this must be a function of the state and the weight.
    #The function must return a numeric f-value.
    #The value will determine your state's position on the Frontier list during a 'custom' search.
    #You must initialize your search engine object as a 'custom' search engine if you supply a custom fval function.

    return (1 - weight) * sN.gval + weight * sN.hval

def weighted_astar(initail_state, timebound = 10):
#IMPLEMENT
    '''Provides an implementation of weighted a-star, as described in the HW1 handout'''
    '''INPUT: a sokoban state that represents the start state and a timebound (number of seconds)'''
    '''OUTPUT: A goal state (if a goal is found), else False'''

    start = time.time()
    MAX_WEIGHT = 1
    MIN_WEIGHT = 0
    weight = MAX_WEIGHT
    se = SearchEngine('custom', 'full')
    best_result = False
    result = se.search(initState=initail_state, heur_fn = heur_alternate, timebound = timebound, fval_function = fval_function, weight = weight, goal_fn=sokoban_goal_state)
    while time.time() - start < timebound: # keep trying different weight while we have time.
        if result: # the weight finds a solution, try smaller weight
            best_result = result
            weight = weight / 1.25
            result = se.search(initState=initail_state, heur_fn = heur_alternate, timebound = timebound / 5, fval_function = fval_function, weight = weight, goal_fn=sokoban_goal_state)
        else: # current weight doesn't find a solution, try a greater weight
            weight = weight * 1.1
            result = se.search(initState=initail_state, heur_fn = heur_alternate, timebound = timebound / 5, fval_function = fval_function, weight = weight, goal_fn=sokoban_goal_state)
    return best_result or result

if __name__ == "__main__":
  #TEST CODE
  solved = 0; unsolved = []; counter = 0; percent = 0; timebound = 2; #2 second time limit for each problem
  print("*************************************")
  print("Running A-star")

  for i in range(0,40): #note that there are 40 problems in the set that has been provided.  We just run through 10 here for illustration.

    print("*************************************")
    print("PROBLEM {}".format(i))

    s0 = PROBLEMS[i] #Problems will get harder as i gets bigger

    se = SearchEngine('astar', 'full')
    final = se.search(s0, sokoban_goal_state, heur_displaced, timebound)

    if final:
      final.print_path()
      solved += 1
    else:
      unsolved.append(i)
    counter += 1

  if counter > 0:
    percent = (solved/counter)*100

  print("*************************************")
  print("{} of {} problems ({} %) solved in less than {} seconds.".format(solved, counter, percent, timebound))
  print("Problems that remain unsolved in the set are Problems: {}".format(unsolved))
  print("*************************************")

  solved = 0; unsolved = []; counter = 0; percent = 0; timebound = 8; #8 second time limit
  print("Running Anytime Weighted A-star")

  for i in range(0,40):
    print("*************************************")
    print("PROBLEM {}".format(i))

    s0 = PROBLEMS[i] #Problems get harder as i gets bigger
    final = weighted_astar(s0, timebound)

    if final:
      final.print_path()
      solved += 1
    else:
      unsolved.append(i)
    counter += 1

  if counter > 0:
    percent = (solved/counter)*100

  print("*************************************")
  print("{} of {} problems ({} %) solved in less than {} seconds.".format(solved, counter, percent, timebound))
  print("Problems that remain unsolved in the set are Problems: {}".format(unsolved))
  print("*************************************")
