import json
import queue
import threading

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from pipelin import run_search_pipeline

app = FastAPI(title="ResearchMind API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173","https://multiagent-ai-system.netlify.app/"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class ResearchReq(BaseModel):
    topic: str


@app.post("/api/research")
def research(req: ResearchReq):
    events = queue.Queue()
    current = {"step": None}  # remembers which step is running, for error reporting

    def on_step(step, status):
        current["step"] = step
        events.put({"type": "status", "step": step, "status": status})

    def worker():
        try:
            state = run_search_pipeline(req.topic, on_step=on_step)
            events.put({
                "type": "result",
                "report": state["report"],
                "feedback": state["feedback"],
                "sources": state["sources"],
            })
        except Exception as e:
            events.put({"type": "error", "step": current["step"], "message": str(e)})
        finally:
            events.put(None)  # signals end of stream

    threading.Thread(target=worker, daemon=True).start()

    def stream():
        while True:
            item = events.get()
            if item is None:
                break
            yield f"data: {json.dumps(item)}\n\n"

    return StreamingResponse(
        stream(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )