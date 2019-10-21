import curses
import time
import csv
import random
import os
import sys
import hashlib
import json
import socket
import select
import threading

from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN, textpad

menu=['Insertar Bloque','Seleccionar Bloque','Reportes','Historial','Salir']

variableJsonEnviar=['vacio']
listIngresarBloque=['vacio','vacio','vacio','vacio','vacio','vacio']
#listaDobleBloques.insertarFinal(index,fechayhora,clasee,dataa, hashant,miHash)

""" ---------------------------------------------------LISTA DOBLE PARA BLOQUES --------------------------------------------------------------------"""
class nodoDobleBloques():

    def __init__(self, index, hora, clase, dato, hashant, hashh):                  
        self.siguiente = None        
        self.anterior =  None
        self.index = index 
        self.hora=hora
        self.clase=clase
        self.dato=dato
        self.hashant=hashant
        self.hashh=hashh
        self.cadenaG=""

class dobleBloques():
    def __init__(self):
        self.primero=None
        self.ultimo=None
        self.size=0

    def estaVacia(self):
        return self.primero is None
    
    def insertarInicio(self, index, hora, clase, dato, hashant, hashh):
        nuevo=nodoDobleBloques(index, hora, clase, dato, hashant, hashh)
        if self.estaVacia():
            self.primero=nuevo
            self.ultimo=nuevo
        else:
            nuevo.siguiente=self.primero
            self.primero.anterior=nuevo
            self.primero=nuevo

        self.size=self.size+1

    def insertarFinal(self, index, hora, clase, dato, hashant, hashh):
        nuevo=nodoDobleBloques(index, hora, clase, dato, hashant, hashh)
        if self.estaVacia():
            self.primero=nuevo
            self.ultimo=nuevo
        else:
            self.ultimo.siguiente=nuevo
            nuevo.anterior=self.ultimo
            self.ultimo=nuevo
            
        self.size=self.size+1

    def vaciar(self):
        self.primero=None
        self.ultimo=None
        self.size=0
    
    def tamanio(self):
        return self.size

    def obtenerHashAnt(self):
        if self.estaVacia():
            print("lista Vacia")
        else:            
            temp=self.primero
            for i in range(self.size-1):
                temp=temp.siguiente
            return temp.hashh

    def obtenerIndex(self):
        if self.estaVacia():
            print("lista Vacia")
        else:            
            temp=self.primero
            for i in range(self.size-1):
                temp=temp.siguiente
            return temp.index

    def getDataDeNodo(self, indexx):
        actual=self.primero
        for i in range(indexx):
            actual=actual.siguiente
        return actual.dato

    def obtenerCadenaParaCarrusel(self, indexx):
        actual=self.primero
        for i in range(indexx):
            actual=actual.siguiente
        cadret="INDEX: "+str(actual.index)+"\n"
        cadret+="TIMESTAMP: " + str(actual.hora) + "\n"
        cadret+="CLASS: " + str(actual.clase) + "\n"
        cadret+="DATA: " + str(actual.dato[0:250]) + ",\n"
        cadret+="PREVIOUSHASH: " + str(actual.hashant) + "\n"
        cadret+="HASH: " + str(actual.hashh)
        return cadret

    def reporteBloques(self):
        if self.primero is not None:
            actual=self.primero
            while actual.siguiente is not None:
                self.cadenaG+="\"Class= " + actual.clase + "\nTimeStamp= " + actual.hora + "\nPHASH= " + actual.hashant + "\n HASH= " + actual.hashh + "\""
                self.cadenaG+=" -> " + "\"Class= " + actual.siguiente.clase + "\nTimeStamp= " + actual.siguiente.hora + "\nPHASH= " + actual.siguiente.hashant + "\n HASH= " + actual.siguiente.hashh + "\" [dir=both];"
                actual=actual.siguiente     
    
    def generarImagenGraphiz(self):
        # open(nombre_archivo.ext, formato)
        f = open("ReportBlockChain.dot", "w") 
        # write("texto a escribir") 
        
        f.write("digraph G {\n")
        f.write("node [shape=record,width=.1,height=.1];")
        
        a=self.cadenaG
        f.write(a)

        f.write("}")
        # CIERRA EL ARCHIVO
        f.close()
        # dot -Tjpg ruta_archivo_dot.dot -o nombre_archivo_salida.jpg
        os.system("dot -Tjpg"+ " ReportBlockChain.dot " +"-o ReportBlockChain.jpg")
        os.system("ReportBlockChain.jpg")

    def limpiarCadenaG(self):
        self.cadenaG=""

    def imprimirLista(self):
    
        if self.estaVacia():
            print("lista Vacia")
        else:            
            temp=self.primero
            for i in range(self.size):
                cad= str(temp.index) + " " + str(temp.hora) + " " + temp.clase + " " + temp.dato + " " + str(temp.hashant) + " " + str(temp.hashh)
                print(cad,end=" ")
                temp=temp.siguiente

""" ------------------------------------------------------- COLA HISTORIAL --------------------------------------------------------------------"""
class nodoHistorial():
    def __init__(self, msjHistorial):                  
        self.siguiente = None        
        self.msjHistorial = msjHistorial 

class colaHistorial():
    def __init__(self):
        self.primero=None
        self.ultimo=None
        self.size=0

    def estaVacia(self):
        return self.primero is None

    def insertarFinal(self, msjHistorial):
        nuevo=nodoHistorial(msjHistorial)
        if self.estaVacia():
            self.primero=nuevo
            self.ultimo=nuevo
        else:
            self.ultimo.siguiente=nuevo
            self.ultimo=nuevo
        self.size=self.size+1

    def obtenerHist(self, index):
        actual=self.primero
        for i in range(index):
            actual=actual.siguiente
        return actual.msjHistorial

    def tamanio(self):
        return self.size

    def eliminar(self):
        aux=self.primero.siguiente
        self.primero.siguiente=None
        self.primero=aux
        self.size=self.size-1
    
    def vaciar(self):
        self.primero=None
        self.ultimo=None
        self.size=0
     
""" ------------------------------------------------------------ ARBOL AVL -------------------------------------------------------------------"""
class nodoArbolAVL():
    def __init__(self,nombre, carnet):
        self.hijoIzq=None
        self.hijoDer=None
        self.nombre=nombre
        self.carnet=carnet
        #self.altura=altura
        self.fe=0

