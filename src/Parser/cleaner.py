import os
import sys

def clean_directory(directory, extension):
    # Проходим по всем файлам и папкам в указанной директории
    for root, dirs, files in os.walk(directory, topdown=False):
        # Удаляем файлы, которые не имеют нужного расширения
        for name in files:
            if not name.endswith(extension):
                file_path = os.path.join(root, name)
                try:
                    print(f'Удаляем файл: {file_path}')
                    os.remove(file_path)
                except PermissionError:
                    print(f'Отказано в доступе: {file_path}. Пропускаем файл.')

        # Удаляем пустые папки
        for name in dirs:
            dir_path = os.path.join(root, name)
            try:
                # Проверяем, пустая ли папка
                if not os.listdir(dir_path):
                    print(f'Удаляем папку: {dir_path}')
                    os.rmdir(dir_path)
            except PermissionError:
                print(f'Отказано в доступе: {dir_path}. Пропускаем папку.')

if __name__ == "__main__":
    # Указываем основную папку и расширение
    main_directory = 'repos'  # Замените на ваш путь
    file_extension = '.py'
    
    clean_directory(main_directory, file_extension)