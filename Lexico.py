"""
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
GRUPO:

Marlon Mascarenhas Castro   RA: 0035449
Ítalo Hylander                 RA:0026894

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

PROG -> programa id pvirg DECLS C-COMP
DECLS -> lambda | variaveis LIST-DECLS
LIST-DECLS -> DECL-TIPO D
D -> lambda | LIST-DECLS
DECL-TIPO -> LIST-ID dpontos TIPO pvirg
LIST-ID -> id E
E -> lambda | virg LIST-ID
TIPO -> inteiro | real | logico | caracter
C-COMP -> abrech LISTA-COMANDOS fechach
LISTA-COMANDOS -> COMANDOS G
G -> lambda | LISTA-COMANDOS
COMANDOS -> IF | WHILE | READ | WRITE | ATRIB
IF -> se abrepar EXPR fechapar C-COMP H
H -> lambda | senao C-COMP
WHILE -> enquanto abrepar EXPR fechapar C-COMP
READ -> leia abrepar LIST-ID fechapar pvirg
ATRIB -> id atrib EXPR pvirg
WRITE -> escreva abrepar LIST-W fechapar pvirg
LIST-W -> ELEM-W L
L -> lambda | virg LIST-W
ELEM-W -> EXPR | cadeia
EXPR -> SIMPLES P
P -> lambda | oprel SIMPLES
SIMPLES -> TERMO R
R -> lambda | opad SIMPLES
TERMO -> FAT S
S -> lambda | opmul TERMO
FAT -> id | cte | abrepar EXPR fechapar | verdadeiro | falso | opneg FAT}

Tokens

G1 = {{PROG, DECLS, C-COMP, LIST-DECLS, DECL-TIPO, D, LIST-ID, E, TIPO, LISTACOMANDOS, G, COMANDOS, IF, WHILE, READ, ATRIB, WRITE, EXPR, H, 
LIST-W, L, ELEM-W, SIMPLES, P, R, TERMO, S, FAT}{programa, id, variaveis, inteiro, real, logico, caracter, abrepar, fechapar,
se, abrech, fechach, senao, enquanto, leia, atrib, escreva, cadeia, cte, verdadeiro, falso, oprel, opad, opmul,
opneg, pvirg, virg, dpontos}, P, PROG}

 Comentarios::

 iniciam com // ate o fim da linha
 iniciam com /* e termina com */

"""


from os import path
import sys
import re

class TipoToken: #declaração de tokens
    OPREL = (1, 'relacional')
    ATRIB = (2, ':=')
    OPAD = (3, '+-')
    OPNEG = (4, '!')
    PVIRG = (5, ';')
    DPONTOS = (6, ':')
    VIRG = (7, ',')
    ABREPAR = (8, '(')
    FECHAPAR = (9, ')')
    ABRECH = (10, '{')
    FECHACH = (11, '}')
    PROGRAMA = (12, 'programa')
    ID = (13, 'id')
    INTEIRO = (14, 'inteiro')
    REAL = (15, 'real')
    LOGICO = (16, 'logico')
    CARACTER = (17, 'caracter')
    SE = (18, 'se')
    SENAO = (19, 'senao')
    ENQUANTO = (20, 'enquanto')
    ESCREVA = (21, 'escreva')
    CADEIA = (22, 'cadeia')
    CTE = (23, 'cte')
    VERDADEIRO = (24, 'verdadeiro')
    FALSO = (25, 'falso')
    ERROR = (26, 'erro')
    FIMARQ = (27, 'fim-de-arquivo')
    LEIA = (28, 'leia')
    OPMUL = (29,'*/')
    VARIAVEIS = (30,"variaveis")

class Token:
    def __init__(self, tipo, lexema, linha):
        self.tipo = tipo
        (const, msg) = tipo
        self.const = const
        self.msg = msg
        self.lexema = lexema
        self.linha = linha

