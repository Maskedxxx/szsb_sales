# main.py

import argparse
parser = argparse.ArgumentParser(description='Neuro-Assistant')
parser.add_argument(
    "--env-file",
    type=str,
    help="Path to .env file containing environment variables",
    dest="env_file"
)
args = parser.parse_args()

from dotenv import load_dotenv
if args.env_file is not None:
    load_dotenv(args.env_file, override=True)

import os
from fastapi import FastAPI
from api.endpoints import router as api_router

app = FastAPI(
    title="AI-Assistant API",
    description="API for the sales department ai-assistant.", 
    version="0.1.0"
)
app.include_router(api_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=os.getenv("HOST"),
        port=int(os.getenv("PORT")),
        log_level="info"
    )
