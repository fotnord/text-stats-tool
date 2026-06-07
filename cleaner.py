"""Модуль для очистки текста перед NLP-обработкой."""

import os
import re
import sys


def clean_text(raw: str) -> str:
    """
    Удаляет HTML-теги, e-mail, URL, лишние пробелы,
    оставляет только буквы, цифры и базовую пунктуацию.
    """
    # Удаление HTML-тегов
    text = re.sub(r"<[^>]+>", "", raw)
    # Удаление e-mail
    text = re.sub(r"\S+@\S+\.\S+", "", text)
    # Удаление URL
    text = re.sub(r"https?://\S+|ftp://\S+", "", text)
    # Нормализация пробелов (все пробелы -> один пробел)
    text = re.sub(r"\s+", " ", text)
    text = text.strip()
    # Только разрешённые символы
    text = re.sub(r"[^\w\s.,!?\-]", "", text, flags=re.UNICODE)
    return text


def process_file(input_path: str, output_path: str) -> None:
    """
    Читает файл, очищает текст и сохраняет результат.
    Обрабатывает ошибки чтения и кодировки.
    """
    try:
        with open(input_path, "r", encoding="utf-8") as f:
            raw = f.read()
    except FileNotFoundError:
        print(f"Файл не найден: {input_path}")
        return
    except UnicodeDecodeError:
        print(f"Ошибка кодировки: {input_path}. Попробуйте другую кодировку.")
        return

    # Очистка текста
    cleaned = clean_text(raw)

    # Создаём папку для выходного файла, если её нет
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Запись результата
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(cleaned)
    print(f"Очищенный текст сохранён в {output_path}")


def validate_text(text: str, forbidden: list) -> list:
    """
    Проверяет текст на наличие запрещённых подстрок.
    Возвращает список найденных нарушений.
    """
    found = []
    lower_text = text.lower()
    for word in forbidden:
        if word.lower() in lower_text:
            found.append(word)
    return found


def main():
    if len(sys.argv) < 3:
        print(
            "Использование: python cleaner.py"
            "<входной_файл> <выходной_файл> [файл_запретов]"
            )
        return

    input_path = sys.argv[1]
    output_path = sys.argv[2]
    forbidden = []
    if len(sys.argv) >= 4:
        try:
            with open(sys.argv[3], "r", encoding="utf-8") as f:
                forbidden = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            print(
                f"Файл запретов не найден:{sys.argv[3]},"
                "продолжаем без валидации")

    process_file(input_path, output_path)

    # Если есть запреты, валидируем результат
    if forbidden:
        with open(output_path, "r", encoding="utf-8") as f:
            cleaned = f.read()
        violations = validate_text(cleaned, forbidden)
        if violations:
            print("Нарушения:", ", ".join(violations))
        else:
            print("Нарушений не найдено.")


if __name__ == "__main__":
    main()
