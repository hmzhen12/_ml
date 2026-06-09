# Micro GPT: A Pure Python Transformer

This repository contains a minimalist, completely dependency-free implementation of a Generative Pre-trained Transformer (GPT) model written entirely in plain Python. It is designed for educational purposes to demonstrate the core mechanics of large language models, backpropagation, and transformer architecture from the ground up.

## Overview

The script implements a character-level language model capable of generating name-like strings. It trains on a dataset of names (borrowed from Andrej Karpathy's `makemore` repository) and learns to predict the next character in a sequence. 

Remarkably, it accomplishes this **without using PyTorch, TensorFlow, NumPy, or any other external mathematical libraries**. Everything, from the automatic differentiation engine to the Adam optimizer, is written from scratch using only standard Python libraries (`os`, `math`, `random`).

## Key Components

### 1. The Dataset & Tokenizer
* **Dataset:** The script automatically downloads a list of names (`names.txt`) if it doesn't find `input.txt` locally.
* **Tokenizer:** It uses a simple character-level tokenizer. It identifies all unique characters in the dataset, maps them to integer IDs (tokens), and reserves a special `BOS` (Beginning of Sequence) token to mark the start and end of a word.

### 2. Autograd Engine (`Value` class)
Inspired by `micrograd`, the `Value` class is the heart of the neural network. It builds a dynamic computation graph.
* It stores both the scalar `data` and its gradient (`grad`).
* It implements Python magic methods (`__add__`, `__mul__`, `__pow__`, etc.) so that standard math operations automatically record the relationship between inputs and outputs.
* The `backward()` method performs reverse-mode automatic differentiation (backpropagation) using a topological sort, computing the gradients for all weights in the network.

### 3. Transformer Architecture
The `gpt` function implements a lightweight GPT-2 style transformer block:
* **Embeddings:** Both Token Embeddings (`wte`) and Positional Embeddings (`wpe`) are added together to give the model a sense of character position.
* **RMSNorm:** Root Mean Square Normalization is used instead of standard LayerNorm for better stability and efficiency.
* **Multi-Head Self-Attention:** Computes Queries, Keys, and Values to figure out which prior characters are most relevant to predicting the next one.
* **MLP Block:** A Feed-Forward Neural Network using the ReLU activation function to add non-linearity.
* **Residual Connections:** Both the Attention and MLP blocks use residual connections to prevent the vanishing gradient problem.

### 4. Custom Adam Optimizer
Instead of standard Stochastic Gradient Descent (SGD), the script implements the **Adam optimizer** with linear learning rate decay. It manages first (`m`) and second (`v`) moment buffers to smoothly and quickly update the model's parameters (`params`) during training.

## Usage

Because there are no external dependencies, running the code is incredibly simple. You only need a standard installation of Python 3.

```bash
python micro_gpt.py
