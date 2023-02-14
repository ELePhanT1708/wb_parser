# -*- coding: utf-8 -*-
from typing import List

import pandas as pd


def read_column_names():
    excel = pd.read_excel('rawExportExcel (16).xlsx')
    column_names = []
    for row in excel:
        column_names.append(row)
    return column_names


def read_json_info():
    json = pd.read_json('z_book.json', encoding='windows-1251')
    list_of_df = []
    for book in json:
        add_row_about_book2df(json[book], list_of_df)
    res_df = pd.concat(list_of_df)
    res_df.to_excel('z_book.xlsx')
    print(res_df)


def create_table():
    column_names = read_column_names()
    df = pd.DataFrame(columns=column_names)
    return df


def add_row_about_book2df(json_data: dict, list_of_df: List[pd.DataFrame]):
    column_names = read_column_names()
    df = pd.DataFrame(columns=column_names)

    img_urls = ', '.join(json_data['pictures'])
    for column in column_names:
        if column == 'Медиафайлы':
            df.loc[0, column] = img_urls
        elif column == 'Номер карточки':
            df.loc[0, column] = 0
        elif column == 'Предмет':
            df.loc[0, column] = 'Учебники'
        else:
            df.loc[0, column] = json_data['Charasteristics'].get(column)
    print(df)
    list_of_df.append(df)


if __name__ == '__main__':
    read_json_info()
    create_table()
