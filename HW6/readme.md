# Mini GPT: scikit-learn Word Classifier

## Overview
Mini GPT is a lightweight, creative approach to building a generative language model. Instead of relying on complex deep learning frameworks or transformers, it uses scikit-learn's `LogisticRegression` to learn and generate text. It models language as an n-gram chain, predicting the next word based on a sliding window of previous words.

## How It Works
The core engine relies on a classical machine learning pipeline adapted for natural language processing:

* **N-Gram Context:** The model reads sentences using a sliding window of `order` words (default is 2).
* **Feature Encoding:** The context window is converted into a concatenated one-hot feature vector.
* **Logistic Regression:** A multinomial logistic regression model learns the conditional probability $P(\text{next\_word} \mid \text{context})$.
* **Inference & Sampling:** During generation, the model predicts a probability distribution over the vocabulary. It samples the next word using **temperature scaling** (to control randomness) and **top-k filtering** (to restrict choices to the most likely candidates).
* **Iteration:** The predicted word is appended to the context, and the process repeats until an `<EOS>` (End of Sequence) token is generated or the maximum word limit is reached.

---

## Technical Notes & Recent Fixes
To ensure the model generates coherent text rather than hallucinations, two critical pipeline alignments are enforced in this version:

### 1. Class Index Alignment
Scikit-learn's `LogisticRegression` dynamically builds a `.classes_` array based strictly on the target variables it sees during `.fit()`. Because the `<UNK>` token is never a target during training, it is omitted from the learned classes, causing a length mismatch between the overall vocabulary and the prediction array. 
* **Resolution:** The generation step maps the index sampled from the probability distribution back to the actual integer class label the model trained on using `self.model.classes_[idx]`.

### 2. Context Padding Consistency
During training, the beginnings of sentences are padded with `<EOS>` tokens so the model learns how sequences typically start. 
* **Resolution:** The `_get_features` method pads short inference contexts with `<EOS>` rather than `<UNK>`, ensuring the model is fed features during inference that exactly match the data distribution it saw during training.

---

## Usage

### Running the Chatbot
Simply execute the Python script. If a pre-trained model (`mini_gpt.pkl`) is not found, it will automatically train itself on the built-in dataset and save the weights for future use.

```bash
python mini_gpt.py