class miArbolAVL():
    root=None
    cadenaG=""
    preport=[]
    def _init_(self):
        self.root=None
        self.cadenaG="" 
        self.preport=[] 

    def obtenerRaiz(self):
        return self.root

    def setRaiz(self, arbolG):
        self.root=arbolG

    def buscarEnAVL(self, valor, nodoAVL):
        if self.root==None:
            return None
        elif nodoAVL.carnet==valor:
            return nodoAVL
        elif nodoAVL.carnet<valor:
            return buscarEnAVL(valor,nodoAVL.hijoDer)
        elif nodoAVL.carnet>valor:
            return buscarEnAVL(valor,nodoAVL.hijoIzq)

    def obtenerFE(self, arbolX):
        if arbolX==None:
            return -1
        else:
            return arbolX.fe

    def rotacionSimpleIzquierda(self, arbolC):
        auxiliar=arbolC.hijoIzq
        arbolC.hijoIzq=auxiliar.hijoDer
        auxiliar.hijoDer=arbolC
        arbolC.fe=max(self.obtenerFE(arbolC.hijoIzq),self.obtenerFE(arbolC.hijoDer))+1
        auxiliar.fe==max(self.obtenerFE(auxiliar.hijoIzq),self.obtenerFE(auxiliar.hijoDer))+1
        return auxiliar

    def rotacionSimpleDerecha(self, arbolC):
        auxiliar=arbolC.hijoDer
        arbolC.hijoDer=auxiliar.hijoIzq
        auxiliar.hijoIzq=arbolC
        arbolC.fe=max(self.obtenerFE(arbolC.hijoIzq),self.obtenerFE(arbolC.hijoDer))+1
        auxiliar.fe==max(self.obtenerFE(auxiliar.hijoIzq),self.obtenerFE(auxiliar.hijoDer))+1
        return auxiliar

    def rotacionDobleIzquierda(self, arbolC):
        arbolC.hijoIzq=self.rotacionSimpleDerecha(arbolC.hijoIzq)
        temporal=self.rotacionSimpleIzquierda(arbolC)
        return temporal

    def rotacionDobleDerecha(self, arbolC):
        arbolC.hijoDer=self.rotacionSimpleIzquierda(arbolC.hijoDer)
        temporal=self.rotacionSimpleDerecha(arbolC)
        return temporal

    def insertarAVL(self, nuevo, subArb):
        nuevoPadre=subArb
        if nuevo.carnet<subArb.carnet:
            if subArb.hijoIzq==None:
                subArb.hijoIzq=nuevo
            else:
                subArb.hijoIzq=self.insertarAVL(nuevo,subArb.hijoIzq)
                if (self.obtenerFE(subArb.hijoIzq)-self.obtenerFE(subArb.hijoDer)==2):
                    if nuevo.carnet<subArb.hijoIzq.carnet:
                        nuevoPadre=self.rotacionSimpleIzquierda(subArb)
                    else:
                        nuevoPadre=self.rotacionDobleIzquierda(subArb)            
        elif nuevo.carnet>subArb.carnet:
            if subArb.hijoDer==None:
                subArb.hijoDer=nuevo
            else:
                subArb.hijoDer=self.insertarAVL(nuevo,subArb.hijoDer)
                if ((self.obtenerFE(subArb.hijoDer)-self.obtenerFE(subArb.hijoIzq)==2)):
                    if nuevo.carnet>subArb.hijoDer.carnet:
                        nuevoPadre=self.rotacionSimpleDerecha(subArb)
                    else:
                        nuevoPadre=self.rotacionDobleDerecha(subArb)   
        else:
            print("Nodo Duplicado")

        #actualizando altura
        if subArb.hijoIzq==None and subArb.hijoDer!=None:
            subArb.fe=subArb.hijoDer.fe+1
        elif subArb.hijoDer==None and subArb.hijoIzq!=None:
            subArb.fe=subArb.hijoIzq.fe+1
        else:
            subArb.fe=max(self.obtenerFE(subArb.hijoIzq), self.obtenerFE(subArb.hijoDer))+1

        return nuevoPadre

    def insertar(self, nom, carne):
        nuevo=nodoArbolAVL(nom,carne)
        if self.root is None:
            self.root=nuevo
        else:
            self.root=self.insertarAVL(nuevo,self.root)

    def recorridoPreOrden(self, arbolR):
        if arbolR!=None:
            print(arbolR.carnet,end=" ")
            self.recorridoPreOrden(arbolR.hijoIzq)
            self.recorridoPreOrden(arbolR.hijoDer)

    def recorridoPosOrden(self, arbolR):
        if arbolR!=None:            
            self.recorridoPosOrden(arbolR.hijoIzq)
            self.recorridoPosOrden(arbolR.hijoDer)
            print(arbolR.carnet,end=" ")

    def recorridoInOrden(self, arbolR):
        if arbolR!=None:            
            self.recorridoInOrden(arbolR.hijoIzq)
            print(arbolR.carnet,end=" ")
            self.recorridoInOrden(arbolR.hijoDer)

    def construirArbolAVLdesdeArbolBinario(self, arbolG):
        if arbolG!=None:            
            self.construirArbolAVLdesdeArbolBinario(arbolG.hijoIzq)
            self.insertar(arbolG.nombre,int(arbolG.carnet))
            self.construirArbolAVLdesdeArbolBinario(arbolG.hijoDer)
    
    def obtenerAlturaNodo(self, arbolG):
        mayor=0
        tempo=0
        if arbolG==None:
            return 0
        else:
            tempo=self.obtenerAlturaNodo(arbolG.hijoIzq)
            if tempo>mayor:
                mayor=tempo
            tempo=self.obtenerAlturaNodo(arbolG.hijoDer)
            if tempo>mayor:
                mayor=tempo
            return mayor+1

    def obtenerFactorEquilibrio(self, arbolG):
        if arbolG.hijoIzq is None and arbolG.hijoDer is None:
            return 0
        elif arbolG.hijoIzq is None and arbolG.hijoDer is not None:
            return 1
        elif arbolG.hijoIzq is not None and arbolG.hijoDer is None:
            return -1
        elif arbolG.hijoIzq is not None and arbolG.hijoDer is not None:
            althi=self.obtenerAlturaNodo(arbolG.hijoIzq)
            althd=self.obtenerAlturaNodo(arbolG.hijoDer)
            op=althd-althi
            return op

    def reporteGraphvizArbol(self, arbolR):
        if arbolR==None:
            return
        else:
            if arbolR.hijoIzq!=None:
                altura=self.obtenerAlturaNodo(arbolR)
                alturaHI=self.obtenerAlturaNodo(arbolR.hijoIzq)
                facte=self.obtenerFactorEquilibrio(arbolR)
                facte2=self.obtenerFactorEquilibrio(arbolR.hijoIzq)
                self.cadenaG+="\"Nombre: " + str(arbolR.nombre) + " \nCarnet: " + str(arbolR.carnet) + " \nFE: " + str(facte) + " \nAltura: " + str(altura) + "\" -> \"Nombre: " + str(arbolR.hijoIzq.nombre) + " \nCarnet: " + str(arbolR.hijoIzq.carnet) + " \nFE: "+ str(facte2) +" \nAltura: " + str(alturaHI) + "\" \n"
            else:
                altura=self.obtenerAlturaNodo(arbolR)
                facte=self.obtenerFactorEquilibrio(arbolR)
                self.cadenaG+="\"Nombre: " + str(arbolR.nombre) + " \nCarnet: " + str(arbolR.carnet) + " \nFE: " + str(facte) + " \nAltura: " + str(altura) + "\" -> \"" + str(arbolR.carnet) + " NULL IZQ \" \n"
            if arbolR.hijoDer!=None:
                altura=self.obtenerAlturaNodo(arbolR)
                alturaDE=self.obtenerAlturaNodo(arbolR.hijoDer)
                facte=self.obtenerFactorEquilibrio(arbolR)
                facte2=self.obtenerFactorEquilibrio(arbolR.hijoDer)
                self.cadenaG+="\"Nombre: " + str(arbolR.nombre) + " \nCarnet: " + str(arbolR.carnet) + " \nFE: " + str(facte) + " \nAltura: " + str(altura) + "\" -> \"Nombre: " + str(arbolR.hijoDer.nombre) + " \nCarnet: " + str(arbolR.hijoDer.carnet) + " \nFE: "+ str(facte2) +" \nAltura: " + str(alturaDE) + "\" \n"
            else:
                altura=self.obtenerAlturaNodo(arbolR)
                facte=self.obtenerFactorEquilibrio(arbolR)
                self.cadenaG+="\"Nombre: " + str(arbolR.nombre) + " \nCarnet: " + str(arbolR.carnet) + " \nFE: " + str(facte) + " \nAltura: " + str(altura) + "\" -> \"" + str(arbolR.carnet) + " NULL DER \" \n"
        self.reporteGraphvizArbol(arbolR.hijoDer)
        self.reporteGraphvizArbol(arbolR.hijoIzq)

    def reporteRecorridoPreOrden(self, arbolR):
        if arbolR!=None:
            cadin="\"Carnet: " + str(arbolR.carnet) + "\nNombre: " + str(arbolR.nombre) + "\""
            self.preport.append(cadin)
            self.reporteRecorridoPreOrden(arbolR.hijoIzq)
            self.reporteRecorridoPreOrden(arbolR.hijoDer)

    def reporteRecorridoPosOrden(self, arbolR):
        if arbolR!=None:            
            self.reporteRecorridoPosOrden(arbolR.hijoIzq)
            self.reporteRecorridoPosOrden(arbolR.hijoDer)
            cadin="\"Carnet: " + str(arbolR.carnet) + "\nNombre: " + str(arbolR.nombre) + "\""
            self.preport.append(cadin)

    def reporteRecorridoInOrden(self, arbolR):
        if arbolR!=None:            
            self.reporteRecorridoInOrden(arbolR.hijoIzq)
            cadin="\"Carnet: " + str(arbolR.carnet) + "\nNombre: " + str(arbolR.nombre) + "\""
            self.preport.append(cadin)
            self.reporteRecorridoInOrden(arbolR.hijoDer)

    def reporteRecorridoPreOrdenConsola(self, arbolR):
        if arbolR!=None:
            cadin=str(arbolR.carnet) + "-" + str(arbolR.nombre)
            self.preport.append(cadin)
            self.reporteRecorridoPreOrdenConsola(arbolR.hijoIzq)
            self.reporteRecorridoPreOrdenConsola(arbolR.hijoDer)

    def reporteRecorridoPosOrdenConsola(self, arbolR):
        if arbolR!=None:            
            self.reporteRecorridoPosOrdenConsola(arbolR.hijoIzq)
            self.reporteRecorridoPosOrdenConsola(arbolR.hijoDer)
            cadin=str(arbolR.carnet) + "-" + str(arbolR.nombre)
            self.preport.append(cadin)

    def reporteRecorridoInOrdenConsola(self, arbolR):
        if arbolR!=None:            
            self.reporteRecorridoInOrdenConsola(arbolR.hijoIzq)
            cadin=str(arbolR.carnet) + "-" + str(arbolR.nombre)
            self.preport.append(cadin)
            self.reporteRecorridoInOrdenConsola(arbolR.hijoDer)

    def generarCadenaRecorrido(self):
        cont=1
        for ml in self.preport:
            if cont == self.preport.__len__():
                break
            else:                
                self.cadenaG+=str(ml) + " -> " + str(self.preport[cont]) + " \n"
            cont=cont+1

    def generarCadenaRecorridoConsola(self):
        cont=1
        for ml in self.preport:
            if cont == self.preport.__len__():
                self.cadenaG+=str(ml) + " -> null"
                break
            else:                
                self.cadenaG+=str(ml) + " -> "           
            cont=cont+1
        return self.cadenaG

    def generarImagenGraphiz(self,nomimg):
        # open(nombre_archivo.ext, formato)        
        f = open(str(nomimg)+".dot", "w") 
        # write("texto a escribir") 
        
        f.write("digraph G {\n")
        f.write("node [shape=record,width=.1,height=.1];")
        
        a=self.cadenaG
        f.write(a)

        f.write("}")
        # CIERRA EL ARCHIVO
        f.close()
        # dot -Tjpg ruta_archivo_dot.dot -o nombre_archivo_salida.jpg
        os.system("dot -Tjpg " + str(nomimg) + ".dot -o " + str(nomimg) + ".jpg")
        os.system(str(nomimg)+".jpg")

    def limpiarCadenaG(self):
        self.cadenaG=""

    def limpiarListRecorrido(self):
        self.preport=[]

    def limpiarRaiz(self):
        self.root=None
    
