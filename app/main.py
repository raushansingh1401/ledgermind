from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return {
        "message": "Reap CFO Agent API is running"
    }