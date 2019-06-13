from tkinter import *
import pymongo
import time

myClient = pymongo.MongoClient("mongodb://localhost:27017/")

todoDB = myClient["todo"]
userCol = todoDB["users"]
listCol = todoDB["lists"]


def show_splash():
    splash_window = Tk()
    splash_window.title("Easy NOTES")
    splash_window.geometry('500x250')

    Label(splash_window, text='WELCOME', font='Helvetica 18 bold').pack(padx=25, pady=25)
    Label(splash_window, text='EASY NOTES is a one stop application where you can manage your notes. It helps '
                              'you focus\n on what matters most and have access to your information when you need it.'
                              '\n\nUse EASY NOTES as the place you put everything.').pack()
    Button(splash_window, text='Take me There!', command=lambda: go).pack(pady=25)

    def go():
        splash_window.destroy()

    splash_window.mainloop()


def show_login():
    login = Tk()
    login.title("Easy NOTES")
    login.geometry("400x400")

    Label(login, text='').pack(pady=5)
    Label(login, text='PLEASE LOGIN TO VIEW NOTES', font="Helvetica 18 bold").pack(pady=3)

    # LOGIN WINDOW WIDGETS & POSITIONING
    def login_query():
        user = entry_user.get()
        password = entry_pass.get()

        query = {"username": user, "password": password}

        if userCol.count_documents(query) > 0:
            login.destroy()
            show_todo_list(user)
        else:
            label_incorrect = Label(login, text="Username/Password is incorrect", fg='RED').pack()
            # time.sleep(5)
            # label_incorrect.pack()

    def signup_query():
        signup_window = Tk()
        signup_window.title("Add a new User here")
        signup_window.geometry("300x400")

        Label(signup_window, text='').pack(pady=5)
        Label(signup_window, text='REGISTER A NEW USER', font="Helvetica 18 bold").pack(pady=3)
        Label(signup_window, text='').pack(pady=10)

        Label(signup_window, text='Enter a new Username').pack()
        entry_user = Entry(signup_window)
        entry_user.pack()

        Label(signup_window, text='').pack(padx=25, pady=25)
        Label(signup_window, text='Enter a password').pack()
        entry_pass = Entry(signup_window, show='*')
        entry_pass.pack()

        Label(signup_window, text='Retype password').pack()
        entry_pass_again = Entry(signup_window, show='*')
        entry_pass_again.pack()

        Label(signup_window, text='').pack(padx=25, pady=5)

        button_add_user = Button(signup_window, text="Create an account", command=lambda:
            btn_add_user(entry_user.get(), entry_pass.get(), entry_pass_again.get()))
        button_add_user.pack()

        def btn_add_user(username, password, password_again):
            if username != "":
                if password == password_again:
                    userCol.insert_one({"username": entry_user.get(), "password": entry_pass.get()})
                    Label(signup_window, text="User " + username + " has been created.\n This window will now close "
                                                                   "after 3 seconds.").pack()
                    signup_window.after(3000, lambda: signup_window.destroy())
                else:
                    Label(signup_window, text="Passwords do not match!", fg='RED').pack()
            else:
                Label(signup_window, text="User name cannot be empty!", fg='RED').pack()

    Label(login, text="").pack(padx=25, pady=25)
    Label(login, text="User Name").pack()

    entry_user = Entry(login)
    entry_user.pack()

    Label(login, text="Password").pack(pady=8)

    entry_pass = Entry(login, show='*')
    entry_pass.pack()

    Label(login, text="").pack(padx=25, pady=25)
    button_submit = Button(login, text="Login", command=login_query)
    button_submit.pack()

    button_signup = Button(login, text="Register", command=signup_query)
    button_signup.pack(padx=25, pady=5)

    login.mainloop()


