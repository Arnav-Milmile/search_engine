"""Flask web app for searching the local arXiv sample."""

import re
from pathlib import Path

import pandas as pd
from flask import Flask, jsonify, render_template, request
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


ROOT = Path(__file__).resolve().parent
DATA_FILE = ROOT / "arxiv_sample.csv"
MAX_QUERY_LENGTH = 300
MAX_RESULTS = 30

app = Flask(__name__)

if not DATA_FILE.is_file():
    raise FileNotFoundError(
        f"{DATA_FILE.name} was not found. Run `python download_arxiv_sample.py` first."
    )

documents = pd.read_csv(DATA_FILE).fillna("")
required_columns = {"doc_id", "title", "abstract", "categories"}
missing_columns = required_columns.difference(documents.columns)
if missing_columns:
    raise ValueError(
        f"{DATA_FILE.name} is missing required columns: {', '.join(sorted(missing_columns))}"
    )

texts = (documents["title"].astype(str) + " " + documents["abstract"].astype(str)).tolist()
vectorizer = TfidfVectorizer(stop_words="english", min_df=5)
document_vectors = vectorizer.fit_transform(texts)


def categories_for(row: pd.Series) -> list[str]:
    return sorted(
        {
            category
            for category in re.split(r"[\s,]+", str(row["categories"]).strip())
            if category
        }
    )


category_values = sorted(
    {category for _, row in documents.iterrows() for category in categories_for(row)}
)


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/api/stats")
def stats():
    return jsonify({"documents": len(documents), "categories": category_values})


@app.get("/api/search")
def search():
    query = request.args.get("q", "").strip()
    if not query:
        return jsonify({"error": "Enter a search query."}), 400
    if len(query) > MAX_QUERY_LENGTH:
        return jsonify({"error": f"Queries must be {MAX_QUERY_LENGTH} characters or fewer."}), 400

    selected_category = request.args.get("category", "").strip()
    if selected_category and selected_category not in category_values:
        return jsonify({"error": "Select a category from the list."}), 400

    try:
        limit = int(request.args.get("limit", "10"))
    except ValueError:
        return jsonify({"error": "Result count must be a number."}), 400
    if not 1 <= limit <= MAX_RESULTS:
        return jsonify({"error": f"Result count must be between 1 and {MAX_RESULTS}."}), 400

    query_vector = vectorizer.transform([query])
    if query_vector.nnz == 0:
        return jsonify({"query": query, "total": 0, "results": []})

    scores = cosine_similarity(query_vector, document_vectors).ravel()
    candidates = range(len(documents))
    if selected_category:
        candidates = (
            index
            for index, row in documents.iterrows()
            if selected_category in categories_for(row)
        )

    ranked = sorted(candidates, key=lambda index: scores[index], reverse=True)
    ranked = [index for index in ranked if scores[index] > 0][:limit]
    results = []
    for index in ranked:
        row = documents.iloc[index]
        doc_id = str(row["doc_id"]).strip()
        results.append(
            {
                "doc_id": doc_id,
                "title": str(row["title"]).strip(),
                "abstract": str(row["abstract"]).strip(),
                "categories": categories_for(row),
                "score": round(float(scores[index]), 4),
                "url": f"https://arxiv.org/abs/{doc_id}",
            }
        )
    return jsonify({"query": query, "total": len(results), "results": results})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
