from dotenv import load_dotenv
import os
import ast
import collections
import requests

from parse.party import get_party_info
import constants

# https://ljhokgo.tistory.com/entry/Python-Oracle-DB-%EC%BF%BC%EB%A6%AC-%EC%8B%9C-Dictionary-%ED%98%95%ED%83%9C%EB%A1%9C-%EC%A1%B0%ED%9A%8C%ED%95%98%EA%B8%B0
def make_dic_factory(cursor):
    column_names = [d[0] for d in cursor.description]

    def create_row(*args):
        return dict(zip(column_names, args))

    return create_row

def upload_party_data(season: str, target_boss: int) -> dict:
    raid_id = f"{season}{'-' + str(target_boss) if target_boss != 0 else ''}"
    print(f"Uploading party data for {raid_id}...")

    scores = get_party_info(season, target_boss)        

    filters = collections.defaultdict(lambda: [0]*9)
    assist_filters = collections.defaultdict(lambda: [0]*9)
    min_partys = 99
    max_partys = 0
    for score in scores:
        party_data: dict = ast.literal_eval(score['PARTY_DATA'])
        score['PARTY_DATA'] = party_data
        
        for party in party_data.values():
            for member in party:
                student_id, star, weapon, is_assist = member // 1000, (member // 100) % 10, (member // 10) % 10, member % 10
                if student_id == 0:
                    continue
                if is_assist == 1:
                    assist_filters[str(student_id)][star + weapon] += 1
                else:
                    filters[str(student_id)][star + weapon] += 1

        min_partys = min(min_partys, len(party_data.keys()))
        max_partys = max(max_partys, len(party_data.keys()))

    upload_json_to_oracle(raid_id, category="v2/party", json_data={
        "filters": filters,
        "assist_filters": assist_filters,
        "min_partys": min_partys,
        "max_partys": max_partys,
        "parties": scores
    })


def upload_summary(season: str, target_boss: int) -> dict:
    raid_id = f"{season}{'-' + str(target_boss) if target_boss != 0 else ''}"
    print(f"Uploading summary for {raid_id}...")

    party_data = get_party_info(season, target_boss)
    torment_party_data = list(filter(lambda x: x['SCORE'] < constants.LUNATIC_MIN_SCORE, party_data))
    torment_data = process_summary(torment_party_data)
    lunatic_party_data = list(filter(lambda x: x['SCORE'] >= constants.LUNATIC_MIN_SCORE, party_data))
    lunatic_data = process_summary(lunatic_party_data)

    data = {
        "torment": torment_data,
        "lunatic": lunatic_data,
    }

    upload_json_to_oracle(raid_id, category="v2/summary", json_data=data)

def process_summary(scores: list[dict]) -> None:
    clear_count = len(scores)
    filters = collections.defaultdict(lambda: [0]*9)
    assist_filters = collections.defaultdict(lambda: [0]*9)
    party_counts = collections.defaultdict(lambda: [0]*4)
    top_partys = collections.defaultdict(int)
    count_arr = [x for x in [100, 200, 500, 1000, 2000, 5000, 10000, 20000] if x < clear_count] + [clear_count]
    for score in scores:
        party_data: dict = ast.literal_eval(score['PARTY_DATA'])
        party_arr = []
        for party in party_data.values():
            for member in party:
                student_id, star, weapon, is_assist = member // 1000, (member // 100) % 10, (member // 10) % 10, member % 10
                if student_id == 0:
                    continue
                if is_assist == 1:
                    assist_filters[str(student_id)][star + weapon] += 1
                filters[str(student_id)][star + weapon] += 1
            party_arr += sorted(list(map(lambda x: str(x // 1000), party)))
        party_index = min(len(party_data.values()), 4) - 1
        for i in count_arr:
            if score["FINAL_RANK"] <= i:
                party_counts[f'in{str(i)}'][party_index] += 1

        top_partys["_".join(party_arr)] += 1
    
    return {
        "clear_count": clear_count,
        "party_counts": party_counts,
        "filters": parse_filters(filters, clear_count),
        "assist_filters": parse_filters(assist_filters, clear_count),
        "top5_partys": collections.Counter(top_partys).most_common(5),
    }

def upload_json_to_oracle(raid_id: str, category: str, json_data: any) -> None:
    load_dotenv()
    oracle_upload_url = os.getenv("BATORMENT_UPLOAD_URL")

    requests.put(f'{oracle_upload_url}/o/batorment/{category}/{raid_id}.json', json=json_data)

def parse_filters(filters: dict[str, list[int]], clear_count: int) -> dict:
    more_than_1per = {key: value for key, value in filters.items() if sum(value) > clear_count // 100}
    return collections.OrderedDict(collections.Counter(more_than_1per).most_common())