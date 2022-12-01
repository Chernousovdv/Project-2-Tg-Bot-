import requests
import json
from fake_useragent import UserAgent


ua = UserAgent()

def champions_list():
    response = requests.get(url='https://op.gg/api/v1.0/internal/bypass/meta/champions?hl=en_US',
                            headers={'user-agent': f'{ua.random}'})
    with open('result.json', 'w') as file:
        json.dump(response.json(), file, indent=4, ensure_ascii=False)
    data = response.json()
    champions = data.get('data')
    return champions
def collect_data(user_input):
    response = requests.get(url='https://op.gg/api/v1.0/internal/bypass/meta/champions?hl=en_US',
    headers={'user-agent': f'{ua.random}'})
    with open('result.json', 'w') as file:
        json.dump(response.json(), file, indent=4, ensure_ascii=False)
    data = response.json()
    champions = data.get('data')
    tg_answer = {}
    for i in champions:
        if i.get('name') == user_input:
            champion_name = i.get('name')
            entips = i.get('enemy_tips')
            alltips = i.get('ally_tips')
            image = i.get('image_url')
            passive = i.get('passive')
            abilities = i.get('spells')
            tg_answer = (
                {
                    'name': champion_name,
                    'enemy_tips': entips,
                    'ally_tips': alltips,
                    'image_url': image,
                    'passive': passive,
                    'spells': abilities
                }
            )
    return tg_answer

