import sys  ## import modulo
import os ## import modulo do SO para trabalhar com funcionalidades que dependem do SO
import socket
import thread
import uuid
from math import radians, cos, sin, asin, sqrt
# tornar o programa executavel
#!/usr/bin/python

#acentuacoes
#-*- coding: iso-8859-1 -*-

# Echo server program
HOST = ''
PORT = 8095              # Arbitrary non-privileged port

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
    print "processando dados"
    try:
        arq_temp = open(arquivo_temporario, 'r')
        print "nome arquivo temporario --->", arquivo_temporario
        saida_temp = "SAIDA_" + arquivo_temporario
        print saida_temp
        arquivo_saida = open (saida_temp, 'w')
        ### processa linha por linha e escreve no arquivo de saida

        for linha in arq_temp:
            ### remover /n do final
            linhaTemp = linha[0:-1]
            #separar valores
            separarVirgula = linhaTemp.split(',')
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
            ### tratar dados
            distancia = haversine(lat1,long1,lat2,long2)
            ### escrever as coordenadas e a distancia no arquivo
            saida = str(lat1) + "," + str(long1) + "," + str(lat2) + "," + str(long2) + "," + str(distancia) + "\n"
            arquivo_saida.write(saida)
        arq_temp.close()
        arquivo_saida.close()
    except:
        print "Erro ao abrir arquivo"
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

        ## processar dados do "fileTemp.csv aqui"
        processarArquivo(conexao, arquivo_temporario)
        ## enviar para o cliente o resultado
        conexao.send("PROCESSAMENTO CONCLUIDO")
    except Exception as msg:
        conexao.send("ERROR")
        #File Error.
        print("Error message: "+str(msg))
        return

# funcao inicia uma nova thread para conexao
def infoConexao(conexao, endereco_cliente):
    mensagem = conexao.recv(1024)
    if (mensagem=="ENVIANDO DADOS"):
        print "Conexao estabelecida com " + str(endereco_cliente)
        conexao.send("PRONTO PARA RECEBER DADOS")
        caminhoArquivo = str(endereco_cliente[1])
        receberDados(conexao, caminhoArquivo)

        msg_retorno = conexao.recv(1024)
        if(msg_retorno == "PRONTO PARA RECEBER RESPOSTA"):
            enviarDados(conexao, caminhoArquivo)
    else:
        conexao.close()
    thread.exit()

def enviarDados(conexao, caminhoArquivo):
    print "Enviando dados cliente"
    caminhoArquivo = "SAIDA_" + caminhoArquivo + "fileTemp.csv"
    print "aqui tem corrage ----> " + caminhoArquivo
    try:
        arquivo = open(caminhoArquivo, 'r')
        dados = arquivo.read()
        conexao.send(dados)
        while dados != "":
            print '[' + dados + ']'
            dados = arquivo.read();
            conexao.send(dados)
        conexao.send("EOF")
        arquivo.close()

        msg_download_concluido = conexao.recv(4096)
        if(msg_download_concluido == "DOWNLOAD CONCLUIDO"):
            print "Encerrar conexao"
            conexao.close()
        else:
            print "DOWNLOAD NAO CONCLUIDO"
            #fechar conexao igual

        conexao.close()
    except:
        print "ALGUM ERRO"
        return False
    return True

### cria socket Ipv4
socket_tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#para zerar o TIME_WAIT do socket
socket_tcp_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


### aciona porta para ouvir

try:
    socket_tcp_server.bind((HOST, PORT))
    print "Porta ativa - ouvindo"
except socket.error as msg:
    print "Erro bind"
    print msg

try:
    socket_tcp_server.listen(5)
    print "Ouvindo..."

except socket.error as msg:
    print msg
    print "Erro listen"


try:
    while 1:
        conexao, endereco_cliente = socket_tcp_server.accept()
        print 'Conectado por ', endereco_cliente
        ##A thread will be create for each connection
        #so, more than one client can be attended
        thread.start_new_thread(infoConexao, tuple([conexao, endereco_cliente]))

except KeyboardInterrupt:
    print("")
    print("Stop listening and TCP closed.")
    socket_tcp_server.close()
    sys.exit()
