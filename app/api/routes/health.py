from fastapi import APIRouter

from sqlalchemy import text

from app.db.database import SessionLocal

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("/live")
def liveness():
    return {"status": "alive"}

@router.get("/ready")
def readiness():
    try:
        with SessionLocal() as session:
            session.execute(text("SELECT 1"))

        return {"status": "ready"}

    except Exception:
        raise HTTPException(
            status_code=503,
            detail="Database unavailable",
        )
    
@router.get("")
def health():
    return {
        "status": "healthy",
        "service": "taskflow",
        "version": "1.1.0",
    }