import wave
import sys
import pyaudio
import socket,os
import threading,pickle,struct
import time, queue
from concurrent.futures import ThreadPoolExecutor
import json
from threading import Thread


lista_clientes = [];

class Cliente_criado():
    def __init__(self,nome):
        self.nome = nome;
        
    def set_nome(self, nome):
        self.nome = nome;
        


class ServidorAtendimento:
    def __init__(self, endereco_servidor="0.0.0.0", porta_servidor=3213, max_conexoes=5):
        # Procedimento de criação do socket e configuração
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((endereco_servidor, porta_servidor))
        self.socket.listen(max_conexoes)

        # Registro de thread para atendimento e registros de usuários
        self.threadClientes = {}
        self.registrosDeUsuarios = {}

        # Inicia uma thread dedicada para escuta de novas conexões
        self.threadEscuta = Thread(target=self.implementacaoThreadEscuta)
        self.threadEscuta.run()

    def handlerDeMensagem(self, mensagem):
        return mensagem

    def implementacaoThreadCliente(self, enderecoDoCliente, socketParaCliente):
        retries = 3
        socketParaCliente.settimeout(10) # timout de 10 segundos

        while True:
            try:
                mensagem = socketParaCliente.recv(512) # aguarda por comando
            except TimeoutError as e:
                print(f"Cliente {enderecoDoCliente} não enviou mensagens nos últimos 10 minutos. Encerrando a conexão")
                socketParaCliente.close() # fecha a conexão com o cliente pelo lado do servidor
                break # quebra o loop infinito e termina a thread
            except Exception as e:
                # caso o socket tenha a conexão fechada pelo cliente ou algum outro erro que não timeout
                print(f"Cliente {enderecoDoCliente} fechou a conexão com exceção: {e}")
                break

            # Se a mensagem for vazia, espere a próxima
            if len(mensagem) != 0:
                retries = 3
            else:
                retries -= 1
                if retries == 0:
                    break
                continue


            print(f"Servidor recebeu do cliente {enderecoDoCliente} a mensagem: {json.loads(mensagem.decode('utf-8'))}")

            # Decodifica mensagem em bytes para utf-8 e
            # em seguida decodifica a mensagem em Json para um dicionário Python
            mensagem_decodificada = json.loads(mensagem.decode("utf-8"))

            # Por enquanto, retorna a mensagem recebida
            resposta = self.handlerDeMensagem(mensagem_decodificada)

            # fim do while
            resposta_bytes = json.dumps(resposta).encode("utf-8")

            print(f"Servidor enviou para o cliente {enderecoDoCliente} a mensagem: {resposta}")

            socketParaCliente.send(resposta_bytes)

        # Testaremos apenas com um usuário por servidor
        # Forçaremos a parada da thread de escuta fechando socket



    def implementacaoThreadEscuta(self):
        while True:
            # Thread fica bloqueada enquanto aguarda por conexões,
            # enquanto servidor continua rodando normalmente
            try:
                (socketParaCliente, enderecoDoCliente) = self.socket.accept()
            except OSError:
                # Como fechamos o socket na thread para cliente,
                # quando tentarmos escutar no mesmo socket, ele não mais
                # existirá e lançará um erro
                # Não é isso que servidores de verdade fazem, é só um exemplo
                print(f"Servidor: desligando thread de escuta")
                break
            self.threadClientes[enderecoDoCliente] = Thread(target=self.implementacaoThreadCliente,
                                                            args=(enderecoDoCliente, socketParaCliente),
                                                            daemon=True) # thread sem necessidade de join, será morta ao final do processo
            self.threadClientes[enderecoDoCliente].run() # inicia thread de atendimento ao novo cliente conectado




def novoHandler(self, mensagem_decodificada):
    resposta = ""
    global lista_clientes;
    if(mensagem_decodificada["operação"] == 0):
        resposta = "conexção encerrada"
        self.socket.close();
    if(mensagem_decodificada["operação"] == 1):
        resposta = "cliente cadastrado"
        novo_cliente = Cliente_criado(mensagem_decodificada["nome"])
        lista_clientes.append(novo_cliente)
        for cliente in lista_clientes:
            print (cliente.nome)

    return resposta

# substitui handler padrão por novo
ServidorAtendimento.handlerDeMensagem = novoHandler
# Cria o servidor


servidor = ServidorAtendimento()

