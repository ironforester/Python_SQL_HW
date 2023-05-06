import psycopg2
from psycopg2.sql import SQL, Identifier


# 1 Функция, создающая структуру БД (таблицы)
def create_table(cursor, table_name, first_column, sec_column, third_column, last_column):
    try:
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS
        {}({} SERIAL PRIMARY KEY,
        {} VARCHAR(30) NOT NULL,
        {} VARCHAR(30) NOT NULL,
        {} VARCHAR(30) NOT NULL);""".format(table_name, first_column,
                                            sec_column, third_column,
                                            last_column))
        cursor.execute("""CREATE TABLE IF NOT EXISTS
        phone(id INTEGER REFERENCES {}({}), phone VARCHAR(30));""".format(table_name, first_column))
    except (Exception, psycopg2.Error) as ex:
        print(ex)
# 2 Функция, позволяющая добавить нового клиента.
def new_client(cursor, name, lastname, email):
    try:
        cursor.execute("""INSERT INTO client(name, lastname, email) VALUES(%s, %s, %s);""", (name, lastname, email))
    except  (Exception, psycopg2.Error) as ex:
        print(ex)

# 3 Функция, позволяющая добавить телефон для существующего клиента.
def add_phone(cursor, name, lastname, phone_number):
    try:
        cursor.execute("""
                    SELECT id FROM client WHERE name=%s AND lastname=%s;
                    """, (name, lastname))
        cl_id = cur.fetchone()[0]
        cursor.execute("""INSERT INTO phone(id, phone) VALUES(%s, %s);""", (cl_id, phone_number))
    except (Exception, psycopg2.Error) as ex:
        print(ex)

 # 4 Функция, позволяющая изменить данные о клиенте.
def change_client(cursor, id, name=None, lastname=None, email=None):
        try:
            arg={'name': name, 'lastname': lastname, 'email': email }
            for key, values in arg.items():
                if values:
                    cursor.execute(SQL("UPDATE client SET {}=%s WHERE id=%s").format(Identifier(key)), (values, id))
        except (Exception, psycopg2.Error) as ex:
            print(ex)

 # 5 Функция, позволяющая удалить телефон для существующего клиента.
    # Сначала выведем имеющиеся у клиента телефоны
def phone_list(cursor, id):
    try:
        cursor.execute("SELECT phone FROM client c LEFT JOIN phone p ON c.id=p.id WHERE c.id=%s;", (id, ))
        # print(cur.fetchall())
        p_list = cursor.fetchall()
        for el in p_list:
            if el == (None,):
                print('No phone number')
        return p_list
    except (Exception, psycopg2.Error) as ex:
        print(ex)

# print(phone_list(4))

# Теперь удалим требуемый номер тф по индексу списка номеров
def phone_del(cursor, id, index):
    try:
        cursor.execute("DELETE FROM phone WHERE phone=%s;", (phone_list(id)[index],))
    except (Exception, psycopg2.Error) as ex:
        print(ex)

 # 6 Функция, позволяющая удалить существующего клиента.

def del_client(cursor, id):
    try:
        cursor.execute("DELETE FROM client WHERE id=%s;", (id,))
        if phone_list(id) != 0:
            cursor.execute("DELETE FROM phone WHERE id=%s;", (id,))
    except (Exception, psycopg2.Error) as ex:
        print(ex)

# 7 Функция, позволяющая найти клиента по его данным: имени, фамилии, email или телефону

def find_client(cursor, name=None, lastname=None, email=None, phone=None):
    try:
        arg={'name': name, 'lastname': lastname, 'email': email, 'phone': phone}
        for key, values in arg.items():
            if values:
                cursor.execute(SQL("""SELECT c.id, name, lastname, email, phone
                FROM client c LEFT JOIN phone p ON c.id=p.id
                WHERE {}=%s""").format(Identifier(key)), (values,))
                print(cursor.fetchall())
    except (Exception, psycopg2.Error) as ex:
        print(ex)

with psycopg2.connect(database='pytdb', user='postgres', password='sanobel') as conn:
    with conn.cursor() as cur:
        # create_table(cur, "client", "id", "name", "lastname", "email")
        # new_client(cur, 'Alex', 'Beettle', 'al.be@yandex.ru')
        # new_client(cur, 'John', 'Gates', 'jg@mail.ru')
        # new_client(cur, 'Petr', 'Perviy', 'pp@mail.ru')
        # new_client(cur, 'Vasiliy', 'Beregovoy', 'vasber@google.com')
        # add_phone(cur, 'Alex', 'Beettle', '89205554421')
        # add_phone(cur, 'Alex', 'Beettle', '8(81367)75512')
        # add_phone(cur, 'Vasiliy', 'Beregovoy', '555224477')
        # change_client(cur, 1, lastname='Frost')
        # change_client(cur, 2, email='forester@mail.ru')
        # print(phone_list(cur, 4))
        # phone_del(cur, 1, 0)
        # del_client(cur, 2)
        # find_client(cur, phone='555224477')
        # find_client(cur, lastname='Perviy')


conn.close()
