# V1 Report: Baseline ChatTutor

## Abstract

ChatTutor V1 is a minimal intent classification chatbot built with a feedforward neural network. It runs on a hand-crafted dataset of 48 samples across 6 intent categories. The purpose was to build a working end-to-end pipeline quickly and identify what needed to improve before investing in real data. Training accuracy reached around 97% but that number is deceptive given the tiny dataset.

## Dataset description

Source: Hand-crafted. No external data was used.

Size: 6 intents, 6-8 patterns each, 48 total utterances.

Intents: greeting, goodbye, thanks, hours, enrollment, tuition.

Preprocessing: Lowercased, split on whitespace. No punctuation removal, no stemming. A word2idx vocabulary was built from scratch using only the training words.

This dataset was always meant to be temporary. The vocabulary it produces is around 120 words. It is not representative of how real users phrase questions.

## Methodology

Architecture:

```
Input (token IDs, length 20)
  -> Embedding(1000, 16)
  -> GlobalAveragePooling1D
  -> Dense(16, relu)
  -> Dropout(0.5)
  -> Dense(6, softmax)
```

Total parameters: approximately 20,000.

Optimizer: Adam. Loss: sparse categorical crossentropy.

## Training process

80 epochs, batch size 8. No early stopping. No validation split. Training ran on all 48 samples. Took under 10 seconds on a laptop CPU.

Best epoch: around epoch 60-70 based on visual inspection of loss curve. Loss dropped quickly in the first 20 epochs and flattened after that.

## Results

Training accuracy: ~97% (final epoch average across runs).

Test accuracy: Not measured, no held-out set.

Confusion matrix: Not generated. With 48 samples across 6 classes, it would show 7-8 samples per intent and would not be statistically meaningful.

## What I learned

The pipeline itself works. Data loading, tokenization, model training, and the chat loop all function correctly. The confidence threshold at 0.6 catches most nonsense inputs but still accepts some false positives when a user uses a word that happens to match a training pattern.

The model almost certainly memorizes the training data instead of learning general patterns. Accuracy is high because it sees the same examples during training and evaluation. This is not a real measure of performance.

## Limitations

1. No generalization. If someone writes "how do I register?" instead of "how do I enroll?", the model may not connect them. The word "register" happens to appear in the dataset so it works. A word like "matriculate" would fail silently.

2. Vocabulary coverage is near zero for real language. 120 words trained vs. 170,000 in a standard English dictionary.

3. No evaluation framework. Without a held-out test set, there is no way to know how this performs on new inputs.

4. Overfitting is near certain. 48 samples, 6 classes, 80 epochs. The model has more parameters than examples.

## Plan for V2

Download the SNIPS NLU dataset. It has ~13,000 utterances across 7 intents including "BookRestaurant", "GetWeather", "PlayMusic", "RateBook", "SearchCreativeWork", "SearchScreeningEvent", and "AddToPlaylist". Add an LSTM layer. Add train/validation/test splits (70/15/15). Measure test accuracy. Implement early stopping to prevent overfitting.

## References

- TensorFlow/Keras documentation: https://keras.io
- SNIPS NLU dataset: https://github.com/snipsco/nlu-benchmark
- Jurafsky and Martin, "Speech and Language Processing" (3rd ed.) - Chapter 4 (Naive Bayes) and Chapter 9 (RNNs) for background on text classification approaches
