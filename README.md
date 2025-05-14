# ピクシブ百科事典 自動検索ツール

このツールは、[IPList スプレッドシート](https://docs.google.com/spreadsheets/d/10QMkXxRhAHhJINRNiXeY92AQCRAPWhB0ZvKnMunWGFQ/edit?gid=923863267#gid=923863267) の `middle_class_ip_name` 列に記載されたリストをもとに、[Pixiv辞書（https://dic.pixiv.net/）](https://dic.pixiv.net/) を自動検索し、**完全一致する記事のURLを取得**・保存します。  
Playwright によるブラウザ自動操作に対応しており、JavaScript描画にも対応しています。

---

## 🔧 処理の流れ

1. `ip_list2.py` に記載されたキーワード（例：「Ｇソニック」「KUN」など）を読み込みます。
2. 1つずつ ピクシブ百科事典で検索し、検索結果ページに表示される記事タイトルとURLを抽出します。
3. **完全一致するタイトル**が見つかった場合のみ、`results.tsv` に保存されます。←一致しなかった場合もリストに該当なしで追加する予定
4. 検索が終了したキーワードは `completed.txt` に記録され、**次回以降はスキップ**されます。
5. エラー時もエラー内容が `results.tsv` に記録され、再実行可能です。

---

## 📁 ファイル構成

| ファイル名 | 説明 |
|------------|------|
| `ip_list.py` | 検索対象のキーワードリスト（Pythonリスト形式） |
| `search_pixiv.py` | メインスクリプト。Playwrightで検索・取得・保存を行います |
| `results.tsv` | 検索結果の出力（TSV形式） |
| `completed.txt` | 検索済みキーワードの記録（1行1語） |
| `requirements.txt` | 必要なPythonライブラリ（`playwright` を含む） |
| `Dockerfile` | Playwright対応済みのDockerビルド定義ファイル |

---

## 🚀 使い方（ローカル）

### 1. 環境準備（Python 3.12+）

```bash
pip install -r requirements.txt
playwright install
```
### 2. 実行

```bash
python search_pixiv.py
```
#### Dockerからの実行
```bash
# イメージのビルド
docker build -t pixiv-scraper .

# 実行（マウントすることでTSVと完了リストも保存される）
docker run --rm -v $(pwd):/app pixiv-scraper
```

## 🗃️ 結果例

```tsv
検索キーワード	ヒットタイトル	URL
Ｇソニック	Gソニック	https://dic.pixiv.net/a/Gソニック
KUN	KUN	https://dic.pixiv.net/a/KUN

```
