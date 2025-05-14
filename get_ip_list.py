# tsvインポート版（のちにスプシから読み取れるようにする）
import csv

def extract_unique_names_from_tsv(tsv_file, column_name="middle_class_ip_name"):
    unique_names = set()
    with open(tsv_file, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            value = row.get(column_name,"").strip()
            if value:
                unique_names.add(value)
    return list(unique_names)

def save_to_python_file(data_list,output_file="ip_list.py"):
    with open(output_file,"w",encoding="utf-8") as f:
        f.write("# 自動生成されたIPリスト\n")
        f.write("ip_list=[\n")
        for name in sorted(data_list):  # 並び順を一定にしたい場合は sorted()
            f.write(f"    '{name}',\n")
        f.write("]\n")

if __name__=="__main__":
    names = extract_unique_names_from_tsv("middle_class_ip_name.tsv")
    save_to_python_file(names)
    print("middle_class_ip_name.tsvを作りました")
            

