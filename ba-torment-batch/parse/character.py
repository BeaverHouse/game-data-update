from dotenv import load_dotenv
import os
import requests
import time
from pprint import pprint

from utils.database import get_postgres


def update_student_info() -> None:
    """
    Update character id and name from SchaleDB

    Args:
        develop (bool): parameter that indicates if the data is for development or not.
    """
    res = requests.get("https://schaledb.com/data/kr/students.min.json")

    student_info = list(map(
        lambda x: (int(x["Id"]), x["Name"]),
        res.json().values()
    ))

    table_name = "ba_torment.students" 

    with get_postgres() as conn:
        cur = conn.cursor()
        cur.execute(f"SELECT student_id FROM {table_name}")
        current_ids = list(map(lambda x: int(x[0]), cur.fetchall()))
        
        update_info = [(id, name) for id, name in student_info if id not in current_ids]
        if not update_info:
            return
        cur.executemany(
            f"INSERT INTO {table_name} (student_id, name) VALUES(%s, %s)",
            update_info
        )
        conn.commit()
        print(f"Updated {len(update_info)} characters:")
        pprint(update_info)

        for id, _ in update_info:
            upload_character_image(id)
            time.sleep(0.3)
        
        print(f"Uploaded {len(update_info)} images")

def upload_character_image(id: int) -> None:
    """
    Upload character image from SchaleDB

    Args:
        id (int): character id
    """
    load_dotenv()
    oracle_upload_url = os.getenv("BATORMENT_UPLOAD_URL")

    res = requests.get(f"https://schaledb.com/images/student/icon/{id}.webp")

    img_bytes = res.content
    res = requests.put(f'{oracle_upload_url}/o/batorment/character/{id}.webp', data=img_bytes)

    if res.status_code != 200:
        print(res.text)
        raise Exception("Failed to upload image")
    
    print(f"Image uploaded for {id}")