# Instruções de execução:
#   lado servidor:
    $ python servidor.py <porta>

#   lado cliente:
    $ python cliente.py <IPserver> <porta> <arquivo_com_as_coordenadas>

# Exemplo:
#   servidor:
    $ python servidor.py 8095

#   cliente:
    $ python cliente.py localhost 8095 coordenadas1.csv




#####  DESCRICAO DO TRABALHO #####

# T3-camada-de-transporte

Implemente dois programas na linguagem de sua eleição. Um se chamará “cliente” e outro “servidor”.

Cliente:
a) inicia por linha de comando com três argumentos (IPServer, porta e coordenadas.csv). Onde “porta” é o número da porta em que o servidor atende. Onde “coordenadas.csv” é um arquivo em que as linhas têm o seguinte formato (Lat1,Long1, Lat2,Long2). Ou seja, a latitude e longitude de dois pontos.

O cliente usa TCP para conectar se com o servidor, lê o arquivo e envia para o servidor.

Servidor:
b) inicia por linha de comando (pode usar porta dinâmica ou por argumento). Cria um socket na porta especificada, escuta e aceita conexões de clientes.
c) usa threads para manipular múltiplos clientes.
d) devolve um arquivo incluindo a distância, em km, entre os pontos. (formato Lat1, Long1, Lat2, Long2, distKm).


Ao completar esta tarefa o estudante recebe no máximo 8 pontos. Os dois pontos adicionais serão aplicados consoante à recursos adicionais no projeto.

Os dois códigos (cliente e servidor), mais uma versão compilada de cada código devem ser submetidos via Moodle em um arquivo no formato T3CT-{primeiroNomeUltimoNomeEmCamelCase}.zip (exclusivamente).
