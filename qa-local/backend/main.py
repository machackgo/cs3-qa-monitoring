from fastapi import FastAPI
from pydantic import BaseModel
import time
from transformers import pipeline

from prometheus_client import Counter, Histogram, start_http_server

app = FastAPI(title="qa-local backend", version="1.0")

MODEL_ID = "google-bert/bert-large-uncased-whole-word-masking-finetuned-squad"
qa_pipe = None

# Prometheus metrics
REQUEST_COUNT = Counter("qa_local_requests_total", "Total QA requests received")
BAD_REQUEST_COUNT = Counter("qa_local_bad_requests_total", "Total bad requests")
LOCAL_ERROR_COUNT = Counter("qa_local_model_errors_total", "Total local model errors")
SUCCESS_COUNT = Counter("qa_local_success_total", "Total successful QA responses")
REQUEST_LATENCY = Histogram("qa_local_request_duration_seconds", "Time spent processing QA requests")

# Start metrics server on separate port
start_http_server(9104)


def get_pipe():
    global qa_pipe
    if qa_pipe is None:
        qa_pipe = pipeline("question-answering", model=MODEL_ID)
    return qa_pipe


class QARequest(BaseModel):
    context: str
    question: str


@app.get("/")
def root():
    return {
        "message": "qa-local backend up",
        "docs": "/docs",
        "health": "/health",
        "metrics_port": 9104,
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/qa")
def qa(req: QARequest):
    REQUEST_COUNT.inc()
    t0 = time.time()

    context = (req.context or "").strip()
    question = (req.question or "").strip()

    if not context:
        BAD_REQUEST_COUNT.inc()
        return {
            "answer": "Please paste some context/passage first.",
            "meta": "bad_request"
        }

    if not question:
        BAD_REQUEST_COUNT.inc()
        return {
            "answer": "Please type a question.",
            "meta": "bad_request"
        }

    if len(context) > 8000:
        context = context[:8000] + "..."

    try:
        pipe = get_pipe()
        out = pipe(question=question, context=context)
    except Exception as e:
        LOCAL_ERROR_COUNT.inc()
        return {
            "answer": f"Local model error: {e}",
            "meta": "local_error"
        }
    finally:
        REQUEST_LATENCY.observe(time.time() - t0)

    SUCCESS_COUNT.inc()
    dt = time.time() - t0

    if isinstance(out, dict):
        answer = out.get("answer") or "(No answer found in the provided context.)"
        score = out.get("score")
    else:
        answer = str(out) if out else "(No answer found in the provided context.)"
        score = None

    meta = f"Mode: Local | Model: {MODEL_ID} | Time: {dt:.2f}s"
    if score is not None:
        meta += f" | Score: {score:.3f}"

    return {
        "answer": answer,
        "meta": meta
    }
