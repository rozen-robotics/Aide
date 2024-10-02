# Используем официальный образ Python
FROM python:3.9-slim

# Создаем рабочую директорию
WORKDIR /app

# Копируем файлы зависимостей и устанавливаем их
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальные файлы проекта
COPY . /app/


# Создаем скрипт для запуска всех программ
RUN echo '#!/bin/bash\n\
python chat.py &\n\
python controls.py &\n\
python coffe.py &\n\
tail -f /dev/null' > start.sh

# Делаем скрипт исполняемым
RUN chmod +x start.sh

# Запускаем скрипт при старте контейнера
CMD ["./start.sh"]