import csv
import json

data_path = "./data/mindbook_book_categories.json"
data_detail_path = "./data/mindbook_book_details.json"


def load_json(data_path):
    with open(data_path, encoding="utf-8") as json_file:
        data = json.load(json_file)
    return data

def convert_json_to_dict():
    data = load_json(data_path)
    result = dict()
    for item in data:
        if item['book_id'] not in result:
            result[item['book_id']] = str(item['category_id'])
        else:
            result[item['book_id']] += ", " + str(item['category_id'])
    return dict(sorted(result.items()))

def write_to_csv():
    result = convert_json_to_dict()
    book_detail = load_json(data_detail_path)
    with open('data.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["id", "categories", "author"])
        for i, item in enumerate(result.items()):
            writer.writerow([item[0], item[1], "author_" + str(book_detail[i]["author_id"]) ])

write_to_csv()