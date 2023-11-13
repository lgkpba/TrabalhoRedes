import wave
import sys
import pyaudio
import socket,os
import threading,pickle,struct
import time, queue
from concurrent.futures import ThreadPoolExecutor
import json
from threading import Thread
from tkinter import *

def end():
    msg = {"nome" : "",
            "operação" : 0}
    threadPool = ThreadPoolExecutor()
    threadPool.submit(cliente(msg))
        
def cliente(mensagem):
    # Recupera endereço do servidor
    socket_cliente_thread = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    nome_servidor = socket.gethostname()
    ip_servidor = socket.gethostbyname_ex(nome_servidor)
    print(ip_servidor)

    # coloca a thread para dormir por dois segundos enquanto o servidor é iniciado
    time.sleep(2)
    socket_cliente_thread.connect(('192.168.0.22', 3213))

    mensagem_bytes = json.dumps(mensagem).encode("utf-8")
    socket_cliente_thread.send(mensagem_bytes)
    msg = socket_cliente_thread.recv(512)
    print("Cliente:", json.loads(msg.decode("utf-8")))
    socket_cliente_thread.close()
    print("Cliente:", socket_cliente_thread)
    
    

def click_criar():
    def click_confirmar():
        nome = txt_box.get("1.0", "end-1c")
        print(nome)
        msg = {"nome" : nome,
               "operação" : 1}
        
        threadPool = ThreadPoolExecutor()
        threadPool.submit(cliente(msg))
        
        
    tela_criar = Tk()
    
    botao_confirmar_usuario = Button(tela_criar,
                                     text = "confirmar",
                                     command = click_confirmar)
    
    
    txt_box = Text(tela_criar,height = 1, width = 25)
    txt_box.pack()
    botao_confirmar_usuario.pack()
    tela_criar.mainloop()
    

tela_inicial = Tk()
botao_criar_usuario = Button(tela_inicial,
                             text = "criar usuário",
                             command = click_criar)
botao_criar_usuario.pack()
botao_encerrar = Button(tela_inicial,
                        text = "encerrar",
                        command = end)

botao_encerrar.pack()
tela_inicial.mainloop()
