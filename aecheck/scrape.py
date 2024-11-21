from models import Character, Style
import constants

import requests
import bs4
import datetime

def get_info_from_aewiki(character: Character):
    """
    Scrape Another Eden Wiki page for character and return relevant informations

    Args:
        character (Character): Character object to scrape

    Returns:
        tuple: Tuple of (code, category, light_shadow, is_awaken, aewiki_url, update_date, personalities, japanese_name, korean_name, english_class_name)
    """
    aewiki_url = f'{constants.AEWIKI_BASE_URL}{character.english_name}{constants.AEWIKI_STYLE_SUFFIXS[character.style]}{constants.AEWIKI_ALTER_SUFFIX if character.is_alter else ""}'

    res = requests.get(aewiki_url)
    if res.status_code != 200:
        raise Exception("Wiki page not found", res.status_code)

    soup = bs4.BeautifulSoup(res.text, 'lxml')

    general_datas = soup.find("article", {"title": "General Data"}).find_all("td")
    is_awaken = "Stellar Awakened" in str(general_datas[0].text)
    light_shadow = str(general_datas[5].text).lower().strip()
    
    obtain = str(general_datas[6].text).strip()
    category = "FREE"
    if obtain == "Dreams":
        category = "ENCOUNTER"
    elif "Symphony" in obtain:
        category = "COLAB"
    
    personalities = list(map(
        lambda x: x.text.strip(),
        general_datas[7].find_all("a")
    ))

    other_datas = soup.find("article", {"title": "Other Data"}).find_all("td")
    code = int(str(other_datas[1].text).strip())
    japanese_name = str(other_datas[2].text).split("(")[0].strip()
    korean_name = str(other_datas[3].text).split("(")[0].strip()
    date_index = 9 if character.is_alter else 6
    update_datestr = str(other_datas[date_index].text).split(" / ")[1].strip() # Oct 10, 2024 or October 10, 2024
    try:
        update_date = datetime.datetime.strptime(update_datestr, "%b %d, %Y").strftime("%Y-%m-%d")
    except ValueError:
        try:
            update_date = datetime.datetime.strptime(update_datestr, "%B %d, %Y").strftime("%Y-%m-%d")
        except ValueError:
            try:
                update_date = datetime.datetime.strptime(update_datestr, "%b %d %Y").strftime("%Y-%m-%d")
            except ValueError:
                update_date = datetime.datetime.strptime(update_datestr, "%Y-%m-%d").strftime("%Y-%m-%d")

    character_classes = soup.find("div", {"class": "character-class"}).find_all("td")
    english_class_name = str(character_classes[7].text).split(" ...▽ ")[0] if character.style != Style.FOUR.value else None

    return (
        code,
        category,
        light_shadow,
        is_awaken,
        aewiki_url,
        update_date,
        personalities,
        japanese_name,
        korean_name,
        english_class_name
    )

def get_dungeon_from_aewiki(style: Style, english_class_name: str):
    """
    Scrape Another Eden Wiki page for character class and return its dungeon name

    Args:
        style (Style): Style of the character
        english_class_name (str): English name of the character class

    Returns:
        str: Name of the dungeon
    """
    if style == Style.AS.value:
        return "Treatise"
    elif style == Style.ES.value:
        return "Codex"
    elif style == Style.FOUR.value:
        return None
    else:
        aewiki_url = f'{constants.AEWIKI_BASE_URL}{english_class_name}_Tome'

        res = requests.get(aewiki_url)
        if res.status_code != 200:
            return "Opus"

        soup = bs4.BeautifulSoup(res.text, 'lxml')
        li_texts = list(map(
            lambda x: x.text.strip(),
            soup.find_all("li")
        ))

        for txt in li_texts:
            if "(VH)" in txt and not txt.startswith("Obtained"):
                return str(txt).split("(")[0].strip()
            
        raise Exception("Dungeon not found")



def get_info_from_altema(character: Character) -> str:
    """
    Scrape Altema page for character and return its Japanese class name

    Args:
        character (Character): Character object to scrape

    Returns:
        str: Japanese name of the character class
    """
    if character.style == Style.FOUR.value:
        return None
    
    def fetch_page_content(url: str) -> str:
        res = requests.get(url)
        if res.status_code != 200:
            raise Exception("Altema page not found")
        return res.text

    def extract_japanese_class_name(td_texts: list) -> str:
        for txt in td_texts:
            if "(★5)" in txt:
                return str(txt).split("(")[0].strip()
        raise Exception("Japanese class name not found")

    altema_url = character.altema_url
    page_content = fetch_page_content(altema_url)
    soup = bs4.BeautifulSoup(page_content, 'lxml')
    td_texts = [td.text.strip() for td in soup.find_all("td")]

    return extract_japanese_class_name(td_texts)
