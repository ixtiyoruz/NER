import os
import json

files = sorted(os.listdir("data/crawled_texts_old"))
files = [os.path.join("data/crawled_texts_old", name) for name in files]
read_json_files = []
for file in files:
    with open(file, 'rt+') as f:
        read_json_files.append(json.load(f))

new_json_files = []
for file_name, json_data in zip(files, read_json_files):
    new_name = file_name.replace("crawled_texts_old","crawled_texts")
    new_json = {}
    keys = list(json_data.keys())
    new_json["status"] = json_data[keys[0]]
    new_json["status"] = json_data["status"]
    new_json["text"] = json_data[keys[0]]
    new_json["url"] = keys[0]
    new_json["file_name"] = new_name
    new_json["label"] = []
    new_json_files.append(new_json)


for new_json_data in new_json_files:
    with open(new_json_data['file_name'], 'wt+') as f:
        f.write(json.dumps(new_json_data))
# print(new_json_files)
