#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import sys
import time


def get_poezd():
    # запросить данные о поезде
    name = input("Название пункта назначения? ")
    no = input("Номер поезда? ")
    time_str = input("Введите время отправления (чч:мм)\n")
    t = time.asctime(time.strptime(time_str, "%H:%M"))[11:-5]
    return {
        "name": name,
        "no": no,
        "t": t,
    }


def list(poezd):
    # Проверить, что список работников не пуст.
    if poezd:
        line = "+-{}-+-{}-+-{}-+".format(
            "-" * 10,
            "-" * 20,
            "-" * 8,
        )
        print(line)
        print("| {:^10} | {:^20} | {:^8} |".format(" No ", "Название", "Время"))
        print(line)

        for idx, po in enumerate(poezd, 1):
            print(
                "| {:>10} | {:<20} | {"
                "} |".format(po.get("no", ""), po.get("name", ""), po.get("t", ""))
            )
        print(line)
    else:
        print("Список поездов пуст.")


def select(poezd, nom):
    result = [po for po in poezd if po.get("no", "") == nom]
    return result


def save_poezd(file_name, poezd):
    # Открыть файл с заданным именем для записи.
    with open(file_name, "w", encoding="utf-8") as fout:
        # Выполнить сериализацию данных в формат JSON.
        # Для поддержки кирилицы установим ensure_ascii=False
        json.dump(poezd, fout, ensure_ascii=False, indent=4)


def load_poezd(file_name):
    # Открыть файл с заданным именем для чтения.
    with open(file_name, "r", encoding="utf-8") as fin:
        return json.load(fin)


def help():
    print("Список команд:\n")
    print("add - добавить поезд;")
    print("list - вывести список поездов;")
    print("select - запросить поезд по номеру;")
    print("load - загрузить данные из файла;")
    print("save - сохранить данные в файл;")
    print("help - отобразить справку;")
    print("exit - завершить работу с программой.")


def main():
    poezd = []

    while True:
        command = input(">>> ").lower()

        if command == "exit":
            break

        elif command == "add":
            po = get_poezd()
            poezd.append(po)
            if len(poezd) > 1:
                poezd.sort(key=lambda item: item.get("no", ""))

        elif command == "list":
            list(poezd)

        elif command.startswith("select"):
            print("Введите номер поезда: ")
            nom = input()
            selected = select(poezd, nom)
            list(selected)

        elif command == "help":
            # Вывести справку о работе с программой.
            help()

        elif command.startswith("save "):
            # Разбить команду на части для выделения имени файла.
            parts = command.split(maxsplit=1)
            # Получить имя файла.
            file_name = parts[1]

            # Сохранить данные в файл с заданным именем.
            save_poezd(file_name, poezd)

        elif command.startswith("load "):
            # Разбить команду на части для выделения имени файла.
            parts = command.split(maxsplit=1)
            # Получить имя файла.
            file_name = parts[1]

            # Сохранить данные в файл с заданным именем.
            poezd = load_poezd(file_name)

        else:
            print(f"Неизвестная команда {command}", file=sys.stderr)


if __name__ == "__main__":
    main()
