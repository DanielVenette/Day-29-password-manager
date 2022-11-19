from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json

FONT = ("Calibri", 12)


# ---------------------------- SEARCH DATABASE ------------------------------- #
def search():
    website_text = website_entry.get()

    try:
        with open("data.json", "r") as file:
            data_dict = json.load(file)
    except FileNotFoundError:
        messagebox.showinfo(title="No Entries", message="You have no saved entries")
        # print("You have no saved entries.")
    else:
        try:
            messagebox.showinfo(
                title=website_text,
                message=f"email/username: {data_dict[website_text]['email']}\n"
                        f"password: {data_dict[website_text]['password']}"
            )
        except KeyError:
            messagebox.showinfo(
                title="Entry Not Found",
                message=f"an entry for {website_text} is not yet saved in your database"
            )
            # print(f"an entry for {website_text} is not yet saved in your database")


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v',
               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
               'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_entry.delete(0, END)

    password_list = []

    password_list += [random.choice(letters) for _ in range(nr_letters)]
    password_list += [random.choice(symbols) for _ in range(nr_symbols)]
    password_list += [random.choice(numbers) for _ in range(nr_numbers)]

    random.shuffle(password_list)

    password = "".join(password_list)
    # for char in password_list:
    #     password += char

    # print(f"Your password is: {password}")
    password_entry.insert(0, password)

    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website_text = website_entry.get()
    email_text = email_entry.get()
    password_text = password_entry.get()
    new_data = {
        website_text: {
            "email": email_text,
            "password": password_text
        }
    }

    if len(website_text) and len(password_text) != 0:
        try:
            with open("data.json", mode="r") as file:
                # load file with old data and put into dictionary
                data = json.load(file)
                # update your dictionary with new data
                data.update(new_data)
        except FileNotFoundError:
            data = new_data

        with open("data.json", mode="w") as file:
            # write new dictionary to file
            json.dump(data, file, indent=4)

            # delete lines from app
            website_entry.delete(0, END)
            password_entry.delete(0, END)
        website_entry.focus()
    else:
        messagebox.showinfo(title="Error", message="Please don't leave any fields empty")


# ---------------------------- UI SETUP ------------------------------- #

# create program window
window = Tk()
window.title("Password Manager")
window.minsize(width=240, height=240)
window.config(padx=20, pady=20)

# create canvas
canvas = Canvas()
canvas.config(width=200, height=200)
logo = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo)
canvas.grid(column=1, row=0)

# create field labels
website_label = Label(text="Website:", font=FONT)
website_label.grid(column=0, row=1)
email_label = Label(text="Email/Username:", font=FONT)
email_label.grid(column=0, row=2)
password_label = Label(text="Password:", font=FONT)
password_label.grid(column=0, row=3)

# create entry fields
website_entry = Entry(width=33)
website_entry.grid(column=1, row=1)
website_entry.focus()
email_entry = Entry(width=53)
email_entry.grid(column=1, row=2, columnspan=2)
email_entry.insert(0, "danvenette@gmail.com")
password_entry = Entry(width=33)
password_entry.grid(column=1, row=3)

# create buttons
search_button = Button(text="Search", width=15, command=search)
search_button.grid(column=2, row=1)
generate_password_button = Button(text="Generate Password", width=15, command=generate_password)
generate_password_button.grid(column=2, row=3)
add_button = Button(text="Add", width=44)
add_button.grid(column=1, row=4, columnspan=2)
add_button["command"] = save


window.mainloop()
