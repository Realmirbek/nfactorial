import smtplib

try:
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login("mamytalievmirbek2008@gmail.com", "rjme yufp jfaz ynqt")
        server.sendmail("mamytalievmirbek2008@gmail.com", "mamytalievmirbek2008@gmail.com", "Test")
    print("✅ Письмо отправлено успешно!")
except Exception as e:
    print(f"❌ Ошибка: {type(e).__name__}: {e}")
    if hasattr(e, 'smtp_error'):
        print(f"SMTP детали: {e.smtp_error.decode()}")