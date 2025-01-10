from postgres import get_postgres
from models import Character, Style
from scrape import get_info_from_aewiki, get_info_from_altema, get_dungeon_from_aewiki
import constants
import urllib.parse
import datetime

def compare_arrays(arr1, arr2):
    """
    Compare two arrays and print the result
    """
    if len(arr1) != len(arr2):
        print(f"Diff at length: {len(arr1)} != {len(arr2)}")
        return

    for i in range(len(arr1)):
        if arr1[i] != arr2[i]:
            print(f"Diff at index {i}: {arr1[i]} != {arr2[i]}")
        else:
            print(f"Same at index {i}: {arr1[i]}")

def compare_character(character: Character):
    code, category, light_shadow, is_awaken, aewiki_url, update_date, personalities, japanese_name, korean_name, english_class_name = get_info_from_aewiki(character)
    japanese_class_name = get_info_from_altema(character)
    english_dungeon_name = get_dungeon_from_aewiki(character.style, english_class_name)

    endpoint_keyword = f'{japanese_name}{constants.SEESAA_SUFFIXS[character.style]}'
    if character.is_original_4star:
        endpoint_keyword += "☆4"
        character.style = "☆4"
    seesaa_url = f'{constants.SEESAA_BASE_URL}{urllib.parse.quote(endpoint_keyword.encode("euc-jp"))}'

    with get_postgres() as conn:
        cur = conn.cursor()

        cur.execute(f"SELECT key FROM aecheck.translations WHERE en = '{english_dungeon_name}' AND key LIKE 'dungeon%'")
        dungeon_id = cur.fetchone()
        dungeon_id = dungeon_id[0] if dungeon_id else None
        
        if character.alter_character_korean_name:
            cur.execute(f"""
            SELECT c.character_code FROM aecheck.characters c 
            LEFT JOIN aecheck.translations t 
            ON c.character_code = t.key
            WHERE t.ko = '{character.alter_character_korean_name}'
            """)
            alter_code = cur.fetchone()[0]
        else:
            alter_code = None

        cur.execute("SELECT character_id FROM aecheck.characters WHERE character_code = %s AND style = %s", (f'c{code}', character.style))
        character_id = cur.fetchone()

        if character_id is None:
            print(f"Character {character.english_name} not found in database")
        else:
            character_id = character_id[0]

            cur.execute("""
            SELECT character_id, character_code, style, category, light_shadow, max_manifest, is_awaken, is_alter, alter_character, seesaa_url, aewiki_url, update_date
            FROM aecheck.characters
            WHERE character_id = %s
            """, (character_id,))

            compare_arrays(
                cur.fetchone(), 
                (character_id, f'c{code}', character.style, category, light_shadow, character.max_manifest, is_awaken, character.is_alter, alter_code, seesaa_url, aewiki_url, datetime.datetime.strptime(update_date, "%Y-%m-%d").date())
            )

            cur.execute("SELECT dungeon_id FROM aecheck.dungeon_mappings WHERE character_id = %s", (character_id,))
            db_dungeon_id = cur.fetchone()
            db_dungeon_id = db_dungeon_id[0] if db_dungeon_id else None
            compare_arrays(
                (db_dungeon_id, ),
                (dungeon_id, )
            )

            cur.execute("SELECT t.en FROM aecheck.personality_mappings pm LEFT JOIN aecheck.translations t ON pm.personality_id = t.key WHERE character_id = %s", (character_id,))
            compare_arrays(
                sorted(list(map(lambda x: x[0], cur.fetchall()))),
                sorted(personalities)
            )

            cur.execute(f"SELECT ko, en, ja FROM aecheck.translations WHERE key = %s", (f'c{code}',))
            compare_arrays(
                cur.fetchone(),
                (korean_name, character.english_name, japanese_name)
            )

            cur.execute("SELECT ko, en, ja FROM aecheck.translations WHERE key = %s", (f'book.{character_id}',))
            db_class_name = cur.fetchone()
            if db_class_name is None: 
                db_class_name = (None, None, None)
            compare_arrays(
                db_class_name,
                (character.korean_class_name, english_class_name, japanese_class_name)
            )

if __name__ == "__main__":
    compare_character(Character(
        english_name="Lokido",
        korean_class_name="테아트랄 베트",
        style=Style.NS.value,
        is_alter=True,
        alter_character_korean_name="로키드",
        altema_url="https://altema.jp/anaden/chara/1130",
    ))