from pathlib import Path
from collections import Counter
from functools import lru_cache
import logging

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

logging.basicConfig(level=logging.INFO)

STOPWORDS = {
    'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from', 
    'has', 'he', 'in', 'is', 'it', 'its', 'of', 'on', 'that', 'the', 
    'to', 'was', 'were', 'will', 'with'
}

app = FastAPI()

templates = Jinja2Templates(directory="templates")

ARTICLES_PATH = Path("articles")

@lru_cache(maxsize=None)
def get_article_content(article_name: str) -> str:
    file_path = ARTICLES_PATH / f"{article_name}.txt"
    if not file_path.exists():
        return f"Article {article_name} not found."
    logging.info(f"Reading content from file: {file_path}")
    with file_path.open("r") as file:
        content = file.read()
    return content

@app.get("/", response_class=HTMLResponse)
async def read_index(request: Request) -> HTMLResponse:
    articles = [file.stem for file in ARTICLES_PATH.glob("*.txt")]
    return templates.TemplateResponse("index.html", {"request": request, "articles": articles})

@app.get("/article/{article_name}", response_class=HTMLResponse)
async def read_article(article_name: str) -> HTMLResponse:
    content = get_article_content(article_name)
    return HTMLResponse(content=content)

@app.post("/process-article/{article_name}")
async def process_article_request(article_name: str) -> dict:
    content = get_article_content(article_name)
    if content == "Article not found.":
        return {"error": "File not found."}
    words = content.lower().split()
    filtered_words = [word for word in words if word not in STOPWORDS]
    return dict(Counter(filtered_words).most_common(5))
