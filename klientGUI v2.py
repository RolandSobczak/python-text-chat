import socket as s
import tkinter
import json
from tkinter import scrolledtext
def send_message(mesage_request):
    mesage_request = json.dumps(mesage_request)
    client.send(mesage_request.encode('utf8'))

def Open_message(id, login):
    main_window.destroy()
    global message_window
    message_window = tkinter.Tk()
    message_window.geometry('720x720')
    message_window.title(login)

    text_area = tkinter.scrolledtext.ScrolledText(message_window)
    text_area.grid(row=0, column=0,padx=20, pady=5)
    text_area.config(state='disabled')

    input_area = tkinter.Text(message_window)
    input_area.config(height=3, width=40)
    input_area.grid(row=1, column=0, padx=5, pady=5)

    send_button = tkinter.Button(message_window, text='Wyślij', command=lambda: send_message({'type': '2', 'message': input_area.get("1.0",'end-1c')}))
    send_button.config(height=3, width=10)
    send_button.grid(row=2, column=0, pady=5, padx=5)
def SerchButton():
    #id_output = id.get
    #token_o = token.get
    search_output = search.get()
    question = {'id': str(id), 'token': str(token), 'type': 'serch', 'input': search_output}
    question = json.dumps(question)
    client.send(question.encode('utf8'))
    answer = client.recv(1024).decode('utf8')
    answer = list(answer.split())
    for index, i in enumerate(answer):
        tkinter.Label(main_window, text=i.split(':')[1]).grid(row=index+2, column=0, pady=5, padx=5)
        tkinter.Button(main_window, text='Wiadomości', command=lambda: Open_message(i.split(':')[0], i.split(':')[1])).grid(row=index+2, column=1, pady=5, padx=5)

def Main():
    log_window.destroy()
    global main_window
    main_window = tkinter.Tk()
    main_window.geometry('720x720')
    main_window.title('komunikator')
    global search
    search = tkinter.Entry(main_window)
    search.grid(row=1, column=0, pady=5)
    tkinter.Label(main_window, text='Wyszukaj użytkownika').grid(row=0, column=0, pady=5, padx=5)

    tkinter.Button(main_window, text='Szukaj', command=SerchButton).grid(row=1, column=1, pady=5, padx=5)

def LoginButton():
    password_output = password.get()
    login_output = login.get()
    output = {'type': '0', 'login': login_output, 'password': password_output}
    output = json.dumps(output)
    client.send(output.encode('utf8'))
    answer = client.recv(1024).decode('utf8')
    if answer == '0':
        tkinter.Label(log_window, text='Konto nie jest aktywne. Aktywuj konto, aby się zalogować').grid(row=6, column=1)
        Login()
    user_json = client.recv(1024).decode('utf8')
    user = json.loads(user_json)
    global id
    global token
    id = user['id']
    token = user['token']
    Main()
def RegisterButton():
    login_output=login.get()
    email_output=email.get()
    phone_output=phone.get()
    password_output=password.get()
    confirm_password_output=confirm_password.get()

    confirm = True

    if len(login_output)==0 or len(email_output)==0 or len(phone_output)==0 or len(password_output)==0 or len(confirm_password_output)==0:
        confirm = False
        tkinter.Label(register_window, text = 'Wszytkie pola muszą zostać wypełnione').grid(row=6, column=1)
        Register()
    if password_output!=confirm_password_output:
        confirm = False
        tkinter.Label(register_window, text = 'Hasła nie są takie same').grid(row=6, column=1)
        Register()
    if email_output.count('@')!=1:
        confirm = False
        tkinter.Label(register_window, text = 'Wprowadź poprawny adres e-mail').grid(row=6, column=1)
        Register()

    if confirm==True:
        output = {'type': '1', 'login' : login_output, 'email' : email_output, 'phone' : phone_output, 'password' : password_output}
        output = json.dumps(output)
        client.send(output.encode('utf8'))

    answer = client.recv(1024).decode('utf8')
    print(answer)
    if answer == '1':
        confirm = False
        tkinter.Label(register_window, text='Login jest już zajęty. Wprowadź inny').grid(row=6, column=1)
        Register()
def Login():
    menu.destroy()
    global log_window
    log_window = tkinter.Tk()
    log_window.geometry('480x450')
    log_window.title('logowanie')

    tkinter.Label(log_window, text='Login').grid(row=0, column=0, pady=5, padx=5)
    global login
    login = tkinter.Entry(log_window)
    login.grid(row=0, column=1, pady=5)

    tkinter.Label(log_window, text='Hasło').grid(row=1, column=0, pady=5, padx=5)
    global password
    password = tkinter.Entry(log_window)
    password.grid(row=1, column=1, pady=5)

    tkinter.Button(log_window, text='zaloguj', command=LoginButton).grid(row=2, column=0, pady=5, padx=5)

    log_window.mainloop()
def Register():
    menu.destroy()
    global register_window
    register_window = tkinter.Tk()
    register_window.geometry('480x250')
    register_window.title('rejestracja')

    tkinter.Label(register_window, text='Login').grid(row=0, column=0, pady=5, padx=5)
    global login
    login = tkinter.Entry(register_window)
    login.grid(row=0, column=1, pady=5, padx=5)

    tkinter.Label(register_window, text='adres e-mail').grid(row=1, column=0, pady=5, padx=5)
    global email
    email = tkinter.Entry(register_window)
    email.grid(row=1, column=1, pady=5, padx=5)

    tkinter.Label(register_window, text='numer telefonu').grid(row=2, column=0, pady=5, padx=5)
    global phone
    phone = tkinter.Entry(register_window)
    phone.grid(row=2, column=1, pady=5, padx=5)

    tkinter.Label(register_window, text='hasło').grid(row=3, column=0, pady=5, padx=5)
    global password
    password = tkinter.Entry(register_window)
    password.grid(row=3, column=1, pady=5, padx=5)

    tkinter.Label(register_window, text='potwierdź hasło').grid(row=4, column=0, pady=5, padx=5)
    global confirm_password
    confirm_password = tkinter.Entry(register_window)
    confirm_password.grid(row=4, column=1, pady=5, padx=5)

    tkinter.Button(register_window, text='zarejestruj', command=RegisterButton).grid(row=5, column=1, pady=5, padx=5)





host  = '127.0.0.1'
port = 5000

client = s.socket(s.AF_INET, s.SOCK_STREAM)
client.connect((host, port))

menu = tkinter.Tk()
menu.geometry('180x80')
menu.title('klientGUI v2')

tkinter.Button(menu, text='logowanie', command=Login).grid(row=0, column=0, pady=10, padx=10)
tkinter.Button(menu, text='rejestracja', command=Register).grid(row=0, column=1, pady=10, padx=10)

menu.mainloop()