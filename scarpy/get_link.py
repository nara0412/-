import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent
import time
import random
import openpyxl

def get_product_link(proxy_url, categories):
    # ======= Selenium 瀏覽器設定 =======
    ua = UserAgent()
    user_agent = ua.random

    options = Options()
    # options.add_argument("--headless")
    options.add_argument(f"user-agent={user_agent}")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--window-size=1920,1080")

    # 設定 proxy 代理
    options.add_argument(f'--proxy-server={proxy_url}')

    driver = webdriver.Chrome(options=options)

    # ======= 儲存所有商品連結 =======
    all_product_links = {}

    try:
        for category in categories:
            base_url = f"https://pcpartpicker.com/products/{category}/"
            print(f"正在爬取分類：{category}")
            driver.get(base_url)
            time.sleep(10)  # 等待 JS 資料加載完成

            product_links = []
            try:
                rows = driver.find_elements(By.CSS_SELECTOR, "#category_content tr")
                for row in rows:
                    try:
                        link = row.find_element(By.CSS_SELECTOR, 'td.td__name a').get_attribute('href')
                        if link:
                            product_links.append(link)
                    except:
                        continue
            except Exception as e:
                print(f"無法讀取分類 {category} 的表格：{e}")

            all_product_links[category] = product_links
            print(f"{category} 共取得 {len(product_links)} 筆連結\n")

            time.sleep(random.uniform(3, 6))  # 模擬人類行為，避免封鎖

    finally:
        driver.quit()

    # ======= 儲存成 Excel =======
    wb = openpyxl.Workbook()
    wb.remove(wb.active)  # 移除預設工作表

    for category, links in all_product_links.items():
        ws = wb.create_sheet(title=category[:31])  # Excel 工作表最多 31 字元
        ws.append(["商品連結"])
        for link in links:
            ws.append([link])

    filename = "pcpartpicker_links_all.xlsx"
    wb.save(filename)
    print(f"\n所有商品連結已儲存至 {filename}")

if __name__ == "__main__":
    # ScraperAPI Proxy Mode 設定
    api_key = "66edc8a76a69bb88bf657e76121eed25"
    proxy_url = f"http://proxy.scraperapi.com:8001?api_key={api_key}"

    # ======= 商品分類 =======
    categories = {
        'video-card', 'motherboard', 'thermal-paste', 'internal-hard-drive',
        'keyboard', 'cpu-cooler', 'external-hard-drive', 'case-fan', 'ups',
        'wireless-network-card', 'mouse', 'case', 'memory', 'monitor',
        'speakers', 'wired-network-card', 'power-supply', 'cpu', 'sound-card',
        'optical-drive', 'fan-controller', 'headphones'
    }

    get_product_link(proxy_url, categories)