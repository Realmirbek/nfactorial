from pathlib import Path
import re

# Путь до index.html (в твоём случае templates/index.html)
file_path = Path("templates/index.html")

if not file_path.exists():
    print("❌ Файл index.html не найден!")
    exit()

# Прочитать файл
content = file_path.read_text(encoding="utf-8")

# Заменить все внешние fetch-запросы на локальный маршрут
# Например: fetch("https://test.nfactorial.school/api/websiteForm" → fetch("/send-contact"
updated_content = re.sub(
    r'fetch\(["\']https://[^"\']+/api/websiteForm["\']',
    'fetch("/send-contact"',
    content
)

# Сохранить файл
file_path.write_text(updated_content, encoding="utf-8")
print("✅ Ссылка сервера успешно заменена на локальный маршрут /send-contact")



#4177490182956583