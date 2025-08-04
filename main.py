from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import smtplib
from email.mime.text import MIMEText
import logging
from pathlib import Path

app = FastAPI()

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Конфигурация почты
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_FROM = "mamytalievmirbek2008@gmail.com"
EMAIL_TO = "mamytalievmirbek2008@gmail.com"
EMAIL_PASSWORD = "rjme yufp jfaz ynqt"  # Ваш пароль приложения Gmail


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/send-contact")
async def send_contact(
        request: Request,
        name: str = Form(...),
        phone: str = Form(...),
        message: str = Form(default="")
):
    try:
        logger.info(f"Получена заявка от: {name}, телефон: {phone}")

        # Проверка номера телефона
        if not phone.startswith("+996") or len(phone) != 13:
            logger.error(f"Неверный формат телефона: {phone}")
            return RedirectResponse(
                url="/?error=Неверный формат телефона. Используйте +996XXXXXXXXX",
                status_code=303
            )

        # Формирование письма
        email_body = f"""
        Новая заявка с сайта nFactorial School:

        Имя: {name}
        Телефон: {phone}
        Сообщение: {message if message else 'Не указано'}

        ---
        Это письмо отправлено автоматически с сайта.
        """

        msg = MIMEText(email_body)
        msg['Subject'] = f'Новая заявка от {name}'
        msg['From'] = EMAIL_FROM
        msg['To'] = EMAIL_TO

        # Отправка письма
        try:
            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                server.starttls()
                server.login(EMAIL_FROM, EMAIL_PASSWORD)
                server.send_message(msg)
                logger.info("Письмо успешно отправлено")
        except Exception as e:
            logger.error(f"Ошибка отправки письма: {str(e)}")
            return RedirectResponse(
                url="/?error=Ошибка при отправке письма. Попробуйте позже.",
                status_code=303
            )

        return RedirectResponse(
            url="/?success=true",
            status_code=303
        )

    except Exception as e:
        logger.error(f"Ошибка обработки формы: {str(e)}", exc_info=True)
        return RedirectResponse(
            url="/?error=Внутренняя ошибка сервера",
            status_code=303
        )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")