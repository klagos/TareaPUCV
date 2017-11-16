#!/usr/bin/env python
# -*- coding: utf-8 -*-
import copy
import math


# Clase main, la cual solo posee metodos abstractos asociados con calculos y la creacion de la partida.
class main:
    # Este metodo a partir del archivo base, crea las instancias de las clases y luego las almacena dentro de la clase
    # partida.
    @staticmethod
    def iniciarPartida():
        # Lista vacia para consumibles, equipamiento y pruebas
        listaConsumibles = list()
        listaEquipamiento = list()
        listaPruebas = list()

        # Variables para lectura de archivo
        arch = open("base.txt")
        nrolinea = 1

        # Lectura de archivo y creacion de objetos
        for linea in arch:
            linea = linea.strip().split(",")
            if nrolinea == 1:
                v, t, stats = linea
                Estudiante = Personaje("", int(v), int(t), int(stats), 0, 0, 0, 0)
            elif nrolinea == 2:
                cantConsumibles, cantEquipamiento = linea
            elif len(linea) == 5:
                nombre, stock, stat, buff, costo = linea
                listaConsumibles.append(Consumible(nombre, int(stock), stat, int(buff), int(costo)))
            elif len(linea) == 3:
                nombre, atributo, multiplicador = linea
                listaEquipamiento.append(Equipamiento(nombre, atributo, float(multiplicador)))
            else:
                nombre, vida, destreza, resistencia, inteligencia, suerte, debilidad = linea
                listaPruebas.append(
                    Prueba(nombre, int(vida), int(destreza), int(resistencia), int(inteligencia), int(suerte),
                           debilidad))
            nrolinea += 1
        # Almacenar objetos en la simulacion
        Partida = Simulacion(listaConsumibles, listaEquipamiento, listaPruebas, Estudiante)

        arch.close()
        return Partida

    # Este metodo hace el calculo cuando el personaje se enfrenta a cierta prueba, retornando el resultado de la formula
    # entregada en el archivo.
    @staticmethod
    def CalculoEvaluacion(Personaje, Prueba):
        listaStatsPer = Personaje.getListaStats()
        listaStatsPrueba = Prueba.getListaStats()
        debilidad = Prueba.getDebilidad()
        if debilidad == "destreza":
            debilidad = Personaje.getDestreza()
        elif debilidad == "resistencia":
            debilidad = Personaje.getResistencia()
        elif debilidad == "inteligencia":
            debilidad = Personaje.getInteligencia()
        else:
            debilidad = Personaje.getSuerte()
        lista = list()
        # 1. self.destreza, 2. self.resistencia, 3. self.inteligencia, 4. self.suerte
        for i in range(len(listaStatsPrueba)):
            lista.append(listaStatsPer[i] - listaStatsPrueba[i])
        suma = sum(lista)
        return suma * int(listaStatsPrueba[0] / debilidad)

    # Este metodo escribe el archivo final al ganar.
    @staticmethod
    def escribirArchivo(nombre, listaI, listaF, listaPruebas, listaEquipados, diccConsumibles, tiempoTotal):
        f = "{0},{1},{2},{3},{4},{5}\n"
        f1 = "{0},{1},{2}\n"
        f2 = "{0},{1}\n"
        v, d, r, inte, s, t = listaI
        arch = open(nombre, "w")
        arch.write(Partida.getPersonaje().getNombre() + "\n")
        arch.write(f.format(v, d, r, inte, s, t))
        v, d, r, inte, s, t = listaF
        arch.write(f.format(v, d, r, inte, s, t))

        prueba1, prueba2, prueba3 = listaPruebas
        arch.write(f1.format(prueba1, prueba2, prueba3))

        for consumible,cantidad in diccConsumibles.items():
            arch.write(f2.format(consumible,cantidad))

        for equipamiento in listaEquipados:
            arch.write(equipamiento + "\n")

        arch.write(str(tiempoTotal) + "\n")
        arch.close()
