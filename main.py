#from classic.scheduler import Scheduler
from src.lighthouse import Lighthouse
import json

import json
from datetime import datetime
from pathlib import Path


def save_json(data: dict, folder: str = "logs", prefix: str = "lighthouse") -> Path:
    """
    Сохраняет словарь в JSON-файл с датой и временем в названии.
    
    Args:
        :param data: dict - данные для сохранения
        :param folder: str - папка для логов
        :param prefix: str - префикс в имени файла
    Returns:    
        :return: Path - путь к сохранённому файлу
    """
    # Папка для логов (создаст если нет)
    path = Path(folder)
    path.mkdir(parents=True, exist_ok=True)

    # Имя файла: prefix_2025-10-01_12-30-45.json
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{prefix}_{timestamp}.json"
    file_path = path / filename

    # Запись в файл
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return file_path

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
        save_json(stat, folder='logs/with_header')

    for stat in stats_with_header:
        save_json(stat, folder='logs/without_headers')

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
