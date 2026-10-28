"""Apex Operations API: a small, dependency-light service used for the DevOps assessment."""
import logging
import time
import uuid
from contextlib import asynccontextmanager
from typing import Literal

from fastapi import Depends, FastAPI, HTTPException, Request, Response
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.orm import Session

from app import db
from app.config import get_settings
from app.logging_config import setup_logging
from app.metrics import DB_UP, LATENCY, REQUESTS

log = logging.getLogger("apex.api")
Status = Literal["open", "in_progress", "done"]


class OperationIn(BaseModel):
    title: str = Field(min_length=1, max_length=200)


class StatusUpdate(BaseModel):
    status: Status


class OperationOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    status: str


def create_app(database_url: str | None = None) -> FastAPI:
    settings = get_settings()
    setup_logging(settings.log_level)
    engine = db.make_engine(database_url or settings.database_url)

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        # Retry so the API survives starting before Postgres is fully ready.
        for attempt in range(1, 11):
            try:
                db.Base.metadata.create_all(engine)
                log.info("database initialised", extra={"status": "ok"})
                break
            except Exception as exc:
                log.warning(
                    "database not ready, retrying",
                    extra={"error": str(exc)[:200], "status": attempt},
                )
                time.sleep(2)
        yield

    app = FastAPI(title="Apex Operations API", version=settings.app_version, lifespan=lifespan)
    app.state.engine = engine

    def get_session():
        with Session(engine) as session:
            yield session

    @app.middleware("http")
    async def observe(request: Request, call_next):
        request_id = request.headers.get("x-request-id", str(uuid.uuid4()))
        start = time.perf_counter()
        status = 500
        try:
            response = await call_next(request)
            status = response.status_code
            response.headers["x-request-id"] = request_id
            return response
        finally:
            elapsed = time.perf_counter() - start
            route = request.scope.get("route")
            path = route.path if route else "unmatched"
            REQUESTS.labels(request.method, path, str(status)).inc()
            LATENCY.labels(request.method, path).observe(elapsed)
            if path not in ("/metrics", "/health"):
                log.info(
                    "request",
                    extra={
                        "request_id": request_id,
                        "method": request.method,
                        "path": request.url.path,
                        "status": status,
                        "duration_ms": round(elapsed * 1000, 2),
                    },
                )

    @app.get("/health")
    def health():
        """Liveness: the process is up. Does not touch dependencies."""
        return {"status": "ok"}

    @app.get("/ready")
    def ready(response: Response):
        """Readiness: the app can serve traffic (database reachable)."""
        if get_settings().simulate_bad_release:
            log.error("simulated bad release", extra={"error": "SIMULATE_BAD_RELEASE=true"})
            response.status_code = 503
            return {"status": "not_ready", "reason": "simulated bad release"}
        ok = db.check_db(app.state.engine)
        DB_UP.set(1 if ok else 0)
        if not ok:
            log.error("database unavailable", extra={"error": "db_unavailable"})
            response.status_code = 503
            return {"status": "not_ready", "reason": "database unavailable"}
        return {"status": "ready"}

    @app.get("/version")
    def version():
        return {"version": settings.app_version}

    @app.get("/metrics")
    def metrics():
        return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

    @app.post("/operations", response_model=OperationOut, status_code=201)
    def create_operation(body: OperationIn, session: Session = Depends(get_session)):
        op = db.Operation(title=body.title)
        session.add(op)
        session.commit()
        session.refresh(op)
        return op

    @app.get("/operations", response_model=list[OperationOut])
    def list_operations(session: Session = Depends(get_session)):
        return session.query(db.Operation).order_by(db.Operation.id).all()

    @app.get("/operations/{op_id}", response_model=OperationOut)
    def get_operation(op_id: int, session: Session = Depends(get_session)):
        op = session.get(db.Operation, op_id)
        if op is None:
            raise HTTPException(status_code=404, detail="operation not found")
        return op

    @app.patch("/operations/{op_id}/status", response_model=OperationOut)
    def update_status(op_id: int, body: StatusUpdate, session: Session = Depends(get_session)):
        op = session.get(db.Operation, op_id)
        if op is None:
            raise HTTPException(status_code=404, detail="operation not found")
        op.status = body.status
        session.commit()
        session.refresh(op)
        return op

    return app


app = create_app()