# La clase dialogo no es instanciada, posee metodos estaticos los cuales tienen directa relacion con el dialogo
# que se va a imprimir en la partida.
class Dialogo:
    @staticmethod
    # Este metodo imprime el saludo del inicio del programa
    def imprimirSaludo():
        print "¡Bienvenido a la simulación de pruebas!"
        print "Por favor escribe el nombre de tu personaje:"

    @staticmethod
    # Imprime la vida, tiempo y stats iniciales a repartir del personaje
    def informarInicio(personaje):
        f = "Muy bien {0}, te informo que posees:"
        f1 = "{0} puntos de Vida base"
        f2 = "{0} puntos de Tiempo"
        f3 = "{0} puntos para gastar en stats iniciales"
        f4 = "¿Como quieres repartir tus {0} puntos?"
        print f.format(personaje.getNombre())
        print f1.format(personaje.getVida())
        print f2.format(personaje.getTiempo())
        print f3.format(personaje.getStats())
        print f4.format(personaje.getStats())

    # Imprime el mensaje de game over cuando el estudiante muere.
    @staticmethod
    def imprimirPerdiste():
        print "¡Perdiste!, los ramos eran muy dificiles..."

    # Imprime el mensaje de felicitaciones cuando el personaje logra superar una prueba.
    @staticmethod
    def imprimirFelicitaciones(hpPerdido):
        f = "¡SÍ! Lo lograste, pero perdiste {0} puntos de vida"
        print f.format(hpPerdido)

    @staticmethod
    # Este metodo imprimira el error al intentar agregar stats que exceden de los que posee el personaje
    def imprimirError1():
        print "Lo siento, esa cantidad excede lo que tienes disponible."
        print "Empezaremos de nuevo por si te equivocaste al repartir."

    @staticmethod
    # Este metodo imprimira que sobraron stats al agregarselos al personaje.
    def imprimirError2():
        print "¡Te sobran puntos! Dadas tus malas matemáticas, te las asignaremos a Suerte (puede que la necesites)."

    # Este metodo imprime un mensaje cuando se intenta consumir un objeto y no se posee el tiempo que requiere consumirlo.
    @staticmethod
    def imprimirError3():
        print "¡No tienes tiempo suficiente para usar este consumible! Intenta con otro"

    @staticmethod
    # Este metodo imprime la lista de consumibles disponibles.
    def imprimirConsumibles(lista):
        f = "{0}.- ({1}) {2}: {3} de tiempo, {4} de {5}"
        contador = 1
        for consumible in lista:
            linea = f.format(contador, consumible.getStock(), consumible.getNombre(), consumible.getCosto(),
                             consumible.getBuff(),
                             consumible.getAtributo())
            contador += 1
            print linea

    @staticmethod
    # Imprime los dialogos sobre los consumibles.
    def imprimirInicioCon():
        print "Aquí están los consumibles, selecciona el número del objeto que deseas."
        print "Para comenzar la evaluación ingresa -1."

    @staticmethod
    # Imprime el texto relacionado con los consumibles y luego se imprime el listado de consumibles
    def imprimirListadoCon(lista):
        Dialogo.imprimirConsumibles(lista)

    @staticmethod
    # Esta funcion imprime la lista de equipamientos disponible en la partida.
    def imprimirEquipamiento(lista):
        f = "{0}.- {1}: Bonificador {2} a {3}"
        contador = 1
        for equipamiento in lista:
            linea = f.format(contador, equipamiento.getNombre(), equipamiento.getMultiplicador(),
                             equipamiento.getAtributo())
            contador += 1
            print linea

    @staticmethod
    # Este metodo imprime el texto relacionado con los equipos y luego se imprime el listado de equipamiento
    def imprimirListadoEq(lista):
        print "Aquí está el listado de todos los equipamientos que hay, elige un número para equiparlo."
        print "En caso de que ya no quieras equiparte más ingresa -1."
        Dialogo.imprimirEquipamiento(lista)

    @staticmethod
    # Este metodo imprime el dialogo relacionado con el inicio de una evaluacion
    def imprimirInterrogacion(Partida, i):
        nombre = Partida.getPersonaje().getNombre()
        nombrePrueba = Partida.getPruebas()[i].getNombre()
        debilidad = Partida.getPruebas()[i].getDebilidad()
        v, d, r, i, s = Partida.getPruebas()[i].getListaStats()
        f = "Prepárate {0} para enfrentar a la {1} (música dramática)"
        f1 = "Esta prueba posee V {0} D {1} R {2} I {3} S {4} y es débil contra la {5} ¿Podrás superarla?"
        print "¡Llegó la hora de la evaluación!"
        print f.format(nombre, nombrePrueba)
        print f1.format(v, d, r, i, s, debilidad)
        print "\n2 horas después. . . y 2 semanas. . .\n"


