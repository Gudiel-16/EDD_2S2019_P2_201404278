import curses
import time
import csv
import random
import os
import sys
import hashlib

from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN, textpad

menu=['Insertar Bloque','Seleccionar Bloque','Reportes','Salir']

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

    def reporte(self):
        contador=1  
        contador2=1      
        cadena='nullInicio[label = "null"];\n' 
        cadena2=""     
        temp=self.primero
        for i in range(self.size):
            cadenaNodo='node'+str(contador)+'[label = "{ <a> |'+str(temp.coordenadas)+' | }  "];\n'
            cadena+=cadenaNodo
            contador=contador+1
            temp=temp.siguiente
        cadena+='nullFinal[label = " null"];\n'

        for j in range(self.size):
            if contador2==1:
                cadena2+='node'+str(contador2)+':a -> nullInicio; \n'
                sig=contador2+1
                cadena2+='node'+str(contador2)+' -> node'+str(sig)+';\n'
            elif contador2==self.size:
                ant=contador2-1
                cadena2+='node'+str(contador2)+' -> nullFinal' + ';\n'
                cadena2+='node'+str(contador2)+' -> node'+str(ant) +';\n'
            else:
                ant=contador2-1
                sig=contador2+1
                cadena2+='node'+str(contador2)+' -> node'+str(sig)+';\n'
                cadena2+='node'+str(contador2)+' -> node'+str(ant)+';\n'
            contador2=contador2+1
        cadena+=cadena2
        return cadena       
    
    def imprimirLista(self):
    
        if self.estaVacia():
            print("lista Vacia")
        else:            
            temp=self.primero
            for i in range(self.size):
                cad= str(temp.index) + " " + str(temp.hora) + " " + temp.clase + " " + temp.dato + " " + str(temp.hashant) + " " + str(temp.hashh)
                print(cad,end=" ")
                temp=temp.siguiente

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
    def _init_(self):
        self.root=None
        self.cadenaG=""


    def obtenerRaiz(self):
        return self.root

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
    
    def reporteGraphvizArbol(self, arbolR):
        if arbolR==None:
            return
        else:
            if arbolR.hijoIzq!=None:
                self.cadenaG+="\"" + str(arbolR.carnet) + "\" -> \"" + str(arbolR.hijoIzq.carnet) + "\" \n"
            else:
                self.cadenaG+="\"" + str(arbolR.carnet) + "\" -> \"" + str(arbolR.carnet) + " NULL IZQ \" \n"
            if arbolR.hijoDer!=None:
                self.cadenaG+="\"" + str(arbolR.carnet) + "\" -> \"" + str(arbolR.hijoDer.carnet) + "\" \n"
            else:
                self.cadenaG+="\"" + str(arbolR.carnet) + "\" -> \"" + str(arbolR.carnet) + " NULL DER \" \n"
        self.reporteGraphvizArbol(arbolR.hijoDer)
        self.reporteGraphvizArbol(arbolR.hijoIzq)

    def generarImagenGraphiz(self):
        # open(nombre_archivo.ext, formato)
        f = open("arbol.dot", "w") 
        # write("texto a escribir") 
        
        f.write("digraph G {\n")
        f.write("node [shape=record,width=.1,height=.1];")
        
        a=self.cadenaG
        f.write(a)

        f.write("}")
        # CIERRA EL ARCHIVO
        f.close()
        # dot -Tjpg ruta_archivo_dot.dot -o nombre_archivo_salida.jpg
        os.system("dot -Tjpg"+ " arbol.dot " +"-o arbol.jpg")
        os.system("arbol.jpg")

    def obtenerCadenaG(self):
        return self.cadenaG

    def limpiarCadenaG(self):
        self.cadenaG=""
    


""" ------------------------------------------------------------ PARA CREAR ARBOL ---------------------------------------------------------------------"""
class ingresarEnLista:

    def __init__(self):
        self.ingresar=""
        self.ingresar2=""
        self.guion=""
        self.listArbol=[]
        self.letrasNum=["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","0","1","2","3","4","5","6","7","8","9"]
        self.simb=[",",":","{","}"]
        self.recorrido=None

    def ingreList(self,cadena):
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
        print(self.listArbol)
        
        miraizz=self.ingresarEnArbol()
        return miraizz
    
    def ingresarEnArbol(self):
        listLlaves=[]
        listMov=[]
        cont=0 #para saber el index de lista en que voy
        contIzqoDer=0
        oa=miArbolAVL()
        miRaiz=oa.obtenerRaiz()

        for ol in self.listArbol: #recorro la lista
            for odcl in ol: #recorro cada caracter de elemento de lista
                if odcl=="{":
                    listLlaves.append("{")
                elif odcl=="}":
                    listLlaves.pop(0)
                    if listMov.__len__()>0:
                        listMov.pop(listMov.__len__()-1)
            if ol=="}}," and listLlaves.count("{")==1: # cambiara de lado el arbol
                listMov.clear()
            elif ol=="value" and listLlaves.count("{")==1: #quiere decir que es la raiz
                nom=self.listArbol[cont+2]
                carn=self.listArbol[cont+4]
                miRaiz=self.ingresarRaiz(nom,carn,miRaiz)
            elif ol=="value" and listLlaves.count("{")>1: #recorrera hacia izq
                nom=self.listArbol[cont+2]
                carn=self.listArbol[cont+4]
                ###
                nuevo=nodoArbolAVL(nom,carn)
                self.recorrido=miRaiz
                contt=1
                print(listMov)
                for rec in listMov:
                    if contt==listMov.__len__(): #validar que sea el ultimo elemento de la lista
                        if listMov[listMov.__len__()-1]=="left":
                            self.recorrido.hijoIzq=nuevo
                        elif listMov[listMov.__len__()-1]=="right":
                            self.recorrido.hijoDer=nuevo
                    elif rec=="left":
                        try:
                            self.recorrido=self.recorrido.hijoIzq
                        except:
                            pass                                        
                    elif rec=="right":
                        try:
                            self.recorrido=self.recorrido.hijoDer
                        except:
                            pass                        
                    contt=contt+1
                ###
            elif ol=="left":
                listMov.append("left")
            elif ol=="right":
                listMov.append("right")
            elif ol=="null":
                listMov.pop(listMov.__len__()-1)
            
            cont=cont+1
        return miRaiz
        
    def ingresarEnArbolConListaHaciaIzquierda(self, nom, carne, listMovi, miArbol):
        nuevo=nodoArbolAVL("a",3)
        recorrido=miArbol
        cont=1
        for rec in listMovi:
            if cont==listMovi.__len__(): #validar que sea el ultimo elemento de la lista
                if listMovi[listMovi.__len__()-1]=="left":
                    miArbol.hijoIzq=nuevo
                    return miArbol
                elif listMovi[listMovi.__len__()-1]=="right":
                    miArbol.hijoDer=nuevo
                    return miArbol
            elif rec=="left":
                recorrido=recorrido.hijoIzq                
            elif rec=="right":
                recorrido=recorrido.hijoDer
            cont=cont+1

    def ingresarRaiz(self, nom, carne, miArbol):
        nuevo=nodoArbolAVL(nom,carne)
        miArbol=nuevo
        return miArbol