""" --------------------------------------------------------- PARA CREAR ARBOL ---------------------------------------------------------------------"""
class ingresarEnLista:

    def __init__(self):
        self.ingresar=""
        self.ingresar2=""
        self.guion=""
        self.listArbol=[]
        self.letrasNum=["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","0","1","2","3","4","5","6","7","8","9"]
        self.simb=[",",":","{","}"]
        self.recorrido=None

    def ingresarEnListParaContruccionArbolBinario(self,cadena):
        for cad in cadena:
            if cad!=" " and cad!="\n" and cad!="\"":
                if cad =="-":
                    self.listArbol.append(self.ingresar)
                    self.listArbol.append("-")
                    self.ingresar=""
                elif cad in self.letrasNum[0:]:
                    if self.ingresar2!="":
                        self.listArbol.append(self.ingresar2)
                        self.ingresar2="" 
                    self.ingresar+=cad               
                elif cad in self.simb[0:]:
                    if self.ingresar!="":
                        self.listArbol.append(self.ingresar)
                        self.ingresar=""
                    self.ingresar2+=cad
        if self.ingresar!="":
            self.listArbol.append(self.ingresar)
        elif self.ingresar2!="":
            self.listArbol.append(self.ingresar2)
        self.ingresar=""
        self.ingresar2=""
        
        miraizz=self.ingresarEnArbolBinario()
        return miraizz
    
    def ingresarEnArbolBinario(self):
        listLlaves=[]
        listMov=[]
        cont=0 #para saber el index de lista en que voy
        contIzqoDer=0
        #oa=miArbolAVL()
        miRaiz=None

        for ol in self.listArbol: #recorro la lista
            for odcl in ol: #recorro cada caracter de elemento de lista
                if odcl=="{":
                    listLlaves.append("{")
                elif odcl=="}":
                    listLlaves.pop(0)
                    if listMov.__len__()>0: #cada vez que encuentre llave, eliminara el ultimo elemento de la lista
                        listMov.pop(listMov.__len__()-1)
            if ol=="value" and listLlaves.count("{")==1: #quiere decir que es la raiz
                carn=self.listArbol[cont+2]
                nom=self.listArbol[cont+4]                
                miRaiz=self.ingresarRaiz(nom,carn,miRaiz)
            elif ol=="value" and listLlaves.count("{")>1: #recorrera hacia izq o der
                carn=self.listArbol[cont+2]
                nom=self.listArbol[cont+4]                
                nuevo=nodoArbolAVL(nom,carn)
                self.recorrido=miRaiz
                contt=1
                for rec in listMov:
                    if contt==listMov.__len__(): #validar que sea el ultimo elemento de la lista
                        if listMov[listMov.__len__()-1]=="left": #ingresara por la izquierda
                            self.recorrido.hijoIzq=nuevo
                        elif listMov[listMov.__len__()-1]=="right": #ingresara por la derecha
                            self.recorrido.hijoDer=nuevo
                    elif rec=="left": #sino es el ultimo recorrera por la izquierda
                        try:
                            self.recorrido=self.recorrido.hijoIzq
                        except:
                            pass                                        
                    elif rec=="right": #sino es el ultimo recorrera por la derecha
                        try:
                            self.recorrido=self.recorrido.hijoDer
                        except:
                            pass                        
                    contt=contt+1
            elif ol=="left":
                listMov.append("left")
            elif ol=="right":
                listMov.append("right")
            elif ol=="null":
                listMov.pop(listMov.__len__()-1)
            
            cont=cont+1
        return miRaiz
    
    def ingresarRaiz(self, nom, carne, miArbol):
        nuevo=nodoArbolAVL(nom,carne)
        miArbol=nuevo
        return miArbol
   
