# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"

    class SearchNode:
        # a node which stores initialState, parent, and corresponding action
        def __init__(self, state, action=None, parent=None):
            self.state = state
            self.action = action
            self.parent = parent

    start = SearchNode(problem.getStartState())

    frontier = util.Stack()
    explored = set()
    frontier.push(start)

    # run until stack is empty
    while not frontier.isEmpty():
        node = frontier.pop()  # choose the deepest node in frontier
        explored.add(node.state)

        if problem.isGoalState(node.state):
            solution = []

            search_node = node
            while(search_node):
                if(search_node.action):
                    solution.insert(0, search_node.action)

                search_node = search_node.parent

            # print(solution)
            return solution

        # expand node
        successors = problem.getSuccessors(node.state)

        for succ in successors:
            # make-child-node
            child_node = SearchNode(succ[0], succ[1], node)
            if child_node.state not in explored:
                frontier.push(child_node)

    # no solution
    return []
    
    util.raiseNotDefined()

def check(frontier, item):
    for n in frontier.list:
        if item == n[0]:
            return True

    return False

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"

    class SearchNode:
        def __init__(self, state, action=None, parent=None):
            self.state = state
            self.action = action
            self.parent = parent


        def is_in_frontier(self, data_structure):
            for n in data_structure.list:
                if n.state == self.state:
                    return True
            return False

    start = SearchNode(problem.getStartState())

    frontier = util.Queue()
    explored = set()
    frontier.push(start)

    # run until queue is empty
    while not frontier.isEmpty():
        node = frontier.pop()
        explored.add(node.state)

        if problem.isGoalState(node.state):
            solution = []

            search_node = node
            while(search_node):
                if(search_node.action):
                    solution.insert(0, search_node.action)

                search_node = search_node.parent

            return solution

        # expand node
        successors = problem.getSuccessors(node.state)

        for succ in successors:
            child_node = SearchNode(succ[0], succ[1], node)
            if child_node.state not in explored and not child_node.is_in_frontier(frontier):
                frontier.push(child_node)

    # no solution
    return []
    
    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch