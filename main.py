from mastodon import Mastodon
import json
import time
from deep_translator import GoogleTranslator
from bs4 import BeautifulSoup

def initialize_mastodon(app_settings):
    mastodon = Mastodon(
        access_token=app_settings["access_token"],
        api_base_url=app_settings["api_base_url"]
    )
    return mastodon
def get_latest_toot(mastodon, account_id):
    timeline = mastodon.account_statuses(id = account_id, limit="1",exclude_reblogs=True)
    if timeline:
        latest_toot = timeline[0]
        return latest_toot
    return None
def monitor_new_toots(mastodon, app_settings,account_id, check_interval=60):
    last_toot_id = None
    while True:
        latest_toot = get_latest_toot(mastodon, account_id)
        
        if latest_toot and latest_toot['id'] != last_toot_id:
            last_toot_id = latest_toot['id']
            translate_and_publish(latest_toot,app_settings)
        time.sleep(check_interval)
def translate_and_publish(latest_toot,app_settings):
    if app_settings["language"] not in latest_toot['language']:
        original_text = latest_toot['content']
        translator = GoogleTranslator(source='auto', target=app_settings["language"])
        translated_text = translator.translate(original_text)
        soup = BeautifulSoup(translated_text, 'html.parser')
        plain_text = soup.get_text()
        mastodon.status_post(plain_text, visibility='public')
with open('settings.json', 'r') as file:
    app_settings = json.load(file)
mastodon = initialize_mastodon(app_settings)
monitor_new_toots(mastodon,app_settings,int(app_settings["account_id"]),check_interval=60)