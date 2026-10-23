# Repository copy

## GitHub destination

- Repository: <https://github.com/Arnav-Milmile/search_engine>
- Owner: `Arnav-Milmile`
- Visibility: Public
- Branch: `main`

The repository has been created and the current project history, including the simplified search frontend and these notes, has been pushed to GitHub.

## Included

The copy contains the Flask search app, its browser assets, the arXiv sample dataset and downloader, the indexing and evaluation scripts, the refreshed inverted index and charts, the detailed PowerPoint presentation, and setup documentation. The `.venv` virtual environment is excluded. To run the app after cloning:

```powershell
python -m pip install -r requirements.txt
python app.py
```

Then open <http://127.0.0.1:5000>.

Run `python download_arxiv_sample.py` only if you want to refresh the included sample from arXiv.

## Keep the copy updated

The local checkout has a remote named `arnav` pointing to the destination. After committing future changes to `main`, publish them with:

```powershell
git push arnav main
```

GitHub authentication is managed by Git Credential Manager. Do not put a personal access token in a remote URL or commit it to the project.
