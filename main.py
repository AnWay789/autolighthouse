#from classic.scheduler import Scheduler
from src.lighthouse import Lighthouse
import json

import json
from datetime import datetime
from pathlib import Path


def log_json(data: dict, filename: str = "logs.jsonl"):
    with open(filename, "a", encoding="utf-8") as f:
        f.write(json.dumps(data, ensure_ascii=False) + "\n")

def start_lighthouse(urls: list[str]):
    lighthouse = Lighthouse()
    
    stats_without_header = []
    stats_with_header = []

    for url in urls:
        stats_without_header.append(lighthouse.run(url=url))

    for url in urls:
        stats_with_header.append(lighthouse.run(url=url, header=True))
    
    return stats_without_header, stats_with_header

def ELK(urls: list[str]):
    stats_without_header, stats_with_header = start_lighthouse(urls)
    
    # (наверное) ТУТ должна быть запись в ELK
    # ниже просто затычка которая сохраняет файлы с логами по папкам создавая json'ы
    for stat in stats_without_header:
        log_json(stat, "with_h.jsonl")

    for stat in stats_with_header:
        log_json(stat, "without_h.jsonl")

    # --- вывод    
    json_without_header = json.dumps(stats_without_header, ensure_ascii=False, indent=2)
    json_with_header = json.dumps(stats_with_header, ensure_ascii=False, indent=2)

    print(f"{json_without_header}\n\n\n{json_with_header}")

def get_lighthouse_stats():
    #sh = Scheduler()

    url_for_test = ["https://example.com"]

    urls: list[str] = [
        "https://polza.ru/",
        "https://polza.ru/catalog/lekarstvennye-sredstva/",
        "https://polza.ru/catalog/flebodia-600-tabletki-pokryt-plen-ob-600-mg-60-sht_13720/"
    ]

    ELK(url_for_test)


if __name__ == "__main__":
    get_lighthouse_stats()
