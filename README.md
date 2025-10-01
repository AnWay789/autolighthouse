(README писал GPT)

# 📊 Lighthouse Python Wrapper

Модуль для запуска [Google Lighthouse](https://github.com/GoogleChrome/lighthouse) из Python и получения только ключевых метрик в **чистом JSON** формате.

---

## ⚙️ Требования

1. **Node.js**

Lighthouse — это Node.js тулза, поэтому нужен Node.


Установка (Ubuntu/Debian):
```bash
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs
```
  

Проверка:
```bash
node -v # v20.x
npm -v # 10.x
```


2. Lighthouse (npm пакет)

Устанавливаем глобально:
```bash
sudo npm install -g lighthouse
```

  

Проверка:
```bash
lighthouse --version
```

### Должно вывести версию, например 12.2.0

  

⚠️ На серверах без GUI Chrome может требовать флаги --no-sandbox и --disable-gpu.

3. Python 3.11+

Минимальная версия — 3.11 (используем | в typing).

4. Python-зависимости

```bash
pip install 
```

```bash
poetry install 
```

⸻

Пример успешного ответа:
```json
{	
	"status": "success",
	
	"url": "https://example.com",
	
	"metrics": {
	
	"fcp_ms": 1234.56,
	
	"fcp_s": 1.23,
	
	"tbt_ms": 50.12,
	
	"tbt_s": 0.05,
	
	"si_ms": 1800.01,
	
	"si_s": 1.8,
	
	"lcp_ms": 2345.67,
	
	"lcp_s": 2.35,
	
	"cls": 0.05
},	
	"error": null,
	
	"message": null	
}
```


Пример ошибки:

```json
{
	"status": "error",
	
	"url": "https://example.com",
	
	"metrics": null,
	
	"error": "Lighthouse failed",
	
	"message": "stderr: ... | stdout: ..."	
}

```

⸻

  

🛠 Полезные флаги Chrome

• --no-sandbox → если падает с ошибкой “No usable sandbox!” (CI/докер).

• --disable-gpu → если нет GPU (часто на серверах).

• --disable-cache → отключает кеш.

• --headless → запускает Chrome без GUI.

  

Пример:

```bash
lighthouse https://example.com \
--chrome-flags="--headless --no-sandbox --disable-gpu --disable-cache"
```

⸻
