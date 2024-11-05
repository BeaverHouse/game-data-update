import polars as pl
import requests
import csv
import os

from parse.rank import get_rank_season
import constants

def get_party_info(season: str) -> list[dict]:
    """
    Get party data

    Args:
        season (str): season starts with "S" or "3S".
        develop (bool): parameter that indicates if the data is for development or not.
    """
    target_boss, rank_df = get_rank_season(season)

    if target_boss == 0:
        return get_party_info_normal(season, rank_df)
    else:
        return get_party_info_triple(season, target_boss, rank_df)
    
def get_party_info_normal(season: str, rank_df: pl.DataFrame):
    url = f"{constants.DATA_BASE_URL}/RaidRankData/{season}/TeamDataDetail_Original.csv"

    party_df = get_party_dataframe(season, url)
    merged_df = rank_df \
      .join(party_df, on="USER_ID", how="left") \
      .filter(pl.col("PARTY_DATA").is_not_null()) \
      .with_columns(pl.col("FINAL_RANK").alias("TORMENT_RANK")) \
      .unique(subset="USER_ID", keep="first") \
      .sort(by="TORMENT_RANK")
    
    return merged_df.to_dicts()

def get_party_info_triple(season: str, target_boss: int, rank_df: pl.DataFrame):
    parsed_season = season[1:]
    url = f"{constants.DATA_BASE_URL}/RaidRankDataER/{parsed_season}/TeamDataDetailBoss{target_boss}_Original.csv"

    party_df = get_party_dataframe(season, url)
    merged_df = rank_df \
      .with_row_index(offset=1) \
      .join(party_df, on="USER_ID", how="left") \
      .rename({"index": "TORMENT_RANK"}) \
      .unique(subset="USER_ID", keep="first") \
      .sort(by="TORMENT_RANK")

    return merged_df.to_dicts()  

def get_party_dataframe(season: str, url: str) -> pl.DataFrame:
    os.makedirs("rawdetail", exist_ok=True)
    file_name = f"rawdetail/{season}D.csv"

    try:
        res = requests.get(url)
        with open(file_name, "wb") as f:
            f.write(res.content)
    except Exception as e:
        print(e)
        return

    with open(file_name, "r") as f:
        reader = csv.reader(f)
        next(reader)
        
        party_list = []
        for row in reader:
            _, _, *party_info = row
            party_info = party_info[:-1]

            user_id = party_info[0]
            if int(user_id) == 6672885: continue
            party_count = len(party_info) // 44
            party_data = parse_party_data(party_info, party_count)
            party_list.append({
                "USER_ID": int(user_id),
                "PARTY_DATA": str(party_data)
            })
    
    os.remove(file_name)
    return pl.DataFrame(party_list)

def parse_party_data(parties: list, party_count: int) -> dict:
    result = {}
    for i in range(party_count):
        try_party = []

        member_info = parties[i*44:(i+1)*44][2:]
        for j in range(6):
            _, student_id, star, _, _, weapon, is_assist = member_info[j*7:(j+1)*7]
            if len(student_id) == 0:
                try_party.append(0)
            else:
                student_id = int(student_id)
                star = int(star)
                weapon = max(0, int(weapon))
                is_assist = 1 if is_assist == "True" else 0
                try_party.append(get_reduced_number(student_id, star, weapon, is_assist))

        result.update({f"party_{i+1}": try_party})
    return result

def get_reduced_number(student_id: int, star: int, weapon: int, is_assist: int) -> int:
    """
    Calculate the reduced number based on the character's star and weapon levels.
    Reduced number has 9 digits.
    - 1 ~ 5th digit: student ID
    - 7th digit: star level
    - 8th digit: weapon level
    - 9th digit: assist or not (1 or 0)

    Args:
        student_id (int): student's id.
        star (int): student's star level.
        weapon (int): student's weapon level.
        is_assist (int): whether the student is an assist or not.
    """
    return student_id * 1000 + star * 100 + weapon * 10 + is_assist 