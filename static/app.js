const searchForm = document.querySelector("#search-form");
const queryInput = document.querySelector("#query");
const categorySelect = document.querySelector("#category");
const limitSelect = document.querySelector("#limit");
const resultsRegion = document.querySelector(".results-section");
const resultsContainer = document.querySelector("#results");
const resultsTitle = document.querySelector("#results-title");
const resultsCount = document.querySelector("#results-count");
const message = document.querySelector("#message");
const corpusCount = document.querySelector("#corpus-count");

function showMessage(text, type = "") {
  message.className = `message ${type}`.trim();
  message.replaceChildren();
  const icon = document.createElement("span");
  icon.className = "message-icon";
  icon.setAttribute("aria-hidden", "true");
  icon.textContent = type === "error" ? "!" : "↳";
  const content = document.createElement("span");
  content.textContent = text;
  message.append(icon, content);
}

function makeResultCard(result, position) {
  const article = document.createElement("article");
  article.className = "result-card";

  const number = document.createElement("span");
  number.className = "result-number";
  number.textContent = String(position).padStart(2, "0");

  const content = document.createElement("div");
  content.className = "result-content";

  const meta = document.createElement("div");
  meta.className = "result-meta";
  const id = document.createElement("span");
  id.textContent = `arXiv:${result.doc_id}`;
  const score = document.createElement("span");
  score.className = "score";
  score.textContent = `${(result.score * 100).toFixed(1)}% match`;
  meta.append(id, score);

  const title = document.createElement("h3");
  const link = document.createElement("a");
  link.href = result.url;
  link.target = "_blank";
  link.rel = "noopener noreferrer";
  link.textContent = result.title;
  title.append(link);

  const abstract = document.createElement("p");
  abstract.className = "abstract";
  abstract.textContent = result.abstract;

  const tags = document.createElement("div");
  tags.className = "category-tags";
  for (const category of result.categories) {
    const tag = document.createElement("span");
    tag.className = "category-tag";
    tag.textContent = category;
    tags.append(tag);
  }

  content.append(meta, title, abstract, tags);
  article.append(number, content);
  return article;
}

async function loadStats() {
  try {
    const response = await fetch("/api/stats");
    if (!response.ok) throw new Error("The search index is unavailable.");
    const stats = await response.json();
    corpusCount.textContent = `${stats.documents.toLocaleString()} PAPERS`;
    for (const category of stats.categories) {
      const option = document.createElement("option");
      option.value = category;
      option.textContent = category;
      categorySelect.append(option);
    }
  } catch {
    corpusCount.textContent = "INDEX UNAVAILABLE";
    showMessage("Could not load the search index. Check that the local sample data is available.", "error");
  }
}

searchForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const query = queryInput.value.trim();
  if (!query) {
    queryInput.focus();
    showMessage("Enter a topic or phrase to start searching.", "error");
    return;
  }

  const params = new URLSearchParams({
    q: query,
    category: categorySelect.value,
    limit: limitSelect.value,
  });
  resultsRegion.setAttribute("aria-busy", "true");
  resultsContainer.replaceChildren();
  resultsCount.textContent = "";
  resultsTitle.textContent = "Searching…";
  showMessage("Searching titles and abstracts…", "loading");

  try {
    const response = await fetch(`/api/search?${params}`);
    const payload = await response.json();
    if (!response.ok) throw new Error(payload.error || "Search failed. Please try again.");

    resultsTitle.textContent = `Results for “${payload.query}”`;
    resultsCount.textContent = `${payload.total} ${payload.total === 1 ? "PAPER" : "PAPERS"}`;
    if (!payload.results.length) {
      showMessage("No matching papers found. Try a broader topic or another category.");
      return;
    }
    message.className = "message hidden";
    payload.results.forEach((result, index) => {
      resultsContainer.append(makeResultCard(result, index + 1));
    });
  } catch (error) {
    resultsTitle.textContent = "Search unavailable";
    showMessage(error.message, "error");
  } finally {
    resultsRegion.setAttribute("aria-busy", "false");
  }
});

loadStats();