""" ------------------------------------------------------------ OBJETOS ---------------------------------------------------------------------"""
listaDobleBloques= dobleBloques()
classMetArbol=miArbolAVL()
classIngreLista=ingresarEnLista()
listHistorial=colaHistorial()

def generarHash(cadenah):
    hash = hashlib.sha256()
    stexto=cadenah
    hash.update(stexto.encode())
    return hash.hexdigest()

def generarCadenaJSON(indexj, fechaj, classj, dataj, prevhash, hashj):
    
    cadgen="{\n"
    cadgen+="\"INDEX\": " + str(indexj) + ",\n"
    cadgen+="\"TIMESTAMP\": \"" + str(fechaj) + "\",\n"
    cadgen+="\"CLASS\": \"" + str(classj) + "\",\n"
    cadgen+="\"DATA\": " + str(dataj) + ",\n"
    cadgen+="\"PREVIOUSHASH\": \"" + str(prevhash) + "\",\n"
    cadgen+="\"HASH\": \"" + str(hashj) + "\"\n"
    cadgen+="}"

    f = open("JsonEnviado.json", "w") 
    f.write(cadgen)
    f.close()
    return cadgen

def validarQueBlockChainEsteBueno(cadenaBC):
    #creo el el .json
    f=open("JsonRecibido.json", "w") 
    f.write(cadenaBC)
    f.close()

    #variables para extraer datos en json
    indexj=""
    fechaj=""
    classj=""
    dataj=""
    prevhash=""
    hashj=""

    #abro el .json creado
    with open("JsonRecibido.json") as contenido:
        result=json.load(contenido)
        for res in result:
            if res=='INDEX':
                indexj=result['INDEX']
            if res=='TIMESTAMP':
                fechaj=result['TIMESTAMP']
            if res=='CLASS':
                classj=result['CLASS']
            if res=='DATA':
                dataj=result['DATA']
            if res=='PREVIOUSHASH':
                prevhash=result['PREVIOUSHASH']
            if res=='HASH':
                hashj=result['HASH']
    
    dataj=str(dataj)

    #se quitan espacios, saltos de linea, se cambia ' por " y se cambia None por null
    dataj=dataj.replace("\n","")
    dataj=dataj.replace(" ","")
    dataj=dataj.replace("\'","\"")
    dataj=dataj.replace('None','null')       

    #concatenacion y generar hash
    cadenaHash=str(indexj)+str(fechaj)+str(classj)+str(dataj)+str(prevhash)
    mihashg=generarHash(cadenaHash)

    #se compueba si el hash esta bueno
    hashBueno='false'
    if hashj==mihashg:
        #ingreso datos a lista ya creada, es espera a que el servidor retorne true para luego agregarla a lista doble enlazada
        #listaDobleBloques.insertarFinal(index,fechayhora,clasee,dataa, hashant,miHash)
        listIngresarBloque[0]=str(indexj)
        listIngresarBloque[1]=str(fechaj)
        listIngresarBloque[2]=str(classj)
        listIngresarBloque[3]=str(dataj)
        listIngresarBloque[4]=str(prevhash)
        listIngresarBloque[5]=str(hashj) 
        hashBueno='true'
        #print("\nBLOCK BUENO\n")
    
    return hashBueno
  
""" ----------------------------------------------------PARA EL MENU PRINCIPAL ---------------------------------------------------------------"""
def print_menu(stdscr, selected_row_idx):
    h, w= stdscr.getmaxyx()
        
    for idx, row in enumerate(menu):
        x=w//2 - len(row)//2
        y=h//2 -len(menu) + idx
        if idx==selected_row_idx:
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y,x,row)
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(y,x,row)


    stdscr.refresh()
  
