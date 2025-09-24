# MykhailApp

**MykhailApp** — backend-приложение для хранения и управления аудиторией телеграм-бота **MykhailBot**.

Репозиторий бота: [https://github.com/medin-misha/MykhailBot.git](https://github.com/medin-misha/MykhailBot.git)

---

## Краткое описание

Приложение хранит информацию о пользователях, их взаимодействиях и обеспечивает асинхронную интеграцию с ботом через брокер сообщений (RabbitMQ / FastStream). В проекте чётко разделены HTTP-представления и AMQP-потребители для обработки событий.

---

## Стек

* PostgreSQL
* FastAPI
* FastStream
* RabbitMQ
* Alembic
* python-dotenv
* Pydantic
* Uvicorn

---

## Структура проекта

```
app/
├── main.py               # точка входа в приложение
├── api/                  # API (HTTP и AMQP)
│   └── v1/               # версия API
│       └── users/        # модуль работы с пользователями
│           ├── views.py   # HTTP-эндпоинты (FastAPI)
│           ├── amqp_publishers.py  #AMQP-продюсерры (FastStream)
│           ├── amqp_consumers.py   # AMQP-консьюмеры (FastStream)
│           └── utils.py        # вспомогательные функции
├── contracts/            # контракты/модели сообщений (AMQP\HTTP)
├── core/                 # базовые модули приложения
│   ├── utils.py          # общие утилиты
│   ├── database.py       # подключение к БД и фабрика сессий
│   └── models/           # SQLAlchemy-модели (включая Base)
├── services/             # бизнес-логика приложения
│   ├── users.py          # логика CRUD для пользователей
│   └── stats.py          # логика для статистики
└── alembic/              # миграции alembic
.env                      # переменные окружения
```

---

## Установка и запуск (локально)
в app/ создай файл .env со следующим содержанием:
```.env
rabbit_url = "amqps://login:password@dog.lmq.cloudamqp.com/khllqnbg"
postgres_url = "postgresql+asyncpg://login:password@mykhail-postgres-medinskijmisa228-e66a.k.aivencloud.com:23233/defaultdb"
# важно: строка postgres_url должна быть ИМЕЕНО формата postgresql+asyncpg
```
---

## Архитектурные идеи

* **api/v1/** — контроллеры (HTTP/AMQP) принимают вход, валидируют, передают в сервисы.
* **services/** — бизнес-логика (CRUD, вычисления, правила).
* **contracts/** — Pydantic-модели для сериализации AMQP-сообщений.
* **core/** — база данных, модели, утилиты.

---
