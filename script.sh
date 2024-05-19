#!/bin/bash


python_script="test.py"

# Перевірка чи файл існує
if [ -f "$python_script" ]; then
    echo "Запускаю Python скрипт $python_script"
    python3 "$python_script" # Запускаємо Python скрипт
else
    echo "Помилка: файл $python_script не знайдено або не може бути запущений."
    exit 1
fi
