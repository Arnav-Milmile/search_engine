"""Download a small arXiv metadata sample for local search and evaluation."""

import csv
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path


SAMPLE_SIZE = 10_000
BATCH_SIZE = 2_000
OUTPUT_FILE = Path(__file__).resolve().parent / "arxiv_sample.csv"
API_URL = "https://export.arxiv.org/api/query"
ATOM_NAMESPACE = "{http://www.w3.org/2005/Atom}"
SEARCH_QUERY = (
    "cat:cs.AI OR cat:cs.LG OR cat:cs.CV OR cat:cs.CL "
    "OR cat:hep-th OR cat:quant-ph OR cat:gr-qc OR cat:astro-ph"
)


def fetch_batch(start: int, count: int) -> list[dict[str, str]]:
    params = urllib.parse.urlencode(
        {
            "search_query": SEARCH_QUERY,
            "start": start,
            "max_results": count,
            "sortBy": "submittedDate",
            "sortOrder": "descending",
        }
    )
    request = urllib.request.Request(
        f"{API_URL}?{params}",
        headers={"User-Agent": "arxiv-search-engine/1.0"},
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        root = ET.fromstring(response.read())

    rows = []
    for entry in root.findall(f"{ATOM_NAMESPACE}entry"):
        identifier = entry.findtext(f"{ATOM_NAMESPACE}id", default="")
        doc_id = identifier.rstrip("/").rsplit("/", 1)[-1]
        title = entry.findtext(f"{ATOM_NAMESPACE}title", default="")
        abstract = entry.findtext(f"{ATOM_NAMESPACE}summary", default="")
        categories = [
            category.get("term", "")
            for category in entry.findall(f"{ATOM_NAMESPACE}category")
        ]
        rows.append(
            {
                "doc_id": doc_id,
                "title": " ".join(title.split()),
                "abstract": " ".join(abstract.split()),
                "categories": " ".join(categories),
            }
        )
    return rows


def main() -> None:
    records: dict[str, dict[str, str]] = {}
    for start in range(0, SAMPLE_SIZE, BATCH_SIZE):
        count = min(BATCH_SIZE, SAMPLE_SIZE - start)
        print(f"Fetching arXiv records {start + 1}-{start + count}...")
        for record in fetch_batch(start, count):
            if record["doc_id"]:
                records[record["doc_id"]] = record
        if start + count < SAMPLE_SIZE:
            time.sleep(3)

    if len(records) < SAMPLE_SIZE:
        raise RuntimeError(
            f"arXiv returned only {len(records)} unique records; "
            f"expected {SAMPLE_SIZE}. No CSV was written."
        )

    temporary_file = OUTPUT_FILE.with_suffix(".csv.tmp")
    with temporary_file.open("w", encoding="utf-8-sig", newline="") as csv_file:
        writer = csv.DictWriter(
            csv_file, fieldnames=("doc_id", "title", "abstract", "categories")
        )
        writer.writeheader()
        writer.writerows(records.values())
    temporary_file.replace(OUTPUT_FILE)
    print(f"Saved {len(records)} records to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
