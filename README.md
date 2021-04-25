# quizAPI
### API для проведения и администрирования опросов
## Развёртывание проекта на тестовом сервере
Активируйте виртуальное окружение и установите необходимые пакеты из requirements.txt
```
pip install -r requirements.txt
```
Создайте миграции для БД и учётку администратора
```
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```
Запустите тестовый сервер
```
python manage.py runserver
```
