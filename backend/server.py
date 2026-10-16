from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from agents import build_reader_agent, build_search_agent, writer_chain, critics_chain

app = FastAPI(title="ResearchMind API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite dev server
    allow_methods=["*"],
    allow_headers=["*"],
)


def to_text(content) -> str:
    """Gemini sometimes returns a list of blocks [{'type': 'text', 'text': ...}]. Flatten to a string."""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "\n".join(
            b.get("text", "") if isinstance(b, dict) else str(b) for b in content
        ).strip()
    return str(content)


class SearchReq(BaseModel):
    topic: str


class ReadReq(BaseModel):
    topic: str
    search_results: str


class WriteReq(BaseModel):
    topic: str
    search_results: str
    scraped_content: str


class CriticReq(BaseModel):
    report: str


@app.post("/api/search")
def search(req: SearchReq):
    try:
        agent = build_search_agent()
        result = agent.invoke(
            {"messages": [("user", f"Find the recent, reliable and detailed information about : {req.topic}")]}
        )
        return {"search_results": to_text(result["messages"][-1].content)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/read")
def read(req: ReadReq):
    try:
        agent = build_reader_agent()
        result = agent.invoke(
            {
                "messages": [
                    (
                        "user",
                        f"Based on the following search results about '{req.topic}', "
                        f"pick the most relevant URL and scrape it for deeper content.\n\n"
                        f"Search Results:\n{req.search_results[:3000]}",
                    )
                ]
            }
        )
        return {"scraped_content": to_text(result["messages"][-1].content)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/write")
def write(req: WriteReq):
    try:
        research = (
            f"SEARCH RESULTS :\n{req.search_results}\n\n"
            f"DETAILED SCRAPPED CONTENT :\n{req.scraped_content}"
        )
        report = writer_chain.invoke({"topic": req.topic, "research": research})
        return {"report": to_text(report)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/critic")
def critic(req: CriticReq):
    try:
        feedback = critics_chain.invoke({"report": req.report})
        return {"feedback": to_text(feedback)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))