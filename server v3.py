import socket as s
import json
import uuid
import mysql.connector
import random
import threading

def recive(user):
        while True:
                message = client.recv(1024).decode('utf8')
                message = json.loads(message)
                if message['type'] == '2':
                        print(message['message'])
def login_user(user):
        question = client.recv(1024).decode('utf8')
        question = json.loads(question)
        if get_mac_address() == user['mac_adr']:
                print(True)
                cursor = data_base.cursor(buffered=True)
                query_serch_user = "SELECT id, login FROM users WHERE login LIKE '%{0}%'".format(question['input'])
                cursor.execute(query_serch_user)
                data_base.commit()
                result = cursor.fetchall()
                result_str = ''
                for i in result:
                        result_str += str(i[0])
                        result_str += ':'
                        result_str += i[1]
                        result_str += ' '
                answer = client.send(result_str.encode('utf8'))
                recive(user)

def get_mac_address():
    mac=uuid.UUID(int = uuid.getnode()).hex[-12:]
    return ":".join([mac[e:e+2] for e in range(0,11,2)])
def check_login(login):
        cursor = data_base.cursor(buffered=True)
        query_check_login = "SELECT * FROM users WHERE login = '{0}'".format(login)
        cursor.execute(query_check_login)
        data_base.commit()
        result = cursor.fetchall()
        if result == []:
                return '0'
        else:
                return '1'
def register(question):
        login = question['login']
        password = question['password']
        email = question['email']
        phone = question['phone']
        check = check_login(login)
        answer = client.send(check.encode('utf8'))
        if check == '0':
                cursor = data_base.cursor()
                query_add_user = "INSERT INTO users(id, login, password, email, phone, active) VALUES (NULL, %s, %s, %s, %s, 0)"
                val = (login, password, email, phone)
                cursor.execute(query_add_user, val)
                data_base.commit()
def login(question):
        login = question['login']
        password = question['password']
        cursor = data_base.cursor(buffered=True)
        query_check_user = "SELECT * FROM users WHERE login = '{0}'".format(login)
        cursor.execute(query_check_user)
        data_base.commit()
        result = cursor.fetchall()
        for i in result:
                tuple = i
                id_data = tuple[0]
                login_data = tuple[1]
                password_data = tuple[2]
                email_data = tuple[3]
                if login == login_data or login == email_data and password == password_data:
                        active = tuple[5]
                        if active == 1:
                                answer = client.send('1'.encode('utf8'))
                                token = ''
                                for i in range(6):
                                        token += str(random.randrange(0,9))
                                mac_adr = get_mac_address()
                                user = {'id': id_data, 'token': token, 'mac_adr': mac_adr}
                                user_send = {'id': id_data, 'token': token}
                                user_send = json.dumps(user)
                                answer = client.send(user_send.encode('utf8'))
                                login_user(user)
                        else:
                                answer = client.send('0'.encode('utf8'))



host = '127.0.0.1'
port = 5000

server_socket = s.socket(s.AF_INET, s.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen(5)

while True:
        data_base = mysql.connector.connect(user='root', host='127.0.0.1', database='komunikator',auth_plugin='mysql_native')
        client,addr = server_socket.accept()
        print('Nowe połącznie z', addr)

        question = client.recv(1024).decode('utf8')
        question = json.loads(question)

        if question['type'] == '1':
                register(question)
        elif question['type'] == '0':
                login(question)


        data_base.close()
        client.close()

        print('Polaczenie zakonczone')b