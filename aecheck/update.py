from postgres import get_postgres
from models import Character, Style
from scrape import get_info_from_aewiki, get_info_from_altema, get_dungeon_from_aewiki
import constants
from image import upload_image

import urllib.parse

def update_character(character: Character):
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
        
        cur.execute("SELECT COUNT(*) FROM aecheck.characters WHERE character_id LIKE 'char0%'")
        count = cur.fetchone()[0]

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
            character_id = f'char{str(count+1).zfill(4)}'
            cur.execute(
                "INSERT INTO aecheck.characters (character_id, character_code, category, style, light_shadow, max_manifest, is_awaken, is_alter, alter_character, seesaa_url, aewiki_url, update_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", 
                (character_id, f'c{code}', category, character.style, light_shadow, character.max_manifest, is_awaken, character.is_alter, alter_code, seesaa_url, aewiki_url, update_date)
            )

            if character.is_alter:
                cur.execute("UPDATE aecheck.characters SET alter_character = %s WHERE character_id = %s AND style IN ('4☆', 'NS')", (f'c{code}', alter_code))

            cur.execute(
                "INSERT INTO aecheck.dungeon_mappings (character_id, dungeon_id) VALUES (%s, %s)",
                (character_id, dungeon_id)
            )

            for personality in personalities:
                cur.execute(f"SELECT key FROM aecheck.translations WHERE en = '{personality}'")
                personality_id = cur.fetchone()[0]
                cur.execute(
                    "INSERT INTO aecheck.personality_mappings (character_id, personality_id) VALUES (%s, %s)",
                    (character_id, personality_id)
                )
            
            cur.execute("SELECT key FROM aecheck.translations WHERE key = %s", (f'c{code}',))   
            if cur.fetchone() is None:
                cur.execute(
                    "INSERT INTO aecheck.translations (key, ko, en, ja) VALUES (%s, %s, %s, %s)",
                    (f'c{code}', korean_name, character.english_name, japanese_name)
                )

            cur.execute(
                "INSERT INTO aecheck.translations (key, ko, en, ja) VALUES (%s, %s, %s, %s)",
                (f'book.{character_id}', character.korean_class_name, english_class_name, japanese_class_name)
            )
        else:
            character_id = character_id[0]

            cur.execute("""
            UPDATE aecheck.characters SET
                category = %s,
                style = %s,
                light_shadow = %s,
                max_manifest = %s,
                is_awaken = %s,
                is_alter = %s,
                alter_character = %s,
                seesaa_url = %s,
                aewiki_url = %s,
                update_date = %s
            WHERE character_id = %s
            """, (
                category,
                character.style,
                light_shadow,
                character.max_manifest,
                is_awaken,
                character.is_alter,
                alter_code,
                seesaa_url,
                aewiki_url,
                update_date,
                character_id
            ))

            cur.execute("UPDATE aecheck.dungeon_mappings SET dungeon_id = %s WHERE character_id = %s", (dungeon_id, character_id))

            cur.execute("DELETE FROM aecheck.personality_mappings WHERE character_id = %s", (character_id,))
            for personality in personalities:
                cur.execute(f"SELECT key FROM aecheck.translations WHERE en = '{personality}'")
                personality_id = cur.fetchone()[0]
                cur.execute(
                    "INSERT INTO aecheck.personality_mappings (character_id, personality_id) VALUES (%s, %s)",
                    (character_id, personality_id)
                )
            
            cur.execute("UPDATE aecheck.translations SET ko = %s, en = %s, ja = %s WHERE key = %s", (korean_name, character.english_name, japanese_name, f'c{code}'))
            cur.execute("UPDATE aecheck.translations SET ko = %s, en = %s, ja = %s WHERE key = %s", (character.korean_class_name, english_class_name, japanese_class_name, f'book.{character_id}'))

    upload_image(character, character_id, code, is_awaken)

if __name__ == "__main__":
    update_character(Character(
        english_name="Rufus",
        korean_class_name=None,
        style=Style.FOUR.value,
        altema_url="https://altema.jp/anaden/chara/67",
        is_original_4star=True
    ))
    update_character(Character(
        english_name="Rufus",
        korean_class_name="블레이즈 히어로",
        style=Style.AS.value,
        altema_url="https://altema.jp/anaden/chara/1114",
    ))
    update_character(Character(
        english_name="Shanie",
        korean_class_name="아크 나이트",
        style=Style.NS.value,
        max_manifest=2,
        alter_character_korean_name="가시나무 저주의 여인 셰이네",
        altema_url="https://altema.jp/anaden/chara/180",
    ))