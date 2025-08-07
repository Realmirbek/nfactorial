import os
import re

# Папка, где лежат твои HTML-файлы (замени при необходимости)
TARGET_DIR = "templates"

OLD_EMAIL = "mamytalievmirbek2008@gmail.com"
NEW_EMAIL = "profidata.tech@gmail.com"

def replace_email_in_file(filepath):
    with open(filepath, "r", encoding="utf-8") as file:
        content = file.read()

    # Заменяем email
    new_content = content.replace(OLD_EMAIL, NEW_EMAIL)

    if content != new_content:
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(new_content)
        print(f"✅ Заменено в: {filepath}")
    else:
        print(f"⚠️ Ничего не найдено в: {filepath}")

# Проход по всем HTML-файлам в папке рекурсивно
for root, _, files in os.walk(TARGET_DIR):
    for name in files:
        if name.endswith(".html"):
            replace_email_in_file(os.path.join(root, name))
