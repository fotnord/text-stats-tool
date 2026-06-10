"""Модуль для базовой статистики текста."""

import sys
import json
import re
import os
from collections import Counter


def word_frequency(text: str, top_n: int = 20, stop_words:list = None) -> dict:
    """
    Возвращает словарь {слово: частота} для top_n самых частотных слов.
    Слова приводятся к нижнему регистру, удаляется базовая пунктуация.
    """
    if stop_words is None:
        stop_words = []
    cleaned = re.sub(r"[^\w\s]", "", text, flags=re.UNICODE)
    words = cleaned.lower().split()
    filtered_words = [w for w in words if w not in stop_words]
    counter = Counter(filtered_words)
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
    except UnicodeDecodeError:
        print(f"Ошибка кодировки: {filepath}. Попробуйте другую кодировку")
        return

    lines = text.splitlines()
    word_count = len(text.split())
    char_count = len(text)

    print(f"Строк: {len(lines)}")
    print(f"Слов: {word_count}")
    print(f"Символов: {char_count}")
    
    base, _ = os.path.splitext(filepath)
    
    # Сохранение общей статистики
    stats = {
        "filename": filepath,
        "lines": len(lines),
        "words": word_count,
        "characters": char_count
    }
   
    stats_filename = base + "_stats.json"
    try:
        with open(stats_filename, "w", encoding="utf-8") as out_f:
            json.dump(stats, out_f, ensure_ascii=False, indent=2)
        print(f"Статистика сохранена в {stats_filename}")
    except Exception as e:
        print(f"Не удалось сохранить JSON: {e}")

    # Сохранение частотности
    russian_stopwords = ["и", "в", "не", "на", "что", "как", "по", "из", "от", "за", "но", "с", "то", "а", "это"]
    freq = word_frequency(text, top_n=20, stop_words=russian_stopwords)
    freq_filename = base + "_freq.json"
try:
        with open(freq_filename, "w", encoding="utf-8") as freq_f:
            json.dump(freq, freq_f, ensure_ascii=False, indent=2)
        print(f"Топ-20 слов сохранён в {freq_filename}")
except Exception as e:
        print(f"Ошибка сохранения частотности: {e}")


if __name__ == "__main__":
    main()