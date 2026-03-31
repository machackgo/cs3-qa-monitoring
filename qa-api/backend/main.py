import os
import time

from fastapi import FastAPI
from pydantic import BaseModel
from huggingface_hub import InferenceClient

from prometheus_client import Counter, Histogram, start_http_server

app = FastAPI(title="qa-api backend", version="1.0")

MODEL_ID = "deepset/bert-base-uncased-squad2"
HF_TOKEN = os.getenv("HF_TOKEN", "").strip()

client = None
if HF_TOKEN:
    client = InferenceClient(model=MODEL_ID, token=HF_TOKEN)

# Prometheus metrics
REQUEST_COUNT = Counter("qa_api_requests_total", "Total QA requests received")
BAD_REQUEST_COUNT = Counter("qa_api_bad_requests_total", "Total bad requests")
API_ERROR_COUNT = Counter("qa_api_hf_errors_total", "Total Hugging Face API errors")
SUCCESS_COUNT = Counter("qa_api_success_total", "Total successful QA responses")
REQUEST_LATENCY = Histogram("qa_api_request_duration_seconds", "Time spent processing QA requests")

# Separate metrics server
start_http_server(9101)


class QARequest(BaseModel):
    context: str
    question: str


@app.get("/")
def root():
    return {
        "message": "qa-api backend up",
        "docs": "/docs",
        "health": "/health",
        "metrics_port": 9101,
    }


@app.get("/health")
def health():
    return {
        "status": "ok",
        "hf_token_present": bool(HF_TOKEN),
        "model": MODEL_ID,
    }


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

    if not HF_TOKEN:
        API_ERROR_COUNT.inc()
        return {
            "answer": "HF_TOKEN is missing in the backend environment.",
            "meta": "hf_token_missing"
        }

    try:
        out = client.question_answering(question=question, context=context)
    except Exception as e:
        API_ERROR_COUNT.inc()
        return {
            "answer": f"Hugging Face API error: {e}",
            "meta": "hf_api_error"
        }
    finally:
        REQUEST_LATENCY.observe(time.time() - t0)

    SUCCESS_COUNT.inc()
    dt = time.time() - t0

    answer = getattr(out, "answer", None) or "(No answer found in the provided context.)"
    score = getattr(out, "score", None)

    meta = f"Mode: API | Model: {MODEL_ID} | Time: {dt:.2f}s"
    if score is not None:
        meta += f" | Score: {score:.3f}"

    return {
        "answer": answer,
        "meta": meta
    }