class TabelaSimbolos:

    def __init__(self):
        # buffer que ira armazenar as variaveis caso tenha a declaracao do tipo a,b,c:integer;
        self.buffer_id =[] 
        ##lista q ira juntar o o id ao tipo;
        self.lista_Id =[] 
        #Lista de palavras resservadas da linguagem;
        self.LisReservadas = ['programa','variaveis','leia', 'escreva','id','inteiro','real','logico','carcter','se','senao','enquanto','cadeia','cte','verdadeiro','falso']
    
    # funcao que adiciona um id ao buffer;    
    def AddBufferID(self,lexema):
        
        self.buffer_id.append(lexema)   
    
    #Funcao que para cada item do buffer de id's associa a um item tipo;
    def AddDicID(self,tipo): #
                
        
        for e in self.buffer_id: 
            aux = e,tipo       
            self.lista_Id.append(aux)               
        self.buffer_id *= 0 
        
    #Salva a tabela de simbolos em um arquivo texto;
    def SalvaTabSimb(self):
    
        self.arquivo = open('TabelaSimbolos.txt','w')
        self.arquivo.write('PALAVRAS RESERVADAS:\n')
        for e in self.LisReservadas:
            self.arquivo.write(e)
            self.arquivo.write(';\n')
        
        self.arquivo.write('\n')
        self.arquivo.write('VARIAVEIS: \n')
        self.arquivo.write('\n')
        for e in self.lista_Id:
            aux1 = e[0]
            aux2 = e [1]
            aux3 = aux1[0]
            aux4 = aux1[1]      
            self.arquivo.write(aux3)
            self.arquivo.write(', ')
            self.arquivo.write(str(aux4))
            self.arquivo.write(': ')
            self.arquivo.write(aux2)
            self.arquivo.write('\n')
        
        self.arquivo.close()




