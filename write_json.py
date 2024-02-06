import json

# {day: {cls: {group: {time: 'PE'}}}}
with open('data.json', 'w', encoding='utf-8') as f:
    times = ['9:00-9:45','10:00-10:45', '11:00-11:45', '11:55-12:40', '13:00-13:45',
             '14:05-14:50', '15:00-15:45', '15:55-16:40']
    classes = ['7', '8', '9', '10', '11']
    data = {}
    for day in ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница']:
        data[day] = {}
        for cls in classes:
            data[day][cls] = {}
            if cls == '7':
                for group in ['1', '2', '3', '4']:
                    data[day][cls][group] = {}
                    for time in times:
                        data[day][cls][group][time] = 'Math'
            else:
                for group in ['1', '2']:
                    data[day][cls][group] = {}
                    for time in times:
                        data[day][cls][group][time] = 'Math'
    print(data)
    json.dump(data, f, ensure_ascii=False, indent=4)