def menu_principal(stdscr):
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

    indice_fila_actual=0

    print_menu(stdscr,indice_fila_actual)
    
    while 1:
        key=stdscr.getch()
        stdscr.clear()

        if key == curses.KEY_UP and indice_fila_actual>0:
            indice_fila_actual-=1
        elif key == curses.KEY_DOWN and indice_fila_actual<len(menu)-1:
            indice_fila_actual+=1
        elif key==curses.KEY_ENTER or key in [10,13]:           
            if indice_fila_actual==0:
                a=""
                stdscr.addstr(2,2,"Ingrese nombre de archivo.csv y luego presione ENTER: \n\n ")
                while True:
                    tecla = stdscr.getch()                    
                    if tecla>48 and tecla <58:#numeros
                        a+=chr(tecla)
                        stdscr.addstr(2,2,"Ingrese nombre de archivo.csv y luego presione ENTER: ")
                        stdscr.addstr(4,2,format(a))
                    elif tecla>64 and tecla<91:#letras mayusculas
                        a+=chr(tecla)
                        stdscr.addstr(2,2,"Ingrese nombre de archivo.csv y luego presione ENTER: ")
                        stdscr.addstr(4,2,format(a))
                    elif tecla>96 and tecla <123:#letras minusculas
                        a+=chr(tecla)
                        stdscr.addstr(2,2,"Ingrese nombre de archivo.csv y luego presione ENTER: ")
                        stdscr.addstr(4,2,format(a))
                    elif tecla==46:#punto
                        a+=chr(tecla)
                        stdscr.addstr(2,2,"Ingrese nombre de archivo.csv y luego presione ENTER: ")
                        stdscr.addstr(4,2,format(a))
                    elif tecla==8:#borrar
                        temp=len(a)
                        a=a[:temp-1]
                        stdscr.addstr(2,2,"Ingrese nombre de archivo.csv y luego presione ENTER: ")
                        stdscr.addstr(4,2,format(a))
                    elif tecla==10:#enter   
                        try:                   
                            archivoBloque(str(a))
                            stdscr.addstr(20,40,"BLOQUE CARGADO CORRECTAMENTE!")
                            stdscr.getch()
                            stdscr.clear()
                            stdscr.refresh()                            
                            break
                        except:
                            stdscr.addstr(20,35,"EL NOMBRE DEL ARCHIVO NO SE ENCONTRO!")
                            stdscr.refresh()
                            stdscr.getch()
                            stdscr.clear()
                            stdscr.refresh() 
                            break  
            elif indice_fila_actual==1:   
                if listaDobleBloques.estaVacia():
                    stdscr.addstr(11,32,"NO HAY BLOQUES!")
                    stdscr.getch()  
                    stdscr.clear()
                    stdscr.refresh() 
                else:    
                   curses.wrapper(menu_bloques)          
            elif indice_fila_actual==2:
                a=""
                stdscr.addstr(2,0,"REPORTES: \n\n1. BlockChain \n2. Visualizar Arbol \n3. Mostrar Recorrido PreOrden \n4. Mostrar Recorrido PosOrden \n5. Mostrar Recorrido InOrden \n6. Mostrar Recorrido PreOrden (Consola) \n7. Mostrar Recorrido PosOrden (Consola) \n8. Mostrar Recorrido InOrden (Consola) \n\n ")
                while True:
                    tecla = stdscr.getch()                    
                    if tecla>48 and tecla <58:#numeros
                        a+=chr(tecla)
                        stdscr.addstr(14,2,format(a))
                    elif tecla>64 and tecla<91:#letras mayusculas
                        a+=chr(tecla)
                        stdscr.addstr(14,2,format(a))
                    elif tecla>96 and tecla <123:#letras minusculas
                        a+=chr(tecla)
                        stdscr.addstr(14,2,format(a))
                    elif tecla==46:#punto
                        a+=chr(tecla)
                        stdscr.addstr(14,2,format(a))
                    elif tecla==8:#borrar
                        temp=len(a)
                        a=a[:temp-1]
                        stdscr.addstr(14,2,format(a))
                    elif tecla==10:#enter                                                
                        if a=="1":
                            try:
                                listaDobleBloques.limpiarCadenaG()
                                listaDobleBloques.reporteBloques()
                                listaDobleBloques.generarImagenGraphiz()
                                stdscr.clear()
                                stdscr.refresh()
                                break
                            except:
                                stdscr.addstr(20,35,"SE PRODUJO UN ERROR!")
                                stdscr.refresh()
                                stdscr.getch()
                                stdscr.clear()
                                stdscr.refresh() 
                                break
                        elif a=="2":
                            try:
                                classMetArbol.limpiarCadenaG()
                                classMetArbol.reporteGraphvizArbol(classMetArbol.obtenerRaiz())
                                classMetArbol.generarImagenGraphiz("ArbolReport")
                                stdscr.clear()
                                stdscr.refresh()
                                break
                            except:
                                stdscr.addstr(20,35,"SE PRODUJO UN ERROR!")
                                stdscr.refresh()
                                stdscr.getch()
                                stdscr.clear()
                                stdscr.refresh() 
                                break
                        elif a=="3":
                            try:
                                classMetArbol.limpiarListRecorrido()
                                classMetArbol.limpiarCadenaG()
                                classMetArbol.reporteRecorridoPreOrden(classMetArbol.obtenerRaiz())
                                classMetArbol.generarCadenaRecorrido()
                                classMetArbol.generarImagenGraphiz("PreOrdenReport")
                                stdscr.clear()
                                stdscr.refresh()                            
                                break
                            except:
                                stdscr.addstr(20,35,"SE PRODUJO UN ERROR!")
                                stdscr.refresh()
                                stdscr.getch()
                                stdscr.clear()
                                stdscr.refresh() 
                                break
                        elif a=="4":
                            try:
                                classMetArbol.limpiarListRecorrido()
                                classMetArbol.limpiarCadenaG()
                                classMetArbol.reporteRecorridoPosOrden(classMetArbol.obtenerRaiz())
                                classMetArbol.generarCadenaRecorrido()
                                classMetArbol.generarImagenGraphiz("PosOrdenReport")
                                stdscr.clear()
                                stdscr.refresh() 
                                break
                            except:
                                stdscr.addstr(20,35,"SE PRODUJO UN ERROR!")
                                stdscr.refresh()
                                stdscr.getch()
                                stdscr.clear()
                                stdscr.refresh() 
                                break
                        elif a=="5":
                            try:
                                classMetArbol.limpiarListRecorrido()
                                classMetArbol.limpiarCadenaG()
                                classMetArbol.reporteRecorridoInOrden(classMetArbol.obtenerRaiz())
                                classMetArbol.generarCadenaRecorrido()
                                classMetArbol.generarImagenGraphiz("InOrdenReport")
                                stdscr.clear()
                                stdscr.refresh() 
                                break
                            except:
                                stdscr.addstr(20,35,"SE PRODUJO UN ERROR!")
                                stdscr.refresh()
                                stdscr.getch()
                                stdscr.clear()
                                stdscr.refresh() 
                                break
                        elif a=="6":
                            try:
                                classMetArbol.limpiarListRecorrido()
                                classMetArbol.limpiarCadenaG()
                                classMetArbol.reporteRecorridoPreOrdenConsola(classMetArbol.obtenerRaiz())
                                micad=classMetArbol.generarCadenaRecorridoConsola()
                                stdscr.addstr(16,0,str(micad))
                                stdscr.getch() 
                                stdscr.clear()
                                stdscr.refresh() 
                                break
                            except:
                                stdscr.addstr(20,35,"SE PRODUJO UN ERROR!")
                                stdscr.refresh()
                                stdscr.getch()
                                stdscr.clear()
                                stdscr.refresh() 
                                break
                        elif a=="7":
                            try:
                                classMetArbol.limpiarListRecorrido()
                                classMetArbol.limpiarCadenaG()
                                classMetArbol.reporteRecorridoPosOrdenConsola(classMetArbol.obtenerRaiz())
                                micad=classMetArbol.generarCadenaRecorridoConsola()
                                stdscr.addstr(16,0,str(micad))
                                stdscr.getch() 
                                stdscr.clear()
                                stdscr.refresh()                             
                                break 
                            except:
                                stdscr.addstr(20,35,"SE PRODUJO UN ERROR!")
                                stdscr.refresh()
                                stdscr.getch()
                                stdscr.clear()
                                stdscr.refresh() 
                                break
                        elif a=="8":
                            try:
                                classMetArbol.limpiarListRecorrido()
                                classMetArbol.limpiarCadenaG()
                                classMetArbol.reporteRecorridoInOrdenConsola(classMetArbol.obtenerRaiz())
                                micad=classMetArbol.generarCadenaRecorridoConsola()
                                stdscr.addstr(16,0,str(micad))
                                stdscr.getch() 
                                stdscr.clear()
                                stdscr.refresh() 
                                break
                            except:
                                stdscr.addstr(20,35,"SE PRODUJO UN ERROR!")
                                stdscr.refresh()
                                stdscr.getch()
                                stdscr.clear()
                                stdscr.refresh() 
                                break 
                        else:
                            stdscr.addstr(22,52,"OPCION INCORRECTA!")
                            stdscr.getch()  
                            stdscr.clear()
                            stdscr.refresh()
                            break 
            elif indice_fila_actual==3:
                if listaDobleBloques.estaVacia():
                    stdscr.addstr(11,32,"NO HAY HISTORIAL!")
                    stdscr.getch()  
                    stdscr.clear()
                    stdscr.refresh() 
                else:    
                   curses.wrapper(menu_Historial) 
            elif indice_fila_actual==len(menu)-1:
                hiloCom.stop()
                sys.exit()                
                '''llegadaMensaje()
                time.sleep(1)
                stdscr.clear()
                stdscr.refresh()
                #stdscr.clear()'''                
        
        print_menu(stdscr,indice_fila_actual)
        stdscr.refresh()

