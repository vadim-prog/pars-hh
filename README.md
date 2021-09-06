# Устанавливаем виртуальную среду:
pip3 install virtualenv

# Создаем каталог для проекта
mkdir Myproject

# Переходим в этот каталог
cd Myproject

# устанавливаем виртуальную среду
python3 -m venv <myenvname>

# Переносим скачанный проект в текущую директорию

# Устанавливаем зависимости для проекта
pip3 install -r requirements.txt

# Запускаем redis через Docker (при условии что Docker и Redis установлены)
docker run -d -p 6379:6379 redis

# Запускаем Celery:
celery -A pars_hh worker -l info

# Запускаем веб-сервер (используем встроенный тестовый сервер)
# В качестве БД используем по умолчанию db.sqlite3
python3 manage.py runserver 7000

# запуска приложения, заходим в браузере по адресу: 
http://127.0.0.1:7000
