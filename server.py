from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from Interface import analyze_repo


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class RepoRequest(BaseModel):
    owner: str
    repo: str
    threshold: int


@app.post("/analyze")
def analyze(data: RepoRequest):

    results = analyze_repo(
        data.owner,
        data.repo,
        data.threshold
    )

    return results