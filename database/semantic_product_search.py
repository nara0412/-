# python semantic_product_search.py

import weaviate
import math
from sentence_transformers import SentenceTransformer, util

client = weaviate.Client("http://localhost:8080")
model = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')

def search_products(query_text: str, category_filter: str = "", limit: int = 20):
    query_vector = model.encode(query_text)

    query = client.query.get("Product", ["name", "price", "category", "link", "rating"]) \
        .with_near_vector({"vector": query_vector}) \
        .with_additional(["certainty"]) \
        .with_limit(limit)

    if category_filter:
        query = query.with_where({
            "path": ["category"],
            "operator": "Equal",
            "valueString": category_filter
        })

    result = query.do()
    return result["data"]["Get"]["Product"]

if __name__ == "__main__":
    query = input("請輸入需求語句：")
    results = search_products(query)

    for i, item in enumerate(results, 1):
        print(f"{i}. {item['name']} （分類：{item['category']}）")
        print(f"   價格：{math.ceil(item['price']*30)} 元")
        print(f"   相似度：{round(item['_additional']['certainty'] * 100, 2)}%")
        print(f"   評價：{item.get('rating', '')}")
        print(f"   連結：{item.get('link', '')}")
        print()