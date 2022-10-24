import sqlite3
 
conn = sqlite3.connect(r"C:\Users\79190\Desktop\kur\botdb\test.db") # или :memory: чтобы сохранить в RAM
cursor = conn.cursor()
 
# Создание таблицы
cursor.execute("""CREATE TABLE albums
                  (title text, artist text, release_date text,
                   publisher text, media_type text)
               """)

