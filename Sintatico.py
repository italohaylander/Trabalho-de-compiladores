"""
    Gramatica G1:
    A -> PROG $#
    PROG -> programa id pvirg DECLS C-COMP;#
    DECLS -> vazio | variaveis  LIST-DECLS;#
    LIST-DECLS -> DECL-TIPO D;#
    D -> vazio | LIST-DECLS# 
    DECL-TIPO -> LIST-ID dpontos TIPO pvirg;#
    LIST-ID -> id E;#
    E -> vazio | virg LIST-ID;#
    TIPO -> inteiro | real | logico | caracter;#
    C-COMP -> abrech LISTA-COMANDOS fechach;#
    LISTA-COMANDOS -> COMANDOS G;#
    G -> vazio | LISTA-COMANDOS;
    COMANDOS -> IF | WHILE | READ | WRITE | ATRIB;#
    IF -> se abrepar EXPR fechapar C-COMP H;#
    H -> vazio | senao C-COMP;#
    WHILE -> enquanto abrepar EXPR fechapar C-COMP;
    READ -> leia abrepar LIST-ID fechapar pvirg;
    ATRIB -> id atrib EXPR pvirg;
    WRITE -> escreva   abrepar LIST-W fechapar pvirg;
    LIST-W -> ELEM-W L;
    L -> vazio | virg LIST-W;
    ELEM-W -> EXPR | cadeia;
    EXPR -> SIMPLES P;
    P -> vazio | oprel SIMPLES;
    SIMPLES -> TERMO R;
    R -> vazio | opad SIMPLES;
    TERMO -> FAT S;
    S -> vazio| opmul TERMO;
    FAT -> id | cte | abrepar EXPR fechapar | verdadeiro | falso | opneg FAT;    
"""
from os import path
import sys
from Lexico import TipoToken as tt,Lexico,Token;
from Lexico import TabelaSimbolos as ts;
class sintatico:

	def __init__(self):
		self.lex = None
		self.tab = None
		self.tokenAtual = None
		self.follow = {
           'A'              : [tt.FIMARQ[0]] ,
           'PROG'           : [tt.FIMARQ[0]] ,
           'DECLS'          : [tt.ABREPAR[0], tt.FIMARQ[0]] ,
           'LIST_DECLS'     : [tt.ABREPAR[0], tt.FIMARQ[0]] ,
           'D'              : [tt.ABREPAR[0], tt.FIMARQ[0]] ,           
           'DECL_TIPO'      : [tt.ABREPAR[0], tt.ID[0], tt.FIMARQ[0]] ,
           'ListId'         : [tt.DPONTOS[0], tt.FECHACH[0], tt.FIMARQ[0]] ,    
           'E'              : [tt.DPONTOS[0], tt.FECHACH[0], tt.FIMARQ[0]] ,          
           'Tipo'           : [tt.PVIRG[0], tt.FIMARQ[0]] ,       
           'C_COMP'         : [tt.FIMARQ[0], tt.ENQUANTO[0], tt.ESCREVA[0], tt.FECHACH[0], tt.ID[0], tt.LEIA[0], tt.SE[0], tt.SENAO[0]],
           'LISTA_COMANDOS' : [tt.FECHACH[0], tt.FIMARQ[0]],
           'G'              : [tt.FECHACH[0], tt.FIMARQ[0]],
           'COMANDOS'       : [tt.ENQUANTO[0], tt.ESCREVA[0], tt.FECHACH[0], tt.ID[0], tt.LEIA[0], tt.SE[0], tt.FIMARQ[0]],
           'IF'             : [tt.ENQUANTO[0], tt.ESCREVA[0], tt.FECHACH[0], tt.ID[0], tt.LEIA[0], tt.SE[0], tt.FIMARQ[0]],
           'H'              : [tt.ENQUANTO[0], tt.ESCREVA[0], tt.FECHACH[0], tt.ID[0], tt.LEIA[0], tt.SE[0], tt.FIMARQ[0]],
           'WHILE'          : [tt.ENQUANTO[0], tt.ESCREVA[0], tt.FECHACH[0], tt.ID[0], tt.LEIA[0], tt.SE[0], tt.FIMARQ[0]],
           'READ'           : [tt.ENQUANTO[0], tt.ESCREVA[0], tt.FECHACH[0], tt.ID[0], tt.LEIA[0], tt.SE[0], tt.FIMARQ[0]],
           'ATRIB'          : [tt.ENQUANTO[0], tt.ESCREVA[0], tt.FECHACH[0], tt.ID[0], tt.LEIA[0], tt.SE[0], tt.FIMARQ[0]],
           'WRITE'          : [tt.ENQUANTO[0], tt.ESCREVA[0], tt.FECHACH[0], tt.ID[0], tt.LEIA[0], tt.SE[0], tt.FIMARQ[0]],
           'LIST_W'         : [tt.FECHACH[0], tt.FIMARQ[0]],
           'L'              : [tt.FECHACH[0], tt.FIMARQ[0]],
           'ELEM_W'         : [tt.FECHACH[0], tt.VIRG[0], tt.FIMARQ[0]],
           'EXPR'           : [tt.FECHACH[0], tt.PVIRG[0], tt.VIRG[0], tt.FIMARQ[0]],
           'P'              : [tt.FECHACH[0], tt.PVIRG[0], tt.VIRG[0], tt.FIMARQ[0]],
           'SIMPLES'        : [tt.FECHACH[0], tt.OPREL[0], tt.PVIRG[0], tt.VIRG[0], tt.FIMARQ[0]],
           'R'              : [tt.FECHACH[0], tt.OPREL[0], tt.PVIRG[0], tt.VIRG[0], tt.FIMARQ[0]],
           'TERMO'          : [tt.FECHACH[0], tt.OPAD[0], tt.OPREL[0], tt.PVIRG[0], tt.VIRG[0], tt.FIMARQ[0]],
           'S'              : [tt.FECHACH[0], tt.OPAD[0], tt.OPREL[0], tt.PVIRG[0], tt.VIRG[0], tt.FIMARQ[0]],
           'FAT'            : [tt.OPAD[0], tt.OPMUL[0], tt.FIMARQ[0]]
        }
	


	def interprete(self,nomearquivo,t):
		if not self.lex is None:
			print('Erro, arquivo ja esta sendo analisado')
		else:
			
			self.lex = Lexico(nomearquivo)#cria o objeto tipo lexico;
			self.lex.abreArquivo()
			self.tabS = ts()#cria o objeto da tabela de simbolos;
			self.tokenAtual = self.lex.getToken()
			self.id1 = 0
			self.A()
			
			if t =='-t':
			#imprime tabela
				self.tabS.SalvaTabSimb()
	
			self.lex.fechaArquivo()
	#verifica se o token atual é igual ao token que casa com a producao;		
	def atualIgual(self,token):
		
		(const,msg) = token
		if(self.tokenAtual.msg == 'erro'):
			print('ERRO LEXICO [linha %d]:  caracter invalido "%s" '% (self.tokenAtual.linha,  self.tokenAtual.lexema))
			self.tokenAtual = self.lex.getToken()
		return self.tokenAtual.const == const

	def consome(self,token):
		
		if self.atualIgual(token): 			
			if (self.tokenAtual.const == 13) and (self.id1 == 0):#verifica se é o primeiro token id que e o nome do programa e nao vai para a tabela de simbolos; 
				self.id1 = 1   
			elif (self.tokenAtual.const == 13) and (self.id1 == 1):
				aux = self.tokenAtual.lexema,self.tokenAtual.linha#id's que vao para o buffer(armazena ids que possuem tipos em comun); 
				self.tabS.AddBufferID(aux)
			if self.tokenAtual.const == 14 or self.tokenAtual.const == 15 or self.tokenAtual.const == 17 or self.tokenAtual.const == 16:
				self.tabS.AddDicID(self.tokenAtual.lexema)#Com a chegada de um token Tipo, o buffer de id e esvaziado;  
			self.tokenAtual = self.lex.getToken()
			print(self.tokenAtual.lexema)
		else:
			(const,msg) = token
			print('ERRO DE SINTAXE [linha %d]: era esperado "%s", atual "%s"'% (self.tokenAtual.linha, msg, self.tokenAtual.lexema))
			raise Exception()#quando ocorre o erro dentro do consome é levantado a exception dentro da funcao que chamou a consome()

