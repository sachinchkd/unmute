import pickle
from pathlib import Path

from src.markov import MarkovTextGenerator, tokenize

BASE_DIR = Path(__file__).resolve().parent.parent

CORPUS_PATH = BASE_DIR / "data" / "corpus.txt"
MODEL_PATH = BASE_DIR / "data" / "markov_model.pkl"

ORDER = 2


def main():
    print("Base dir:", BASE_DIR)
    print("Corpus path:", CORPUS_PATH)
    print("Model path:", MODEL_PATH)

    if not CORPUS_PATH.exists():
        raise FileNotFoundError(f"Corpus not found: {CORPUS_PATH}")

    text = CORPUS_PATH.read_text(encoding="utf-8").strip()

    print("Corpus characters:", len(text))

    if not text:
        raise ValueError("corpus.txt is empty. Run prepare_corpus.py first.")

    tokens = tokenize(text)

    print("Token count:", len(tokens))

    if len(tokens) < ORDER + 5:
        raise ValueError("Not enough tokens to train Markov model.")

    generator = MarkovTextGenerator(order=ORDER)
    generator.train(text)

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)

    with MODEL_PATH.open("wb") as file:
        pickle.dump(generator, file)

    print("Training complete.")
    print("Order:", ORDER)
    print("Chain states:", len(generator.chain))
    print("Sentence starts:", len(generator.starts))
    print("Saved model to:", MODEL_PATH)


if __name__ == "__main__":
    main()