# La clase simulacion es la partida encargada de almacenar todas las clases instaciadas a partir del archivo base.txt
# este posee un atributo temporal, el cual almacenara los atributos iniciales de un personaje antes de usar los
# consumibles.
class Simulacion:
    def __init__(self, consumibles, equipo, pruebas, personaje):
        self.consumibles = consumibles
        self.equipo = equipo
        self.pruebas = pruebas
        self.personaje = personaje
        self.copyPersonaje = copy.deepcopy(personaje)
        self.dic = {}

    def getDiccionarioConsumibles(self):
        diccionario = dict()
        for consumible in self.consumibles:
            diccionario[consumible.getNombre()] = 0
        return diccionario

    # Metodo para obtener lista de nombres de pruebas
    def getListaPruebas(self):
        lista = list()
        for prueba in self.pruebas:
            lista.append(prueba.getNombre())
        return lista

    # Diccionario temporal con atributos para redefinir stats del personaje
    def asignarDic(self, dic):
        self.dic = dic

    def asignarNombre(self, nombre):
        return self.personaje.asignarNombre(nombre)

    # Este metodo llama al metodo del personaje para aplicar el consumible
    def usarConsumible(self, atributo, buff, costo):
        return self.personaje.usarConsumible(atributo, buff, costo)

    # Este metodo llama al metodo del personaje para redefinir sus stats despues de utilizar consumibles.
    def redefinirStatsPersonaje(self):
        self.personaje.redefinirStats(self.dic)

    # Este metodo llama al metodo del personaje de quitar Hp
    def daniarPersonaje(self, hpPerdido):
        self.personaje.quitarHp(hpPerdido)

    # Este metodo recrea la evaluacion, entregando pares de valores donde el primero es un booleano el cual es verdadero
    # o falso dependiendo si gana o no, y el  segundo es la cantidad de vida perdida. La vida perdida es 0 en el caso de
    # que el personaje haya ganado.
    def evaluacion(self, i):
        vidaPerdida = main.CalculoEvaluacion(self.getPersonaje(), self.getPruebas()[i])
        return abs(vidaPerdida)

    # Este metodo llama al metodo del personaje para verificar si esta vivo.
    def personajeVivo(self):
        return self.personaje.vivo()

    # Este metodo cumple la funcion de restar el stock de un consumible si es utilizado
    def restarStockConsumible(self, indice):
        objeto = self.consumibles[indice]
        objeto.restarStock()

    # Este metodo cumple la funcion de verificar si es que el stock de un consumible es 0.
    def stockCero(self, indice):
        objeto = self.consumibles[indice]
        return objeto.stockCero()

    # Este metodo cumple la funcion de remover un consumible de la lista de disponibles.
    def removerConsumible(self, indice):
        objeto = self.consumibles[indice]
        self.consumibles.remove(objeto)

    # Este metodo cumple la funcion de remover un equipable de la lista de equipos.
    def removerEquipo(self, indice):
        objeto = self.equipo[indice]
        self.equipo.remove(objeto)

    # Este metodo cumple la funcion de obtener los atributos de un equipable
    def getEAtributo(self, indice):
        objeto = self.equipo[indice]
        return objeto.getAtributo()

    def getENombre(self, indice):
        objeto = self.equipo[indice]
        return objeto.getNombre()

    # Este metodo cumple la funcion de obtener los atributos de un consumible.
    def getCAtributo(self, indice):
        objeto = self.consumibles[indice]
        return objeto.getAtributo()

    # Este metodo cumple la funcion de obtener el costo de tiempo de un consumible
    def getCosto(self, indice):
        objeto = self.consumibles[indice]
        return objeto.getCosto()

    # Este metodo cumple la funcion de obtener el multiplicador de un equipable
    def getMultiplicador(self, indice):
        objeto = self.equipo[indice]
        return objeto.getMultiplicador()

    # Este metodo cumple la funcion de obtener el bonificador de un consumible
    def getBuff(self, indice):
        objeto = self.consumibles[indice]
        return objeto.getBuff()

    def getConsumibles(self):
        return self.consumibles

    def getEquipo(self):
        return self.equipo

    def getPruebas(self):
        return self.pruebas

    def getPersonaje(self):
        return self.personaje

    def getcopyPersonaje(self):
        return self.copyPersonaje

    def getStatsPersonaje(self):
        return self.personaje.getListaStats()

    def imprimirStatsPersonaje(self):
        self.personaje.imprimirStats()

    def buffearAtributo(self, multiplicador, atributo):
        self.personaje.buffearAtributo(multiplicador, atributo)

    def imprimirStatsIniciales(self):
        self.personaje.imprimirStatsIniciales()

    def sumarStatsPersonaje(self, vida, destreza, resistencia, inteligencia, suerte):
        self.personaje.sumarStats(vida, destreza, resistencia, inteligencia, suerte)

