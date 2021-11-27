###Локальная установка:

1. команда терминала: git clone или загрузить zip файл и расспокавать
2. отркрыть заргуженную папку или архив
3. создать вертуальное окружение: python3 -m venv venv
4. активировать виртуальное окружение source venv/bin/activate
5. ввести команду: "pip3 -r install requirements.txt" для установки зависимости
6. изменить подключение к mysql базе данных в файле ./drfapi/settings.py в блоке
`DATABASES = {
   'default': {
   'ENGINE': 'django.db.backends.mysql',
   'NAME': 'drf-test-task',
   'USER': '<db_user_name>',
   'PASSWORD': '<db_user_password>',
   'OPTIONS': {
   'charset': 'utf8mb4',
   'use_unicode': True,
   },
   }
   }`
где '<db_user_name>' логин пользователя базы данных,
где '<db_user_password>' пароль пользователя базы данных
7. создать миграцию: python manage.py makemigrations
8. применить миграции: python manage.py migrate
9. создать супер пользователя (admin): python manage.py createsuperuser
10. запустить сервер: python manage.py runserver
11. open postman collection file: Drf test task.postman_collection.json

###Инструция по postman:

1. post: admin/login' - вход пользователя
2. get: admin/logout' - выход пользователя
3. post: admin/vote-quest/save/<id>|none - сохранить вопрос опроса по id если id не передан будет создан новый опрос, для создание нужно передать: vote_id, quest, quest_type
где vote_id это id опроса, где quest текст вопроса, где quest_type тип вопроса text или select или multiselect где text это отвер текстом, где select это ответ выбором одного ответа, где multiselect выбор несколько ответов
4. post: admin/vote/delete/<id> - удаление опроса по id
5. post: admin/vote-quest/delete/<id> - удаление ворос опроса по id
6. post: admin/vote/save/<id>|none - сохранение опроса с данными: start_date, end_date, name, description формат даты: YYYY-MM-dd H:m:i если не передать id будет создан новый
7. get: user/vote/list - список актуальных опросов

8. get: user/vote/answer/<vote_id>/<user_id> - сохранение ответа пользователя по user_id и vote_id если user_id если не передан user_id то будут сохранет как анонимных ответ который будет иметь id равному 0
9. get: user/vote/statistic/<user_id> - статистика ответов по user_id

для создание, изменение, удаление опроса и вопроса опроса нужно прередать в headers данные
"Authorization" со значением "Token 'токен полученных в ответе входа'" премер значение: Token 2ea9f5e8f036f85c09e0e23f1b7c379d900ac6e9