""" ------------------------------------------------------PARA MOSTRAR BLOQUES --------------------------------------------------------------"""

def menu_bloques(stdscr): #INICIA LAS PROPIEDADES BASICAS
    curses.curs_set(0) # SETEA EL CURSOR EN LA POSICION 0
    index = 0
    pintar_menu(stdscr, 0) # VA A INICAR EN EL INDICE 0
    while True:
        tecla = stdscr.getch() # OBTENEMOS EL CARACTER DEL TECLADO
        if(tecla == curses.KEY_RIGHT): # VERIFICAMOS SI EL FLECHA A LA DERECHA
            index = index + 1
        elif (tecla == curses.KEY_LEFT ): # VERIFICAMOS SI ES FLECHA A LA IZQUIERDA
            index = index - 1
        elif (tecla == 27): # SI ES LA TECLA DE SCAPE.... 
            stdscr.clear()
            stdscr.refresh()
            curses.wrapper(menu_principal)
        elif (tecla==curses.KEY_ENTER) or tecla in [10,13]:
            try:
                classMetArbol.limpiarCadenaG()
                classMetArbol.limpiarRaiz()
                nuevar=listaDobleBloques.getDataDeNodo(index)
                arb=classIngreLista.ingresarEnListParaContruccionArbolBinario(nuevar) 
                classMetArbol.construirArbolAVLdesdeArbolBinario(arb)
            except:
                stdscr.addstr(20,35,"OCURRIO UN ERROR!")
                stdscr.refresh()
                stdscr.getch()
            #classMetArbol.setRaiz(nuevar)
        if( index < 0): # EN CASO DE QUE EL INDICE SE VUELVA NEGAVITO LO DEJAMOS EN 0
            index = listaDobleBloques.tamanio()-1
        if( index >= listaDobleBloques.tamanio()): # EN CASO QUE EL INDICE SE VUELVA MAYOR AL SIZE DEL ARREGLO...
            index = 0 # ... LO LIMITAMOS AL ULTIMO INDICE VALIDO
        pintar_menu(stdscr, index) # MANDAMOS A REPINTAR LA PANTALLA

def pinter_ventana(stdscr):
    # -----------------------------------------------------------
    # PINTAMOS EL MARCO DEL MENU
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE) # COLOR DEL MARCO
    stdscr.attron(curses.color_pair(1)) # PERMITE HABILITAR UN ATRIBUTO ESPECIFICO
    stdscr.box("|", "-") ## PINTA EL MARCO
    stdscr.attroff(curses.color_pair(1)) # DESHABILITA EL ATRIBUTO ESPECIICO
    stdscr.refresh()
    # -----------------------------------------------------------

