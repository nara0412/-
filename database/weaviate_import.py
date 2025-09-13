# python weaviate_import.py

import json
import weaviate
from sentence_transformers import SentenceTransformer

client = weaviate.Client("http://localhost:8080")
model = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')

with open("standardized_products.json", "r", encoding="utf-8") as f:
    products = json.load(f)

for i, p in enumerate(products):
    combined = f"本商品類別為：{p['category']}。{p['name']}"
    if p.get("specs"):
        combined += " " + json.dumps(p["specs"], ensure_ascii=False)
    if p.get("comments"):
        combined += " " + " ".join(p["comments"])

    # 處理價格
    try:
        price = float(p.get("price", 0))
    except:
        price = 0.0

    vec = model.encode(combined)

    obj = {
        "name": p["name"],
        "category": p["category"],
        "price": price,
        "link": p.get("link", ""),
        "rating": p.get("rating", ""),
        "combined_text": combined
    }

    try:
        client.data_object.create(data_object=obj, class_name="Product", vector=vec)
    except Exception as e:
        print(f"第 {i+1} 筆匯入失敗：{p['name']}\n原因：{e}\n")

    if (i + 1) % 100 == 0:
        print(f"已匯入 {i + 1} 筆商品")

print("全部商品匯入完成")
