from typing import Tuple
import polars as pl
import sys

import constants

def get_rank_season(season: str, target_boss: int = 0) -> pl.DataFrame:
    """
    Get rank data

    Args:
        season (str): season starts with "S" or "3S".
        target_boss (int): target boss number if it's Grand Assault (대결전).
    """
    if target_boss != 0:
        return get_rank_season_triple(season, target_boss)
    else:
        return get_rank_season_normal(season)


def get_rank_season_normal(season: str) -> pl.DataFrame:
    """
    Get "Total Assault (총력전)" rank data
    """
    url = f"{constants.DATA_BASE_URL}/RaidRankData/{season}/TeamDataDetail_Original.csv"
    
    try:
        df = pl.read_csv(url, schema=pl.Schema({"Rank": pl.Int64, "BestRankingPoint": pl.Int64, "AccountId": pl.Int64}), truncate_ragged_lines=True)
        return df.rename({"AccountId": "USER_ID", "Rank": "FINAL_RANK", "BestRankingPoint": "SCORE"}) \
              .unique(keep="first") \
              .filter(pl.col("FINAL_RANK") <= constants.PLATINUM_CUT) \
              .sort(by="SCORE", descending=True)
    except Exception as e:
        print(e)
        sys.exit(1)

def get_rank_season_triple(season: str, target_boss: int) -> pl.DataFrame:
    """
    Get "Grand Assault (대결전)" rank data
    """
    parsed_season = season[1:]
    url = f"{constants.DATA_BASE_URL}/RaidRankDataER/{parsed_season}/FullData_Original.csv"
    
    try:
        df = pl.read_csv(url, truncate_ragged_lines=True)
        return df.select(pl.col("AccountId", "Rank", "BestRankingPoint", f"Boss{target_boss}")) \
              .rename({"AccountId": "USER_ID", "Rank": "FINAL_RANK", f"Boss{target_boss}": "SCORE"}) \
              .unique(keep="first") \
              .filter(pl.col("FINAL_RANK") <= constants.PLATINUM_CUT) \
              .sort(by="SCORE", descending=True)
    except Exception as e:
        print(e)
        sys.exit(1)