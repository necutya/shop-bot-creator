# Shop Bot Creator
Инструкция по запуску:   
Лучше запускать на линуксе, так ккна виде будет отсутствовать 
возможность отправлять публикацию пользователям, но если это не тестить, 
то можно и на винде.  
В данной версии не работает большинство фукнционала.  
- В первую очередь нужно проверить наличие базы данных, а именно Postgres.
Создать базу данных shop_bot_creator_db. (также желательно установить Celery и Redis, если на Линуксе, для возможности тестить отправку публикаций в бот)
- Далее нужно создать виртуальное окружение Питона:
``python3 -m venv env`` и подключится к нему ``source env/bin/activate`` - для Линукса,
``env/Scripts/activate.bat`` - для Винды.
- Далее нужно установить зависимости прописав в корне проекта ``pip install -r requirements.txt`` - для Винды,
``pip3 install -r requirements.txt`` - для Линукса.
- Далее нужно создать `.env` файл и скопировать значения с `env.example` и подставить свои локальны параметры при необходимости.
- Далее создаем миграции `python manage.py makemigrations` и запускаем их `python manage.py migrate`
- Далее запускаем проект `python manage.py runserver localhost:8000` и всё работает. 
- Папку `old_code_for_use` не трагаем, в ней код с предыдущего проекта 
---
При работе под каждую фичу создавайте ветку локально, работайте в ней, потом пушьте локальную версию на удалённый репозиторий и просите мердж реквест, так мы будем уверены, что ничего не сломаем и не будет нестыковок в проекте.  
Все команды есть в интернете:)
---
Если что-то непонятно по запуску пишите в лс в телеграмме, но лучше гуглите :stuck_out_tongue_winking_eye: