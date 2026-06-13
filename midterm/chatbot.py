"""
ChatTutor V1 - Baseline proof of concept.
Small hand-crafted dataset, feedforward neural network, basic intent classification.
"""

import json
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

# ─── Config ────────────────────────────────────────────────────────────────────
VOCAB_SIZE = 200
EMBEDDING_DIM = 32
MAX_SEQ_LEN = 8
EPOCHS = 100
BATCH_SIZE = 4
CONFIDENCE_THRESHOLD = 0.6
DATA_PATH = "data/intents.json"


# ─── Data loading and preprocessing ────────────────────────────────────────────
def load_data(path):
    with open(path, "r") as f:
        data = json.load(f)
    return data["intents"]


def build_vocab(intents):
    word2idx = {"<PAD>": 0, "<UNK>": 1}
    for intent in intents:
        for pattern in intent["patterns"]:
            for word in pattern.lower().split():
                if word not in word2idx:
                    word2idx[word] = len(word2idx)
    return word2idx


def tokenize(text, word2idx, max_len):
    tokens = [word2idx.get(w, 1) for w in text.lower().split()]
    tokens = tokens[:max_len]
    tokens += [0] * (max_len - len(tokens))
    return tokens


def prepare_dataset(intents, word2idx):
    X, y = [], []
    tag2idx = {intent["tag"]: i for i, intent in enumerate(intents)}
    for intent in intents:
        for pattern in intent["patterns"]:
            X.append(tokenize(pattern, word2idx, MAX_SEQ_LEN))
            y.append(tag2idx[intent["tag"]])
    return np.array(X), np.array(y), tag2idx


# ─── Model ──────────────────────────────────────────────────────────────────────
def build_model(vocab_size, embedding_dim, max_len, num_classes):
    model = keras.Sequential([
        layers.Embedding(vocab_size, embedding_dim, input_length=max_len),
        layers.GlobalAveragePooling1D(),
        layers.Dense(16, activation="relu"),
        layers.Dropout(0.5),
        layers.Dense(num_classes, activation="softmax"),
    ])
    model.compile(
        optimizer="adam",
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )
    return model


# ─── Training ───────────────────────────────────────────────────────────────────
def train(model, X, y):
    history = model.fit(X, y, epochs=EPOCHS, batch_size=BATCH_SIZE, verbose=0)
    final_acc = history.history["accuracy"][-1]
    print(f"Training complete. Final accuracy: {final_acc:.2%}")
    return history


# ─── Inference ──────────────────────────────────────────────────────────────────
def predict_intent(text, model, word2idx, tag2idx):
    tokens = np.array([tokenize(text, word2idx, MAX_SEQ_LEN)])
    probs = model.predict(tokens, verbose=0)[0]
    idx2tag = {v: k for k, v in tag2idx.items()}
    top_idx = int(np.argmax(probs))
    confidence = float(probs[top_idx])
    if confidence < CONFIDENCE_THRESHOLD:
        return "unknown", confidence
    return idx2tag[top_idx], confidence


def get_response(tag, intents):
    for intent in intents:
        if intent["tag"] == tag:
            return np.random.choice(intent["responses"])
    return "I didn't understand that. Could you rephrase?"


# ─── Chat loop ──────────────────────────────────────────────────────────────────
def chat(model, word2idx, tag2idx, intents):
    print("ChatTutor V1 - type 'quit' to exit")
    print("-" * 40)
    while True:
        user_input = input("You: ").strip()
        if not user_input:
            continue
        if user_input.lower() in ("quit", "exit", "bye"):
            print("Bot: Goodbye!")
            break
        tag, confidence = predict_intent(user_input, model, word2idx, tag2idx)
        if tag == "unknown":
            print(f"Bot: I'm not sure what you mean. (confidence: {confidence:.2f})")
        else:
            response = get_response(tag, intents)
            print(f"Bot: {response}  [{tag}, {confidence:.2f}]")


# ─── Main ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    intents = load_data(DATA_PATH)
    word2idx = build_vocab(intents)
    X, y, tag2idx = prepare_dataset(intents, word2idx)

    num_classes = len(tag2idx)
    model = build_model(VOCAB_SIZE, EMBEDDING_DIM, MAX_SEQ_LEN, num_classes)

    print(f"Training on {len(X)} samples, {num_classes} intents...")
    train(model, X, y)

    chat(model, word2idx, tag2idx, intents)
