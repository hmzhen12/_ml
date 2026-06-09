# Multi-Layer Perceptron (MLP) for Solving the XOR Problem

This repository features a basic **Multi-Layer Perceptron (MLP)** implementation built completely from scratch using a custom deep learning micro-library called `nn0`. The primary objective of this project is to demonstrate how a simple neural network can learn to solve the non-linear **XOR (Exclusive OR)** logic gate problem.

---

## About the XOR Problem

The XOR gate outputs `1` (True) only when its two binary inputs are different. If the inputs are identical, it outputs `0` (False).

| Input $X_1$ | Input $X_2$ | Target Output ($Y$) |
| :---: | :---: | :---: |
| 0 | 0 | 0 |
| 0 | 1 | 1 |
| 1 | 0 | 1 |
| 1 | 1 | 0 |

The XOR problem holds a historical significance in AI. Because its data points are **non-linearly separable** (they cannot be divided by a single straight line), a *Single-Layer Perceptron* fails completely. To solve it, we require a *Multi-Layer Perceptron* coupled with non-linear activation functions (like ReLU).

---

## Network Architecture

The MLP model configured in the script uses the following setup:

* **Input Layer:** 2 nodes (accepting the XOR input pairs).
* **Hidden Layer:** 4 units with **ReLU** (Rectified Linear Unit) activation functions.
* **Output Layer:** 1 node (predicting a continuous scalar value).

---

## Code Workflow Breakdown

The Python script is divided into three functional phases:

### 1. Parameter Initialization & Optimizer Setup
* **Weights ($W$)** are randomly initialized between -1 and 1 using `random.uniform(-1, 1)`.
* **Biases ($b$)** are initialized to `0.0`.
* Every parameter is wrapped in a `Value` node to support *autograd* (automatic differentiation).
* The **Adam** optimizer is configured with a learning rate (`lr`) of `0.1` to handle smooth parameter updates.

### 2. The Training Loop
The network trains for **201 epochs**. For every sample in the XOR truth table, it executes:
* **Forward Pass:**
    1. Computes the hidden layer linear combination: $\text{hidden} = (X \cdot W_1) + b_1$
    2. Applies the non-linear activation: $\text{ReLU}(x) = \max(0, x)$
    3. Computes the final prediction output: $\text{prediction} = (\text{hidden\_act} \cdot W_2) + b_2$
* **Loss Calculation:** Uses **Mean Squared Error (MSE)** to quantify how far the prediction is from the ground truth: $\text{Loss} = (\text{prediction} - y)^2$.
* **Backpropagation:** Calls `loss.backward()` to automatically calculate the gradients for every parameter from output back to input.
* **Weight Update:** The `optimizer.step()` method modifies the weights and biases using the calculated gradients to minimize error in subsequent epochs.

### 3. Model Evaluation
Once training completes, the model runs a final inference cycle across all XOR inputs to verify if the continuous predicted outputs closely approximate the targets `0` or `1`.

---

## Core Components

This script relies on a custom `nn0` module which provides:
* **`Value`**: The core data structure storing scalars (`.data`), accumulated gradients (`.grad`), and the `.backward()` utility for reverse-mode automatic differentiation.
* **`linear(inputs, weights)`**: A helper function executing a dot product between the inputs and layer weights.
* **`Adam`**: An adaptive gradient descent optimizer that accelerates network convergence.

---

## How to Run

1. Ensure `nn0.py` is present in the exact same directory as your main script.
2. Run the script using your terminal:
   ```bash
   python main.py
