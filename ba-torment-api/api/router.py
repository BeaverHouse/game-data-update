from fastapi import APIRouter, HTTPException

from ..utils.database import get_postgres
from ..utils.youtube import parse_youtube_embed_link
from ..models import RaidInfo, YoutubeLinkInfo

api_router = APIRouter(tags=["BA torment"])

@api_router.get("/")
async def root():
    return {"message": "BA torment API"}

@api_router.get("/students")
async def get_students():
    table_name = "ba_torment.students"
    with get_postgres() as conn:
        cur = conn.cursor()
        cur.execute(f"SELECT student_id, name FROM {table_name}")
        students = cur.fetchall()

    return {str(id): name for id, name in students}

@api_router.get("/raids")
async def get_ranks() -> list[RaidInfo]:
    table_name = "ba_torment.raids"
    with get_postgres() as conn:
        cur = conn.cursor()
        cur.execute(f"SELECT raid_id, name FROM {table_name} WHERE status = 'COMPLETE' ORDER BY created_at ASC")
        ranks = cur.fetchall()

    return list(map(lambda x: RaidInfo(id=x[0], description=x[1]), ranks))

@api_router.post("/raid")
async def register_rank(raid_info: RaidInfo):
    table_name = "ba_torment.raids"
    with get_postgres() as conn:
        cur = conn.cursor()
        cur.execute(f"INSERT INTO {table_name} (raid_id, name, status) VALUES (:1, :2, 'PENDING')", (raid_info.id, raid_info.description))
        conn.commit()

@api_router.get("/links/{season}", response_model=list[YoutubeLinkInfo], response_model_exclude_none=True)
async def get_youtube_links(season: str) -> list[YoutubeLinkInfo]: 
    table_name = "ba_torment.named_users"
    with get_postgres() as conn:
        cur = conn.cursor()
        cur.execute(f"""
            SELECT user_id, description, youtube_url, score 
            FROM {table_name}
            WHERE raid_id = '{season}' OR raid_id IS NULL
            ORDER BY score DESC NULLS LAST
        """)
        links = cur.fetchall()

    return [YoutubeLinkInfo(
        user_id=int(user_id),
        description=description,
        youtube_url=youtube_url,
        score=int(score)
    ) for user_id, description, youtube_url, score in links]

@api_router.post("/link")
async def register_link(link_info: YoutubeLinkInfo):
    if link_info.youtube_url.startswith("https://www.youtube.com/@"):
        youtube_link = link_info.youtube_url
    elif link_info.score < 31076000:
        raise HTTPException(status_code=400, detail="Invalid link")
    else:
        youtube_link = parse_youtube_embed_link(link_info.youtube_url)
    table_name = "ba_torment.named_users"
    try:
        with get_postgres() as conn:
            cur = conn.cursor()
            cur.execute(
                f"INSERT INTO {table_name} (user_id, raid_id, description, youtube_url, score) VALUES (%s, %s, %s, %s, %s)", 
                (link_info.user_id, link_info.raid_id, link_info.description, youtube_link, link_info.score)
            )
            conn.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))