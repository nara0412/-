import os
import json

all_files = set(os.listdir("json_data"))

# 輸出標準化結果
standardized_data = []

def standardize_item(item, category):
    return {
        "category": category,
        "name": item.get("name"),
        "price": item.get("price"),
        "specs": item.get("specs", {}),
        "rating": item.get("rating"),
        "link": item.get("link"),
        "comments": item.get("comments", []),
        # "image": item.get("image", [])
    }

for filename in all_files:
    if not filename.endswith(".json"):
        continue

    filepath = os.path.join("json_data", filename)
    category = filename.replace(".json", "")

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            for item in data:
                standardized_data.append(standardize_item(item, category))
    except FileNotFoundError:
        print(f"尚未提供檔案：{filename}，將略過。")

# 儲存成標準化JSON
with open("standardized_products.json", "w", encoding="utf-8") as f:
    json.dump(standardized_data, f, ensure_ascii=False, indent=2)

print(f"已完成，共處理 {len(standardized_data)} 筆商品資料。")