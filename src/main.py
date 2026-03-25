import os 
from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from src import indexer
from src.searcher import search
from src.models import SearchResponse

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

index = indexer.DocumentIndex()
index.build()

@app.get("/", response_class=HTMLResponse)
def home():
    with open("static/index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

@app.get("/search", response_model=SearchResponse)
def search_api(q: str = Query(..., description="Search query")):
    results = search(q, index)
    return {
        "query": q,
        "results": results,
    }

@app.post("/index")
def reindex():
    index.build()
    return {"message": "Index rebuilt successfully"}


@app.get("/health")
def health_check():
    return {"status": "ok"}