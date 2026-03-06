from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from analyzer import analyze_repo



app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class RepoRequest(BaseModel):
    owner: str
    repo: str
    threshold: int


@app.post("/analyze")
async def analyze(data: RepoRequest):
    start = time.time()
    result= await analyze_repo(
        data.owner,
        data.repo,
        data.threshold
    )
    print("Total Time:", time.time() - start)
    return result