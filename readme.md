## Памятка

Создание миграции

    alembic revision --autogenerate -m "название миграции"

команда выполнит операции обновления, исходя из текущей версии базы данных , к заданной целевой редакции head тоесть последней

    alembic upgrade head

Если база данных пустая или еще какието приколы с бд незнаю что делает но иногда помогает

    alembic stamp head

Запускать бекенд так (команда повершелл)

    alembic upgrade head; uvicorn backend.main:app --host localhost

Запускать фронтенд так (команда повершелл)
    cd .\frontend\; npm run dev

чтоб запустить на пустой базе данных раскоментируй строчку в файле
backend/db/session.py
чтоб не писало что связей нет
это их создаст

`Base.metadata.create_all(engine)`

на следущие запуски закоментруй