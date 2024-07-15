from fastapi import FastAPI
import uvicorn

from main_api.api.v1.api import app_router


app = FastAPI()

app.include_router(app_router)

if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8010, reload=True)