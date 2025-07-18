import os
import re
from pathlib import Path


def split_html_file(input_file="index.html", output_dir="fastapi_project"):
    # Создаем структуру папок
    project_path = Path(output_dir)
    (project_path / "templates").mkdir(parents=True, exist_ok=True)
    (project_path / "static" / "css").mkdir(parents=True, exist_ok=True)
    (project_path / "static" / "js").mkdir(parents=True, exist_ok=True)

    # Читаем исходный файл
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Извлекаем CSS (внутри <style> и inline в тегах)
    css_content = []

    # Внутренние стили в <style>
    style_matches = re.findall(r'<style[^>]*>(.*?)<\/style>', content, re.DOTALL)
    css_content.extend(style_matches)

    # Удаляем <style> из HTML
    content = re.sub(r'<style[^>]*>.*?<\/style>', '', content, flags=re.DOTALL)

    # Извлекаем JS (внутри <script> без src)
    js_content = []
    script_matches = re.findall(r'<script(?!.*src=)[^>]*>(.*?)<\/script>', content, re.DOTALL)
    js_content.extend(script_matches)

    # Удаляем inline скрипты из HTML
    content = re.sub(r'<script(?!.*src=)[^>]*>.*?<\/script>', '', content, flags=re.DOTALL)

    # Заменяем оставшиеся script src на правильные пути
    content = re.sub(
        r'(<script.*src=["\'])(?!http)(.*?)(["\'].*?>)',
        lambda m: f'{m.group(1)}/static/js/{os.path.basename(m.group(2))}{m.group(3)}',
        content
    )

    # Заменяем ссылки на CSS файлы
    content = re.sub(
        r'(<link.*href=["\'])(?!http)(.*?\.css)(["\'].*?>)',
        lambda m: f'{m.group(1)}/static/css/{os.path.basename(m.group(2))}{m.group(3)}',
        content
    )

    # Заменяем ссылки на другие статические файлы (images, fonts)
    content = re.sub(
        r'(<(?:img|source).*src=["\'])(?!http)(.*?)(["\'].*?>)',
        lambda m: f'{m.group(1)}/static/{os.path.basename(m.group(2))}{m.group(3)}',
        content
    )

    # Добавляем необходимое для FastAPI (Jinja2 request)
    head_end = content.find('</head>')
    if head_end != -1:
        content = content[:head_end] + '\n    {{ super() }}\n' + content[head_end:]

    # Сохраняем HTML
    with open(project_path / "templates" / "index.html", 'w', encoding='utf-8') as f:
        f.write(content)

    # Сохраняем CSS
    if css_content:
        with open(project_path / "static" / "css" / "style.css", 'w', encoding='utf-8') as f:
            f.write('\n\n'.join(css_content))

    # Сохраняем JS
    if js_content:
        with open(project_path / "static" / "js" / "script.js", 'w', encoding='utf-8') as f:
            f.write('\n\n'.join(js_content))

    # Создаем main.py для FastAPI
    main_py_content = """from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI()

# Статические файлы
app.mount("/static", StaticFiles(directory="static"), name="static")

# Шаблоны Jinja2
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
"""
    with open(project_path / "main.py", 'w', encoding='utf-8') as f:
        f.write(main_py_content)

    print(f"Проект успешно создан в папке {output_dir}!")
    print(f"Запустите его командой: uvicorn main:app --reload")


if __name__ == "__main__":
    split_html_file()