class Prueba:
    def __init__(self, nombre, vida, destreza, resistencia, inteligencia,
                 suerte, debilidad):
        self.nombre = nombre
        self.vida = vida
        self.destreza = destreza
        self.resistencia = resistencia
        self.inteligencia = inteligencia
        self.suerte = suerte
        self.debilidad = debilidad

    def getListaStats(self):
        return [self.vida, self.destreza, self.resistencia, self.inteligencia, self.suerte]

    def getDebilidad(self):
        return self.debilidad

    def getNombre(self):
        return self.nombre


class Personaje:
    def __init__(self, nombre, v, t, stats, destreza, resistencia, inteligencia, suerte):
        self.nombre = nombre
        self.vida = v
        self.tiempo = t
        self.stats = stats
        self.destreza = destreza
        self.resistencia = resistencia
        self.inteligencia = inteligencia
        self.suerte = suerte

    def asignarNombre(self, nombre):
        self.nombre = nombre

    def quitarHp(self, hpPerdido):
        self.vida -= hpPerdido

    def vivo(self):
        if self.vida >= 0:
            return True
        return False

    def getNombre(self):
        return self.nombre

    def getVida(self):
        return self.vida

    def getTiempo(self):
        return self.tiempo

    def getStats(self):
        return self.stats

    def getDestreza(self):
        return self.destreza

    def getResistencia(self):
        return self.resistencia

    def getInteligencia(self):
        return self.inteligencia

    def getSuerte(self):
        return self.suerte

    def getListaStats(self):
        return [self.vida, self.destreza, self.resistencia, self.inteligencia, self.suerte]

    # Esta funcion imprime los stats actuales del personaje
    def imprimirStats(self):
        f = "Stats actuales: V {0} D {1} R {2} I {3} S {4}\nTiempo disponible: {5}\n"
        print f.format(self.vida, self.destreza, self.resistencia, self.inteligencia,
                       self.suerte,
                       self.tiempo)

    # Esta funcion imprime los stats iniciales del personaje
    def imprimirStatsIniciales(self):
        f = "Vida: {0} Destreza: {1} Resistencia: {2} Inteligencia: {3} Suerte: {4}\n"
        print "Tus stats iniciales son:"
        print f.format(self.vida, self.destreza, self.resistencia, self.inteligencia,
                       self.suerte)

    # Esta funcion modifica los stats del personaje al inicio.
    def sumarStats(self, vida, destreza, resistencia, inteligencia, suerte):
        self.vida += vida
        self.destreza += destreza
        self.resistencia += resistencia
        self.inteligencia += inteligencia
        self.suerte += suerte

    def buffearAtributo(self, multiplicador, atributo):
        if atributo == "destreza":
            self.destreza = int(math.floor(self.destreza * multiplicador))
        elif atributo == "resistencia":
            self.resistencia = int(math.floor(self.resistencia * multiplicador))
        elif atributo == "inteligencia":
            self.inteligencia = int(math.floor(self.inteligencia * multiplicador))
        else:
            self.suerte = int(math.floor(self.suerte * multiplicador))

    # Esta funcion retorna un booleano si es que se pudo utilizar el consumible
    # respecto al tiempo que posee el personaje.
    def usarConsumible(self, atributo, buff, costo):
        if (self.tiempo - costo) >= 0:
            self.tiempo -= costo
            if atributo == "destreza":
                self.destreza += buff
            elif atributo == "inteligencia":
                self.inteligencia += buff
            elif atributo == "suerte":
                self.suerte += buff
            else:
                self.resistencia += buff
            return True
        else:
            return False

    def redefinirStats(self, dic):
        destreza, resistencia, inteligencia, suerte = dic["destreza"], dic["resistencia"], dic["inteligencia"], dic["suerte"]
        self.destreza -= destreza
        self.resistencia -= resistencia
        self.inteligencia -= inteligencia
        self.suerte -= suerte


