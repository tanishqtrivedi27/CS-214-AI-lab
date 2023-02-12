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
    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    frontier = util.PriorityQueue()
    explored = set()
    startNode = problem.getStartState()
    cost = {}
    parent = {}
    parent[startNode] = (None, None) # parent, direction
    cost[startNode] = 0
    frontier.push(startNode, cost[startNode])

    while (not frontier.isEmpty()):
        n = frontier.pop()

        if n in explored:
            continue
        explored.add(n)
        if (problem.isGoalState(n)):
            """
                RECONSTRUCT PATH
            """
            solution = []
            x = parent[n]
            while (x != (None, None)):
                solution.append(x[1])
                x = parent[x[0]]

            solution.reverse()
            return solution

        moveGen = problem.getSuccessors(n)
        for m in moveGen:
            if m[0] not in cost:
                cost[m[0]] = cost[n] + m[2]
                parent[m[0]] = (n, m[1])
                frontier.push(m[0], cost[m[0]])
            elif cost[m[0]] > cost[n] + m[2]:
                cost[m[0]] = cost[n] + m[2]
                parent[m[0]] = (n, m[1])
                frontier.update(m[0], cost[m[0]])

    return []

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    open = util.PriorityQueue()
    g = {}
    parent = {}
    f = {}
    closed = set()
    startNode = problem.getStartState()
    open.push(startNode, 1)
    parent[startNode] = (None, None) #parent, direction
    g[startNode] = 0
    f[startNode] = g[startNode] + heuristic(startNode, problem)
    """
        PROPAGATE IMPROVEMENT
    """ 
    def propagateImprovement(m):
        move = problem.getSuccessors(m[0])
        for x in move:
            g1 = g.setdefault(m)
            if g1 == None : g1 = float('inf')
            k2 = x[2]
            g2 = g.setdefault(x[0])
            if g2 == None : g2 = float('inf')
            if(g1 + k2 < g2):
                parent[x[0]] = (m[0], x[1])
                g[x[0]] = g1 + k2
                f[x[0]] = g[x[0]] + heuristic(x[0], problem)

                if x[0] in closed:
                    propagateImprovement(x)

    while (not open.isEmpty()):
        n = open.pop()
        closed.add(n)

        if (problem.isGoalState(n)):
            """
                RECONSTRUCT PATH
            """
            solution = []
            x = parent[n]
            while (x!= (None, None)):
                solution.append(x[1])
                x = parent[x[0]]
            
            solution.reverse()
            return solution
        
        MoveGen = problem.getSuccessors(n)
        for m in MoveGen:
            g1 = g.setdefault(n)
            if g1 == None : g1 = float('inf')
            k = m[2]
            g2 = g.setdefault(m[0])
            if g2 == None : g2 = float('inf')
            if (g1 + k < g2):
                parent[m[0]] = (n, m[1])
                g[m[0]] = g1 + k
                f[m[0]] = g[m[0]] + heuristic(m[0], problem)

                if (m[0] in open.heap): continue
                if (m[0] in closed): propagateImprovement(m)
                else: open.push(m[0], f[m[0]])

    return []

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
