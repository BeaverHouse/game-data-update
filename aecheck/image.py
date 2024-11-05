import PIL
import PIL.Image
from dotenv import load_dotenv
import os
import io
import requests

from models import Character
import constants

def upload_image(character: Character, character_id: str, character_code: int, is_awaken: bool):
    load_dotenv()
    img_suffix = constants.IMG_SUFFIXS[character.style]
    oracle_upload_url = os.getenv("AECHECK_UPLOAD_URL")

    command_img = PIL.Image.open(f'aecheck/img/{character_code}{img_suffix}.png')
    command_img.thumbnail((120, 120))
    output_png = io.BytesIO()
    command_img.save(output_png, format="PNG")
    command_img_png_bytes = output_png.getvalue()
    requests.put(f'{oracle_upload_url}/o/aecheck/character/{character_id}.png', data=command_img_png_bytes)
    
    output_png = io.BytesIO()
    command_img.save(output_png, format="WEBP")
    command_img_webp_bytes = output_png.getvalue()
    requests.put(f'{oracle_upload_url}/o/aecheck/character/{character_id}.webp', data=command_img_webp_bytes)

    print(f"Image uploaded for {character.english_name}")

    if is_awaken:
        awaken_img = PIL.Image.open(f'aecheck/img/{character_code}{img_suffix}_opened.png')
        awaken_img.crop((15, 15, 120, 120))

        output_png = io.BytesIO()
        awaken_img.save(output_png, format="PNG")
        awaken_img_png_bytes = output_png.getvalue()
        requests.put(f'{oracle_upload_url}/o/aecheck/staralign/{character_id}.png', data=awaken_img_png_bytes)

        output_png = io.BytesIO()
        awaken_img.save(output_png, format="WEBP")
        awaken_img_webp_bytes = output_png.getvalue()
        requests.put(f'{oracle_upload_url}/o/aecheck/staralign/{character_id}.webp', data=awaken_img_webp_bytes)

        print(f"Awaken image uploaded for {character.english_name}")
