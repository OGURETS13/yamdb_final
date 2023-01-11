## Описание 

Это api который позволяет пользователям создавать и просматривать посты, комментарии к ним, а также подписываться на других пользователей 


## Как запустить проект: 

Клонировать репозиторий и перейти в него в командной строке: 

``` 
git clone https://github.com/OGURETS13/api_yamdb.git
``` 


Cоздать и активировать виртуальное окружение: 

``` 

python3 -m venv env 

``` 

 

``` 

source env/bin/activate 

``` 

 

Установить зависимости из файла requirements.txt: 

 

``` 

python3 -m pip install --upgrade pip 

``` 

 

``` 

pip install -r requirements.txt 

``` 

 

Выполнить миграции: 

 

``` 

python3 manage.py migrate 

``` 

 

Запустить проект: 

 

``` 

python3 manage.py runserver 

``` 

## Пользователи

### Алгоритм регистрации пользователей
Пользователь отправляет POST-запрос на добавление нового пользователя с параметрами email и username на эндпоинт /api/v1/auth/signup/.
YaMDB отправляет письмо с кодом подтверждения (confirmation_code) на адрес email.
Пользователь отправляет POST-запрос с параметрами username и confirmation_code на эндпоинт /api/v1/auth/token/, в ответе на запрос ему приходит token (JWT-токен).
При желании пользователь отправляет PATCH-запрос на эндпоинт /api/v1/users/me/ и заполняет поля в своём профайле (описание полей — в документации).

### Пользовательские роли
- Аноним — может просматривать описания произведений, читать отзывы и комментарии.
- Аутентифицированный пользователь (user) — может, как и Аноним, читать всё, дополнительно он может публиковать отзывы и ставить оценку произведениям (фильмам/книгам/песенкам), может комментировать чужие отзывы; может редактировать и удалять свои отзывы и комментарии. Эта роль присваивается по умолчанию каждому новому пользователю.
- Модератор (moderator) — те же права, что и у Аутентифицированного пользователя плюс право удалять любые отзывы и комментарии.
- Администратор (admin) — полные права на управление всем контентом проекта. Может создавать и удалять произведения, категории и жанры. Может назначать роли пользователям.
- Суперюзер Django — обладет правами администратора (admin)
 



## Эндпоинты и запросы
```
/api/v1/auth/signup/
/api/v1/auth/token/
/api/v1/categories/
/api/v1/genres/
/api/v1/titles/
/api/v1/titles/{title_id}/reviews/
/api/v1/titles/{title_id}/reviews/{review_id}/comments/
/api/v1/users/
```



### Пример `get` запроса 

`/api/v1/titles/{title_id}/reviews/` 

Пример ответа

```
[
  {
  "count": 2,
  "next": "string",
  "previous": "string",
  "results": [
      {
      "id": 1,
      "text": "string",
      "author": "string",
      "score": 1,
      "pub_date": "2019-08-24T14:15:22Z"
      },
      {
      "id": 2,
      "text": "string",
      "author": "string",
      "score": 1,
      "pub_date": "2019-08-24T14:15:22Z"
      }
    ]
  }
]
```


### Пример `post` запроса 

`/api/v1/titles/{title_id}/reviews/{review_id}/comments/` 

Тело запроса
```
{
  "text": "string"
}
```

Пример ответа

```
{
  "id": 1,
  "text": "string",
  "author": "string",
  "pub_date": "2019-08-24T14:15:22Z"
}
```

### Пример `patch` запроса

`/api/v1/users/{username}/` 

Тело запроса
```
{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string",
  "role": "user"
}
```

Пример ответа

```
{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string",
  "role": "user"
}
```

 
