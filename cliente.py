import sys  ## import modulo
import os ## import modulo do SO para trabalhar com funcionalidades que dependem do SO
import socket
import time

# tornar o programa executavel
#!/usr/bin/python
#acentuacoes
# -*- coding: utf-8 -*-

def enviarDados(IPServer, porta, caminhoArquivo):
	mensagem = socket_tcp_cliente.recv(512)
	if(mensagem == "PRONTO PARA RECEBER DADOS"):
		try:
			print (">>>Enviando arquivo " + caminhoArquivo + " para " + IPServer + ":" + str(porta) + "...")
			arquivo = open(caminhoArquivo, 'r')
			dados = arquivo.read();
			socket_tcp_cliente.send(dados)
			while dados != "":
				dados = arquivo.read();
				socket_tcp_cliente.send(dados)
			socket_tcp_cliente.send("EOF") # pra "avisar ao servidor que terminou o arquivo"
			arquivo.close()
			msg_concluido = socket_tcp_cliente.recv(512)
			if(msg_concluido == "DOWNLOAD CONCLUIDO"): # servidor baixou o arquivo
				msg_processamento = socket_tcp_cliente.recv(512)
				if(msg_processamento == "PROCESSAMENTO CONCLUIDO"): #servidor conclui o processamento dos dados, preparar para receber a saida
					socket_tcp_cliente.send("PRONTO PARA RECEBER RESPOSTA")
					receberDados(caminhoArquivo)
				else:
					print (">>>Nao foi possivel processar os dados")
					sys.exit()
			else:
				print (">>>Servidor nao concluiu o dowload!")
				sys.exit() #socket_tcp_cliente.close()
		except Exception as msg:
			print(">>>Error message: "+str(msg))
			return False
		return True
	elif(mensagem == "ERRO"):
		print (">>>Servidor nao conseguiu receber dados!")
		return False
	else:
		print (">>>Algum erro" + mensagem)
		return False

def receberDados(caminhoArquivo):
	caminhoArquivo = "SAIDA" + caminhoArquivo
	print (">>>Recebendo resultado...")
	try:
		arq_temp = open(caminhoArquivo, 'w')
		while True:
			dados = socket_tcp_cliente.recv(4096)
			if(dados == "EOF"):
				arq_temp.close()
				break
			arq_temp.write(dados)
		socket_tcp_cliente.send("DOWNLOAD CONCLUIDO")
		time.sleep(3)
		socket_tcp_cliente.close()
		print (">>>Conexao encerrada!")
	# caso ocorra alguma excecao
	except Exception as msg:
		print(">>>Error message: "+str(msg))
		return False

# Le os argumentos da linha de comando
try:
	IPServer = sys.argv[1]
	porta = int(sys.argv[2])
	caminhoArquivo = sys.argv[3]
except:
	print ("Erro nos parametros de execucao!")
	sys.exit()

# verifica se o arquivo com as coordenadas existe, para iniciar a conexao
if (os.path.exists(caminhoArquivo)):
	try:
		socket_tcp_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # cria socket do lado cliente utilizando IPV4 com protocolo TCP
		socket_tcp_cliente.connect((IPServer, int(porta))) # conecta com o servidor
		print (">>>Conectado ao servidor " + IPServer + ":" + str(porta))
	except socket.error as msg:
		print (">>>Erro ao conectar com o servidor " + IPServer + ":" + str(porta))
		print (">>>"+ str(msg))
		sys.exit()
	socket_tcp_cliente.send("ENVIANDO DADOS")
	enviarDados(IPServer,porta,caminhoArquivo)
else:
	print(">>>Arquivo " + str(caminhoArquivo) + " nao encontrado!")
	sys.exit()
