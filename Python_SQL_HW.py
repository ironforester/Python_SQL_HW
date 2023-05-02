import psycopg2
from psycopg2.sql import SQL, Identifier

with psycopg2.connect(database='pytdb', user='postgres', password='you have to use your own') as conn:

    # 1 Функция, создающая структуру БД (таблицы)
    def create_table(table_name, first_column, sec_column, third_column, last_column):
        with conn.cursor() as cur:
            try:
                cur.execute("""
                CREATE TABLE IF NOT EXISTS 
                {}({} SERIAL PRIMARY KEY, 
                {} VARCHAR(30) NOT NULL, 
                {} VARCHAR(30) NOT NULL, 
                {} VARCHAR(30) NOT NULL);""".format(table_name, first_column,
                                                    sec_column, third_column,
                                                    last_column))
                cur.execute("""CREATE TABLE IF NOT EXISTS 
                phone(id INTEGER REFERENCES {}({}), phone VARCHAR(30));""".format(table_name, first_column))
                conn.commit()
            except (Exception, psycopg2.Error) as ex:
                print(ex)

    create_table("client", "id", "name", "lastname", "email")

    # 2 Функция, позволяющая добавить нового клиента.
    def new_client(name, lastname, email):
        with conn.cursor() as cur:
            try:
                cur.execute("""INSERT INTO client(name, lastname, email) VALUES(%s, %s, %s);""", (name, lastname, email))
                conn.commit()
            except (Exception, psycopg2.Error) as ex:
                print(ex)
    new_client('Alex', 'Beettle', 'al.be@yandex.ru')
    new_client('John', 'Gates', 'jg@mail.ru')
    new_client('Petr', 'Perviy', 'pp@mail.ru')
    new_client('Vasiliy', 'Beregovoy', 'vasber@google.com')

    # 3 Функция, позволяющая добавить телефон для существующего клиента.
    def add_phone(name, lastname, phone_number):
        with conn.cursor() as cur:
            try:
                cur.execute("""
                            SELECT id FROM client WHERE name=%s AND lastname=%s;
                            """, (name, lastname))
                cl_id = cur.fetchone()[0]
                cur.execute("""INSERT INTO phone(id, phone) VALUES(%s, %s);""", (cl_id, phone_number))
                conn.commit()
            except (Exception, psycopg2.Error) as ex:
                print(ex)

    add_phone('Alex', 'Beettle', '89205554421')
    add_phone('Alex', 'Beettle', '8(81367)75512')
    add_phone('Vasiliy', 'Beregovoy', '555224477')

    # 4 Функция, позволяющая изменить данные о клиенте.
    def change_client(id, name=None, lastname=None, email=None):
        with conn.cursor() as cur:
            try:
                arg={'name': name, 'lastname': lastname, 'email': email }
                for key, values in arg.items():
                    if values:
                        cur.execute(SQL("UPDATE client SET {}=%s WHERE id=%s").format(Identifier(key)), (values, id))
                        conn.commit()
            except (Exception, psycopg2.Error) as ex:
                print(ex)

    change_client(1, lastname='Frost')
    change_client(2, email='forester@mail.ru')

    # 5 Функция, позволяющая удалить телефон для существующего клиента.
    # Сначала выведем имеющиеся у клиента телефоны
    def phone_list(id):
        with conn.cursor() as cur:
            try:
                cur.execute("SELECT phone FROM client c LEFT JOIN phone p ON c.id=p.id WHERE c.id=%s;", (id, ))
                p_list = cur.fetchall()
                for el in p_list:
                    if el == (None,):
                        print('No phone number')
                return p_list
            except (Exception, psycopg2.Error) as ex:
                print(ex)

    print(phone_list(1))

    # Теперь удалим требуемый номер тф по индексу списка номеров

    def phone_del(id, index):
        with conn.cursor() as cur:
            try:
                cur.execute("DELETE FROM phone WHERE phone=%s;", (phone_list(id)[index],))
                conn.commit()
            except (Exception, psycopg2.Error) as ex:
                print(ex)

    phone_del(1, 0)
    
    # 6 Функция, позволяющая удалить существующего клиента.

    def del_client(id):
        with conn.cursor() as cur:
            try:
                cur.execute("DELETE FROM client WHERE id=%s;", (id,))
                if phone_list(id) != 0:
                    cur.execute("DELETE FROM phone WHERE id=%s;", (id,))
                conn.commit()
            except (Exception, psycopg2.Error) as ex:
                print(ex)
    del_client(2)

    # 7 Функция, позволяющая найти клиента по его данным: имени, фамилии, email или телефону


    def find_client(name=None, lastname=None, email=None, phone=None):
        with conn.cursor() as cur:
            try:
                arg={'name': name, 'lastname': lastname, 'email': email, 'phone': phone}
                for key, values in arg.items():
                    if values:
                        cur.execute(SQL("""SELECT c.id, name, lastname, email, phone 
                        FROM client c LEFT JOIN phone p ON c.id=p.id 
                        WHERE {}=%s""").format(Identifier(key)), (values,))
                        print(cur.fetchall())
            except (Exception, psycopg2.Error) as ex:
                print(ex)

    find_client(phone='555224477')
    find_client(lastname='Perviy')
