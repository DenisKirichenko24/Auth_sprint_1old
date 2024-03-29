# Проектная работа 6 и 7  спринтов

# Сервис аутентификации и авторизации
https://github.com/DenisKirichenko24/Auth_sprint_1


## Добавлены в 7 спринте
- OAuth 2.0 c помощью Yandex и Google
- Трассировка - Jaeger
- Партицирование таблиц
- Ограничение количества запросов (rate limiter)
- JSON схема

## Основные сущности
- Пользователи — логин, email, пароль
- Роли — имя, описание.
- Роль-Пользователь — пользователь, роль.
- История входов — пользователь, время входа, id входа

## Основные компоненты системы
- PostgreSQL — Основная БД для хранения данных пользователя, ролей, входов 
- SQLAlchemy - используется как ORM.

## Используемые технологии
- Flask
- PostgreSQL
- Pytest
- SQLAlchemy

## Работа с проектом
### Запуск
1. Проект запускается командой
  ```python src/main.py runserver```
2. Эндпоинт /signup POST-запрос
  ```Регистрация пользователя с передачей в body "username", "email", "password"```
3. Эндпоинт /login POST-запрос. Также получение двух токенов (access и refresh)

  ```Вход в аккаунт с передачей в body "email", "password" ```
  
4. Эндпоинт /refresh POST-запрос. Сбрасывание рефреш-токена и выдача новой пары токенов.

  ```В headers запроса отправляем access-токен пользователя KEY: 'refresh-token', value: 'refresh token'```
  
5. Эндпоинт /change_password POST-запрос. Смена пароля для текущего пользователя

  ```В body передаем "email", "old_password", "new_password"```
  
  ```В headers access-токен пользователя```
  
  ```В headers запроса отправляем access-токен пользователя KEY: 'x-access-token', value: 'access token'```
  
6. Эндпоинт /change_data POST-запрос. Смена персональных данных (юзернейма и почты) для текущего пользователя

  ```Для смены почты - В body передаем "email", "old_mail", "new_mail"```
  
  ```Для смены юзернейма - В body передаем "email", "old_username", "new_username"```
  
  ```В headers запроса отправляем access-токен пользователя KEY: 'x-access-token', value: 'access token'```
  
 7. Эндпоинт /history GET-запрос. Получение все истории входов текущего пользователя
 
  ```В body запроса передаем "email" пользователя```
  
  ```В headers запроса отправляем access-токен пользователя KEY: 'x-access-token', value: 'access token'```
  
