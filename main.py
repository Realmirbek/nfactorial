from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import smtplib
from email.mime.text import MIMEText
import logging

app = FastAPI()

# Логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Папки
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# 📧 SMTP конфигурация — новый аккаунт
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_FROM = "profidata.tech@gmail.com"
EMAIL_TO = "profidata.tech@gmail.com"
EMAIL_PASSWORD = "yhbb ipdm shsh ynbx"  # Пароль приложения

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/send-contact")
async def send_contact(request: Request, name: str = Form(...), phone: str = Form(...), message: str = Form("")):
    try:
        logger.info(f"Получена заявка: {name}, {phone}")

        # Валидация номера
        if not phone.startswith("+7") or len(phone) != 12 or not phone[2:].isdigit():
            return RedirectResponse(url="/?error=Неверный формат номера", status_code=303)

        # Текст письма
        email_body = f"""
        Новая заявка:

        Имя: {name}
        Телефон: {phone}
        Сообщение: {message or '—'}
        """

        msg = MIMEText(email_body)
        msg["Subject"] = f"Заявка от {name}"
        msg["From"] = EMAIL_FROM
        msg["To"] = EMAIL_TO

        # Отправка
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