def pintar_menu(stdsrc, index):
    # -----------------------------------------------------------
    stdsrc.clear() # LIMPIA LA CONSOLA
    pinter_ventana(stdsrc) # MANDA A PINTAR EL MARCO
    altura, ancho = stdsrc.getmaxyx() # OBTIENE LA ALTURA Y ANCHO DE LA PANTALLA
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLUE) # COLOR DE LAS OPCIONES, INIICIALIZA UNA PAREJA DE COLORES EL COLOR DE LETRA Y COLOR DE FONDO RESPECTIVAMENTE
    y = int(0) 
    x = int(0)
    stdsrc.addstr(y,x, listaDobleBloques.obtenerCadenaParaCarrusel(index), curses.color_pair(2)) # HAGREGA UNA CADENA  LA PANTALLA EN COORDENADAS Y, X Y UN ATRIBUTO EN ESTE CASO ES LA PAREJA DE COLORES
    stdsrc.refresh()

""" ------------------------------------------------------PARA MOSTRAR HISTORIAL --------------------------------------------------------------"""

def menu_Historial(stdscr): #INICIA LAS PROPIEDADES BASICAS
    curses.curs_set(0) # SETEA EL CURSOR EN LA POSICION 0
    index = 0
    pintar_menu_Historial(stdscr, 0) # VA A INICAR EN EL INDICE 0
    while True:
        tecla = stdscr.getch() # OBTENEMOS EL CARACTER DEL TECLADO
        if(tecla == curses.KEY_RIGHT): # VERIFICAMOS SI EL FLECHA A LA DERECHA
            index = index + 1
        elif (tecla == curses.KEY_LEFT ): # VERIFICAMOS SI ES FLECHA A LA IZQUIERDA
            index = index - 1
        elif (tecla == 27): # SI ES LA TECLA DE SCAPE.... 
            stdscr.clear()
            stdscr.refresh()
            curses.wrapper(menu_principal)
        elif (tecla==curses.KEY_ENTER) or tecla in [10,13]:
            stdscr.clear()
            stdscr.refresh()
            curses.wrapper(menu_principal)
        if( index < 0): # EN CASO DE QUE EL INDICE SE VUELVA NEGAVITO LO DEJAMOS EN 0
            index = listHistorial.tamanio()-1
        if( index >= listHistorial.tamanio()): # EN CASO QUE EL INDICE SE VUELVA MAYOR AL SIZE DEL ARREGLO...
            index = 0 # ... LO LIMITAMOS AL ULTIMO INDICE VALIDO
        pintar_menu_Historial(stdscr, index) # MANDAMOS A REPINTAR LA PANTALLA

def pinter_ventana_Historial(stdscr):
    # -----------------------------------------------------------
    # PINTAMOS EL MARCO DEL MENU
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE) # COLOR DEL MARCO
    stdscr.attron(curses.color_pair(1)) # PERMITE HABILITAR UN ATRIBUTO ESPECIFICO
    stdscr.box("|", "-") ## PINTA EL MARCO
    stdscr.attroff(curses.color_pair(1)) # DESHABILITA EL ATRIBUTO ESPECIICO
    stdscr.refresh()
    # -----------------------------------------------------------

def pintar_menu_Historial(stdsrc, index):
    # -----------------------------------------------------------
    stdsrc.clear() # LIMPIA LA CONSOLA
    pinter_ventana_Historial(stdsrc) # MANDA A PINTAR EL MARCO
    altura, ancho = stdsrc.getmaxyx() # OBTIENE LA ALTURA Y ANCHO DE LA PANTALLA
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLUE) # COLOR DE LAS OPCIONES, INIICIALIZA UNA PAREJA DE COLORES EL COLOR DE LETRA Y COLOR DE FONDO RESPECTIVAMENTE
    y = int(altura/2) 
    x = int((ancho/2)-(len(listHistorial.obtenerHist(index))/2))
    stdsrc.addstr(y,x, listHistorial.obtenerHist(index), curses.color_pair(2)) # HAGREGA UNA CADENA  LA PANTALLA EN COORDENADAS Y, X Y UN ATRIBUTO EN ESTE CASO ES LA PAREJA DE COLORES
    stdsrc.refresh()

def llegadaMensaje():
    fullscreen = curses.initscr() 
    # Dibuja un borde al rededor de los límites del window
    fullscreen.border(0)    
    # Se coloca el texto aproximadamente en el centro
    fullscreen.addstr(12, 25, "----- ENTRADA DE MENSAJE! ------")    
    # Para que los cambios se muestren hay que usar refresh()
    fullscreen.refresh()    
    # Se detiene el programa hasta que una tecla sea pulsada
    #fullscreen.getch()    
    # Se desactiva curses
    #curses.endwin()
 
""" -----------------------------------------------LECTURA ARCHIVO E INGRESO DE DATOS -------------------------------------------------------"""

def archivoBloque(ruta): 
    
    clasee=""
    dataa=""

    with open(ruta) as f:
        reader=csv.reader(f)
        #Obtenemos el nombre de clase, y la estructura data de archivo .csv
        for row in reader:
            us="{0}".format(row[0])
            uss=str(us)
            if uss=="class":
                 #fila 0 de archivo .csv
                clasee="{0}".format(row[1]) #fila 1 de archivo .csv
            elif uss=="data":
                #us="{0}".format(row[0]) #fila 0 de archivo .csv
                dataa="{0}".format(row[1]) #fila 1 de archivo .csv
                #se crea el arbol binario
                #arb=classIngreLista.ingresarEnListParaContruccionArbolBinario(dataa)                 
                #se crea el arbol AVL
                #classMetArbol.limpiarCadenaG()
                #classMetArbol.limpiarRaiz()           
                #classMetArbol.construirArbolAVLdesdeArbolBinario(arb)  
                #classMetArbol.reporteGraphvizArbol(classMetArbol.obtenerRaiz())
                #classMetArbol.generarImagenGraphiz()

     #      
    dataa=str(dataa)
    #

    #verificar si es bloque genesis (bloque cabeza o el primero)
    if listaDobleBloques.estaVacia():
        index="0"
        fecha=time.strftime("%d-%m-%y") 
        hora=time.strftime("%H:%M:%S")
        fechayhora=fecha+"-::"+hora
        hashant="0000"   
        dataa=dataa.replace("\n","")
        dataa=dataa.replace(" ","")
        dataa=dataa.replace("\'","\"")
        cadenaParaHash=str(index) + str(fechayhora) +str(clasee)+str(dataa)+str(hashant)
        miHash=generarHash(cadenaParaHash)        
        listIngresarBloque[0]=str(index)
        listIngresarBloque[1]=str(fechayhora)
        listIngresarBloque[2]=str(clasee)
        listIngresarBloque[3]=str(dataa)
        listIngresarBloque[4]=str(hashant)
        listIngresarBloque[5]=str(miHash) 
        variableJsonEnviar[0]=generarCadenaJSON(index,fechayhora,clasee,dataa,hashant,miHash)
        #validarQueBlockChainEsteBueno(variableJsonEnviar[0])
        #listaDobleBloques.insertarFinal(index,fechayhora,clasee,dataa, hashant,miHash)
    else:
        index=int(listaDobleBloques.obtenerIndex())+1
        fecha=time.strftime("%d-%m-%y")  
        hora=time.strftime("%H:%M:%S")
        fechayhora=fecha+"-::"+hora
        hashant=listaDobleBloques.obtenerHashAnt()
        dataa=dataa.replace("\n","")
        dataa=dataa.replace(" ","")
        dataa=dataa.replace("\'","\"")
        cadenaParaHash=str(index)+str(fechayhora)+str(clasee)+str(dataa)+str(hashant)
        miHash=generarHash(cadenaParaHash)
        listIngresarBloque[0]=str(index)
        listIngresarBloque[1]=str(fechayhora)
        listIngresarBloque[2]=str(clasee)
        listIngresarBloque[3]=str(dataa)
        listIngresarBloque[4]=str(hashant)
        listIngresarBloque[5]=str(miHash)
        variableJsonEnviar[0]=generarCadenaJSON(index,fechayhora,clasee,dataa,hashant,miHash)
        #validarQueBlockChainEsteBueno(variableJsonEnviar[0])
        #listaDobleBloques.insertarFinal(index,fechayhora,clasee,dataa,hashant,miHash)

