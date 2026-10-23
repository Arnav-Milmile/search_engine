# Repository transfer notes

## Destination

- GitHub account: `Arnav-Milmile`
- Suggested repository name: `search_engine`
- Suggested visibility: public
- Suggested URL: <https://github.com/Arnav-Milmile/search_engine>

## What to transfer

The project source includes the Flask frontend, arXiv sample downloader, analysis scripts, README, and dependency list. The 10,000-record `arxiv_sample.csv` is generated locally and ignored by Git; run `python download_arxiv_sample.py` after cloning to fetch it.

The generated inverted index and charts in the working directory may reflect local analysis runs. Review them separately before including them in a copy.

## Publish this working copy

Create an empty repository at the destination above. From the project folder, add it as a remote and push the current branch:

```powershell
git remote add destination https://github.com/Arnav-Milmile/search_engine.git
git push destination main
```

If the destination remote already exists, update its URL instead:

```powershell
git remote set-url destination https://github.com/Arnav-Milmile/search_engine.git
git push destination main
```

GitHub authentication is required to create the repository and push. Do not put a personal access token in a remote URL or commit it to the project.

## Run after cloning

```powershell
python -m pip install -r requirements.txt
python download_arxiv_sample.py
python app.py
```

Open <http://127.0.0.1:5000> to use the search page.
