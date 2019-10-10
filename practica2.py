import curses
import time
import csv
import random
import os
import sys

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

listaDobleBloques= dobleBloques()

""" -----------------------------------------------------PARA EL MENU PRINCIPAL ----------------------------------------------------------------"""
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
                            stdscr.addstr(20,40,"USUARIOS CARGADOS CORRECTAMENTE!")
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
                   return          
            elif indice_fila_actual==2:
                return                                  
            elif indice_fila_actual==len(menu)-1:
                listaDobleBloques.imprimirLista()
                sys.exit()
        
        print_menu(stdscr,indice_fila_actual)
        stdscr.refresh()


def archivoBloque(ruta): 
    
    clasee=""
    dataa=""

    with open(ruta) as f:
        reader=csv.reader(f)
        contadorCD=0       
        #Obtenemos el nombre de clase, y la estructura data de archivo .csv
        for row in reader:
            if contadorCD==0:
                us="{0}".format(row[0]) #fila 0 de archivo .csv
                clasee="{0}".format(row[1]) #fila 1 de archivo .csv
            elif contadorCD==1:
                us="{0}".format(row[0]) #fila 0 de archivo .csv
                dataa="{0}".format(row[1]) #fila 1 de archivo .csv
            contadorCD=contadorCD+1
    
    #verificar si es bloque genesis (bloque cabeza o el primero)
    if listaDobleBloques.estaVacia():
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
        listaDobleBloques.insertarFinal(str(obidx), fechayhora, clasee, dataa, hashant, "gudiel")

            
curses.wrapper(menu_principal)
            