""" ------------------------------------------------------------ OBJETOS ---------------------------------------------------------------------"""
listaDobleBloques= dobleBloques()
classMetArbol=miArbolAVL()
classIngreLista=ingresarEnLista()

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
                    #try:                   
                        archivoBloque(str(a))
                        stdscr.addstr(20,40,"USUARIOS CARGADOS CORRECTAMENTE!")
                        stdscr.getch()
                        stdscr.clear()
                        stdscr.refresh()                            
                        break
                    '''except:
                        stdscr.addstr(20,35,"EL NOMBRE DEL ARCHIVO NO SE ENCONTRO!")
                        stdscr.refresh()
                        stdscr.getch()
                        stdscr.clear()
                        stdscr.refresh() 
                        break  '''
            elif indice_fila_actual==1:                               
                   return          
            elif indice_fila_actual==2:
                return                                  
            elif indice_fila_actual==len(menu)-1:
                listaDobleBloques.imprimirLista()
                sys.exit()
        
        print_menu(stdscr,indice_fila_actual)
        stdscr.refresh()

""" ------------------------------------------------------PARA MOSTRAR BLOQUES --------------------------------------------------------------"""
'''
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
            nombreUsuarioActual[0]=listaDobleCircularUsuarios.obtenerNombre(index)
        if( index < 0): # EN CASO DE QUE EL INDICE SE VUELVA NEGAVITO LO DEJAMOS EN 0
            index = listaDobleCircularUsuarios.tamanio()-1
        if( index >= listaDobleCircularUsuarios.tamanio()): # EN CASO QUE EL INDICE SE VUELVA MAYOR AL SIZE DEL ARREGLO...
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
    y = int(altura/2) 
    x = int((ancho/2)-(len(listaDobleCircularUsuarios.obtenerNombre(index))/2))
    stdsrc.addstr(y,x, listaDobleCircularUsuarios.obtenerNombre(index), curses.color_pair(2)) # HAGREGA UNA CADENA  LA PANTALLA EN COORDENADAS Y, X Y UN ATRIBUTO EN ESTE CASO ES LA PAREJA DE COLORES
    stdsrc.refresh()
'''

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
                arb=classIngreLista.ingreList(dataa)  
                classMetArbol.reporteGraphvizArbol(arb)
                classMetArbol.generarImagenGraphiz()              

    #verificar si es bloque genesis (bloque cabeza o el primero)
    '''if listaDobleBloques.estaVacia():
        fecha=time.strftime("%d-%m-%y") 
        hora=time.strftime("%H:%M:%S")
        fechayhora=fecha+"-::"+hora
        listaDobleBloques.insertarFinal(str(0), fechayhora, clasee, dataa, "0000", "gudiel")
    else:
        hashant=listaDobleBloques.obtenerHashAnt()
        obidx=int(listaDobleBloques.obtenerIndex())+1
        fecha=time.strftime("%d-%m-%y")  
        hora=time.strftime("%H:%M:%S")
        fechayhora=fecha+"-::"+hora
        listaDobleBloques.insertarFinal(str(obidx), fechayhora, clasee, dataa, hashant, "gudiel")'''

'''
classMetArbol.insertar("a",10)
classMetArbol.insertar("a",5)
classMetArbol.insertar("a",13)
classMetArbol.insertar("a",1)
classMetArbol.insertar("a",6)
classMetArbol.insertar("a",17)
classMetArbol.insertar("a",16)
aja=classMetArbol.obtenerRaiz()
aja=aja.hijoIzq
aja=aja.hijoIzq
aja.hijoIzq=nodoArbolAVL("s",3)
classMetArbol.recorridoPreOrden(classMetArbol.obtenerRaiz())
classMetArbol.reporteGraphvizArbol(classMetArbol.obtenerRaiz())
classMetArbol.generarImagenGraphiz()
'''
'''
hashsha = hashlib.sha256()
stexto="hola Altaruru, hoy es lunes 1 de Octubre de 2018"
hashsha.update(stexto.encode())
print (hashsha.hexdigest())

            '''
curses.wrapper(menu_principal)

prueba=[]
print(prueba)
#prueba.pop(prueba.__len__()-1)
print(prueba.__len__())




    