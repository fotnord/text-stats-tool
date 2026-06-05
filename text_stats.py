"""Модуль для базовой статистики текста."""

import sys
import json
import re
from collections import Counter


def word_frequency(text: str, top_n: int = 20) -> dict:
    """
    Возвращает словарь {слово: частота} для top_n самых частотных слов.
    Слова приводятся к нижнему регистру, удаляется базовая пунктуация.
    """
    cleaned = re.sub(r"[^\w\s]", "", text, flags=re.UNICODE)
    words = cleaned.lower().split()
    counter = Counter(words)
    return dict(counter.most_common(top_n))


def main():
    if len(sys.argv) < 2:
        print("Укажи путь к файлу: python text_stats.py <имя_файла>")
        return

    filepath = sys.argv[1]
    print(f"Читаю файл: {filepath}")

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            text = f.read()
    except FileNotFoundError:
        print(f"Файл не найден: {filepath}")
        return

    lines = text.splitlines()
    word_count = len(text.split())
    char_count = len(text)

    print(f"Строк: {len(lines)}")
    print(f"Слов: {word_count}")
    print(f"Символов: {char_count}")

    # Сохранение общей статистики
    stats = {
        "filename": filepath,
        "lines": len(lines),
        "words": word_count,
        "characters": char_count
    }
    output_filename = filepath.replace(".txt", "_stats.json")
    try:
        with open(output_filename, "w", encoding="utf-8") as out_f:
            json.dump(stats, out_f, ensure_ascii=False, indent=2)
        print(f"Статистика сохранена в {output_filename}")
    except Exception as e:
        print(f"Не удалось сохранить JSON: {e}")

    # Сохранение частотности
    freq = word_frequency(text, top_n=20)
    freq_filename = filepath.replace(".txt", "_freq.json")
    try:
        with open(freq_filename, "w", encoding="utf-8") as freq_f:
            json.dump(freq, freq_f, ensure_ascii=False, indent=2)
        print(f"Топ-20 слов сохранён в {freq_filename}")
    except Exception as e:
        print(f"Ошибка сохранения частотности: {e}")


if __name__ == "__main__":
    main()