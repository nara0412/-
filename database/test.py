import weaviate

client = weaviate.Client("http://localhost:8080")

# 測試class是否存在
if client.schema.exists("Product"):
    print("yes")