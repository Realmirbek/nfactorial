from bs4 import BeautifulSoup

def remove_duplicate_ids(html: str) -> str:
    soup = BeautifulSoup(html, 'html.parser')
    seen_ids = set()

    for tag in soup.find_all(attrs={"id": True}):
        tag_id = tag.get("id")
        if tag_id in seen_ids:
            print(f"Удалён дублирующийся id='{tag_id}' в теге: <{tag.name}>")
            del tag["id"]
        else:
            seen_ids.add(tag_id)

    return str(soup)

# Пример использования:
if __name__ == "__main__":
    with open("templates/index.html", "r", encoding="utf-8") as file:
        html_content = file.read()

    cleaned_html = remove_duplicate_ids(html_content)

    with open("templates/index.html", "w", encoding="utf-8") as file:
        file.write(cleaned_html)

    print("Готово: сохранён файл index.html без дублирующихся id.")