class Equipamiento:
    def __init__(self, nombre, atributo, multiplicador):
        self.nombre = nombre
        self.atributo = atributo
        self.multiplicador = multiplicador

    def getNombre(self):
        return self.nombre

    def getMultiplicador(self):
        return self.multiplicador

    def getAtributo(self):
        return self.atributo


class Consumible:
    def __init__(self, nombre, stock, atributo, buff, costo):
        self.nombre = nombre
        self.stock = stock
        self.atributo = atributo
        self.buff = buff
        self.costo = costo

    # Esta funcion verifica si el stock del consumible es 0
    def stockCero(self):
        if self.stock == 0:
            return True
        return False

    # Esta funcion resta 1 en el stock del consumible
    def restarStock(self):
        self.stock -= 1

    def getNombre(self):
        return self.nombre

    def getStock(self):
        return self.stock

    def getAtributo(self):
        return self.atributo

    def getBuff(self):
        return self.buff

    def getCosto(self):
        return self.costo

# Los metodos de las clases que no han sido comentados se debe a que el mismo nombre explica lo que realiza.

# ------ Main --------
if __name__ == '__main__':
    # Crear Partida
    Partida = main.iniciarPartida()
    tiempoInicial = Partida.getPersonaje().getTiempo()
    Dialogo.imprimirSaludo()
    nombre = raw_input("> ")
    Partida.asignarNombre(nombre)
    Dialogo.informarInicio(Partida.getPersonaje())

    # Aplicar stats
    maxStats = Partida.personaje.getStats()

    while True:
        vida, destreza, resistencia, inteligencia, suerte = 0, 0, 0, 0, 0
        total = 0
        print "Vida:"
        vida = int(raw_input(">"))
        total += vida
        if total > maxStats:
            Dialogo.imprimirError1()
            continue
        elif total == maxStats:
            break
        print "Destreza:"
        destreza = int(raw_input(">"))
        total += destreza
        if total > maxStats:
            Dialogo.imprimirError1()
            continue
        elif total == maxStats:
            break

        print "Resistencia:"
        resistencia = int(raw_input(">"))
        total += resistencia
        if total > maxStats:
            Dialogo.imprimirError1()
            continue
        elif total == maxStats:
            break

        print "Inteligencia:"
        inteligencia = int(raw_input(">"))
        total += inteligencia
        if total > maxStats:
            Dialogo.imprimirError1()
            continue
        elif total == maxStats:
            break

        print "Suerte:"
        suerte = int(raw_input(">"))
        total += suerte
        if total > maxStats:
            Dialogo.imprimirError1()
            continue
        elif total == maxStats:
            break
        else:
            Dialogo.imprimirError2()
            suerte = suerte + maxStats - total
            break

    # Se aplican los stats ingresados al personaje
    Partida.sumarStatsPersonaje(vida, destreza, resistencia, inteligencia, suerte)
    # Se imprimen los stats iniciales.
    Partida.imprimirStatsIniciales()

    # Proceso de equipamiento
    Dialogo.imprimirListadoEq(Partida.equipo)
    ingreso = ""
    cantEquipados = 0
    listaEquipados = list()
    while cantEquipados != 3:
        print ""
        ingreso = int(raw_input("> "))
        print ""
        if ingreso == -1:
            break
        nombreEquipamiento = Partida.getENombre(ingreso - 1)
        listaEquipados.append(nombreEquipamiento)
        multiplicador = Partida.getMultiplicador(ingreso - 1)
        atributo = Partida.getEAtributo(ingreso - 1)
        Partida.buffearAtributo(multiplicador, atributo)
        Partida.removerEquipo(ingreso - 1)
        Dialogo.imprimirEquipamiento(Partida.getEquipo())
        cantEquipados += 1

    listaInicial = Partida.getStatsPersonaje()
    Partida.personaje.imprimirStats()

    # Variable i para la cantidad de pruebas a enfrentar y diccionario para ver buffeos por consumibles
    # Variable hpTotalPerdido para imprimir al final
    # Variable diccTemp que se almacenara en la clase Simulacion
    i = 0
    hpTotalPerdido = 0
    tiempoTotalConsumido = 0
    diccConsumibles = Partida.getDiccionarioConsumibles()

    # Uso de consumibles para el personaje y sus evaluaciones
    while True:
        Dialogo.imprimirInicioCon()
        diccTemp = {"destreza": 0, "inteligencia": 0, "suerte": 0, "resistencia": 0}
        while True and len(Partida.getConsumibles()) != 0:
            Dialogo.imprimirListadoCon(Partida.getConsumibles())
            print ""
            ingreso = int(raw_input("> "))
            print ""

            if ingreso == -1:
                break
            else:
                atributo = Partida.getCAtributo(ingreso - 1)
                buff = Partida.getBuff(ingreso - 1)
                costo = Partida.getCosto(ingreso - 1)
                tiempoTotalConsumido += costo
                usado = Partida.usarConsumible(atributo, buff, costo)
                if usado:
                    nombreConsumible = Partida.getConsumibles()[ingreso - 1].getNombre()
                    diccConsumibles[nombreConsumible] += 1
                    diccTemp[atributo] += buff
                    Partida.restarStockConsumible(ingreso - 1)
                    if Partida.stockCero(ingreso - 1):
                        Partida.removerConsumible(ingreso - 1)
                    Partida.imprimirStatsPersonaje()
                else:
                    Dialogo.imprimirError3()
        Partida.asignarDic(diccTemp)
        Dialogo.imprimirInterrogacion(Partida, i)

        # Inicio de evaluacion
        hpPerdido = Partida.evaluacion(i)
        hpTotalPerdido += hpPerdido
        Partida.daniarPersonaje(hpPerdido)
        Partida.redefinirStatsPersonaje()

        # Si el personaje esta vivo, se imprime el dialogo de felicidades y se le
        # suma 1 a nuestro contador de pruebas. En el caso contrario el juego termina.
        if Partida.personajeVivo():
            Dialogo.imprimirFelicitaciones(hpPerdido)
            i += 1
            if i == 3:
                break
            print "¿Estás listo para el siguiente combate? Mejor prepárate antes.\n"
            Partida.imprimirStatsPersonaje()
        else:
            print "¡Perdiste!, los ramos eran muy dificiles..."
            break

    if Partida.personajeVivo():
        print "¡Felicidades, has ganado!"
        input = raw_input("¿Deseas guardar las estadisticas en un archivo? (S/N): ")
        if input == "S":
            tiempoFinal = Partida.getPersonaje().getTiempo()
            nombreArch = raw_input("Nombre del archivo (Ej: estadisticas.txt): ")
            listaFinal = Partida.getStatsPersonaje()
            listaInicial.append(tiempoInicial)
            listaFinal.append(tiempoFinal)
            listaPruebas = Partida.getListaPruebas()
            main.escribirArchivo(nombreArch, listaInicial, listaFinal, listaPruebas, listaEquipados, diccConsumibles, tiempoTotalConsumido )
        print "FIN."