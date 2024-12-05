from fastapi import FastAPI
# from api.task import router as task_router

app = FastAPI(
    title="Video GUI"
)


@app.get("/ping")
async def root():
    return "pong"
