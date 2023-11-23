
import socket
import json
import math
import time

# funcao stub seno
def sen(x: float) -> float:
    return math.sin(x)

# funcao stub cosseno
def cos(x: float) -> float:
    return math.cos(x)

# funcao stub tangente
def tan(x: float) -> float:
    return math.tan(x)


# variavel global dicionario com as funcoes
funcoes = {"sen": sen,
           "cos": cos,
           "tan": tan
           }


class Servidor:
    # localhost se comunica com a propria maquina, mudar para o endereço ip real na rede
    def __init__(self, endereco_servidor='localhost', porta_servidor=4900, max_conexoes=1):

        # cria e configura socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # endereço ip 'localhost' e porta 4900
        self.socket.bind((endereco_servidor, porta_servidor))
        # sem conexões simultâneas, servidor simples e humilde que aceita apenas um única conexão
        self.socket.listen(max_conexoes)
        # print(socket.gethostbyname(socket.gethostname())) so pra pegar ip
        self.loopServidor()

    def loopServidor(self):
        while True:
            timeout = 300
            self.socket.settimeout(timeout)  # define espera para conexão
            try:
                # servidor aceita conexão - treeway handshake
                (socketParaCliente, enderecoDoCliente) = self.socket.accept()
                pacote = socketParaCliente.recv(256)  # servidor recebe pacote
            except TimeoutError as e:  # não houve conexão
                print(
                    f"{timeout} segundos se passaram e não houve tentiva de conexão")
                break
            except Exception as e:  # se der erro, deu erro
                print(e)
                break

            # decodifica pacote json em dicionario
            rqst = json.loads(pacote.decode("utf-8"))
            print(
                f"Servidor recebeu do cliente {enderecoDoCliente} a mensagem: {rqst}")
            
            respFalsa = json.dumps("Resposta de mentira").encode("utf-8") # cira uma resposta a mais, apenas para testes
            respBytes = self.handler(rqst).encode("utf-8")  # processa resposta
            
            print(
                    f"Servidor enviou para cliente cliente {enderecoDoCliente} a mensagem: {respBytes.decode('utf-8')}")

            # force_delay = 12
            # time.sleep(force_delay)  # testar o que acontece se a resposta atrasar

            socketParaCliente.send(respBytes) # envia resposta já em bytes
            socketParaCliente.send(respBytes) # envia a resposta mais uma vez, para testes
            socketParaCliente.send(respFalsa) # envia resposta falsa para testes

            # break  # !!!!!! Servidor temrmina após enviar resposta, arrumar dps

    def handler(self, rqst):
        # pega nome e parametro do request
        (nome, param) = (rqst["nome"], rqst["parametro"])
        print(param)

        try:
            rtrn = funcoes[nome](param)  # executa funcao stub localmente
        except TypeError as e:
            param = f"'{param}'"
            rtrn = f"Error: {str(e)}"
        except Exception as e:  # captura erro
            rtrn = f"Error: {str(e)}"

        resp = {
               "chamada": f"{nome}({param})",
               
                "retorno": rtrn,

                "fim": "///"
               }
        print(resp)
        return json.dumps(resp)  # retorna resposta já convertida em json


server = Servidor()
print("SERVIDOR ENCERRADO")
del server  # literalmente apaga o servidor da memória