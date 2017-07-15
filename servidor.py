import os ## import modulo do SO para trabalhar com funcionalidades que dependem do SO
import socket
import sys
import thread
import time
from math import radians, cos, sin, asin, sqrt
# tornar o programa executavel
#!/usr/bin/python

#acentuacoes
#-*- coding: iso-8859-1 -*-

# Echo server program
HOST = ''
PORT = int(sys.argv[1])

## funcao de haversine, que calcula a distancia entre dois pontos
def haversine(lat1,long1,lat2,long2):
    RAIO_PLANETA_TERRA = 6371  # in km
    # convert all latitudes/longitudes from decimal degrees to radians
    lat1, long1, lat2, long2 = map(radians, (lat1, long1, lat2, long2))
    # calculate haversine
    latitude = lat2 - lat1
    longitude = long2 - long1
    d = sin(latitude * 0.5) ** 2 + cos(lat1) * cos(lat2) * sin(longitude * 0.5) ** 2
    h = 2 * RAIO_PLANETA_TERRA * asin(sqrt(d))
    return h

# funcao que faz o processamento dos dados enviados pelo cliente
def processarArquivo(conexao, arquivo_temporario):
    print (">>>Processando dados...")
    try:
        arq_temp = open(arquivo_temporario, 'r')
        saida_temp = "SAIDA_" + arquivo_temporario
        arquivo_saida = open (saida_temp, 'w')
        ### processa linha por linha e escreve no arquivo de saida
        for linha in arq_temp:
            linhaTemp = linha[0:-1] ### remover /n do final
            separarVirgula = linhaTemp.split(',') #separar valores
            #tirar todos os espacos
            lat1 = separarVirgula[0].split()
            long1 = separarVirgula[1].split()
            lat2 = separarVirgula[2].split()
            long2 = separarVirgula[3].split()
            #cast pra float
            lat1 = float(lat1[0])
            long1 = float(long1[0])
            lat2 = float(lat2[0])
            long2 = float(long2[0])
            distancia = haversine(lat1,long1,lat2,long2) ### tratar dados
            saida = str(lat1) + ", " + str(long1) + ", " + str(lat2) + ", " + str(long2) + ", " + str(distancia) + "\n" ### escrever as coordenadas e a distancia no arquivo
            arquivo_saida.write(saida)
        arq_temp.close()
        os.remove(arquivo_temporario)
        arquivo_saida.close()
    except:
        print (">>>Erro ao abrir arquivo")
        sys.exit()

# funcao que faz a comunicacao com o cliente fazendo a leitura do arquivo ( que o cliente esta enviando ao server)
def receberDados(conexao, caminhoArquivo):
    arquivo_temporario = caminhoArquivo + "fileTemp.csv"
    try:
        arq_temp = open(arquivo_temporario, 'w')
        while 1:
            dados = conexao.recv(4096)
            if(dados == "EOF"):
                arq_temp.close()
                break
            arq_temp.write(dados)
        conexao.send("DOWNLOAD CONCLUIDO")
        processarArquivo(conexao, arquivo_temporario)
        conexao.send("PROCESSAMENTO CONCLUIDO")
    except Exception as msg:
        conexao.send("ERRO") #File Error.
        print(">>>Error message: "+str(msg))
        return

# funcao com a conexao com o cliente, depois de iniciada a thread
def CONEXAO(conexao, endereco_cliente):
    mensagem = conexao.recv(512)
    if (mensagem=="ENVIANDO DADOS"):
        conexao.send("PRONTO PARA RECEBER DADOS")
        caminhoArquivo = str(endereco_cliente[1])
        receberDados(conexao, caminhoArquivo)
        msg_retorno = conexao.recv(512)
        if(msg_retorno == "PRONTO PARA RECEBER RESPOSTA"):
            enviarDados(conexao, caminhoArquivo, endereco_cliente)
    else:
        conexao.close()
    thread.exit()

def enviarDados(conexao, caminhoArquivo, endereco_cliente):
    print (">>>Enviando dados para cliente...")
    caminhoArquivo = "SAIDA_" + caminhoArquivo + "fileTemp.csv"
    try:
        arquivo = open(caminhoArquivo, 'r')
        dados = arquivo.read()
        conexao.send(dados)
        while dados != "":
            #print ('[' + dados + ']')
            dados = arquivo.read();
            conexao.send(dados)
        conexao.send("EOF")
        arquivo.close()
        os.remove(caminhoArquivo) #para remover o arquivo temporario do diretorio
        msg_download_concluido = conexao.recv(512)
        if(msg_download_concluido == "DOWNLOAD CONCLUIDO"):
            print (">>>Encerrando conexao...")
            conexao.close()
            time.sleep(5)
            print (">>>Conexao com " + str(endereco_cliente) + " encerrada!")
        else:
            print (">>>DOWNLOAD NAO CONCLUIDO")
            #fechar conexao igual
        conexao.close()
    except:
        print (">>>Erro ao enviar resultado para o cliente")
        return False
    return True

### cria socket Ipv4
socket_tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#para zerar o TIME_WAIT do socket
socket_tcp_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
### aciona porta para ouvir
try:
    socket_tcp_server.bind((HOST, PORT))
    print (">>>Porta " + str(PORT) + " ativa")
except socket.error as msg:
    print (">>>Erro bind")
    print (">>>" + msg)

try:
    socket_tcp_server.listen(5)
    print (">>>Ouvindo...")

except socket.error as msg:
    print (">>>"+msg)
    print (">>>Erro listen")

try:
    while 1:
        conexao, endereco_cliente = socket_tcp_server.accept()
        print (">>>Conexao TCP ativa com " + str(endereco_cliente))

        #cria thread para cada cliente q solicitar conexao
        thread.start_new_thread(CONEXAO , tuple([conexao, endereco_cliente]))

except KeyboardInterrupt:
    print(">>>Parando de ouvir e encerrando conexao TCP")
    socket_tcp_server.close()
    sys.exit()