#------------------------------------------------------------------------------------------------------
#Essa parte do codigo trata as funcoes que sao respectivas a cada nao terminal pertencente a gramatica;
#---------------------------------------------------------------------------------------------------------
#O uso do try dentro das funcoes foi uma forma de abstrair o modo panico,(discutido juntamente com os mebros da dupla do Mateus Soares e Rodrigo Pacheco)
#onde caso nao seja possivel realizar alguma das 'operacoes' a mesma levantara uma exception e um novo token que esteja certo e case com uma producao.ou seja
#um porto seguro para que se continue a compilacao;
	def A(self):
		try:
			self.PROG()
			self.consome(tt.FIMARQ)
		except:
			while not self.tokenAtual.const in self.follow['A']:#encontra o proximo token que esta no follow de A
				self.tokenAtual = self.lex.getToken() 

	def PROG(self):
		try:
			self.consome(tt.PROGRAMA)
			self.consome(tt.ID)
			self.consome(tt.PVIRG)
			self.DECLS()
			self.C_COMP()
		except:
			while not self.tokenAtual.const in self.follow['PROG']:
				self.tokenAtual = self.lex.getToken()


	def DECLS(self):
		try:	
			if(self.atualIgual(tt.VARIAVEIS)):
				self.consome(tt.VARIAVEIS)
				self.LIST_DECLS()
			else:
				pass
		except:
			while not self.tokenAtual.const in self.follow['DECLS']:		
				self.tokenAtual = self.lex.getToken()
				
	def LIST_DECLS(self):
		try:
			self.DECL_TIPO()
			self.D()
		except:
			while not self.tokenAtual.cosnt in self.follow['LIST_DECLS']:	
				self.tokenAtual = self.lex.getToken()
				
	def DECL_TIPO(self):
		try:	
			self.LIST_ID()
			self.consome(tt.DPONTOS)
			self.TIPO()
			self.consome(tt.PVIRG)
		except:
			while not self.tokenAtual.const in self.follow['DECL_TIPO']: 	
				self.tokenAtual = self.lex.getToken()
					
	def D(self):
		try:	
			if(self.atualIgual(tt.ID)):
				self.LIST_DECLS()
			else:
				pass
		except:
			while not self.tokenAtual.const in self.follow['D']:
				self.tokenAtual = self.lex.getToken()
				
	def LIST_ID(self):
		try:	
			self.consome(tt.ID)
			self.E()
		except:
			while not self.tokenAtual.const in self.follow['LIST_ID']:	
				self.tokenAtual = self.lex.getToken()
				
	
	def E(self):
		try:
			if(self.atualIgual(tt.VIRG)):
				self.consome(tt.VIRG)
				self.LIST_ID()
			else:
				pass
		except:
			while not self.tokenAtual.const in self.follow['E']:
				self.tokenAtual = self.lex.getToken()
					
		

	def TIPO(self):
		try:	
			if(self.atualIgual(tt.INTEIRO)):
				self.consome(tt.INTEIRO)
			elif(self.atualIgual(tt.REAL)):
				self.consome(tt.REAL)
			elif(self.atualIgual(tt.LOGICO)):
				self.consome(tt.LOGICO)
			else:
				self.consome(tt.CARACTER)
		except:
			while not self.tokenAtual.const in self.follow['TIPO']:
				self.tokenAtual = self.lex.getToken()
				

	def C_COMP(self):             
		try:
			self.consome(tt.ABRECH)    
			self.LISTA_COMANDOS()
			self.consome(tt.FECHACH)
		except:
			while not self.tokenAtual.const in self.follow['C_COMP']:
				self.tokenAtual = self.lex.getToken()
				
	def LISTA_COMANDOS(self):
		try:	
			self.COMANDOS()
			self.G()
		except:
			while not self.tokenAtual.const in self.follow['LISTA_COMANDOS']:
				self.tokenAtual = self.lex.getToken()
				
	def G(self):
		try:
			if(self.atualIgual(tt.SE)):
				self.LISTA_COMANDOS()
			elif(self.atualIgual(tt.ENQUANTO)):
				self.LISTA_COMANDOS()
			elif(self.atualIgual(tt.LEIA)):
				self.LISTA_COMANDOS()
			elif(self.atualIgual(tt.ESCREVA)):
				self.LISTA_COMANDOS()
			elif(self.atualIgual(tt.ID)):
				 self.LISTA_COMANDOS()
			else:
				pass	 
		except:
			while not self.tokenAtual.const in self.follow['G']:
				self.tokenAtual = self.lex.getToken()
				

	def COMANDOS(self):
		try:
			if(self.atualIgual(tt.SE)):
				self.IF()
			elif(self.atualIgual(tt.ENQUANTO)):
				self.WHILE()
			elif(self.atualIgual(tt.LEIA)):
				self.READ()
			elif(self.atualIgual(tt.ESCREVA)):
				self.WRITE()
			else:
				self.ATRIB()
		except:
			while not self.tokenAtual.const in self.follow['COMANDOS']:
				self.tokenAtual = self.lex.getToken()
				
	def IF(self):
		try:	
			self.consome(tt.SE)
			self.consome(tt.ABREPAR)
			self.EXPR()
			self.consome(tt.FECHAPAR)
			self.C_COMP()
			self.H()
		except:
			while not self.tokenAtual.cosnt in self.follow['IF']:
				self.tokenAtual = self.lex.getToken()
				
	def H(self):
		try:
			if(self.atualIgual(tt.SENAO)):
				self.consome(tt.SENAO)
				self.C_COMP()
			else:
				pass
		except:
			while not self.tokenAtual.const in self.follow['H']:
				self.tokenAtual = self.lex.getToken()
				
	def WHILE(self):
		try:	
			self.consome(tt.ENQUANTO)
			self.consome(tt.ABREPAR)
			self.EXPR()
			self.consome(tt.FECHAPAR)
			self.C_COMP()
		except:
			while not self.tokenAtual.cosnt in self.follow['WHILE']:
				self.tokenAtual = self.lex.getToken()	
				
	def READ(self):
		try:	
			self.consome(tt.LEIA)
			self.consome(tt.ABREPAR)
			self.LIST_ID()
			self.consome(tt.FECHAPAR)
			self.consome(tt.PVIRG)
		except:
			while not self.tokenAtual.cosnt in self.follow['READ']:
				self.tokenAtual = self.lex.getToken()	
				
	def ATRIB(self):
		try:	
			self.consome(tt.ID)
			self.consome(tt.ATRIB)    
			self.EXPR()
			self.consome(tt.PVIRG)
		except:
			while not self.tokenAtual.const in self.follow['ATRIB']:
				self.tokenAtual = self.lex.getToken()
				


	def WRITE(self):
		try:	
			self.consome(tt.ESCREVA)
			self.consome(tt.ABREPAR)
			self.LIST_W()
			self.consome(tt.FECHAPAR)
			self.consome(tt.PVIRG)
		except:	
			while not self.tokenAtual.const in self.follow['WRITE']:
				self.tokenAtual = self.lex.getToken()	
				

	def LIST_W(self):
		try:	
			self.ELEM_W()
			self.L()
		except:
			while not self.tokenAtual.const in self.follow['LIST_W']:
				self.tokenAtual = self.lex.getToken()

	def L(self):
		try:	
			if(self.atualIgual(tt.VIRG)):
				self.consome(tt.VIRG)
				self.LIST_W()
			else:
				pass
		except:
			while not self.tokenAtual.const in self.follow['L']:
				self.tokenAtual = self.lex.getToken()
				

	def ELEM_W(self):
		try:	
			if(self.atualIgual(tt.CADEIA)):
				self.consome(tt.CADEIA)
			else:
				self.EXPR()
		except:
			while not self.tokenAtual.const in self.follow['ELEM_W']:
				self.tokenAtual = self.lex.getToken()
				
	def EXPR(self):
		try:
			self.SIMPLES()
			self.P()
		except:
			while not self.tokenAtual.const in self.follow['EXPR']:
				self.tokenAtual = self.lex.getToken()
				
	def P(self):
		try:
			if(self.atualIgual(tt.OPREL)):
				self.consome(tt.OPREL)
				self.SIMPLES()
			else:
				pass
		except:
			while not self.tokenAtual.const in self.follow['P']:
				self.tokenAtual = self.lex.getToken()		
				


	def SIMPLES(self):
		try:
			self.TERMO()
			self.R()
		except:
			while not self.tokenAtual.const in self.follow['SIMPLES']:
				self.tokenAtual = self.lex.getToken()
				
	def R(self):
		try:
			if(self.atualIgual(tt.OPAD)):
				self.consome(tt.OPAD)
				self.SIMPLES()
			else:
				pass
		except:
			while not self.tokenAtual.const	in self.follow['R']:
				self.tokenAtual = self.lex.getToken()		
				
	def TERMO(self):
		try:	
			self.FAT()    
			self.S()
		except:
			while not self.tokenAtual.const in self.follow['TERMO']:	
				self.tokenAtual = self.lex.getToken()
				
	def S(self):
		try:
			if(self.atualIgual(tt.OPMUL)):
				self.consome(tt.OPMUL)
				self.TERMO()
			else:
				pass
		except:
			while not self.tokenAtual.const in self.follow['S']:
				self.tokenAtual = self.lex.getToken()
				
	def FAT(self):
		try:	
			if(self.atualIgual(tt.ID)):
				self.consome(tt.ID)
			elif(self.atualIgual(tt.CTE)):
				self.consome(tt.CTE)
			elif(self.atualIgual(tt.ABREPAR)):
				self.consome(tt.ABREPAR)
				self.EXPR()
				self.consome(tt.FECHAPAR)
			elif(self.atualIgual(tt.VERDADEIRO)):
				self.consome(tt.VERDADEIRO)
			elif(self.atualIgual(tt.FALSO)):
				self.consome(tt.FALSO)
			else:
				self.consome(tt.OPNEG)
				self.FAT()
		except:
			while not self.tokenAtual.const in self.follow['FAT']:
				self.tokenAtual = sel.lex.getToken()
				

              

if __name__== "__main__":

#nome = input("Entre com o nome do arquivo: ")
	aux = []
	for param in sys.argv:
		aux.append(param)
	nomearquivo = aux[1]
	if len(aux) == 3: 
		escreve = aux[2]
	else:
		escreve = None	
	parser = sintatico()
	parser.interprete(nomearquivo,escreve)
	
	    
            

            
                  
    
        
