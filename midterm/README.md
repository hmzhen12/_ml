# ChatTutor V1 - Baseline

This version is a proof of concept. It trains a small feedforward neural network on 6 hand-crafted intent categories and runs a basic chat loop in the terminal. The dataset is tiny and temporary. The goal was to confirm the pipeline works before spending time on real data.

## Install and run

```bash
pip install -r requirements.txt
python chatbot.py
```

Python 3.8+ required. No GPU needed. Training takes under 10 seconds on a laptop CPU.

## Expected output

```
Training on 48 samples, 6 intents...
Training complete. Final accuracy: 97.92%
ChatTutor V1 - type 'quit' to exit
----------------------------------------
You: how do I sign up for classes
Bot: To enroll, log in to the student portal and select your courses during registration week.  [enrollment, 0.91]
You: quit
Bot: Goodbye!
```

## Known limitations

- 48 training samples is not enough for real generalization. The model memorizes patterns.
- Any word not in the dataset gets mapped to `<UNK>`. About 90% of real English vocabulary will be unknown.
- 6 intents is too narrow for a real FAQ chatbot.
- Confidence threshold (0.6) needs tuning. Currently either too loose or too strict depending on input.
- No train/test split, so accuracy numbers are meaningless as generalization metrics.

## V1

Built the full pipeline from scratch: JSON data loading, tokenization, vocabulary construction, model training, and a chat loop. None of this existed before.
