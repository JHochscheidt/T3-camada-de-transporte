import sys  ## import modulo
import os ## import modulo do SO para trabalhar com funcionalidades que dependem do SO
import socket

# tornar o programa executavel
#!/usr/bin/python

#acentuacoes
# -*- coding: utf-8 -*-

# Funcao que mostra como deve ser a entrada, caso ocorra algum erro
def informacoesEntrada():
	print("Argumentos:")
	print("python "+__file__+" <IPServer> <porta> <caminho_do_arquivo_coordenadas.csv>")
	sys.exit()

def enviarDados(IPServer, porta, caminhoArquivo):
    mensagem = socket_tcp_cliente.recv(4096)
    if(mensagem == "PRONTO"):
        # servidor esta pronto para receber dados
        try:
            print "Enviando arquivo para " + IPServer + ":" + str(porta)
            arquivo = open(caminhoArquivo, 'r')
            dados = arquivo.read();
            socket_tcp_cliente.send(dados)
            while dados != "":
                dados = arquivo.read();
                socket_tcp_cliente.send(dados)
            socket_tcp_cliente.send("***EOF***")
            arquivo.close()
            msg_enviado = socket_tcp_cliente.recv(4096)
            if(msg_enviado == "DOWNLOAD CONCLUIDO"):
                ### aqui fazer metodo que le o arquivo gerado no servidor que sera enviado de volta para o cliente
                msg_processamento = socket_tcp_cliente.recv(4096)
                if(msg_processamento == "PROCESSAMENTO CONCLUIDO"):
                    socket_tcp_cliente.send("PRONTO PARA RECEBER")
                    receberDados(caminhoArquivo)
                else:
                    print "NAO FOI POSSIVEL PROCESSAR DADOS"

            else:
                print "Erro ao enviar o arquivo"
                socket_tcp_cliente.close()


        except Exception as msg:
            print("Error message: "+str(msg))
            return False
        return True
    elif(mensagem == "ERRO"):
        print "servidor nao permitiu conexao por algum motivo"
        return False

    else:
        print "Algum erro" + mensagem
        return False

def receberDados(caminhoArquivo):
    caminhoArquivo = "SAIDA" + caminhoArquivo
    try:
        arq_temp = open(caminhoArquivo, 'wb')
        #socket_tcp_cliente.send("PRONTO")
        print "Baixando arquivo..."

        while 1:
            dados = socket_tcp_cliente.recv(4096)
            print dados
            if(dados == "***EOF***"):
                print "Fechando arquivo..."
                arq_temp.close()
                print "Arquivo fechado"
                break
            else:
                print "Escrevendo"
                arq_temp.write(dados)

        socket_tcp_cliente.send("DOWNLOAD CONCLUIDO")
        #print "Download de arquivo concluido"

    except Exception as msg:
        socket_tcp_cliente.send("ERROR")
        #File Error.
        print("Error message: "+str(msg))
        return

# Funcao para enviar o arquivo para o servidor
#def enviarArquivo(IPServer, porta, caminhoArquivo):
#    socket.sendfile(caminhoArquivo)

# Le os argumentos da linha de comando, caso houver algum erro nos parametros, exibe mensagem de ajuda de como deve ser a entrada
try:
	IPServer = sys.argv[1]
	porta = int(sys.argv[2])
	caminhoArquivo = sys.argv[3]
except:
	informacoesEntrada()


socket_tcp_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#If the file exists
#Start the connection with the server
if (os.path.exists(caminhoArquivo)):
	try:
		socket_tcp_cliente.connect((IPServer, int(porta)))
		print "Conectado ao servidor " + IPServer + ":" + str(porta)
	except socket.error as msg:
		print "Nao foi possivel conexao com o servidor " + IPServer + ":" + str(porta)
		print msg
		sys.exit()

        socket_tcp_cliente.send("PRONTO PARA ENVIAR ARQUIVO")
        enviarDados(IPServer,porta,caminhoArquivo)

else:
	print("File does not exists.")
	sys.exit()
