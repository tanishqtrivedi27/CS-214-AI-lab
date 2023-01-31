import time
import random
import sys

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

        while (len(unvisited) != 0):
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

    def tspACO(self):
        start = time.time()
        while(time.time() - start < 299):
            ants = []
            pheromonesDelta = [[0.0 for i in range(self.N)] for j in range(self.N)]

            for j in range(self.numAnts):
                ant = Ant(self.adjMatrix, self.pheromones, self.alpha, self.beta)

                ants.append(ant)

                if (ant.getCost(self.adjMatrix) < self.bestCost):
                    self.bestCost = ant.getCost(self.adjMatrix)
                    self.bestTour = ant.currentPath
                    print(self.bestCost)
                    print(self.bestTour, end="---------------------------------------------\n")

                ants.sort(key=lambda x: x.getCost(self.adjMatrix))

            for c in ants[:self.KBest]:
                for i, v in enumerate(c.currentPath):
                    nextOne = c.currentPath[(i+1)%self.N]
                    pheromonesDelta[v][nextOne] += self.Q/self.adjMatrix[v][nextOne]

            for i in range(self.N):
                for j in range(self.N):
                    self.pheromones[i][j] = (1-self.rho)*self.pheromones[i][j] + pheromonesDelta[i][j]



def main():
    # start = time.time()
    file1 = open(sys.argv[1], 'r')
    file1.readline()
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
    '''
    tour = tsp(adjMatrix, n)
    file2 = open(r"output.txt", "w")
    cost  = 0
    for i in tour:
        k, j = i
        cost = cost + j
        file2.write(f"{k} {j}\n")
    file2.close()
    end = time.time()
    print((end-start) * 10**3, "ms")
    print(cost)
    '''
    alpha=3
    beta=3
    rho=0.1
    Q=0.1
    numAnts = N
    aco = AntColony(adjMatrix, numAnts, alpha, beta, rho, Q)
    aco.tspACO()
    # print(ant.currentPath)
    # print(ant.getCost())


if __name__ == "__main__":
    main()