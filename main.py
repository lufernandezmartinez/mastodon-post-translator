from mastodon import Mastodon
import json
import time
from deep_translator import GoogleTranslator
from bs4 import BeautifulSoup

def initialize_mastodon(app_settings):
    try:
        mastodon = Mastodon(
            access_token=app_settings["access_token"],
            api_base_url=app_settings["api_base_url"]
        )
        return mastodon
    except Exception as e:
        raise e

def get_latest_toot(mastodon, account_id):
    try:
        timeline = mastodon.account_statuses(id = account_id, limit="1",exclude_reblogs=True)
        if timeline:
            latest_toot = timeline[0]
            return latest_toot
    except Exception as e:
        return None
def monitor_new_toots(mastodon, app_settings,account_id, check_interval=60):
    try:
        last_toot_id = None
        while True:
            latest_toot = get_latest_toot(mastodon, account_id)

            if latest_toot and latest_toot['id'] != last_toot_id:
                last_toot_id = latest_toot['id']
                translate_and_publish(latest_toot,app_settings)
            time.sleep(check_interval)
    except Exception as e:
        return None
def translate_and_publish(latest_toot,app_settings):
    try:
        if app_settings["language"] not in latest_toot['language']:
            original_text = latest_toot['content']
            translator = GoogleTranslator(source='auto', target=app_settings["language"])
            translated_text = translator.translate(original_text)
            soup = BeautifulSoup(translated_text, 'html.parser')
            plain_text = soup.get_text()
            mastodon.status_post(plain_text, visibility='public')
    except Exception as e:
        return None
def main():
    while True:
        try:
            with open('settings.json', 'r') as file:
                app_settings = json.load(file)
            mastodon = initialize_mastodon(app_settings)
            monitor_new_toots(mastodon,app_settings,int(app_settings["account_id"]),check_interval=60)
        except Exception as e:/home/lufernandez/Desktop/Clase/EIE/EIE_T1_A1_Luis_Fernandez.pdf