def comunicacionConServerSiempreEscuchando():
       
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if len(sys.argv) != 3:
        print ("Correct usage: script, IP address, port number")
        exit()
    IP_address = str(sys.argv[1])
    Port = int(sys.argv[2])
    server.connect((IP_address, Port))   

    while True:
        try:
            # mantiene una lista de posibles flujos de entrada
            read_sockets = select.select([server], [], [], 1)[0]
            import msvcrt
            if msvcrt.kbhit(): read_sockets.append(sys.stdin)

            for socks in read_sockets:
                if socks == server: #si recibe un mensaje
                    message = socks.recv(2048)
                    msj=message.decode('utf-8')
                    msj=str(msj)
                    if msj=='true' and listIngresarBloque[0]!='vacio': #guardara en lista
                        try:
                            #se ingresa al historial
                            fecha=time.strftime("%d-%m-%y") 
                            hora=time.strftime("%H:%M:%S")
                            cadinsert=fecha+"-::"+hora+"  TRUE"
                            listHistorial.insertarFinal(str(cadinsert))
                            listaDobleBloques.insertarFinal(listIngresarBloque[0],listIngresarBloque[1],listIngresarBloque[2],listIngresarBloque[3], listIngresarBloque[4],listIngresarBloque[5])
                            #reseteo en espera de otro bloque
                            listIngresarBloque[0]='vacio'
                            listIngresarBloque[1]='vacio'
                            listIngresarBloque[2]='vacio'
                            listIngresarBloque[3]='vacio'
                            listIngresarBloque[4]='vacio'
                            listIngresarBloque[5]='vacio' 
                        except:
                            fecha=time.strftime("%d-%m-%y") 
                            hora=time.strftime("%H:%M:%S")
                            cadinsert=fecha+"-::"+hora+"  ERROR AL LEER TRUE"
                            listHistorial.insertarFinal(str(cadinsert))
                    elif msj=='false': #no guardara en lista
                        try:
                            #se ingresa al historial
                            fecha=time.strftime("%d-%m-%y") 
                            hora=time.strftime("%H:%M:%S")
                            cadinsert=fecha+"-::"+hora+"  FALSE"
                            listHistorial.insertarFinal(str(cadinsert))
                            #reseteo en espera de otro bloque
                            listIngresarBloque[0]='vacio'
                            listIngresarBloque[1]='vacio'
                            listIngresarBloque[2]='vacio'
                            listIngresarBloque[3]='vacio'
                            listIngresarBloque[4]='vacio'
                            listIngresarBloque[5]='vacio'
                        except:
                            fecha=time.strftime("%d-%m-%y") 
                            hora=time.strftime("%H:%M:%S")
                            cadinsert=fecha+"-::"+hora+"  ERROR AL LEER FALSE"
                            listHistorial.insertarFinal(str(cadinsert))
                    else: #sera un blockchain el que recibe
                        try:
                            #se ingresa al historial
                            fecha=time.strftime("%d-%m-%y") 
                            hora=time.strftime("%H:%M:%S")
                            cadinsert=fecha+"-::"+hora+"  BLOCKCHAIN"
                            listHistorial.insertarFinal(str(cadinsert))
                            #se valida que el blockchain este bueno
                            resp=validarQueBlockChainEsteBueno(msj)
                            #se envia msj segun sea la respuesta
                            if resp == 'false': 
                                nNessage = 'false'
                                server.sendall(nNessage.encode('utf-8'))
                                sys.stdout.write(nNessage)
                                sys.stdout.flush()
                            else:
                                nNessage = 'true'
                                server.sendall(nNessage.encode('utf-8'))
                                sys.stdout.write(nNessage)
                                sys.stdout.flush()
                        except:
                            #se ingresa al historial el error
                            fecha=time.strftime("%d-%m-%y") 
                            hora=time.strftime("%H:%M:%S")
                            cadinsert=fecha+"-::"+hora+"  ERROR AL LEER BLOCKCHAIN"
                            listHistorial.insertarFinal(str(cadinsert))
                            nNessage = 'false'
                            server.sendall(nNessage.encode('utf-8'))
                            sys.stdout.write(nNessage)
                            sys.stdout.flush()

                else: #para enviar mensaje al servidor (se envia el blockchain)
                    if variableJsonEnviar[0]!='vacio': 
                        try:
                            message = variableJsonEnviar[0]
                            server.sendall(message.encode('utf-8'))
                            sys.stdout.write(message)
                            sys.stdout.flush()
                            variableJsonEnviar[0]='vacio' 
                        except:
                            fecha=time.strftime("%d-%m-%y") 
                            hora=time.strftime("%H:%M:%S")
                            cadinsert=fecha+"-::"+hora+"  ERROR AL ENVIAR BLOCKCHAIN"
                            listHistorial.insertarFinal(str(cadinsert))
        except:
            fecha=time.strftime("%d-%m-%y") 
            hora=time.strftime("%H:%M:%S")
            cadinsert=fecha+"-::"+hora+"  ERROR AL LEER MSJ ENTRANTE"
            listHistorial.insertarFinal(str(cadinsert))
            continue                   

    server.close()


#validarQueBlockChainEsteBueno("na")
hiloCom=threading.Thread(target=comunicacionConServerSiempreEscuchando)
hiloCom.start()

curses.wrapper(menu_principal)



    