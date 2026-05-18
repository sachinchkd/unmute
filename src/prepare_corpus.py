import json
import re
import unicodedata
from pathlib import Path

RAW_PATH = Path("data/raw_posts.jsonl")
CORPUS_PATH = Path("data/corpus.txt")
CLEAN_POSTS_PATH = Path("data/clean_posts.jsonl")

MIN_CHARS = 20


def has_devanagari(text: str) -> bool:
    return bool(re.search(r"[\u0900-\u097F]", text))


def clean_devanagari_text(text: str) -> str:
    text = unicodedata.normalize("NFC", text)

    # Remove URLs
    text = re.sub(r"https?://\S+|www\.\S+", " ", text)

    # Remove hashtags symbol but keep possible Devanagari words
    text = text.replace("#", "")

    # Keep only Devanagari, Nepali punctuation, spaces, and common punctuation
    text = re.sub(
        r"[^\u0900-\u097F\s।॥.,!?;:()\"'%-]",
        " ",
        text,
    )

    # Normalize spaces
    text = re.sub(r"\s+", " ", text).strip()

    return text


def load_records(path: Path) -> list[dict]:
    raw = path.read_text(encoding="utf-8").strip()

    if not raw:
        return []

    # Supports JSON array: [{...}, {...}]
    try:
        data = json.loads(raw)

        if isinstance(data, list):
            return data

        if isinstance(data, dict):
            return [data]

    except json.JSONDecodeError:
        pass

    # Supports JSONL: one JSON object per line
    records = []

    with path.open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            line = line.strip()

            if not line:
                continue

            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                print(f"Skipping invalid JSON on line {line_number}")
                continue

            if isinstance(record, dict):
                records.append(record)

    return records


def main():
    if not RAW_PATH.exists():
        raise FileNotFoundError(f"Missing file: {RAW_PATH}")

    records = load_records(RAW_PATH)

    clean_posts = []
    seen = set()

    skipped_empty = 0
    skipped_no_devanagari = 0
    skipped_short = 0
    skipped_duplicate = 0

    for record in records:
        # Use ONLY the actual Facebook post text field.
        # Ignore comments, likes, shares, media, OCR, reactions, etc.
        raw_text = record.get("text", "")

        if not raw_text:
            skipped_empty += 1
            continue

        if not has_devanagari(raw_text):
            skipped_no_devanagari += 1
            continue

        text = clean_devanagari_text(raw_text)

        if len(text) < MIN_CHARS:
            skipped_short += 1
            continue

        if text in seen:
            skipped_duplicate += 1
            continue

        seen.add(text)

        clean_posts.append({
            "postId": record.get("postId"),
            "url": record.get("url") or record.get("topLevelUrl"),
            "time": record.get("time"),
            "text": text,
        })

    CORPUS_PATH.write_text(
        "\n\n".join(post["text"] for post in clean_posts),
        encoding="utf-8",
    )

    with CLEAN_POSTS_PATH.open("w", encoding="utf-8") as file:
        for post in clean_posts:
            file.write(json.dumps(post, ensure_ascii=False) + "\n")

    total_tokens = sum(len(post["text"].split()) for post in clean_posts)

    print("Corpus preparation complete.")
    print(f"Loaded records: {len(records)}")
    print(f"Clean Devanagari posts: {len(clean_posts)}")
    print(f"Approx word count: {total_tokens}")
    print(f"Skipped empty: {skipped_empty}")
    print(f"Skipped no Devanagari: {skipped_no_devanagari}")
    print(f"Skipped short: {skipped_short}")
    print(f"Skipped duplicate: {skipped_duplicate}")
    print(f"Saved corpus: {CORPUS_PATH}")
    print(f"Saved clean posts: {CLEAN_POSTS_PATH}")


if __name__ == "__main__":
    main()