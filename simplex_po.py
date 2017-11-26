#-*- coding: utf-8 -*-
#funcao_objetivo = ('max', '-1x_1 - 1x_2 = 0')
#restricao = ['4x_1 + 1x_2 <= 21','2x_1 + 3x_2 >= 13','-1x_1 + 1x_2 = 1']


# Pesquisa Operacional
# Jorge de Arruda Martina

class Simplex(object):
    def __init__(self,num_variavel, restricao, funcao_objetivo):
        self.if_ok = False # Se o simplex foi resolvido
        self.topo = []
        self.num_var_ini = num_variavel
        self.tipo = funcao_objetivo[0] # 'max' ou 'min'
        self.funcao_objetivo = funcao_objetivo[1]
        self.restricao = restricao
        self.matriz, self.num_var_s, self.num_var_a = self.gerar_matriz([funcao_objetivo[1]]+restricao)
        self.matriz_ini = self.gerar_matriz([funcao_objetivo[1]]+restricao)
        if self.tipo == 'min':
            for i in range(len(self.matriz[0])):
                self.matriz[0][i] = - self.matriz[0][i]
                self.matriz_ini[0][0][i] =  self.matriz_ini[0][0][i]
            
        print self.matriz, self.num_var_s, self.num_var_a
        self.num_var_total = self.num_var_ini + self.num_var_s
        self.base = self.base()
        if self.num_var_a > 0:
            self.fase_1()
        self.solucionar(self.matriz,self.matriz[0],0)
        

        # Criar lista com as variávéis do topo da matriz
        self.topo.append('Base')
        for i in range(self.num_var_ini+self.num_var_s):
            self.topo.append("x_"+str(i+1))
        self.topo.append('L.B')


        if self.tipo == 'min':
            self.matriz[0][-1] = - self.matriz[0][-1]
        l_b = self.matriz[0][-1]
        print "\nSOLUÇÂO FINAL - Base ",self.base
        print "\t",self.tipo,": ",l_b
        for i in range(len(self.base)):
            if i != 0:
                j = self.base[i].split('x_')
                print "\t -", self.base[i],"= ", self.matriz[i][-1],"\n"

    def gerar_matriz(self,matriz_string):
        num_adi_var_s = 0  # Número adicional de váriaveis de folga ou excesso
        num_adi_var_a = 0  # Número adicional de váriaveis artificiais
        num_linha = len(matriz_string)
        
        for expressao in range(1,num_linha):
            print matriz_string[expressao]
            if '>=' in matriz_string[expressao]:
                num_adi_var_s += 1
                num_adi_var_a += 1
            elif '<=' in matriz_string[expressao]:
                num_adi_var_s += 1
            elif '=' in matriz_string[expressao]:
                num_adi_var_a += 1
        print "num_adi_var_s: ",num_adi_var_s,"  num_adi_var_a: ",num_adi_var_a
        matriz = []
        cont_exp_r = 0 # Verificar o número de expressões com "=" ou ">=" foram transformadas
        cont_exp_s = 0 # Verificar o número de expressões com "<=" ou ">=" foram transformadas
        for expre in range(num_linha):  # Iterar pelas linhas da matriz
            expressao = []
            termos = matriz_string[expre].split(' ')  # Extrair termos da expressões
            for term in range(len(termos)):  # Iterar por termos da expressões
                if '_' in termos[term]:  # Verificar se o termo posssui relação com uma variável
                    valor = termos[term].split('x_')  # Separar o múltiplo e o índice de X, do termo
                    if termos[term - 1] is '-':  # Verificar o termo anterior = "-", se for o múltiplo é negativo e adiciona-o a lista da expressão
                        expressao.append(-(float(valor[0])))
                    else:
                        expressao.append(float(valor[0]))
                elif expre != 0:
                    if (termos[term] == '<=') :  # Verifica se é o fim da expressões
                        for var in range(num_adi_var_s):  # Adiciona na expressão os múltiplos para as variáveis de folga
                            if var == cont_exp_s:
                                expressao.append(1.0)
                            else:
                                expressao.append(0.0)
                        for var in range(num_adi_var_a):  # Adiciona na expressão os múltiplos para as variáveis artificial
                            expressao.append(0.0)
                        
                        cont_exp_s += 1
                        expressao.append(float(termos[term + 1]))  # Adiciona o termo independente à expressão
                    elif  (termos[term] == '>='):  # Verifica se é o fim da restrição
                        for var in range(num_adi_var_s):  # Adiciona na expressão os múltiplos para as variáveis de folga
                            if var == cont_exp_s:
                                expressao.append(-1.0)
                            else:
                                expressao.append(0.0)
                        for var in range(num_adi_var_a):  # Adiciona na expressão os múltiplos para as variáveis artificial
                            if var == cont_exp_r:
                                expressao.append(1.0)
                            else:
                                expressao.append(0.0)

                        cont_exp_r += 1
                        cont_exp_s += 1
                        expressao.append(float(termos[term + 1]))  # Adiciona o termo independente à expressã0
                    elif  (termos[term] == '='):  # Verifica se é o fim da restrição
                        for var in range(num_adi_var_s):  # Adiciona na expressão os múltiplos para as variáveis de folga
                            expressao.append(0.0)
                        for var in range(num_adi_var_a):  # Adiciona na expressão os múltiplos para as variáveis artificial
                            if var == cont_exp_r:
                                expressao.append(1.0)
                            else:
                                expressao.append(0.0)

                        cont_exp_r += 1
                        expressao.append(float(termos[term + 1]))  # Adiciona o termo independente à expressã
            
            if expre == 0:
                print "Oi ",matriz_string[expre]
                for var in range(num_adi_var_s+num_adi_var_a+1):
                    expressao.append(0.0)
            matriz.append(expressao)
        return matriz,num_adi_var_s,num_adi_var_a

    def base(self):
        coluna = []
        coluna.append('Z')
        cont_a = 0
        for i in range(len(self.restricao)):
            if '<=' in self.restricao[i]:
                coluna.append(('x_'+str(i+self.num_var_ini+1)))
            else:
                coluna.append(('a_'+str(cont_a)))
                cont_a += 1
        print "\nColuna de variáveis base: ", coluna
        print "\t(╯°□°）╯ Fim - def base(self):\n"
        return coluna

    def pivo(self,matriz,objetivo,fase):
        print '\n\nInicio de def pivo(self,objetivo):'
        linha = 0
        coluna = 0
        menor = 0
        num_var_total = self.num_var_total
        if fase == 1:
            num_var_total = num_var_total + self.num_var_a 
        for i in range(num_var_total): # Iterar pelos termos da equação objetivo e procurar a coluna pivo
            if (objetivo[i] < 0) and (objetivo[i] < menor): # verificar qual o maior número negativo absoluto
                menor = objetivo[i]
                coluna = i
        if ((menor == 0) and (coluna == 0)): # Critério de parada, não há valores negativos na função objetivo
            self.if_ok = True
            return linha, coluna
        menor = 0
        # Iterar pelos linhas da matriz de equações de restrição e procurar a linha pivo
        for i in range(len(self.restricao)): 
            if (matriz[i+1][coluna] > 0) and ((((matriz[i+1][-1]) / matriz[i+1][coluna]) < menor) or (menor==0)):
                menor = ((matriz[i+1][-1]) / matriz[i+1][coluna])
                linha = i+1
        print "\n\tAntes, base= ", self.base
        # Atualizar a coluna de variavéis base
        if coluna <= self.num_var_ini+self.num_var_s:
            self.base[linha] = 'x_' + str(coluna+1)
        else:
            self.base[linha] = 'r_' + str(coluna+1)
        print "\tApos, base=: ",self.base
        print "\nPivo[%d][%d] = %1.2f" % (linha,coluna,matriz[linha][coluna])
        print "(╯°□°）╯ Fim - def pivo(self):\n"
        return linha,coluna

    def solucionar(self,matriz,objetivo,fase):
        print "Inicio solucionar(self,matriz):"
        num_var_total = 0
        if fase == 1: # Verificar se a fase_1 ou fase_final
            num_var_total = self.num_var_ini + self.num_var_s + self.num_var_a
        else:
            num_var_total = self.num_var_ini + self.num_var_s

        print "\tNum_var_total: ", num_var_total,"   self.num_var_ini: ", self.num_var_ini,"   self.num_adi_var_s",self.num_var_s,"   self.num_adi_var_a",self.num_var_a
        print "\tFase: ", fase, "   Objetivo: ",objetivo
        print "\tMatriz: ", matriz
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        while not self.if_ok:
            pivo = self.pivo(matriz,objetivo,fase) # Calcular a linha e coluna pivo
            if (self.if_ok == True):
                break

            # # # # # # # # # # # # # # # # # # Nova linha pivo # # # # # # # # # # # # # # # # # # # # # # # # # #
            print "(Antes) Matriz: ", matriz
            print "\tLinha pivo: ", matriz[pivo[0]],"    div    ",  abs(matriz[pivo[0]][pivo[1]])
            temp = []
            for i in range(num_var_total+1): # Dividir a linha pivo pelo número pivo para gerar a nova linha
                print "\t\tColuna ",i,"= ",matriz[pivo[0]][i],"   New Coluna ",i," = ", " (", matriz[pivo[0]][i]," / abs(" ,matriz[pivo[0]][pivo[1]]," )"
                temp.append(matriz[pivo[0]][i] / abs(matriz[pivo[0]][pivo[1]]))
            matriz[pivo[0]] = temp
            print "(Após)  Matriz: ", matriz,"\n\n\n"
            # # # # # # # # # # # # # # # # # # Nova linha pivo # # # # # # # # # # # # # # # # # # # # # # # # # #
         
            # # # # # # # # # # # # # # # # # # Novas expressões # # # # # # # # # # # # # # # # # # # # # # # # # #
            for i in range(len(self.restricao)+1):
                if i != pivo[0]:
                    print "(self ) Matriz: ", self.matriz
                    print "(Antes) Matriz: ", matriz
                    print "\tLinha ",i,": ", matriz[i], "  +  ( ", matriz[pivo[0]], " * ", -(matriz[i][pivo[1]])," )"
                    nova_linha = []
                    print "(Após)  matriz: ", matriz, "\n"
                    for j in range(num_var_total + 1):
                        print "\tColuna ", j, ": ", matriz[i][j], "  +  ( ", matriz[pivo[0]][j], " * ", -(matriz[i][pivo[1]])," )"
                        nova_linha.append(matriz[i][j] +  (matriz[pivo[0]][j] *  -(matriz[i][pivo[1]]) ))
                    matriz[i] = nova_linha
                    print "(Após)  matriz: ", matriz, "\n"
            # # # # # # # # # # # # # # # # # # Novas expressões # # # # # # # # # # # # # # # # # # # # # # # # # #

            # # # # # # # # # # # # # # # # # # Nova restrcão, se for fase 1 # # # # # # # # # # # # # # # # # # # #
            if fase == 1:
                print "(Antes) Objetivo(fase 1): ", objetivo
                print "\tNew Objetivo = ", objetivo, "  +  ( ", matriz[pivo[0]], " * ", -(objetivo[pivo[1]])," )"
                nova_linha = []
                for j in range(num_var_total + 1):
                    print "\t\tColuna ", j, ": ", objetivo[j], "  +  ( ", matriz[pivo[0]][j], " * ", -(objetivo[pivo[1]])," )"
                    nova_linha.append(objetivo[j] +  (matriz[pivo[0]][j] *  -(objetivo[pivo[1]]) ))
                objetivo = nova_linha
                print "(Após)  Objetivo(fase 1): ", objetivo, "\n"
            # # # # # # # # # # # # # # # # # # Nova restrcão, se for fase 1 # # # # # # # # # # # # # # # # # # # #
            else:
                objetivo = matriz[0]
        print "(╯°□°）╯ Fim - def solucionar(self,matriz,objetivo,fase) Fase: ", fase,"\n"
        if fase == 1:
            return matriz,objetivo
        return matriz,matriz[0]

    def fase_1(self):
        objetivo = []
         # Calcular função objetivo = - somatorio( restrição(">=") )
        l_b = 0.0
        for i in range(self.num_var_total):
            var = 0.0
            for j in range(len(self.restricao)):
                if 'a_' in self.base[j+1]:
                    var = var + self.matriz[j+1][i]
                    if i == 0 :
                        l_b = l_b + self.matriz[j+1][-1]
            var = - var
            objetivo.append(var)
        for j in range(self.num_var_a):
            objetivo.append(0.0)
        l_b = -l_b
        objetivo.append(l_b)
        print "\tObjetivo fase 1: ", objetivo
        print "self.matriz: ", self.matriz
        print "objetivo: ", self.funcao_objetivo
        
        matriz = self.matriz

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        while not self.if_ok:
            matriz,objetivo = self.solucionar(matriz,objetivo,1)
        print "\tObjetivo fase 1: ", objetivo
        print "     matriz: ", matriz
        print "ini.matriz: ", self.matriz_ini
        print "self.matriz: ", self.matriz
        print "objetivo: ", self.funcao_objetivo
        new_exp = []
        new_matriz = []
        for i in range(len(self.matriz)):
            print "Old exp: ", matriz[i]
            for j in range(self.num_var_ini+self.num_var_s):
                new_exp.append(matriz[i][j])
            new_exp.append(matriz[i][-1])
            print "New exp: ", new_exp
            new_matriz.append(new_exp)
            new_exp = []
        self.matriz = new_matriz
        print "\tObjetivo fase 1: ", objetivo
        print "     matriz: ", matriz
        print "ini.matriz: ", self.matriz_ini
        print "self.matriz: ", self.matriz
        print "objetivo: ", self.funcao_objetivo,"\n\n"
        self.if_ok = False