def show_todo_list(username):

    todo_window = Tk()
    todo_window.geometry("400x700")
    todo_window.title("Notes of " + username)

    Label(todo_window, text='').pack(pady=5)
    Label(todo_window, text='TODO NOTES', font="Helvetica 18 bold").pack(pady=3)
    Label(todo_window, text='').pack(pady=10)

    notes = ''
    for count, x in enumerate(listCol.find({"username": username},
                         {"_id": 0,  "title": 1, "content": 1}), start=1):
        x = dict(x)
        notes += "Note " + str(count) + "\n~~~~~~\n" + x['title'] + " : " + x['content'] + "\n\n"

    Label(todo_window, text=notes, font=("times", 12)).pack()

    Label(todo_window, text='').pack(pady=10)
    btn_create = Button(todo_window, text="Add a new note", command=lambda: add_new_note(username))
    btn_create.pack()

    btn_update = Button(todo_window, text="Update a note", command=lambda: update_note(username))
    btn_update.pack(pady=5)

    btn_delete = Button(todo_window, text="Delete note", command=lambda: delete_note(username))
    btn_delete.pack(pady=5)

    def add_new_note(user):
        add_window = Tk()
        add_window.title("Add a note for " + user)
        add_window.geometry("300x400")

        Label(add_window, text='').pack(pady=5)
        Label(add_window, text='ADD A NEW NOTE', font="Helvetica 18 bold").pack(pady=3)
        Label(add_window, text='').pack(pady=10)

        Label(add_window, text="").pack(padx=25, pady=15)
        Label(add_window, text="Enter a title").pack()

        entry_title = Entry(add_window)
        entry_title.pack()
        Label(add_window, text="").pack(pady=3)
        # entry_title.place(x= 15, y = 200, height=200)
        Label(add_window, text="Enter note below").pack()

        entry_content = Entry(add_window)
        # entry_content.place(x=85, y=160, height=150)
        entry_content.pack()

        Label(add_window, text="").pack(pady=10)

        btn_add = Button(add_window, text="Add Note", command=lambda: add(entry_title.get(), entry_content.get()))
        # btn_add.place(x=110, y=400)
        btn_add.pack()

        def add(title, content):
            if title == '':
                Label(add_window, text="Title cannot be empty!", fg='RED').pack()
            else:
                listCol.insert_one({"username": username, "title": title, "content": content})

                Label(add_window, text="Note was successfully added.\nThis window will close after 3 seconds!",
                      fg='BLUE').pack()

                time.sleep(3)

                todo_window.destroy()
                add_window.destroy()
                show_todo_list(username)

    def update_note(user):
        update_window = Tk()
        update_window.title("Update a note for " + user)
        update_window.geometry("300x500")

        Label(update_window, text='').pack(pady=5)
        Label(update_window, text='UPDATE A NOTE', font="Helvetica 18 bold").pack(pady=3)
        Label(update_window, text='').pack(pady=10)

        Label(update_window, text="").pack(padx=25, pady=25)
        Label(update_window, text="Enter title of the note to edit").pack()

        entry_title = Entry(update_window)
        entry_title.pack()

        Label(update_window, text="").pack(pady=10)
        # entry_title.place(x= 15, y = 200, height=200)
        Label(update_window, text="Enter new note below").pack()

        entry_content = Entry(update_window)
        # entry_content.place(x=85, y=160, height=150)
        entry_content.pack()

        Label(update_window, text="").pack(pady=10)
        btn_update = Button(update_window, text="Update Note", command=lambda: update(entry_title.get(),
                                                                                      entry_content.get()))
        # btn_update.place(x=110, y=400)
        btn_update.pack()

        def update(title, content):
            new_title = title
            new_content = content

            for x in listCol.find({"username": user}, {"_id": 0,  "title": 1, "content": 1}):
                if x["title"] == new_title:
                    oldRecord = {"title": x["title"], "content": x["content"]}
                    newRecord = {"$set": {"title": new_title, "content": new_content}}
                    listCol.update_one(oldRecord, newRecord)

                    Label(update_window, text="Note was updated successfully!"
                                              "\nThis window will now close after 3 seconds.", fg='BLUE').pack()

                    time.sleep(3)

                    todo_window.destroy()
                    update_window.destroy()
                    show_todo_list(username)

                else:
                    Label(update_window, text="No matching notes were found!").pack()

    def delete_note(user):

        delete_window = Tk()
        delete_window.title("Delete a note for " + user)
        delete_window.geometry("300x300")

        Label(delete_window, text='').pack(pady=5)
        Label(delete_window, text='DELETE A NOTE', font="Helvetica 18 bold").pack(pady=3)
        Label(delete_window, text='').pack(pady=10)

        # Label(delete_window, text="").pack(padx=25, pady=25)
        Label(delete_window, text="Enter title of the note to delete").pack()

        entry_title = Entry(delete_window)
        entry_title.pack()

        Label(delete_window, text="").pack(pady=10)

        Label(delete_window, text="").pack(padx=25, pady=25)
        btn_delete = Button(delete_window, text="Delete Note",
                            command=lambda: delete(entry_title.get()))
        btn_delete.pack()

        def delete(title):
            # todo_window.destroy()
            if title != "":
                query = {"username": user, "title": title}
                listCol.delete_one(query)
                todo_window.destroy()
                Label(delete_window, text="").pack(pady=5)
                Label(delete_window,
                      text="Record was deleted successfully!\nThis window will now close after 3 seconds.", fg='BLUE')\
                    .pack()
                # todo_window.destroy()

                delete_window.after(3000, lambda: delete_window.destroy())

                show_todo_list(username)
            else:
                Label(delete_window, text="No matching notes were found!", fg='RED').pack()


show_splash()
show_login()
