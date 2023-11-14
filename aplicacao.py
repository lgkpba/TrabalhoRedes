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


        
def cliente():  #essa primeira parte inicia a conexao com o servidor
    # Recupera endereço do servidor
    socket_cliente_thread = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    nome_servidor = socket.gethostname()
    ip_servidor = socket.gethostbyname_ex(nome_servidor)
    print(ip_servidor)

    # coloca a thread para dormir por dois segundos enquanto o servidor é iniciado
    time.sleep(2)
    socket_cliente_thread.connect(('192.168.0.22', 3213))

    print("Cliente:", socket_cliente_thread)
    def receber():
        while True:
            try:
                mensagem = socket_cliente_thread.recv(512) # aguarda por comando
            except TimeoutError as e:
                print(f"Cliente {enderecoDoCliente} não enviou mensagens nos últimos 10 minutos. Encerrando a conexão")
                socket_cliente_thread.close()
                break # quebra o loop infinito e termina a thread
            except Exception as e:
                print(f"Cliente {enderecoDoCliente} fechou a conexão com exceção: {e}")
                break

            # Se a mensagem for vazia, espere a próxima
            if len(mensagem) != 0:
                retries = 3
                return mensagem
            else:
                retries -= 1
                if retries == 0:
                    break
                continue
            
            
    def click_acessar():
        def click_confirma_acesso():
            nome = txt_box.get("1.0", "end-1c")
            msg = {"nome" : nome,
                   "operação": 2}
            mensagem = json.dumps(msg).encode("utf-8")
            socket_cliente_thread.send(mensagem)
            resposta = receber()
            
            resposta_decode = json.loads(resposta.decode("utf-8"))
            
            if resposta_decode == "conectando...":
                print ("conexão bem sucedida")
            else:
                print("tente outro nome")
            
        
        tela_acessar = Tk()
        
        confirma_acesso = Button(tela_acessar,
                                 text = "confirmar",
                                 command = click_confirma_acesso)
        txt_box = Text(tela_acessar,height = 1, width = 25)
        
        txt_box.pack()
        confirma_acesso.pack()
        tela_acessar.mainloop()
    
    def end():  #função q encerra a conexao
        msg = {"nome" : "",
                "operação" : 0}
        mensagem = json.dumps(msg).encode("utf-8")
        socket_cliente_thread.send(mensagem)
    
    def click_criar(): #função pra criar cliente
        def click_confirmar(): #função pra confirmar a criação do cliente
            nome = txt_box.get("1.0", "end-1c")
            print(nome)
            msg = {"nome" : nome,
                   "operação" : 1}
            mensagem = json.dumps(msg).encode("utf-8")
            socket_cliente_thread.send(mensagem)
        
        
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
    botao_acessar = Button(tela_inicial,
                           text = "acessar",
                           command = click_acessar)
    botao_acessar.pack()
    
    tela_inicial.mainloop()
    

threadPool = ThreadPoolExecutor()
threadPool.submit(cliente())
socket_cliente_thread.close()  #fecha a thread do socket se fechar o programa
