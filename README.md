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
│           ├── views_http.py   # HTTP-эндпоинты (FastAPI)
│           ├── views_amqp.py   # AMQP-консьюмеры (FastStream)
│           ├── schemas.py      # Pydantic-схемы
│           └── utils.py        # вспомогательные функции
├── contracts/            # контракты/модели сообщений (AMQP)
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

---

## Архитектурные идеи

* **api/v1/** — контроллеры (HTTP/AMQP) принимают вход, валидируют, передают в сервисы.
* **services/** — бизнес-логика (CRUD, вычисления, правила).
* **contracts/** — Pydantic-модели для сериализации AMQP-сообщений.
* **core/** — база данных, модели, утилиты.

---
