import sqlite3
import asyncio

def drop_table():
    with sqlite3.connect('main.db') as conn:
        c = conn.cursor()
        c.execute("DROP TABLE IF EXISTS users")
        c.execute("DROP TABLE IF EXISTS orders")
        c.execute("DROP TABLE IF EXISTS payments")
        print('Таблицы сброшены')

def create_all_db():
    with sqlite3.connect('main.db') as conn:
        c = conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS users (
                  id INTEGER PRIMARY KEY,
                  username TEXT,
                  email TEXT
                  )""")
        c.execute("""CREATE TABLE IF NOT EXISTS orders (
                  id INTEGER PRIMARY KEY, 
                  user_id INTEGER,
                  amount INTEGER,
                  created_at INTEGER
                  )""")
        c.execute("""CREATE TABLE IF NOT EXISTS payments (
                  id INTEGER PRIMARY KEY,
                  order_id INTEGER,
                  status TEXT,
                  paid_at
                  )""")
        print('Таблицы созданы')

def create_users():
    with sqlite3.connect('main.db') as conn:
        c = conn.cursor()

        c.executemany("INSERT INTO users (id, username, email) VALUES (?, ?, ?)", [
            (1, "alice", "alice@example.com"),
            (2, "bob", "bob@example.com"),
            (3, "kirill", "kirill@example.com"),
            (4, "charlie", "charlie@example.com"),
            (5, "diana", "diana@example.com"),
            (6, "eva", "eva@example.com"),
            (7, "danil", "danil@example.com"),
        ])

        c.executemany("INSERT INTO orders (id, user_id, amount, created_at) VALUES (?, ?, ?, ?)", [
            (1, 1, 200, 20230901),
            (2, 1, 150, 20230905),
            (3, 2, 500, 20230907),
            (4, 3, 1200, 20230910),
            (5, 3, 300, 20230912),
            (6, 4, 50, 20230913),
            (7, 5, 1050, 20230915),
        ])

        c.executemany("INSERT INTO payments (id, order_id, status, paid_at) VALUES (?, ?, ?, ?)", [
            (1, 1, "paid", 20230902),
            (2, 2, "paid", 20230906),
            (3, 3, "unpaid", None),
            (4, 4, "paid", 20230911),
            (5, 5, "unpaid", None),
            (6, 6, "paid", 20230914),
            (7, 7, "paid", 20230916),
        ])
        print('Данные добавлены')

drop_table()
create_all_db()
create_users()

# 1 Выведи всех пользователей с их заказами 
# 2 Выведи всех пользователей и их заказы, включая тех, у кого заказов нет 
# 3 Выведи все заказы и статусы оплат
# 4 Покажи пользователей, которые не сделали ни одного заказа 
# 5 Найди пользователей с суммарными заказами больше 1000
# 6 Покажи последние 5 оплат с именем пользователя

# 1
def users_and_orders():
    with sqlite3.connect('main.db') as conn:
        c = conn.cursor()
        c.execute("""SELECT u.id, u.username, o.amount FROM users u JOIN orders o ON u.id = o.user_id""")
        users = c.fetchall()
        for i in users:
            print(f'Id: {i[0]} | {i[1]} - Amount {i[-1]}')
    
# 2
def all_user_and_order():
    with sqlite3.connect('main.db') as conn:
        c = conn.cursor()
        c.execute("""SELECT u.id, u.username, o.amount FROM users u LEFT JOIN orders o ON u.id = o.user_id""")
        for i in c.fetchall():
            print(f'Id: {i[0]} | {i[1]} - Amount {i[-1]}')

# 3
def all_orders_and_status():
    with sqlite3.connect('main.db') as conn:
        c = conn.cursor()
        c.execute("""SELECT o.amount, p.status FROM orders o JOIN payments p ON o.id = p.order_id""")
        for i in c.fetchall():
            print(f'Amount: {i[0]} - {i[-1]}')

# 4
def no_orders():
    with sqlite3.connect('main.db') as conn:
        c = conn.cursor()
        c.execute("""SELECT u.username FROM users u LEFT JOIN orders o ON u.id = o.user_id WHERE o.user_id is null""")
        for i in c.fetchall():
            print(i[0])

# 5 
def order_count_1000():
    with sqlite3.connect('main.db') as conn:
        c = conn.cursor()
        c.execute("""SELECT u.username, SUM(o.amount) AS total_amount
                    FROM users u JOIN orders o ON u.id = o.user_id GROUP BY u.username HAVING total_amount > 1000""")
        for i in c.fetchall():
            print(i[0])

def latest_orders():
    with sqlite3.connect('main.db') as conn:
        c = conn.cursor()
        c.execute("""SELECT u.username, p.status FROM users u JOIN orders o ON u.id = o.user_id JOIN payments p ON o.id = p.order_id AND p.status = 'paid' ORDER BY p.paid_at DESC LIMIT 5""")
        for i in c.fetchall():
            print(i)


