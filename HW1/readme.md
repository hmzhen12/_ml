# TSP Resolution using Hill Climbing Algorithm

This repository contains a Python implementation of the **Traveling Salesman Problem (TSP)** solved via the **Hill Climbing** optimization algorithm. This project demonstrates how local search heuristics can be applied to NP-hard combinatorial optimization problems.

---

## Project Overview

The **Traveling Salesman Problem (TSP)** asks the following question: *"Given a list of cities and the distances between each pair of cities, what is the shortest possible route that visits each city exactly once and returns to the origin city?"*

Since Hill Climbing is designed to maximize a value (climbing to the highest "height"), this implementation maps the TSP minimization problem into a maximization problem by defining the **height** as:

$$\text{Height} = \text{Total Tour Distance} \times -1$$

Thus, a shorter path yields a higher (less negative) value, allowing the algorithm to correctly converge toward an optimal solution.

---

## 🛠️ Features & Assignment Requirements Met

As specified in the assignment prompt, this implementation includes:
* **Sequential Initial Solution:** Starts with a basic chronological route: $1 \rightarrow 2 \rightarrow 3 \rightarrow \dots \rightarrow n \rightarrow 1$.
* **`height()` Function:** Calculates the total Euclidean distance of the tour and multiplies it by `-1`.
* **`neighbor()` Function (2-opt Swap):** Breaks two edges $(a, b)$ and $(c, d)$ randomly and reconnects them as $(a, d)$ and $(b, c)$ by reversing the sub-array sequence.
* **Early Stopping Mechanism:** Terminates searching if no better neighbor is found after a consecutive number of tries (`maxFails`).

---

## Code Structure

The script is divided into four logical parts:

| Section | Component | Description |
| :--- | :--- | :--- |
| **1** | **Problem Definition** | Contains the coordinate data (`CITIES`) and the Euclidean distance math helper. |
| **2** | **`TSPSolution` Class** | Encapsulates the state of a tour. It handles calculating the current fitness (`height`), generating mutations (`neighbor`), and formatting the console output (`str`). |
| **3** | **`hillClimbing` Function** | The core iterative evaluation loop that manages state transitions and counters for consecutive failures. |
| **4** | **Execution Block** | Initializes parameters, sets up the initial sequential tour, and fires up the execution. |

---

## How to Run

### Prerequisites
* **Python 3.x** (No external libraries required; relies completely on built-in `math` and `random` modules).

### Steps
1. Clone or download this repository.
2. Run the script using your terminal:
   ```bash
   python hill_climbing_tsp.py
