import json


with open('users.json', 'w', encoding='utf-8') as f:
    data = {'admin': '12345678'}
    json.dump(data, f, ensure_ascii=False, indent = 4)