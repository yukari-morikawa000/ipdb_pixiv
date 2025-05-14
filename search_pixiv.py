from playwright.sync_api import sync_playwright # type: ignore
import urllib.parse
import os
import csv
from ip_list2 import ip_list

# 全角半角を区別しない
def normalize(text):
    import unicodedata
    return unicodedata.normalize("NFKC", text.strip().lower())

def search_pixiv_dic(keyword):
    search_url = "https://dic.pixiv.net/search?query=" + urllib.parse.quote(keyword)
    results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(search_url)

        # 検索結果全ての<article>を対象とする
        articles = page.locator("article")
        count = articles.count()
        for i in range(count):
            title_el = articles.nth(i).locator("div.info h2 a")
            if title_el.count() == 0:
                continue

            title = title_el.inner_text().strip()
            href = title_el.get_attribute("href")
            if normalize(title) == normalize(keyword):
                full_url = urllib.parse.urljoin("https://dic.pixiv.net", href)
                results.append((title, full_url))

        browser.close()
    return results

if __name__ == "__main__":
    result_path = "results.tsv"
    complete_path = "completed.txt"

    # すでに完了しているキーワードを読み込み
    if os.path.exists(complete_path):
        with open(complete_path, "r", encoding="utf-8") as f:
            completed = set(line.strip() for line in f if line.strip())
    else:
        completed = set()

    # 出力ファイルを追記モードで開く
    with open(result_path, "a", encoding="utf-8", newline="") as result_file, \
         open(complete_path, "a", encoding="utf-8") as done_file:
        
        writer = csv.writer(result_file, delimiter="\t")

        # 初回時だけヘッダーを書く（TSVが空なら）
        if os.stat(result_path).st_size == 0:
            writer.writerow(["検索キーワード","ヒットタイトル","URL"])


        for word in ip_list:
            if word in completed:
                print(f"スキップ済み：{word}")
                continue

            print(f"検索: {word}")
            try:
                candidates = search_pixiv_dic(word)
                if candidates:
                    for title, link in candidates:
                        print(f" {title} → {link}")
                else:
                    print("該当なし")

            except Exception as e:
                print(f"エラー発生：{word}→{e}")
                writer.writerow([word + "ERROR", str(e)])

            # 完了マーク
            done_file.write(word + "\n")
            done_file.flush()