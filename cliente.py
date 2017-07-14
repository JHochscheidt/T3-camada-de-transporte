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
	print("python "+__file__+" <IPServer> <porta> <caminho_do_arquivo_coordenadas>")
	sys.exit()

def enviarDados(IPServer, porta, caminhoArquivo):
	mensagem = socket_tcp_cliente.recv(4096)
	if(mensagem == "PRONTO PARA RECEBER DADOS"):
		try:
			print "Enviando arquivo para " + IPServer + ":" + str(porta)
			arquivo = open(caminhoArquivo, 'r')
			dados = arquivo.read();
			socket_tcp_cliente.send(dados)
			while dados != "":
				dados = arquivo.read();
				socket_tcp_cliente.send(dados)
			# pra "avisar ao servidor que terminou o arquivo"
			socket_tcp_cliente.send("EOF")
			print "fim arquivo"
			arquivo.close()

			msg_concluido = socket_tcp_cliente.recv(4096)
			if(msg_concluido == "DOWNLOAD CONCLUIDO"):
				print "cliente baixou arquivo"
				msg_processamento = socket_tcp_cliente.recv(4096)
				if(msg_processamento == "PROCESSAMENTO CONCLUIDO"):
					socket_tcp_cliente.send("PRONTO PARA RECEBER RESPOSTA")
					print "cliente pronto para receber resposta"
					receberDados(caminhoArquivo)
				else:
					print "NAO FOI POSSIVEL PROCESSAR DADOS"
			else:
				print "Erro ao enviar o arquivo"
				#socket_tcp_cliente.close()
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
	print "pronto para receber"
	try:
		arq_temp = open(caminhoArquivo, 'w')
		while True:
			dados = socket_tcp_cliente.recv(4096)
			if(dados == "EOF"):
				arq_temp.close()
				break
			arq_temp.write(dados)
		socket_tcp_cliente.send("DOWNLOAD CONCLUIDO")
		socket_tcp_cliente.close()
	except Exception as msg:
		print("Error message: "+str(msg))
		return False

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

	socket_tcp_cliente.send("ENVIANDO DADOS")
	enviarDados(IPServer,porta,caminhoArquivo)

else:
	print("File does not exists.")
	sys.exit()
