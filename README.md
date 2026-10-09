# HSE Document Finder

REST-приложение на FastAPI для хранения и поиска документов учебного офиса НИУ ВШЭ. Проект демонстрирует разработку API: Pydantic-модели, слоистая архитектура, логирование, тесты и настройка через переменные окружения.

Приложение предназначено для:
- учебных целей — как пример построения REST API на FastAPI;
- быстрого прототипирования внутренних сервисов документооборота.

## Установка

### 1. Клонирование репозитория

```bash
git clone https://github.com/lou-amphibi/hse_infr_document_finder.git
cd hse_infr_document_finder
```

### 2. Создание виртуального окружения

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux / macOS:**
```bash
python -m venv venv
source venv/bin/activate
```

### 3. Установка зависимостей

Для запуска приложения:
```bash
pip install -r requirements.txt
```

Для разработки (включая тесты):
```bash
pip install -r requirements-dev.txt
```

## Запуск приложения

```bash
uvicorn main:app --reload
```

После запуска откройте:

- **Swagger UI** — http://127.0.0.1:8000/docs
- **ReDoc** — http://127.0.0.1:8000/redoc

На странице `/docs` можно в интерактивном режиме вызывать все эндпоинты и смотреть схемы запросов и ответов.

### Запуск без `--reload` (обычный режим)

Флаг `--reload` предназначен только для разработки: uvicorn следит за изменениями файлов и перезапускает приложение. В обычной работе (демонстрация, сервер) используйте команду без него:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

Такой режим:
- не тратит ресурсы на отслеживание файлов;
- стабильнее — процесс не перезапускается в неожиданный момент;
- в проде обычно запускается с несколькими воркерами: `--workers 4`.

Остановить сервер — `Ctrl+C` в терминале.

## Запуск тестов

```bash
pytest
```

Для подробного вывода:
```bash
pytest -v
```

Для запуска конкретного файла или теста:
```bash
pytest tests/test_documents.py
pytest tests/test_documents.py::test_create_document
```

## Переменные окружения

Приложение читает настройки из переменных окружения. Если переменная не задана — используется значение по умолчанию.

| Переменная | По умолчанию | Описание |
|---|---|---|
| `APP_NAME` | `HSE Document Finder` | Название приложения — в Swagger UI и логах |
| `APP_VERSION` | `1.0.2` | Версия приложения — в `/version` и в Swagger UI |
| `LOG_LEVEL` | `INFO` | Уровень логирования: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL` |

### Как задать переменные

**В PyCharm (Run Configuration):**

1. `Edit Configurations` → выберите конфигурацию запуска.
2. Поле `Environment variables` — добавьте, например:
   ```
   APP_NAME=HSE Document Finder;APP_VERSION=1.0.2;LOG_LEVEL=DEBUG
   ```
   На Windows разделитель — `;`, на Linux / macOS — `:`.

**В терминале:**

Windows PowerShell:
```powershell
$env:LOG_LEVEL="DEBUG"; uvicorn main:app --reload
```

Linux / macOS:
```bash
LOG_LEVEL=DEBUG uvicorn main:app --reload
```

### Пример: подробное логирование

```bash
LOG_LEVEL=DEBUG uvicorn main:app --reload
```

В этом режиме в консоль попадают DEBUG-сообщения из сервисного слоя — полезно при отладке.

## Проверка работы

### `/health`

Эндпоинт для проверки, что приложение живо:

```bash
curl http://127.0.0.1:8000/health
```

Ответ:
```json
{"status": "ok"}
```

### `/version`

Возвращает текущую версию приложения (значение переменной `APP_VERSION`):

```bash
curl http://127.0.0.1:8000/version
```

Ответ:
```json
{"version": "1.0.2"}
```

### Логи

Все логи пишутся в **stdout** — в терминал, из которого запущен `uvicorn`, или в панель `Run` в PyCharm.

При старте приложения в логах видно:
- название и версию приложения;
- количество загруженных документов;
- текущие значения настроек из переменных окружения;
- ссылку на Swagger UI.

При каждом запросе логируется:
- входящий HTTP-метод и путь;
- что сделал сервисный слой (нашёл, создал, удалил, не нашёл);
- какой статус-код отдан клиенту.

Формат строки:

```
2026-10-10 12:30:15 | INFO     | hse_doc | GET /documents/7 — found 'Устав НИУ ВШЭ'
```

## Эндпоинты

| Метод | Путь | Описание | Успешный статус |
|---|---|---|---|
| GET | `/documents` | Список документов с фильтрами `doc_type` и `year` | 200 |
| POST | `/documents` | Создать новый документ | 201 |
| POST | `/documents/search` | Найти документ по полному совпадению | 200 |
| GET | `/documents/{document_id}` | Получить документ по ID | 200 |
| DELETE | `/documents/{document_id}` | Удалить документ по ID | 204 |
| GET | `/health` | Проверка работоспособности | 200 |
| GET | `/version` | Версия приложения | 200 |

### Примеры запросов

Список всех документов:
```bash
curl http://127.0.0.1:8000/documents
```

Фильтр по типу:
```bash
curl "http://127.0.0.1:8000/documents?doc_type=учебный"
```

Создать документ:
```bash
curl -X POST http://127.0.0.1:8000/documents \
  -H "Content-Type: application/json" \
  -d '{"title": "Тестовый документ", "author": "Иван Иванов", "year": 2024, "type": "учебный"}'
