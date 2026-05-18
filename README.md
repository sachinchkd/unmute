# Balen Bolcha

An unofficial Devanagari/Nepali-style ipsum text generator built with a Markov chain model.

The app uses a cleaned text corpus, trains a Markov chain model, and serves generated text through a FastAPI backend with a React + TypeScript + Tailwind frontend.

> This project is unofficial and is not affiliated with, endorsed by, or connected to Balen or any public figure. It is intended as a parody/filler-text generator.

---

## Features

- Devanagari-focused text generation
- Adjustable paragraph count
- Adjustable text length
- Markov chain based generator
- FastAPI backend
- React + TypeScript frontend
- Tailwind CSS + shadcn-style UI components
- Docker-ready deployment
- Render-compatible setup

---

## Tech Stack

### Backend

- Python
- FastAPI
- Uvicorn
- Markov chain text generation
- uv for Python dependency management

### Frontend

- React
- TypeScript
- Vite
- pnpm
- Tailwind CSS
- shadcn-style components

### Deployment

- Docker
- Render Web Service

---

## Project Structure

```txt
balen-bolcha/
├─ data/
│  ├─ raw_posts.jsonl
│  ├─ clean_posts.jsonl
│  ├─ corpus.txt
│  └─ markov_model.pkl
│
├─ src/
│  ├─ __init__.py
│  ├─ app.py
│  ├─ markov.py
│  ├─ prepare_corpus.py
│  └─ train_markov.py
│
├─ frontend/
│  ├─ index.html
│  ├─ package.json
│  ├─ pnpm-lock.yaml
│  ├─ vite.config.ts
│  ├─ tailwind.config.ts
│  ├─ postcss.config.js
│  ├─ tsconfig.json
│  ├─ tsconfig.app.json
│  ├─ tsconfig.node.json
│  ├─ components.json
│  └─ src/
│     ├─ App.tsx
│     ├─ main.tsx
│     ├─ index.css
│     ├─ vite-env.d.ts
│     ├─ lib/
│     │  └─ utils.ts
│     └─ components/
│        └─ ui/
│           ├─ button.tsx
│           ├─ card.tsx
│           ├─ input.tsx
│           ├─ label.tsx
│           ├─ select.tsx
│           └─ textarea.tsx
│
├─ Dockerfile
├─ .dockerignore
├─ .gitignore
├─ pyproject.toml
├─ uv.lock
└─ README.md
