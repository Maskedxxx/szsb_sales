# main.py

from dotenv import load_dotenv
load_dotenv('.env.docker', override=True)

import os
from fastapi import FastAPI
from api.endpoints import router as api_router

app = FastAPI()
app.include_router(api_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=os.getenv("HOST"),
        port=int(os.getenv("PORT")),
        log_level="debug"
    )
