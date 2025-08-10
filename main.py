from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import smtplib
from email.mime.text import MIMEText
import logging

app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Статические файлы и шаблоны
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_FROM = "profidata.tech@gmail.com"
EMAIL_TO = "profidata.tech@gmail.com"
EMAIL_PASSWORD = "yhbb ipdm shsh ynbx"  # пароль приложения

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/static/{file_path:path}")
async def debug_static(file_path: str):
    print(f"Запрошен файл: {file_path}")  # Увидишь какие файлы ищет фронтенд
    return FileResponse(f"static/{file_path}")


import os
from pathlib import Path


def fix_static_files():
    static_dir = Path("static")

    # Создаем словарь для соответствия базовых имен (без хэшей)
    name_mapping = {
        "chunk-4FZPUS4R": "chunk-",
        "p7r50UIhH99jKK4nNgJ4kde4pGs5G": "p7r50UIhH",
        "script_main": "script_main"
    }

    for file in static_dir.glob("*.*"):
        # Ищем файлы по частичному соответствию
        for pattern, new_prefix in name_mapping.items():
            if pattern in file.name:
                new_name = file.name.replace(file.name.split(".")[0],
                                             new_prefix + file.name.split(".")[0][len(new_prefix):])
                file.rename(static_dir / new_name)
                break


fix_static_files()




@app.post("/send-contact")
async def send_contact(
    name: str = Form(...),
    phone: str = Form(...),
    message: str = Form(""),
    utm_source: str = Form(""),
    utm_medium: str = Form(""),
    utm_campaign: str = Form(""),
    utm_term: str = Form(""),
    utm_content: str = Form("")
):
    try:
        logger.info(f"Получена заявка: {name}, {phone}")

        # Проверка телефона
        if not phone.startswith("+7") or len(phone) != 12 or not phone[2:].isdigit():
            return RedirectResponse(url="/?error=Неверный формат номера", status_code=303)

        email_body = f"""
Новая заявка:

Имя: {name}
Телефон: {phone}
Сообщение: {message or '—'}

UTM-метки:
utm_source: {utm_source}
utm_medium: {utm_medium}
utm_campaign: {utm_campaign}
utm_term: {utm_term}
utm_content: {utm_content}
"""

        msg = MIMEText(email_body)
        msg["Subject"] = f"Заявка от {name}"
        msg["From"] = EMAIL_FROM
        msg["To"] = EMAIL_TO

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_FROM, EMAIL_PASSWORD)
            server.send_message(msg)

        return RedirectResponse(url="/?success=true", status_code=303)

    except Exception as e:
        logger.error(f"Ошибка отправки: {e}")
        return RedirectResponse(url="/?error=Ошибка сервера", status_code=303)




if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
