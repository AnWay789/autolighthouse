from classic.scheduler import Scheduler
from src.lighthouse import Lighthouse
from src.config import Config
from src.loger import log_call, log_msg, LogLevel
import json, httpx, os, dotenv

def log_json(data: dict, filename: str = "logs.jsonl"):
    with open(filename, "a", encoding="utf-8") as f:
        f.write(json.dumps(data, ensure_ascii=False) + "\n")

@log_call
def start_lighthouse(metadata: dict, urls: list[str], header: dict):
    log_msg("Запускаем lighthouse...",LogLevel.INFO.value)
    lh = Lighthouse()

    results = []
    for url in urls:
        result = lh.run(url=url,
            metadata=metadata,
            header=header)
        
        results.append(result)
    
    post_in_ELK(results)

@log_call
def post_in_ELK(results: list):
    log_msg("Отправляем в елку логи...",LogLevel.INFO.value)
    dotenv.load_dotenv("creds.env")
    url = "https://10.222.0.3:9200/runner-vm-bots-logs/_doc/"
    for result in results:
        with httpx.Client(verify=False) as client:
            auth = ("fluent_bit_system", f"{os.getenv("ELK_AUTH")}")
            header = {"Content-Type" : "application/json"}
            data = result
            resp = client.post(url=url, headers=header, json=data, auth=auth)
            log_msg(f"Status: {resp.status_code}\n{resp.json()}", LogLevel.DEBUG.value)

@log_call
def get_lighthouse_stats():
    config = Config()
    configs = config.get_lighthouse_configs()
    for cfg in configs:
        start_lighthouse(metadata=cfg.metadata, 
                         urls=cfg.urls, 
                         header=cfg.headers if cfg.headers else {})


if __name__ == "__main__":
    scheduler = Scheduler()
    scheduler.by_cron('*/10 * * * *', get_lighthouse_stats)
    scheduler.run()
