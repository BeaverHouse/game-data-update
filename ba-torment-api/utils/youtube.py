import urllib.parse

from fastapi import HTTPException

def parse_youtube_embed_link(link: str) -> str:
    if link.startswith("https://youtu.be/"):
        id = link.split("/")[-1]
    elif link.startswith("https://www.youtube.com/watch?v="):
        id = urllib.parse.parse_qs(urllib.parse.urlparse(link).query)["v"][0]
    else:
        raise HTTPException(status_code=400, detail="Invalid link")
    return f'https://www.youtube.com/embed/{id}'