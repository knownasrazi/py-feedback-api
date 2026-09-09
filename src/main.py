from fastapi import FastAPI

app = FastAPI(title="py-feedback-api")

@app.get("/")
async def root():
    return {"name": "py-feedback-api", "tag": "Feedback, Python fast."}