class Lexico:
    # dicionario de palavras reservadas
    reservadas = { 'programa': TipoToken.PROGRAMA, 'variaveis': TipoToken.VARIAVEIS, 'leia': TipoToken.LEIA, 'escreva': TipoToken.ESCREVA
    , 'id': TipoToken.ID, 'inteiro': TipoToken.INTEIRO, 'real': TipoToken.REAL, 'logico': TipoToken.LOGICO, 'caracter': TipoToken.CARACTER
    , 'se': TipoToken.SE, 'senao': TipoToken.SENAO, 'enquanto': TipoToken.ENQUANTO, 'cadeia': TipoToken.CADEIA, 'cte': TipoToken.CTE, 'verdadeiro': TipoToken.VERDADEIRO
    , 'falso': TipoToken.FALSO}

    def __init__(self, nomeArquivo):
        self.nomeArquivo = nomeArquivo
        self.arquivo = None
        #os atributos buffer e linha sao incluidos no metodo abreArquivo

    def abreArquivo(self):
            if not self.arquivo is None:
                print('ERRO: Arquivo ja aberto')
                quit()
                #erro se o arquivo ja está aberto

            elif path.exists(self.nomeArquivo):
                self.arquivo = open(self.nomeArquivo, "r")
                #fila de caracteres 'deslidos' pelo ungetChar
                self.buffer = ''
                self.linha = 1
            else:
                print('ERRO: Arquivo "%s" inexistente.' % self.nomeArquivo) #erro se o arquivo não existe
                quit()
	            
    def fechaArquivo(self): #função para fechar arquivo
            if self.arquivo is None:
                print('ERRO: Nao ha arquivo aberto')
                quit()
            else:
                self.arquivo.close()

    def getChar(self): #pegar uma letra do arquivo
        if self.arquivo is None:
            print('ERRO: Nao ha arquivo aberto')
            quit()
        elif len(self.buffer) > 0:
            c = self.buffer[0]
            self.buffer = self.buffer[1:]
            return c
        else:
            c = self.arquivo.read(1)
            # se nao foi eof, pelo menos um car foi lido
            # senao len(c) == 0
            if len(c) == 0:
                return None
            else:
                return c.lower()

    def ungetChar(self, c): # 'desler uma letra do arquivo'
        if not c is None:
            self.buffer = self.buffer + c

    def getToken(self):
        lexema = '' #inicialização do lexema
        estado = 1 #inicialização do estado
        car = None # inicialização do car (vai guardar o char que esta sendo lido)
        alfanumerico = "[a-zA-Z0-9]" #declara o alfanumerico, letras e numeros
        alfa = "[a-zA-Z]" #declara todas as letras
        while (True):
            if estado == 1:
                # estado inicial que faz primeira classificacao
                car = self.getChar()
                if car is None: #retorna fim de arquivo
                    return Token(TipoToken.FIMARQ, '<eof>', self.linha)
                elif car in {' ', '\t', '\n'}: #final de arquivo ou tabulaçao ou espaço entram nesse if para tratamento
                    if car == '\n': #final de linha
                        self.linha = self.linha + 1 #soma uma linha 
                elif car == '"': #tratamento de cadeia
                	estado = 2
                elif bool(re.match(alfa,car)): #qualquer coisa que começa com uma letra
                    estado = 3
                elif car.isdigit() or car is '.': #qualquer coisa que começa com um numero ou '.'
                    estado = 4
                elif car in {':=', '=', ';', ':', ',', '+', '{', '}', '-', '*', '!', '(', ')', '<', '>', '<=', '>=', '<>'}: #caracteres aceitos pela linguagem
                    estado = 5
                elif car == '/':#tratamento de comentarios ou divisão ou comentarios de bloco
                	aux = car + self.getChar()
                	if aux == '/*':#tratamento de blocos
                		estado = 6
                	elif aux == '//':#tratamento de comentario de linha
                		estado = 7
                	else: #caso for divisão
                		estado = 5
                else:
                    return Token(TipoToken.ERROR, '<' + car + '>', self.linha) #caso não for nenhum, é um erro


            elif estado == 2: #caso 2 trata cadeias
            	controller = 0
            	while True:
            		car = self.getChar()
            		if car == '"':
            			return Token(TipoToken.CADEIA, lexema, self.linha)
            			break
            		lexema = lexema + car


            elif estado == 3:
                # estado que trata nomes (identificadores ou palavras reservadas)
                lexema = lexema + car
                car = self.getChar()
                if car is None or (not re.match(alfanumerico,car)):
                    # terminou o nome
                    self.ungetChar(car)

                    if lexema in Lexico.reservadas:
                        return Token(Lexico.reservadas[lexema], lexema, self.linha)
                    else:
                    	if len(lexema) <= 32:
                    		return Token(TipoToken.ID, lexema, self.linha)
                    	else:
                    		return Token(TipoToken.ERRO, '<' + lexema + '>', self.linha)

            

            elif estado == 4:
                # estado que trata numeros inteiros
                lexema = lexema + car
                car = self.getChar()

                if car is None or not car.isdigit():
                    # terminou o numero
                    if not car == '.':
	                    self.ungetChar(car)
	                    return Token(TipoToken.CTE, lexema, self.linha)

            elif estado == 5:
                # estado que trata outros tokens primitivos comuns
                lexema = lexema + car
                if car == '=':
                	return Token(TipoToken.OPREL, lexema, self.linha)
                elif car == '<':
                    return Token(TipoToken.OPREL, lexema, self.linha)
                elif car == '>':
                    return Token(TipoToken.OPREL, lexema, self.linha)
                elif car == '<=':
                    return Token(TipoToken.OPREL, lexema, self.linha)
                elif car == '>=':
                    return Token(TipoToken.OPREL, lexema, self.linha)
                elif car == '<>':
                    return Token(TipoToken.OPREL, lexema, self.linha)
                elif car == '+':
                	return Token(TipoToken.OPAD, lexema, self.linha)
                elif car == '-':
                    return Token(TipoToken.OPAD, lexema, self.linha)
                elif car == '*':
                    return Token(TipoToken.OPMUL, lexema, self.linha)
                elif car == '/':
                    return Token(TipoToken.OPMUL, lexema, self.linha)
                elif car == '!':
                    return Token(TipoToken.OPNEG, lexema, self.linha)
                elif car == ';':
                    return Token(TipoToken.PVIRG, lexema, self.linha)
                elif car == ':':
                	aux = car + self.getChar()
                	if aux == ':=':
                		return Token(TipoToken.ATRIB, aux, self.linha)
                	else:
                		return Token(TipoToken.DPONTOS, lexema, self.linha)
                		self.ungetChar(car)
                elif car == ',':
                    return Token(TipoToken.VIRG, lexema, self.linha)
                elif car == '(':
                    return Token(TipoToken.ABREPAR, lexema, self.linha)
                elif car == ')':
                    return Token(TipoToken.FECHAPAR, lexema, self.linha)
                elif car == '{':
                    return Token(TipoToken.ABRECH, lexema, self.linha)
                elif car == '}':
                    return Token(TipoToken.FECHACH, lexema, self.linha)
                elif car == ';':
                    return Token(TipoToken.PTVIRG, lexema, self.linha)

            elif estado == 6:
                # consumindo comentario
                if(car == '/'):
                	while (aux != '*/'):
	                    car = self.getChar()
	                    if car == '\n':
	                    	self.linha = self.linha + 1
	                    if car == None:#se chegar no final de arquivo e o comentario de bloco não foi finalizado
	                    	return Token(TipoToken.FIMARQ, '<eof>', self.linha)
	                    if (car == '*'):
	                    	aux = car + self.getChar()
	                    	car = self.getChar()

	                self.ungetChar(car)

	                estado = 1

            elif estado == 7:
            	#estado de trata comentarios de linha
                while (not car is None) and (car != '\n'):
                    car = self.getChar()
                self.ungetChar(car)
                estado = 1
