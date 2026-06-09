import random
import math

CITIES = {
    1: (0, 0),
    2: (1, 5),
    3: (5, 6),
    4: (5, 1),
    5: (2, 2)
}

def calculate_distance(city1, city2):
    """Calculates the Euclidean distance between two cities"""
    x1, y1 = CITIES[city1]
    x2, y2 = CITIES[city2]
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

class TSPSolution:
    def __init__(self, tour):
        self.tour = tour

    def height(self):
        """Calculates the 'height' value (Total Distance * -1)"""
        total_distance = 0
        n = len(self.tour)
        for i in range(n):
            current_city = self.tour[i]
            next_city = self.tour[(i + 1) % n] # Returns to the starting city at the end
            total_distance += calculate_distance(current_city, next_city)
        
        # Based on instructions: height = distance * -1
        return -total_distance

    def neighbor(self):
        """Generates a neighbor by swapping paths (2-opt swap)"""
        n = len(self.tour)
        new_tour = list(self.tour)
        
        # Select two random indices to cut the paths
        idx1 = random.randint(0, n - 2)
        idx2 = random.randint(idx1 + 1, n - 1)
        
        # Reverse the sub-tour between idx1 and idx2
        # This represents changing (a,b)(c,d) into (a,d)(b,c)
        new_tour[idx1:idx2+1] = reversed(new_tour[idx1:idx2+1])
        
        return TSPSolution(new_tour)

    def str(self):
        """String representation of the solution and its total distance"""
        tour_text = " -> ".join(map(str, self.tour)) + f" -> {self.tour[0]}"
        actual_distance = -self.height()
        return f"[{tour_text}] (Total Distance: {actual_distance:.2f})"

def hillClimbing(s, maxGens, maxFails):
    print("start: ", s.str())
    fails = 0
    for gens in range(maxGens):
        snew = s.neighbor()
        sheight = s.height()
        nheight = snew.height()
        if (nheight >= sheight):
            print(f"Gen {gens}: {snew.str()}")
            s = snew
            fails = 0
        else:
            fails = fails + 1
        if (fails >= maxFails):
            print(f" Early stop at Gen {gens} because fails >= maxFails")
            break
    print("solution: ", s.str())
    return s

if __name__ == "__main__":
    initial_tour = list(CITIES.keys()) 
    initial_solution = TSPSolution(initial_tour)
    
    best_solution = hillClimbing(initial_solution, maxGens=1000, maxFails=100)
