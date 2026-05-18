import random
import re
from collections import defaultdict
from pathlib import Path


def tokenize(text: str) -> list[str]:
    """
    Devanagari tokenizer.
    Keeps Devanagari words, numbers, and punctuation as separate tokens.
    """
    pattern = r"[\u0900-\u097F]+|[०-९0-9]+|[।॥.!?,;:]"
    return re.findall(pattern, text)


def detokenize(tokens: list[str]) -> str:
    text = " ".join(tokens)

    for punct in ["।", "॥", ".", "!", "?", ",", ";", ":"]:
        text = text.replace(f" {punct}", punct)

    return text.strip()


class MarkovTextGenerator:
    def __init__(self, order: int = 2):
        if order < 1:
            raise ValueError("Order must be at least 1.")

        self.order = order
        self.chain = defaultdict(list)
        self.starts = []

    def train(self, text: str):
        tokens = tokenize(text)

        if len(tokens) <= self.order:
            raise ValueError("Corpus is too small. Add more Devanagari post text.")

        for i in range(len(tokens) - self.order):
            key = tuple(tokens[i:i + self.order])
            next_token = tokens[i + self.order]

            self.chain[key].append(next_token)

            # Sentence start detection
            if i == 0 or tokens[i - 1] in ["।", "॥", ".", "!", "?"]:
                if all(token not in ["।", "॥", ".", "!", "?"] for token in key):
                    self.starts.append(key)

    def generate_paragraph(self, token_count: int = 80) -> str:
        if not self.chain:
            raise ValueError("Model is not trained.")

        current = random.choice(self.starts or list(self.chain.keys()))
        output = list(current)

        while len(output) < token_count:
            key = tuple(output[-self.order:])
            options = self.chain.get(key)

            if not options:
                current = random.choice(self.starts or list(self.chain.keys()))
                output.extend(current)
                continue

            output.append(random.choice(options))

        text = detokenize(output[:token_count])

        if text and text[-1] not in ["।", "॥", ".", "!", "?"]:
            text += "।"

        return text

    def generate(self, paragraphs: int = 3, length: str = "medium") -> str:
        length_map = {
            "short": 40,
            "medium": 80,
            "long": 140,
            "extra_long": 220,
        }

        token_count = length_map.get(length, 80)

        return "\n\n".join(
            self.generate_paragraph(token_count)
            for _ in range(paragraphs)
        )


def load_generator(corpus_path: str = "data/corpus.txt", order: int = 2):
    text = Path(corpus_path).read_text(encoding="utf-8")

    generator = MarkovTextGenerator(order=order)
    generator.train(text)

    return generator