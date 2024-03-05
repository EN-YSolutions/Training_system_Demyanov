# Модуль администратора для Образовательного портала


## Отчёты
Находятся в ветке [docs](https://github.com/EN-YSolutions/Training_system_Demyanov/tree/docs)


## Инструкция по запуску на Linux
1. Установить Python (предустановлен в большинстве дистрибутивов)
2. Установить [Docker и Docker Compose](https://docs.docker.com/engine/install/)
3. Задать параметры в файле `.env`:

   - `LISTEN_ADDR`, `LISTEN_PORT` — Адрес и порт, на котором будет запущен сервер
   - `TLS_CERT`, `TLS_KEY` — Путь до TLS-сертификата и соответствующего ему ключа. Можно использовать [EasyRSA](https://github.com/OpenVPN/easy-rsa) или OpenSSL для их генерации
   - `PG_HOST`, `PG_PORT` — Адрес и порт, по которому доступна СУБД PostgreSQL
   - `PG_USER`, `PG_PASSWD` — Имя пользователя и пароль для доступа к СУБД PostgreSQL
   - `PG_DB` — Название базы данных, использумой сервером
   - `JWT_SECRET` — Секрет для подписания JWT-токенов сервером

4. Создание виртуального окружения (venv) и его активация

   ```sh
   $ python -m venv .venv
   $ source .venv/bin/activate
   ```

5. Установка зависимостей в виртуальное окружение

   ```sh
   $ pip install -r requirements.txt
   ```

6. Запуск СУБД PostgreSQL

   Если значение переменной окружения `PG_DB` в файле `.env` было изменено, то необходимо это же значение устнановить переменной `POSTGRES_DB` в файле `compose.yaml` (строка #11)

   ```sh
   $ docker compose up -d
   ```

7. Запуск сервера

   ```sh
   $ python .
   ```
