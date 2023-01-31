import time

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
    
    
def tspACO():
    pass


def main():
    start = time.time()
    file1 = open("euc_100", 'r')
    file1.readline()
    n = int(file1.readline())
    coordinates = []
    for i in range(n):
        line = file1.readline()
        list2 = line.split()
        coordinates.append((list2[0], list2[1]))

    
    adjMatrix = []
    for i in range(n):
        line = file1.readline()
        list2 = line.split()
        list2 = [float(x) for x in list2]
        adjMatrix.append(list2)

    file1.close()
    tour = tsp(adjMatrix, n)
    file2 = open(r"output.txt", "w")
    for i in tour:
        k, j = i
        file2.write(f"{k} {j}\n")
    file2.close()
    end = time.time()
    print((end-start) * 10**3, "ms")


    


if __name__ == "__main__":
    main()