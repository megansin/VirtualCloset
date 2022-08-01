from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfile
from tkcalendar import DateEntry
import mysql
from mysql.connector.errors import Error


def create_server_connection(host_name, user_name, user_password):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")
    return connection


def create_database(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Database created successfully")
    except Error as err:
        print(f"Error: '{err}'")


def create_db_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")
    return connection


def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")


# submit function
def submit():
    # get info from entries/variables
    color = str(color_entry_box.get())
    type = str(type_entry_box.get())
    size = str(size_entry_box.get())
    last_worn = str(last_worn_entry_box.get())
    stored = str(stored_entry_box.get())
    clean = cleanVar.get()
    seasons = ""

    if winterVar.get() != 0:
        seasons = seasons + "winter"
    if springVar.get() != 0:
        seasons = seasons + "spring"
    if summerVar.get() != 0:
        seasons = seasons + "summer"
    if fallVar.get() != 0:
        seasons = seasons + "fall"

    # enter into database
    connection = create_db_connection("localhost", "root", "megan123", "closet")
    get_last_id_query = "SELECT clothing_id FROM clothing WHERE clothing_id=(SELECT MAX(clothing_id) FROM clothing);"
    cursor = connection.cursor()
    cursor.execute(get_last_id_query)
    record = cursor.fetchone()
    clothing_id = record[0] + 1
    insert_query = "INSERT INTO clothing VALUES (" + str(clothing_id) + ", '" + color + "', '" + type + "', '" \
                   + seasons + "', '" + size + "', " + "NULL" + ", '" + str(clean) + "', '" + stored + "', '" \
                   + filePath.get() + "')"
    execute_query(connection, insert_query)

    # clear entries
    color_entry_box.delete(0, END)
    type_entry_box.delete(0, END)
    size_entry_box.delete(0, END)
    last_worn_entry_box.delete(0, END)
    stored_entry_box.delete(0, END)
    winterVar.set(0)
    springVar.set(0)
    summerVar.set(0)
    fallVar.set(0)
    cleanVar.set(2)
    filePath.set("")


# open img function
def open_file():
    file_path = askopenfile(mode='r', filetypes=[('Image Files', '*jpeg')])

    if file_path is not None:
        pass

    filePath.set(file_path.name.lower())


# set up application window
window = tk.Tk()
window.title("Welcome to Your Virtual Closet!")
window.geometry('600x450')


# set up variables
sizes = ["OS", "XS", "S", "M", "L", "XL"]
cleanVar = IntVar()
cleanVar.set(2)
winterVar = IntVar()
springVar = IntVar()
summerVar = IntVar()
fallVar = IntVar()
filePath = StringVar()


# entry boxes
color_entry_box = tk.Entry(window)
color_entry_box.grid(row=0, column=1, padx=20, pady=10)
type_entry_box = tk.Entry(window)
type_entry_box.grid(row=1, column=1, pady=10)
winter_box = tk.Checkbutton(window, text="Winter", width=15, variable=winterVar)
winter_box.grid(row=2, column=1)
spring_box = tk.Checkbutton(window, text="Spring", width=15, variable=springVar)
spring_box.grid(row=2, column=2)
summer_box = tk.Checkbutton(window, text="Summer", width=15, variable=summerVar)
summer_box.grid(row=3, column=1)
fall_box = tk.Checkbutton(window, text="Fall", width=15, variable=fallVar)
fall_box.grid(row=3, column=2)
size_entry_box = ttk.Combobox(window, values=sizes)
size_entry_box.grid(row=4, column=1, pady=10)
last_worn_entry_box = DateEntry(window, selectmode='day')
last_worn_entry_box.grid(row=7, column=1, pady=10)
last_worn_entry_box._top_cal.overrideredirect(False)
is_clean_yes = Radiobutton(window, text="Yes", variable=cleanVar, value=1).grid(row=6, column=1)
is_clean_no = Radiobutton(window, text="No", variable=cleanVar, value=0).grid(row=6, column=2)
stored_entry_box = tk.Entry(window)
stored_entry_box.grid(row=5, column=1, pady=10)
file_name_entry_box = Button(window, text='Choose File', command=lambda:open_file())
file_name_entry_box.grid(row=8, column=1, pady=10)


# entry box labels
color = tk.Label(window, text="Color:").grid(row=0, column=0)
type = tk.Label(window, text="Type:").grid(row=1, column=0)
seasons = tk.Label(window, text="Seasons:").grid(row=2, column=0, pady=10)
size = tk.Label(window, text="Size:").grid(row=4, column=0)
last_worn = tk.Label(window, text="Last Worn:").grid(row=5, column=0)
is_clean = tk.Label(window, text="Clean?").grid(row=6, column=0, pady=10)
stored = tk.Label(window, text="Stored In:").grid(row=7, column=0)
file_name = tk.Label(window, text="File Name:").grid(row=8, column=0)


# create submit button
submit_btn = tk.Button(window, text="Add to Closet", command=submit).grid(row=9, column=0, columnspan=2, pady=10, padx=10, ipadx=10)


# run window
window.mainloop()
