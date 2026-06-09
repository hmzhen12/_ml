import random
from nn0 import Value, Adam, linear

random.seed(42)

W1 = [[Value(random.uniform(-1, 1)) for _ in range(2)] for _ in range(4)]
b1 = [Value(0.0) for _ in range(4)]

W2 = [[Value(random.uniform(-1, 1)) for _ in range(4)]]
b2 = [Value(0.0)]

params = [w for row in W1 for w in row] + b1 + [w for row in W2 for w in row] + b2
optimizer = Adam(params, lr=0.1)

X_data = [[0, 0], [0, 1], [1, 0], [1, 1]]
Y_data = [0, 1, 1, 0]

print("--- Training XOR Multi-Layer Perceptron ---")

for epoch in range(201):
    epoch_loss = 0
    for x, y in zip(X_data, Y_data):
        x_nodes = [Value(x[0]), Value(x[1])]
        
        hidden_linear = linear(x_nodes, W1)
        hidden_preact = [hidden_linear[i] + b1[i] for i in range(4)]
        hidden_act = [h.relu() for h in hidden_preact]
      
        output_linear = linear(hidden_act, W2)
        prediction = output_linear[0] + b2[0]
        
        loss = (prediction - y) ** 2
        epoch_loss += loss.data
       
        loss.backward()
        optimizer.step()

    if epoch % 40 == 0:
        print(f"Epoch {epoch:3d} | Total Epoch Loss: {epoch_loss:.4f}")

print("\n--- Final Model Evaluation ---")
for x in X_data:
    x_nodes = [Value(x[0]), Value(x[1])]
    hidden_act = [(h + b).relu() for h, b in zip(linear(x_nodes, W1), b1)]
    pred = linear(hidden_act, W2)[0] + b2[0]
    print(f"Input: {x} -> Predicted Output: {pred.data:.4f} (Target: {1 if x[0]!=x[1] else 0})")
