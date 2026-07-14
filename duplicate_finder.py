#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# duplicate_finder.py
# Поиск дубликатов файлов с цветным выводом и удалением.

import os
import hashlib
import argparse
from collections import defaultdict
from colorama import init, Fore, Style

init(autoreset=True)

def hash_file(filepath, blocksize=4096):
    hasher = hashlib.md5()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(blocksize), b''):
            hasher.update(chunk)
    return hasher.hexdigest()

def find_duplicates(directory):
    hash_map = defaultdict(list)
    for root, dirs, files in os.walk(directory):
        for file in files:
            full_path = os.path.join(root, file)
            try:
                h = hash_file(full_path)
                hash_map[h].append(full_path)
            except Exception:
                pass
    return {h: paths for h, paths in hash_map.items() if len(paths) > 1}

def main():
    parser = argparse.ArgumentParser(description="поиск дубликатов файлов")
    parser.add_argument("directory", help="папка для поиска")
    parser.add_argument("--delete", action="store_true", help="удалить дубликаты (оставить первый)")
    parser.add_argument("--dry-run", action="store_true", help="показать, что будет удалено")
    args = parser.parse_args()

    if not os.path.isdir(args.directory):
        print("Ошибка: папка не существует")
        return

    duplicates = find_duplicates(args.directory)
    if not duplicates:
        print(f"{Fore.GREEN}Дубликатов не найдено.{Style.RESET_ALL}")
        return

    print(f"{Fore.CYAN}Найдено {len(duplicates)} групп дубликатов:{Style.RESET_ALL}")

    for h, paths in duplicates.items():
        print(f"\n{Fore.YELLOW}Хеш: {h}{Style.RESET_ALL}")
        for i, p in enumerate(paths):
            if i == 0:
                print(f"  {Fore.GREEN}{p} (оригинал){Style.RESET_ALL}")
            else:
                print(f"  {Fore.RED}{p} (дубликат){Style.RESET_ALL}")

        if args.delete:
            for p in paths[1:]:
                if args.dry_run:
                    print(f"  {Fore.YELLOW}[DRY RUN] Удалил бы: {p}{Style.RESET_ALL}")
                else:
                    os.remove(p)
                    print(f"  {Fore.RED}Удалён: {p}{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
