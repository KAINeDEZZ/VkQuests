import json

with open('keys.json', 'r') as file:
    __keys = json.load(file)

TORTOISE_ORM = {
    "connections": {
        "default": f'postgres://{__keys.get("db_user")}:{__keys.get("db_password")}@localhost:5432/vk_quests'
        },

    "apps": {
        "core": {
            "models": [
                "database",
                "aerich.models"
            ],
            "default_connection": "default",
        },
    },

    'use_tz': False,
    'timezone': 'Asia/Yekaterinburg'
}


TOKEN = __keys.get('token', ''),
GROUP_ID = __keys.get('group_id', 0),

DIALOGS = __keys.get('dialogs', [])
