# arXiv Search Engine

A TF-IDF search engine for arXiv abstracts, with a browser-based search interface and command-line evaluation scripts.

## Requirements

- Python 3.10 or newer
- pip

## Setup

Install the dependencies:

```powershell
python -m pip install -r requirements.txt
```

The repository includes a 10,000-paper arXiv sample. To refresh it from the public arXiv API, run `python download_arxiv_sample.py`.

## Run the frontend

```powershell
python app.py
```

Open <http://127.0.0.1:5000> in your browser. Search by title or abstract, optionally filter by arXiv category, and choose how many results to display. The first start builds the TF-IDF index from `arxiv_sample.csv`.

## Run the analysis scripts

```powershell
python step1_prepare_data.py
python step3_search_engine.py
python step4_ablation.py
```

These scripts generate the inverted index and evaluation chart and print search metrics and the ablation study to the terminal. `step2_inverted_index.py` is an alternate standalone inverted-index builder.

## Repository copy

See [transfer.md](transfer.md) for the repository-copy and GitHub setup notes.

## Project presentation

The detailed 15-slide project deck is available as [project_presentation.pptx](project_presentation.pptx).

## Project files

- `app.py` — Flask API and search index
- `templates/index.html`, `static/` — browser interface
- `download_arxiv_sample.py` — downloads a local arXiv sample
- `project_presentation.pptx` — detailed project overview and evaluation
- `step1_prepare_data.py` — builds an inverted index and term-frequency chart
- `step3_search_engine.py` — evaluates search and Rocchio feedback
- `step4_ablation.py` — compares preprocessing configurations
