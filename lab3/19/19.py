import time
import random
import sys

"""
    The solution of travelling salesperson problem using
    nearest-neighbour heuristic
"""
def tsp(adjMatrix, n):
    i = 0
    for i in adjMatrix:
        for j in range(n):
            i[j] = (i[j], j)

    tour = []
    visited = set()
    currentCity = 0
    tour.append((currentCity, 0))
    visited.add(currentCity)
    while (len(visited) != n):
        adjMatrix[currentCity] = sorted(adjMatrix[currentCity])
        for i in range(n):
            if(adjMatrix[currentCity][i][0] == 0.0 or adjMatrix[currentCity][i][1] in visited):
                continue
            else:
                # tour.append(adjMatrix[currentCity][i][1])
                tour.append((adjMatrix[currentCity][i][1], adjMatrix[currentCity][i][0]))
                visited.add(adjMatrix[currentCity][i][1])
                currentCity = adjMatrix[currentCity][i][1]
                break

    return tour
    
""" 
    Ant colony Optimization
"""
class Ant:
    def __init__(self, adjMatrix, pheromones, alpha, beta):
        self.currentPath = []
        self.findPath(adjMatrix, pheromones, alpha, beta)

    def findPath(self, adjMatrix, pheromones, alpha, beta):
        N = len(adjMatrix)
        unvisited = list(range(N))
        firstCity = random.randint(0, N-1)
        self.currentPath.append(firstCity)
        unvisited.remove(firstCity)

        while (len(self.currentPath) < N):
            i = self.currentPath[-1]
            prob = [pheromones[i][j]**alpha * (1/adjMatrix[i][j])**beta for j in unvisited]
            probSet = [j/sum(prob) for j in prob]

            nextCity = random.choices(unvisited, weights=probSet)[0]
            self.currentPath.append(nextCity)
            unvisited.remove(nextCity)


    def getCost(self, adjMatrix):
        cost = 0
        N = len(adjMatrix)
        for i in range(len(self.currentPath)):
            cost = cost + adjMatrix[self.currentPath[i]][self.currentPath[(i+1) % N]]

        return cost

class AntColony:
    def __init__(self, adjMatrix, numAnts, alpha, beta, rho, Q):
        self.adjMatrix = adjMatrix
        self.N = len(adjMatrix)
        self.alpha = alpha
        self.beta = beta
        self.rho = rho
        self.Q = Q
        self.KBest = int(0.1*self.N + 1)
        self.pheromones = [[0.1 for i in range(self.N)] for j in range(self.N)]
        self.bestCost = float('Inf')
        self.numAnts = numAnts
        self.bestTour = []

    """
        In the ant colony optimization algorithms, an artificial ant is a simple computational agent 
        that searches for good solutions to a given optimization problem.
    """
    def tspACO(self):
        while(time.time() - start < 199):
            ants = []
            pheromonesDelta = [[0.0 for i in range(self.N)] for j in range(self.N)]

            for j in range(self.numAnts):
                ant = Ant(self.adjMatrix, self.pheromones, self.alpha, self.beta)

                ants.append(ant)

                if (ant.getCost(self.adjMatrix) < self.bestCost):
                    self.bestCost = ant.getCost(self.adjMatrix)
                    self.bestTour = ant.currentPath
                    print("The tour length is =", self.bestCost, sep=' ')
                    print(*self.bestTour, sep=" ")
                    print("....................................................................................................................................")

            ants.sort(key=lambda x: x.getCost(self.adjMatrix))
            """ 
                computation of pheromone delta
            """
            for c in ants[:self.KBest]:
                for i, v in enumerate(c.currentPath):
                    nextOne = c.currentPath[(i+1)%self.N]
                    pheromonesDelta[v][nextOne] += self.Q/self.adjMatrix[v][nextOne]
            """ 
                pheromone update
            """
            for i in range(self.N):
                for j in range(self.N):
                    self.pheromones[i][j] = (1-self.rho)*self.pheromones[i][j] + pheromonesDelta[i][j]
     

def main():
    file1 = open(sys.argv[1], 'r')
    isEuclid = file1.readline()
    N = int(file1.readline())
    coordinates = []

    for i in range(N):
        line = file1.readline()
        list2 = line.split()
        coordinates.append((list2[0], list2[1]))

    adjMatrix = []
    for i in range(N):
        line = file1.readline()
        list2 = line.split()
        list2 = [float(x) for x in list2]
        adjMatrix.append(list2)
    file1.close()

    if (isEuclid == "euclidean\n"):
        #3, 6, 0.1, 0.1, N use this for 100, 250
        alpha=3
        if N > 200 : beta = 20
        else : beta = 6
        rho=0.1
        Q=0.1
        numAnts = N
        aco = AntColony(adjMatrix, numAnts, alpha, beta, rho, Q)
        aco.tspACO()
        tour = aco.bestTour

    elif (isEuclid == "noneuclidean\n"):
        alpha=5
        beta=20
        rho=0.05
        Q=0.05
        numAnts = N//4
        aco = AntColony(adjMatrix, numAnts, alpha, beta, rho, Q)
        aco.tspACO()
        tour = aco.bestTour


    """
        2-opt
        2-edge exchange
        The main idea behind it is to take a route that crosses over itself and reorder it so that it does not. 
        A complete 2-opt local search will compare every possible valid combination of the swapping mechanism.
    """
    cost = aco.bestCost

    for city1 in range(1, N-2): #len(tour) - 2 = 98
        for city2 in range(city1+1, N):
            if city2-city1 == 1 : continue
            lengthDelta = - adjMatrix[tour[city1-1]][tour[city1]] - adjMatrix[tour[city2-1]][tour[city2]] + adjMatrix[tour[city1-1]][tour[city2-1]] + adjMatrix[tour[city1]][tour[city2]]
            if (lengthDelta < 0):
                tour[city1:city2] = tour[city2-1:city1-1:-1]
                cost = cost + lengthDelta
                print("The 2-edge tour length is =", cost, sep=' ')
                print(tour)
                print("....................................................................................................................................")

    for city1 in range(1, N-2): #len(tour) - 2 = 98
        for city2 in range(city1+1, N):
            if city2-city1 == 1 : continue
            lengthDelta = - adjMatrix[tour[city1-1]][tour[city1]] - adjMatrix[tour[city2-1]][tour[city2]] + adjMatrix[tour[city1-1]][tour[city2-1]] + adjMatrix[tour[city1]][tour[city2]]
            if (lengthDelta < 0):
                tour[city1:city2] = tour[city2-1:city1-1:-1]
                cost = cost + lengthDelta
                print("The 2-edge tour length is =", cost, sep=' ')
                print(tour)
                print("....................................................................................................................................")

if __name__ == "__main__":
    start = time.time()
    main()