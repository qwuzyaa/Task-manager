Описание таблиц БД.
В проекте используются две таблицы:
  users - информация о пользователе,
  tasks - информация о задаче. 

Таблица USERS
Состоит из столбцов: id (INTEGER PRIMARY KEY) - уникальный идентификатор пользователя, username (VARCHAR NOT NULL) - им пользователя при регистрации, password (VARCHAR NOT NULL) - пароль для регистрации и дальнейшего входа, created_time (DATETIME DEFAULT CURRENT_TIMESTAMP) - время регистрации. 

Таблица TASKS
Состоит из столбцов user_id (INTEGER PRIMARY KEY) - уникальный идентификатор пользователя, id (INTEGER PRIMARY KEY) - уникальный идентификатор задачи, name - (VARCHAR NOT NULL) - название задачи, description (VARCHAR) - описание задачи, может быть пустым, created_time (DATETIME DEFAULT CURRENT_TIMESTAMP) - время создания задачи, time_limit (DATETIME) - ограничение времени выполнения задачи, status - (BOOLEAN DEFAULT 0) - статус выполнения. 

Связь между таблицами осуществляется через столец id в таблице users и столбец user_id в таблице tasks. Таким обрахом пользователь види только свои задачи и никакие другие. 
