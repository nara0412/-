# python weaviate_setup.py
# http://localhost:8080/v1/schema

import weaviate

client = weaviate.Client("http://localhost:8080")

# 測試class是否存在
# if client.schema.exists("Product"):
#     client.schema.delete_class("Product")

schema = {
    "class": "Product",
    "vectorizer": "none",
    "properties": [
        {"name": "name", "dataType": ["text"]},
        {"name": "category", "dataType": ["text"]},
        {"name": "price", "dataType": ["number"]},
        {"name": "link", "dataType": ["text"]},
        {"name": "rating", "dataType": ["text"]},
        {"name": "combined_text", "dataType": ["text"]},
    ]
}

client.schema.create_class(schema)
print("Product schema 建立完成")