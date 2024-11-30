import os
import csv
import xml.etree.ElementTree as ET
from collections import Counter
import time


class CSVProcessor:
    """Класс для обработки CSV-файлов"""

    @staticmethod
    def process(file_path):
        duplicates = Counter()
        building_floors = Counter()

        try:
            with open(file_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile, delimiter=';')
                for row in reader:
                    city = row.get('city', '').strip()
                    floor = row.get('floor', '').strip()
                    house = row.get('house', '').strip()
                    street = row.get('street', '').strip()

                    # Проверяем и обрабатываем этажность
                    if floor and floor.isdigit():
                        # Формируем запись с всеми необходимыми полями
                        record = {'city': city, 'floor': floor, 'house': house, 'street': street}
                        duplicates[tuple(record.items())] += 1
                        building_floors[(city, int(floor))] += 1
                    else:
                        print(f"Некорректное значение этажности: '{floor}' для города: '{city}'")

            return duplicates, building_floors

        except Exception as e:
            print(f"Ошибка обработки CSV-файла: {e}")
            return None, None


class XMLProcessor:
    """Класс для обработки XML-файлов"""

    @staticmethod
    def process(file_path):
        duplicates = Counter()
        building_floors = Counter()

        try:
            tree = ET.parse(file_path)
            root = tree.getroot()

            for item in root.findall('item'):
                city = item.attrib.get('city', '').strip()
                floor = item.attrib.get('floor', '').strip()
                house = item.attrib.get('house', '').strip()
                street = item.attrib.get('street', '').strip()

                # Пропускаем пустые значения
                if not city or not floor:
                    continue

                # Формируем запись с всеми необходимыми полями
                record = {'city': city, 'floor': floor, 'house': house, 'street': street}
                duplicates[tuple(record.items())] += 1

                # Считаем этажность
                if floor.isdigit():
                    building_floors[(city, int(floor))] += 1
                else:
                    print(f"Некорректное значение этажности: {floor} для города {city}")

            return duplicates, building_floors

        except Exception as e:
            print(f"Ошибка обработки XML-файла: {e}")
            return None, None


def display_statistics(duplicates, building_floors, elapsed_time):
    """Вывод статистики"""
    print("\nСтатистика обработки файла:")

    # Группируем данные по каждому городу
    cities = {}
    for (city, floor), count in building_floors.items():
        if city not in cities:
            cities[city] = {}
        cities[city][floor] = count

    # Вывод информации по каждому городу
    for city, floors_data in cities.items():
        print(f"\nГород: {city}")
        for floor, count in sorted(floors_data.items()):
            print(f"   Этажей: {floor} - Количество зданий: {count}")

    # Дублирующиеся записи
    print("\n1) Дублирующиеся записи:")
    for record, count in duplicates.items():
        if count > 1:
            # Преобразуем кортеж обратно в словарь для удобного вывода
            record_dict = dict(record)
            print(f"   Запись: {record_dict}")

    print(f"\nВремя обработки файла: {elapsed_time:.2f} секунд\n")


def main():
    # Предопределенные пути файлов
    xml_file_path = r"C:\Users\MireyUwU\Downloads\address.xml"
    csv_file_path = r"C:\Users\MireyUwU\Downloads\address.csv"

    print("Добро пожаловать в приложение для работы со справочниками городов!")
    print("Введите:")
    print("1 - для выбора XML-файла")
    print("2 - для выбора CSV-файла")
    print("exit - для завершения работы программы.")

    while True:
        user_input = input("\nВаш выбор: ").strip()

        if user_input.lower() == 'exit':
            print("Завершение работы программы.")
            break

        if user_input == '1':
            file_path = xml_file_path
            processor = XMLProcessor()
        elif user_input == '2':
            file_path = csv_file_path
            processor = CSVProcessor()
        else:
            print("Ошибка: неверный ввод. Попробуйте снова.")
            continue

        if not os.path.isfile(file_path):
            print("Ошибка: файл не найден. Проверьте путь к файлу.")
            continue

        start_time = time.time()
        duplicates, building_floors = processor.process(file_path)

        if duplicates is not None and building_floors is not None:
            elapsed_time = time.time() - start_time
            display_statistics(duplicates, building_floors, elapsed_time)


if __name__ == "__main__":
    main()
