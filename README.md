# Менеджер задач
[![Actions Status](https://github.com/3FANG/python-django-developer-project-52/actions/workflows/task-manager-check.yml/badge.svg)](https://github.com/3FANG/python-django-developer-project-52/actions)[![Maintainability](https://api.codeclimate.com/v1/badges/476a969f4e489a4446bd/maintainability)](https://codeclimate.com/github/3FANG/python-django-developer-project-52/maintainability)[![Test Coverage](https://api.codeclimate.com/v1/badges/476a969f4e489a4446bd/test_coverage)](https://codeclimate.com/github/3FANG/python-django-developer-project-52/test_coverage)

https://task-manager-poject.onrender.com _(стоит перейти на Railway)_

## Зависимости
Python ^3.10  
Poetry ^1.4  
PostgreSQL ^16

## Установка
1. Склонировать репозиторий:
 ```bash
 git clone https://github.com/3FANG/python-django-developer-project-52.git
 ```
2. В корень проекта добавить файл ```.env``` Список переменных - ```.env_EXAMPLE```

3. В директории проекта выполнить:
 ```bash
 make build 
```
## Запуск приложения
Используйте ```make start``` для запуска приложения. После запуска оно будет доступно по адресу http://127.0.0.1:8000

## Демонстрация проекта

- ### Главная странца

![homepage](https://github.com/3FANG/python-django-developer-project-52/assets/111867964/1f38599c-a593-4383-8ec0-739de9a5a561)

> Для использования приглашения вам необходимо зарегистрироваться. Для этого нажмите на кнопку **Регистрация**. Также вы можете изменить тему сайта, используя кнопку в правом нижнем углу.

- ### Регистрация

![registration](https://github.com/3FANG/python-django-developer-project-52/assets/111867964/a0e8f6c6-b528-4445-bc9b-1c8c9393a4db)

> Для регистрации заполните все поля формы, затем нажмите кнопку **Зарегистрировать**. После этого вы будете перенаправлены на страницу авторизации, где вы должны вести имя и пароль раннее зарегистрированного пользователя.

- ### Вход

![login](https://github.com/3FANG/python-django-developer-project-52/assets/111867964/b5aae5c6-264f-4b50-8535-83db6b09026a)

> Если у вас уже есть зарегистрированный аккаунт, нажмите на кнопку **Вход** и введите свои авторизационные данные.

- ### Пользователи

![users](https://github.com/3FANG/python-django-developer-project-52/assets/111867964/0ecad08b-f6dc-46e4-a98d-bfbfe16175be)

> На странице со всеми пользователями вы можете редактировать данные своего аккаунты, либо вовсе удалить его. Изменения или удалять аккаунт другого пользователя нельзя.

- ### Статусы

![statuses](https://github.com/3FANG/python-django-developer-project-52/assets/111867964/0691b374-f63b-445e-bdd7-edc3e75dcc63)

> Страница со всеми статусами. С их помощью можно понять, что происходит с задачей, сделана она или нет. Их также можно создавать, редактировать и удалять.

- ### Метки

![labels](https://github.com/3FANG/python-django-developer-project-52/assets/111867964/75b059ef-5ccc-44ef-9b93-4b07254cc08d)

> Метки — гибкая альтернатива категориям. Они позволяют группировать задачи по разным признакам: например, багам или фичам.

- ### Задачи

![tasks](https://github.com/3FANG/python-django-developer-project-52/assets/111867964/d0f6a8f6-1327-4703-8c58-c744f961dfaf)

> Страница со всеми задачами. Их можно фильтровать по статусу, исполнителю или меткам. Можно выводить список только своих задач. Конкретную задачу можно просмотреть, нажава на ее название. Также их можно редактировать, менять исполнителя или добавлять несколько меток.

