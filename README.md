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
## Типы данных
- Quiz

     Поле | Тип | Опционально    
     --- | --- | ---   
     title | String | Нет
     desc | String | Да
     start_date | Date | Нет
     end_date | Date | Нет
     
- Question

     Поле | Тип | Опционально    
     --- | --- | ---   
     type | Choices* | Нет
     text | String | Нет
     offered_answers | List of OfferedAnswer | Да
     
     *type choices:
     - 'T' - Text Answer  
     - 'C' - One Choice
     - 'M' - Multiply Choice
- OfferedAnswer
    Поле | Тип | Опционально    
     --- | --- | ---   
     offered_answer | String | Нет
 
- Reply
    Поле | Тип | Опционально    
     --- | --- | ---   
     answers | List of Answer | Нет
     
- Answer
    Поле | Тип | Опционально    
     --- | --- | ---   
     question_id | Int | Нет
     answer | String | Нет
     
- User
    Поле | Тип | Опционально    
     --- | --- | ---   
     name | String | Да
     
## Конечные точки и методы
- `/api/quizzes/`
  - `GET`  
    - Описание: Получение списка опросов  
    - Авторизация: Basic authentication
    - Параметры: Отсутсвуют  
  - `POST`  
    - Описание: Создание опроса  
    - Авторизация: Basic authentication
    - Параметры: 
   
     BODY:  
       > Quiz
     
- `/api/quizzes/{id}/`
  - `GET`  
    - Описание: Получение опроса 
    - Авторизация: Basic authentication
    - Параметры: 

     PATH:
      >Quiz ID
  - `PUT`  
    - Описание: Изменение опроса
    - Авторизация: Basic authentication
    - Параметры:  
    
     PATH:
     >Quiz ID 
 
       BODY:   
     >Quiz     
   - `DELETE`  
     - Описание: Удаление опроса 
     - Авторизация: Basic authentication
     - Параметры:
      
     PATH:
     >Quiz ID 
- `/api/quizzes/{id}/questions/`
  - `GET`  
    - Описание: Получение списка вопрсов опроса 
    - Авторизация: Basic authentication
    - Параметры:
    
     PATH:
     >Quiz ID 
  - `POST`  
    - Описание: Создание вопрсов опроса  
    - Авторизация: Basic authentication
    - Параметры:
    
    PATH:
     >Quiz ID 
   
     BODY:  
     > List of Question
- `/api/quizzes/{id}/questions/{q_id}/`
  - `PUT`  
    - Описание: Измение вопроса в опросе 
    - Авторизация: Basic authentication
    - Параметры:
    
     PATH:
     >Quiz ID  
     >Question ID
     
     BODY:  
     >Question
  - `DELETE`  
    - Описание: Создание вопрсов опроса  
    - Авторизация: Basic authentication
    - Параметры:
    
    PATH:
     >Quiz ID   
     >Question ID
   
     BODY:  
     > List of Question
- `/api/quizzes/active/`
  - `GET`  
    - Описание: Получение списка активный опросов на текущую дату
    - Авторизация: AllowAny
    - Параметры: Отсутсвуют
- `/api/quizzes/active/{id}/questions/`
  - `GET`  
    - Описание: Получение  активного опроса на текущую дату
    - Авторизация: AllowAny
    - Параметры: 
    
    PATH:
     >Quiz ID
- `/api/quizzes/active/{id}/reply/{u_id}/`
  - `POST`  
    - Описание: Отправка ответа на опрос
    - Авторизация: AllowAny
    - Параметры: 
    
    PATH:
     >Quiz ID
     >User ID
    
     BODY:  
     >Reply
- `/api/quizzes/user/{id}/replys/`
  - `GET`  
    - Описание: Получение  списка ответов на опросы
    - Авторизация: AllowAny
    - Параметры: 
    
    PATH:
     >User ID
- `/api/newuser/`
  - `POST`  
    - Описание: Создание пользователя
    - Авторизация: AllowAny
    - Параметры: 
      
     BODY:  
     >User
