
import socket
import time
import json

# printa funcoes disponiveis
def printFuncoes():
    sen = "sen(x) - retorna o valor (arredondado) do seno de x radianos (float), sendo x um número real (float)\n"
    cos = "cos(x) - retorna o valor (arredondado) do cosseno de x radianos (float), sendo x um número real (float)\n"
    tan = "tan(x) - retorna a valor (arredondado) da tangente de x radianos (flaot), sendo x número real (float)\n\n"
    info = "digite 'funcoes()' para ver as funções disponíveis e 'quit()', para sair do programa"
    print("\n\n" + "     RPC - FUNÇÕES TRIGONOMÉTRICAS     ".center(len(cos), "#") + "\n")
    print("Funções Disponíveis: ")
    print(sen+cos+tan+info)

# verifica se há os parentesis ou chaves do input estão fechados
def loopCheckEntrada(en):
    count = 0
    for char in en:
        if char == '(' or char == "[":
            count += 1
        elif char == ')' or char == "]":
            count -= 1
        if count < 0:
            return False
    return (count == 0)

# verifica a entrada, tratando os casos de inputs inválidos
def verificaEntrada(en):
    if (en == "q" or en == "Q" or en == "F" or en == "f"):
        return en

    elif (en == "" or en.isspace()):
        return False

    elif ((not en[0].isalpha)):
        print("NameError: Função não reconhecida")
        return False

    elif ((en.split("(")[0] not in funcoes)):
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
    socketCliente.connect(('192.168.0.22', 4900))
    # cria requisição
    rqst = {
        "nome": "sen",
        "parametro": x
    }
    # converte requisição para json e converte para bytes
    rqstBytes = json.dumps(rqst).encode("utf-8")
    
    socketCliente.send(rqstBytes)  # envia requisição
    respBytes = socketCliente.recv(256).decode(
        "utf-8")  # recebe resposta e converte
    resp = json.loads(respBytes)["retorno"]  # pega retorno da funcao
    socketCliente.close()
    return resp

# funçao stub cosseno - mesma coisa do seno
def cos(x: float) -> float:
    # cria e configura socket
    socketCliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socketCliente.connect(('192.168.0.22', 4900))
    # cria requisição
    rqst = {
        "nome": "sen",
        "parametro": x
    }
    # converte requisição para json e converte para bytes
    rqstBytes = json.dumps(rqst).encode("utf-8")

    socketCliente.send(rqstBytes)  # envia requisição
    respBytes = socketCliente.recv(256).decode(
        "utf-8")  # recebe resposta e converte
    resp = json.loads(respBytes)["retorno"]  # pega retorno da funcao
    socketCliente.close()
    return resp

# funcao stub tangente


def tan(x: float) -> float:
    # cria e configura socket
    socketCliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socketCliente.connect(('192.168.0.22', 4900))
    # cria requisição
    rqst = {
        "nome": "sen",
        "parametro": x
    }
    # converte requisição para json e converte para bytes
    rqstBytes = json.dumps(rqst).encode("utf-8")
    
    socketCliente.settimeout(3)
    tentativas = 0
    resp = ""
    
    while(tentativas < 3):
        tentativas += 1
        try:
            socketCliente.send(rqstBytes)  # envia requisição
            respBytes = socketCliente.recv(256).decode(
                "utf-8")  # recebe resposta e converte
            resp = json.loads(respBytes)["retorno"]  # pega retorno da funcao
            if(resp != ""):
                break
        except TimeoutError as e:  #sem resposta
            pass
        time.sleep(1)
            
    
        
        
        
    socketCliente.close()
    print(tentativas)   #mosta o numero de tentativas que foram feitas. ta aqui so pra teste
    if(resp != ""):
        return resp
    else:
        return False
    


# variavel global lista com as funções possiveis
funcoes = ["sen", "cos", "tan", "quit", "funcoes"]

# funcao principal
def main():
    printFuncoes()
    print(">>> ", end="")
    while True:  # laço principal do programa
        en = verificaEntrada(input())
        resposta = False
        if (not en):
            pass
        elif (en == "q" or en == "Q" or en[0:4] == "quit"):
            break
        elif (en == "f" or en == "F" or en[0:8] == "funcoes"):
            printFuncoes()
        else:  # bloco onde a aplicação tenta executar o input já tratado
            try:
                resposta = eval(en)  # eval executa as funções stubs
            except Exception as e:
                print(f"Error: {e}")
            if(resposta == False):
                print("servidor não está respondendo")
            else:
                print(resposta)
        print(">>> ", end="")


# inicia função princiapl
if __name__ == "__main__":
    main()
