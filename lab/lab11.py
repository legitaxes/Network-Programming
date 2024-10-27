### import libraries
import sqlite3


### fixed variables
FILE = "lab-deliverables\\score2.txt"
DATABASE = "lab-deliverables\\lab11.db"


### functions
def read_file(file):
    f = open(file, encoding='utf-8')
    txt = f.read()
    f.close()
    return txt


def connect_db():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    return conn, c


def find_unique_names(data_list):
    unique_names = []
    for data in data_list:
        if data == "":
            continue
        split_data = data.split(" ")
        first_name = split_data[2]
        last_name = split_data[3]
        name = first_name + " " + last_name
        if name not in unique_names:
            unique_names.append(name)
    return unique_names


def assign_identity_no(unique_names):
    identity_no = 1
    identity_dict = {}
    for name in unique_names:
        identity_dict[name] = identity_no
        identity_no += 1
    return identity_dict


def create_table():
    conn, c = connect_db()
    # use c to execute SQL commands
    c.execute('''DROP TABLE IF EXISTS persons''')
    c.execute('''DROP TABLE IF EXISTS scores''')
    c.execute('''CREATE TABLE if not exists persons (identity integer, name text, second_name text)''')
    c.execute('''CREATE TABLE if not exists scores (task_no integer, score integer, identity integer)''')
    conn.commit()
    conn.close()


def insert_data():
    txt = read_file(FILE)
    data_list = txt.split("\n")
    # find unique occurences of names 
    unique_names = find_unique_names(data_list)

    # assign identity number to each unique name
    identity_dict = assign_identity_no(unique_names)
    conn, c = connect_db()
    for name, identity in identity_dict.items():
        first_name, last_name = name.split(" ")
        c.execute("INSERT INTO persons VALUES (?, ?, ?)", (identity, first_name, last_name))


    for data in data_list:
        ### insert score data into the database
        if data == "":
            continue
        split_data = data.split(" ")
        task_number = split_data[1]
        first_name = split_data[2]
        last_name = split_data[3]
        score = split_data[4]
        c.execute("INSERT INTO scores VALUES (?, ?, ?)", (task_number, score, identity_dict[first_name+" "+last_name]))
    conn.commit()
    conn.close()


def print_table():
    conn, c = connect_db()
    c.execute("SELECT * FROM persons")
    print("Persons Table")
    print(c.fetchall())
    print()
    c.execute("SELECT * FROM scores")
    print("Scores Table")
    print(c.fetchall())
    conn.close()


def query1():
    conn, c = connect_db()
    c.execute("SELECT name, second_name, sum(score) FROM persons JOIN scores ON persons.identity = scores.identity GROUP BY persons.identity ORDER BY sum(score) DESC LIMIT 10")
    result = c.fetchall()
    for row in result:
        print(f'{row[0]} {row[1]} with total points {row[2]}')
    conn.close()


def query2():
    conn, c = connect_db()
    c.execute("SELECT task_no, sum(score) FROM scores GROUP BY task_no ORDER BY sum(score) LIMIT 10")
    result = c.fetchall()
    for row in result:
        print(f'Task {row[0]} with total points {row[1]}')
    conn.close()


def main():
    create_table()
    insert_data()
    print_table()
    # list 10 persons who have the highest number of total points
    query1()
    print()
    # list 10 most difficult tasks, that is, the 10 tasks which have minimal total points
    query2()

if __name__ == "__main__":
    main()
