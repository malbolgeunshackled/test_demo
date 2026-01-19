import json
import csv

# 1) читаем purchase_log.txt в память (предполагаем, что каждая строка — JSON)
purchases = {}  # user_id -> category
with open('purchase_log.txt', 'r', encoding='utf-8') as f:
    for line_num, line in enumerate(f, 1):
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            # если строки невалидны, можно пропустить или логировать
            # print(f"skip bad json on line {line_num}")
            continue
        user = obj.get('user_id')
        cat = obj.get('category')
        if user and cat is not None:
            purchases[user] = cat

# 2) читаем visit_log.csv построчно и пишем funnel.csv только для пользователей, у которых есть покупка
with open('visit_log.csv', 'r', encoding='utf-8', newline='') as vis_f, \
     open('funnel.csv', 'w', encoding='utf-8', newline='') as out_f:

    reader = csv.DictReader(vis_f)
    # Гарантируем заголовок user_id,source,category в выходном файле
    writer = csv.writer(out_f)
    writer.writerow(['user_id', 'source', 'category'])

    # Для каждой строки visit_log — если есть покупка в purchases -> записать с категорией
    for row in reader:
        # допустим, в visit_log.csv есть столбец 'user_id' и 'source'
        user = row.get('user_id')
        if not user:
            continue
        if user in purchases:
            source = row.get('source', '')  # на случай отсутствующего столбца
            category = purchases[user]
            writer.writerow([user, source, category])
