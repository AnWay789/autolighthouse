# Lighthouse Performance Monitor

Проект для автоматического мониторинга производительности веб-страниц с помощью Google Lighthouse. Позволяет запускать аудит производительности для множества URL с конфигурируемыми параметрами и метаданными.

## 🚀 Возможности

- **Массовый аудит** - запуск Lighthouse для множества URL из конфигурации
- **Гибкая конфигурация** - настройка через YAML-файл
- **Кастомные заголовки** - поддержка различных заголовков (Cookie, Authorization и др.)
- **Повторные попытки** - автоматические ретраи при ошибках
- **Структурированное логирование** - детальные логи выполнения
- **Метаданные** - обогащение результатов тестов дополнительной информацией

## 📦 Установка

### Предварительные требования

1. **Node.js** (для Lighthouse)
```bash
npm install -g lighthouse
```

2. **Python 3.8+**
```bash
python --version
```

3. **Установка зависимостей Python**
```bash
pip install .
```
```bash
# Poetry поддерживает указание файла конфигурации
poetry install --file poetry_pyproject.toml
```

### Зависимости Python

```python
# requirements.txt
pyyaml
tenacity
dataclasses  # для Python < 3.7
```

## ⚙️ Конфигурация

### Структура конфигурационного файла (`config.yaml`)

```yaml
configs:
  - metadata:
      project: "nuxt"
      page_type: "Главная"
    urls:
      - "https://polza.ru/"
    headers:
      Cookie: "ssr=1;nuxt=1"
  
  - metadata:
      project: "bitrix" 
      page_type: "Главная"
    urls:
      - "https://polza.ru/"
    headers:  # Опционально
```

### Параметры конфигурации

- **metadata** - метаданные для логирования:
  - `project` - название проекта
  - `page_type` - тип страницы
- **urls** - список URL для тестирования
- **headers** - заголовки HTTP (опционально)

## 🛠 Использование

### Базовый пример

```python
from src.config import Config
from src.lighthouse import Lighthouse

# Загрузка конфигурации
config = Config("config.yaml")

# Инициализация Lighthouse
lighthouse = Lighthouse()

# Запуск тестов для всех конфигураций
for lighthouse_config in config.get_lighthouse_configs():
    for url in lighthouse_config.urls:
        result = lighthouse.run(
            url=url,
            metadata=lighthouse_config.metadata,
            header=lighthouse_config.headers or {}
        )
        print(result)
```

### Результат выполнения

```json
{
  "@timestamp": "2025-01-15T10:30:45.123Z",
  "status": "success",
  "metadata": {
    "project": "nuxt",
    "page_type": "Главная"
  },
  "url": "https://polza.ru/",
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

## 📊 Метрики

Проект собирает следующие метрики производительности:

| Метрика | Описание | Единицы измерения |
|---------|-----------|-------------------|
| **FCP** | First Contentful Paint | мс и секунды |
| **TBT** | Total Blocking Time | мс и секунды |
| **SI** | Speed Index | мс и секунды |
| **LCP** | Largest Contentful Paint | мс и секунды |
| **CLS** | Cumulative Layout Shift | безразмерная |

## 🔧 Классы и методы

### `Config`

Класс для работы с конфигурацией проекта.

```python
config = Config("config.yaml")
configs = config.get_lighthouse_configs()  # List[LighthouseConfig]
```

### `Lighthouse`

Основной класс для запуска аудита производительности.

```python
lighthouse = Lighthouse()
result = lighthouse.run(
    url="https://example.com",
    metadata={"project": "test"},
    timeout_sec=240,
    header={"Cookie": "test=1"}
)
```

### `LighthouseConfig`

Dataclass для хранения конфигурации теста:

```python
@dataclass
class LighthouseConfig:
    metadata: Dict[str, str]    # Метаданные проекта
    urls: List[str]             # Список URL
    headers: Dict[str, str]     # HTTP-заголовки
```

## 🐛 Обработка ошибок

Проект включает комплексную обработку ошибок:

- **Таймауты** - автоматические повторные попытки
- **Ошибки Lighthouse** - детальное логирование
- **Проблемы с JSON** - валидация выходных данных
- **Отсутствие бинарника** - понятные сообщения об ошибках

## 📝 Логирование

Используется структурированное логирование с декораторами:

- `@log_call` - логирование вызовов методов
- `@log_msg` - пользовательские сообщения
- Уровни логирования: `DEBUG`, `INFO`, `WARNING`, `ERROR`

## 🔄 Параметры повторных попыток

- **Максимум попыток**: 3
- **Интервал**: 2 секунды
- **Ретраи для**: таймауты, ошибки процесса, проблемы с JSON

## 🚨 Возможные проблемы и решения

### "No usable sandbox!"
Добавьте в `base_cmd`:
```python
"--chrome-flags=--headless --disable-cache --no-sandbox"
```

### Отсутствие GPU
```python
"--chrome-flags=--headless --disable-cache --disable-gpu"
```

### Большой размер вывода
Проект использует `--only-audits` для ограничения вывода только необходимыми метриками.
