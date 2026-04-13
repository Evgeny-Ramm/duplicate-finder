#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import hashlib
import argparse
from collections import defaultdict
from tqdm import tqdm

def hash_file(filepath, algo='md5', blocksize=4096):
    """Вычисляет хеш файла. По умолчанию md5."""
    hash_func = hashlib.new(algo)
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(blocksize), b''):
            hash_func.update(chunk)
    return hash_func.hexdigest()

def find_duplicates(directory, algo='md5'):
    """Обходит директорию, группирует файлы по хешу."""
    hash_map = defaultdict(list)
    # Собираем все файлы
    file_paths = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            full_path = os.path.join(root, file)
            file_paths.append(full_path)
    
    # Вычисляем хеш для каждого файла с прогресс-баром
    for path in tqdm(file_paths, desc="Хеширование файлов"):
        try:
            h = hash_file(path, algo)
            hash_map[h].append(path)
        except Exception as e:
            print(f"Ошибка при обработке {path}: {e}")
    
    # Оставляем только те хеши, у которых больше одного файла
    duplicates = {h: paths for h, paths in hash_map.items() if len(paths) > 1}
    return duplicates

def main():
    parser = argparse.ArgumentParser(description="Поиск дубликатов файлов по содержимому")
    parser.add_argument("directory", help="Директория для поиска дубликатов")
    parser.add_argument("--algo", default="md5", choices=["md5", "sha1", "sha256"], 
                        help="Алгоритм хеширования (по умолчанию md5)")
    args = parser.parse_args()
    
    if not os.path.isdir(args.directory):
        print("Ошибка: директория не существует")
        return
    
    print(f"Поиск дубликатов в {args.directory} (алгоритм {args.algo})")
    duplicates = find_duplicates(args.directory, args.algo)
    
    if not duplicates:
        print("Дубликатов не найдено.")
        return
    
    print(f"\nНайдено {len(duplicates)} групп дубликатов:\n")
    for h, paths in duplicates.items():
        print(f"Хеш: {h}")
        for p in paths:
            print(f"  - {p}")
        print()

if __name__ == "__main__":
    main()
