from dotenv import load_dotenv

from parse.character import update_student_info
from parse.result import upload_party_data, upload_summary
from utils.database import get_postgres

load_dotenv()

def ba_data_batch() -> None:
    print(f"Updating BA torment data...")
    update_student_info()
    print(f"Updated student info")

    with get_postgres() as conn:
        cur = conn.cursor()
        raid_table = "ba_torment.raids"
        cur.execute(f"SELECT raid_id FROM {raid_table} WHERE status = 'PENDING' ORDER BY created_at ASC")
        seasons = list(map(lambda x: x[0], cur.fetchall()))

        for season in seasons:
            upload_party_data(season)
            upload_summary(season)
            cur.execute(f"UPDATE {raid_table} SET status = 'COMPLETE', updated_at = CURRENT_TIMESTAMP WHERE raid_id = '{season}'")
            conn.commit()
            print(f"Updated {season}")

    print("Done!")

if __name__ == "__main__":
    load_dotenv()
    ba_data_batch()