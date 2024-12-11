import json
import ast
import collections

def read_input(season: str):
    with open(f"ba-torment-manual/input/{season}.json", "r") as file:
        return json.load(file)

def write_output(season: str, category: str, data: list):
    with open(f"ba-torment-manual/output/{season}-{category}.json", "w") as file:
        json.dump(data, file, indent=4)

def parse_party_data(season: str):
    input_data = read_input(season)
    datas = input_data["d"]

    output_data = []
    for data in datas:
        torment_rank = data['r']
        final_rank = data['r'] if season.startswith("S") else -1
        user_id = -torment_rank
        score = data['s']
        party_data = get_party_detail(data['t'])

        output_data.append({
            "USER_ID": user_id,
            "TORMENT_RANK": torment_rank,
            "FINAL_RANK": final_rank,
            "SCORE": score,
            "PARTY_DATA": str(party_data)
        })
    
    return output_data

def get_party_detail(party_data):
    party_count = len(party_data)
    result = {}
    for i in range(party_count):
        try_party = []
        for striker in party_data[i]["m"]:
            if striker is None:
                try_party.append(0)
            else:
                try_party.append(get_reduced_number(striker))
        for special in party_data[i]["s"]:
            if special is None:
                try_party.append(0)
            else:
                try_party.append(get_reduced_number(special))
        result.update({f"party_{i+1}": try_party})
    return result

def get_reduced_number(striker):
    student_id = striker["id"]
    star = striker["star"]
    weapon = striker["weaponStar"]
    is_assist = 1 if striker["isAssist"] == True else 0
    return student_id * 1000 + star * 100 + weapon * 10 + is_assist 

# https://ljhokgo.tistory.com/entry/Python-Oracle-DB-%EC%BF%BC%EB%A6%AC-%EC%8B%9C-Dictionary-%ED%98%95%ED%83%9C%EB%A1%9C-%EC%A1%B0%ED%9A%8C%ED%95%98%EA%B8%B0
def make_dic_factory(cursor):
    column_names = [d[0] for d in cursor.description]

    def create_row(*args):
        return dict(zip(column_names, args))

    return create_row

def upload_party_data(season: str) -> dict:
    print(f"Uploading party data for {season}...")

    scores = parse_party_data(season)
        
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

    write_output(season, "total", data={
        "filters": dict(sorted(filters.items())),
        "assist_filters": dict(sorted(assist_filters.items())),
        "min_partys": min_partys,
        "max_partys": max_partys,
        "parties": scores
    })

def upload_summary(season: str) -> dict:
    print(f"Uploading summary for {season}...")

    scores = parse_party_data(season)

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

    write_output(season, "summary", data={
        "clear_count": clear_count,
        "party_counts": party_counts,
        "filters": parse_filters(filters, clear_count),
        "assist_filters": parse_filters(assist_filters, clear_count),
        "top5_partys": collections.Counter(top_partys).most_common(5),
    })

def parse_filters(filters: dict[str, list[int]], clear_count: int) -> dict:
    more_than_1per = {key: value for key, value in filters.items() if sum(value) > clear_count // 100}
    return collections.OrderedDict(collections.Counter(more_than_1per).most_common())

if __name__ == "__main__":
    season = "S72"  
    upload_party_data(season)
    upload_summary(season)

