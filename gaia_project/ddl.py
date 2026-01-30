import duckdb
import pandas as pd
import os

def create_db():
    """
    Инициализирует базу данных DuckDB, создает таблицы и 
    заполняет их данными из CSV-файлов папки source.
    """
    con = duckdb.connect('my.db')
       
    data_files = {
        'gaia_main': 'source/gaia_main.csv',
        'gaia_params': 'source/gaia_params.csv',
        'gaia_variability': 'source/gaia_variability.csv'
    }
    
    for table, path in data_files.items():
        if os.path.exists(path):
            df = pd.read_csv(path)
            con.execute(f"CREATE OR REPLACE TABLE {table} AS SELECT * FROM df")
            print(f"Успех: Таблица {table} создана из {path}")
        else:
            print(f"Ошибка: Файл {path} не найден!")
            
    con.close()

if __name__ == "__main__":
    create_db()
