import logging
import sys

import inngest.fast_api
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.analytics.router import router as analytics_router
from app.chat.router import router as chat_router
from app.employees.router import router as employees_router
from app.inngest_app.client import client as inngest_client
from app.inngest_app.functions import get_functions
from app.middleware.error_handler import global_exception_handler
from app.middleware.timing import TimingMiddleware
from app.ml.router import router as ml_router
from app.settings.router import router as settings_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)-8s [%(name)s] %(message)s",
    datefmt="%H:%M:%S",
    stream=sys.stdout,
)

app = FastAPI(title="Acme Corp HR Chatbot", version="0.1.0")

app.add_middleware(TimingMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(Exception, global_exception_handler)

app.include_router(chat_router)
app.include_router(ml_router)
app.include_router(employees_router)
app.include_router(analytics_router)
app.include_router(settings_router)

inngest.fast_api.serve(app, inngest_client, get_functions())


@app.get("/api/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
