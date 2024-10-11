import os
import pandas as pd

def clean_text(text):
    """Предобработка текста: удаление лишних символов и приведение к нижнему регистру."""
    text = text.lower()  # Приведение к нижнему регистру
    text = ''.join(c for c in text if c.isalnum() or c.isspace())  # Удаление небуквенных символов
    return text

def preprocess_data(content):
    """Автоматическая предобработка данных."""
    cleaned_lines = []
    for line in content.splitlines():
        cleaned_line = clean_text(line)
        if cleaned_line:  # Убираем пустые строки
            cleaned_lines.append(cleaned_line)
    return "\n".join(cleaned_lines)

def process_python_files(main_directory, output_directory):
    """Парсит .py файлы, предобрабатывает их содержимое и сохраняет в датасет."""
    dataset = []

    # Проходим по всем папкам в основной директории
    for root, dirs, files in os.walk(main_directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                print(f'Обрабатываем файл: {file_path}')

                # Чтение содержимого файла
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Предобработка данных
                cleaned_content = preprocess_data(content)
                dataset.append({'file_path': file_path, 'content': cleaned_content})

                # Удаление файла после обработки
                os.remove(file_path)
        
        # Удаление пустых папок
        if not os.listdir(root):  # Если папка пустая
            os.rmdir(root)

    # Сохранение датасета в CSV
    if dataset:
        df = pd.DataFrame(dataset)
        output_file = os.path.join(output_directory, 'dataset.csv')
        df.to_csv(output_file, index=False)
        print(f'Датасет сохранен в файл: {output_file}')
    else:
        print('Не найдено файлов для обработки.')

if __name__ == "__main__":
    main_directory = 'repos'  # Путь к основной папке
    output_directory = 'dataset'  # Папка для сохранения датасета

    os.makedirs(output_directory, exist_ok=True)  # Создаем папку, если не существует
    process_python_files(main_directory, output_directory)