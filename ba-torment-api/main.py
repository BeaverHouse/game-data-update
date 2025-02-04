from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from .log.middleware import LogMiddleware

load_dotenv()

from .api.router import api_router

origins = [
    "http://localhost:5173",
]

# https://github.com/fastapi/fastapi/issues/2787#issuecomment-932666555
app = FastAPI(root_path="/ba-torment")
app.add_middleware(LogMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_origin_regex=r"^https://.*bluearchive-torment\.netlify\.app$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api_router)