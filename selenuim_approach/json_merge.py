# -*- coding: utf-8 -*-

import json
import os


def combine_jsons():
    # этот код собирает все частички обратно вместе в один словарик
    # тут нужно поменять название папки везде, где "ПРОФСПЕЦТОРГ" на то которое будет в будущем
    # и запускай мейн
    all_data_dict = {}
    for json_file in os.listdir(r'ПРОФСПЕЦТОРГ/details'):
        with open(f'ПРОФСПЕЦТОРГ/details/{json_file}', 'r+', encoding='utf-8') as file:
            file_data = json.load(file)
        all_data_dict.update(file_data)
    with open('ПРОФСПЕЦТОРГ/summary.json', "w", encoding='utf-8') as outfile:  # save to json file
        json.dump(all_data_dict, outfile, ensure_ascii=False, indent=4)


def main():
    combine_jsons()


if __name__ == '__main__':
    main()
    # после отработки появляется файл summary со всеми товарами
    # после переход в скрипт json2table.py