```

Поиск документа:
```bash
curl -X POST http://127.0.0.1:8000/documents/search \
  -H "Content-Type: application/json" \
  -d '{"title": "Устав НИУ ВШЭ", "author": "Учёный совет", "year": 2019, "type": "нормативный"}'
```

Удалить документ:
```bash
curl -X DELETE http://127.0.0.1:8000/documents/7
```

## Хранение данных

Документы хранятся **в памяти процесса** в словаре `DOCUMENTS` (`core/doc_const.py`). Это означает:

- при перезапуске сервера все изменения (созданные и удалённые документы) сбрасываются к исходному набору;
- одновременная работа нескольких воркеров приведёт к рассинхронизации данных.

## Диагностика проблем

### `ModuleNotFoundError: No module named 'fastapi'`

Не активировано виртуальное окружение или не установлены зависимости.

```bash
venv\Scripts\activate          # Windows
source venv/bin/activate       # Linux / macOS
pip install -r requirements.txt
```

### `Address already in use` — порт 8000 занят

Остановите старый сервер (`Ctrl+C`) или запустите на другом порту:

```bash
uvicorn main:app --reload --port 8001
```

### DEBUG-логи не появляются

Переменная `LOG_LEVEL=DEBUG` не подхватилась. При старте в логах есть строка `Log level: <значение>` — если там `INFO`, переменная не задана.

Задайте её одним из способов:

```powershell
$env:LOG_LEVEL="DEBUG"; uvicorn main:app --reload    # Windows PowerShell
```
```bash
LOG_LEVEL=DEBUG uvicorn main:app --reload            # Linux / macOS
```

Либо в PyCharm: `Edit Configurations` → `Environment variables` → `LOG_LEVEL=DEBUG`.

### `Cannot connect to host 127.0.0.1:8000`

Сервер не запущен. Запустите в отдельном терминале:

```bash
uvicorn main:app --reload
```

Дождитесь строки `Application startup complete.` в логах, прежде чем отправлять запросы.

### Где искать больше информации

- **Swagger UI** — http://127.0.0.1:8000/docs — интерактивная документация
- **Логи приложения** — в терминале с запущенным `uvicorn` или в панели `Run` в PyCharm
- **Логи CI** — на GitHub во вкладке **Actions** → выберите запуск
- **Артефакт сборки** — на GitHub в **Actions** → запуск → блок **Artifacts** внизу страницы
