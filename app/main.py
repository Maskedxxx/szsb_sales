# api_service.py

import os
from fastapi import FastAPI
from dotenv import load_dotenv
from api.endpoints import router as api_router
load_dotenv('.env', override=True)

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
