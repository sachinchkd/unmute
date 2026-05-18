from markov import load_generator

generator = load_generator(
    corpus_path="data/corpus.txt",
    order=2,
)

text = generator.generate(
    paragraphs=3,
    length="medium",
)

print(text)