import socket
import time
import json

# printa funcoes disponiveis
def printFuncoes():
    sen = "sen(x) - retorna o valor (arredondado) do seno de x radianos (float), sendo x um número real (float)\n"
    cos = "cos(x) - retorna o valor (arredondado) do cosseno de x radianos (float), sendo x um número real (float)\n"
    tan = "tan(x) - retorna a valor (arredondado) da tangente de x radianos (flaot), sendo x número real (float)\n\n"
    info = "digite 'funcoes' para ver as funções disponíveis e 'quit', para sair do programa"
    print("\n\n" + "     RPC - FUNÇÕES TRIGONOMÉTRICAS     ".center(len(cos), "#") + "\n")
    print("Funções Disponíveis: ")
    print(sen+cos+tan+info)

# verifica se há os parentesis ou chaves do input estão fechados
def loopCheckEntrada(en):
    count = 0
    for char in en:
        if char == "(" or char == "[":
            count += 1
        elif char == ")" or char == "]":
            count -= 1
        if count < 0:
            return False
    return (count == 0)

# verifica a entrada, tratando os casos de inputs inválidos
def verificaEntrada(en):
    if (en == "q" or en == "Q" or en == "F" or en == "f" or en == "funcoes"):
        return en

    elif (en == "" or en.isspace()):
        return False

    elif ((not en[0].isalpha)):
        print("NameError: Função não reconhecida")
        return False

    elif ((en.split("(")[0] not in funcoesLista)):
        print("NameError: Função não reconhecida")
        return False

    elif (not loopCheckEntrada(en)):
        print("NameError: Função não reconhecida")
        return False

    return en

# funçoes stub - todas tentam se comunicar com o servidor atraves de pacotes json

# funçao stub seno
def sen(x: float) -> float:
    # cria e configura socket
    socketCliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socketCliente.connect(('localhost', 4900))
    # cria requisição
    rqst = {
        "nome": "sen",
        "parametro": x
    }
    # converte requisição para json e converte para bytes
    rqstBytes = json.dumps(rqst).encode("utf-8")

    socketCliente.settimeout(3)
    tentativas = 0
    resp = None

    while (tentativas < 3):
        tentativas += 1
        try:
            socketCliente.send(rqstBytes)  # envia requisição
            respBytes = socketCliente.recv(256).decode("utf-8")  # recebe resposta e converte
            resp = json.loads(respBytes)["retorno"]  # pega retorno da funcao
            if (resp is not None):
                break
        except TimeoutError as e:  # sem resposta
            pass
        time.sleep(1)

    fim = json.loads(respBytes)["fim"]
    
    if(fim == "///"):
        socketCliente.close()
    # print(tentativas)   #mosta o numero de tentativas que foram feitas. ta aqui so pra teste
    if (resp is not None):
        return resp
    else:
        return False


# funçao stub cosseno - mesma coisa do seno
def cos(x: float) -> float:
    # cria e configura socket
    socketCliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socketCliente.connect(('localhost', 4900))
    # cria requisição
    rqst = {
        "nome": "cos",
        "parametro": x
    }
    # converte requisição para json e converte para bytes
    rqstBytes = json.dumps(rqst).encode("utf-8")

    socketCliente.settimeout(3)
    tentativas = 0
    resp = None

    while (tentativas < 3):
        tentativas += 1
        try:
            socketCliente.send(rqstBytes)  # envia requisição
            respBytes = socketCliente.recv(256).decode(
                "utf-8")  # recebe resposta e converte
            resp = json.loads(respBytes)["retorno"]  # pega retorno da funcao
            if (resp is not None):
                break
        except TimeoutError as e:  # sem resposta
            pass
        time.sleep(1)
    
    fim = json.loads(respBytes)["fim"]
    
    if(fim == "///"):
        socketCliente.close()

    # print(tentativas)   #mosta o numero de tentativas que foram feitas. ta aqui so pra teste
    if (resp is not None):
        return resp
    else:
        return False


# funcao stub tangente
def tan(x: float) -> float:
    # cria e configura socket
    socketCliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socketCliente.connect(('localhost', 4900))
    # cria requisição
    rqst = {
        "nome": "tan",
        "parametro": x
    }
    # converte requisição para json e converte para bytes
    rqstBytes = json.dumps(rqst).encode("utf-8")

    socketCliente.settimeout(3)
    tentativas = 0
    resp = None

    while (tentativas < 3):
        tentativas += 1
        try:
            socketCliente.send(rqstBytes)  # envia requisição
            respBytes = socketCliente.recv(256).decode(
                "utf-8")  # recebe resposta e converte
            resp = json.loads(respBytes)["retorno"]  # pega retorno da funcao
            if (resp is not None):
                break
        except TimeoutError:  # sem resposta
            pass
        time.sleep(1)

    fim = json.loads(respBytes)["fim"]
    
    if(fim == "///"):
        socketCliente.close()
    # print(tentativas)   #mosta o numero de tentativas que foram feitas. ta aqui so pra teste
    if (resp is not None):
        return resp
    else:
        return False

# variavel global lista com as funções possiveis
funcoesLista = ["sen", "cos", "tan", "quit", "funcoes"]

# funcao principal
def main():
    printFuncoes()
    print(">>> ", end="")
    while True:  # laço principal do programa
        en = verificaEntrada(input())
        resposta = False
        if (not en):
            pass
        elif (en == "q" or en == "Q" or en == "quit"):
            break
        elif (en == "f" or en == "F" or en == "funcoes"):
            printFuncoes()
        else:  # bloco onde a aplicação tenta executar o input já tratado
            try:
                resposta = eval(en)  # eval executa as funções stubs
            except Exception as e:
                resposta = f"Error: {e}"
            if (resposta == False and type(resposta) == bool): # respsta = 0.0 tb dava False
                resposta = "Error: Servidor não está respondendo"
            print(resposta)
        print(">>> ", end="")


# inicia função princiapl
if __name__ == "__main__":
    main()
