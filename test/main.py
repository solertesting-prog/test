from app.api import app


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.api:app",
        host="localhost",
        port=3001,
        log_level="info",
        reload=True,
        workers=1,
    )