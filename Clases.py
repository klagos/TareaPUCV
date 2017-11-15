#!/usr/bin/env python
# -*- coding: utf-8 -*-
import copy
import math

class main:
    @staticmethod
    def crearPartida(arch):
        # Lista vacia para consumibles, equipamiento y pruebas
        listaConsumibles = list()
        listaEquipamiento = list()
        listaPruebas = list()

        # Variables para lectura de archivo
        nrolinea = 1
        cantidad = 0

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
                    Prueba(nombre, int(vida), int(destreza), int(resistencia), int(inteligencia), int(inteligencia),
                           debilidad))
            nrolinea += 1

        # Almacenar objetos en la simulacion
        Partida = Simulacion(listaConsumibles, listaEquipamiento, listaPruebas, Estudiante)
        return Partida


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
        print "Vida Prueba:",listaStatsPrueba[0], "Debilidad ", debilidad
        return suma*int(listaStatsPrueba[0]/debilidad)

class Dialogo:
    @staticmethod
    # Esta funcion imprime el saludo del inicio del programa
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

    @staticmethod
    def imprimirPerdiste():
        print "¡Perdiste!, los ramos eran muy dificiles..."

    @staticmethod
    def imprimirFelicitaciones(hpPerdido):
        f = "¡SÍ! Lo lograste, pero perdiste {0} puntos de vida"
        print f.format(hpPerdido)
    # Esta funcion imprimira el error al intentar agregar stats que exceden de los que posee el personaje
    def imprimirError1():
        print "Lo siento, esa cantidad excede lo que tienes disponible."
        print "Empezaremos de nuevo por si te equivocaste al repartir."

    @staticmethod
    # Esta funcion imprimira que sobraron stats al agregarselos al personaje.
    def imprimirError2():
        print "¡Te sobran puntos! Dadas tus malas matemáticas, te las asignaremos a Suerte (puede que la necesites)."

    @staticmethod
    def imprimirError3():
        print "¡No tienes tiempo suficiente para usar este consumible! Intenta con otro"

    @staticmethod
    # Esta funcion imprime la lista de consumibles que posee el personaje
    def imprimirConsumibles(lista):
        f = "{0}.- ({1}) {2}: {3} de tiempo, {4} de {5}"
        contador = 1
        for consumible in lista:
            linea = f.format(contador, consumible.getStock(), consumible.getNombre(), consumible.getCosto(), consumible.getBuff(),
                             consumible.getAtributo())
            contador += 1
            print linea

    @staticmethod
    # Imprime el texto relacionado con los consumibles y luego se imprime el listado de consumibles
    def imprimirListadoCon(lista):
        print "Aquí están los consumibles, selecciona el número del objeto que deseas."
        print "Para comenzar la evaluación ingresa -1."
        Dialogo.imprimirConsumibles(lista)

    @staticmethod
    # Esta funcion imprime la lista de equipamiento que posee el personaje
    def imprimirEquipamiento(lista):
        f = "{0}.- {1}: Bonificador {2} a {3}"
        contador = 1
        for equipamiento in lista:
            linea = f.format(contador, equipamiento.getNombre(), equipamiento.getMultiplicador(), equipamiento.getAtributo())
            contador += 1
            print linea

    @staticmethod
    # Esta funcion imprime el texto relacionado con los equipos y luego se imprime el listado de equipamiento
    def imprimirListadoEq(lista):
        print "Aquí está el listado de todos los equipamientos que hay, elige un número para equiparlo."
        print "En caso de que ya no quieras equiparte más ingresa -1."
        Dialogo.imprimirEquipamiento(lista)

    @staticmethod
    def imprimirInterrogacion(Partida, i):
        nombre = Partida.getPersonaje().getNombre()
        nombrePrueba = Partida.getPruebas()[i].getNombre()
        debilidad = Partida.getPruebas()[i].getDebilidad()
        v,d,r,i,s = Partida.getPruebas()[i].getListaStats()

        f = "Prepárate {0} para enfrentar a la {1} (música dramática)"
        f1 = "Esta prueba posee V {0} D{1} R {2} I {3} S {4} y es débil contra la {5} ¿Podrás superarla?"
        print "¡Llegó la hora de la evaluación!"
        print f.format(nombre, nombrePrueba)
        print f1.format(v,d,r,i,s,debilidad)

class Simulacion:
    def __init__(self, consumibles, equipo, pruebas, personaje):
        self.consumibles = consumibles
        self.equipo = equipo
        self.pruebas = pruebas
        self.personaje = personaje
        self.copyPersonaje = copy.deepcopy(personaje)

    def daniarPersonaje(self, hpPerdido):
        self.personaje.quitarHp(hpPerdido)

    def evaluacion(self, i):
        vidaPerdida = main.CalculoEvaluacion(self.getPersonaje(), self.getPruebas()[i])
        if vidaPerdida < 0:
            return False, abs(vidaPerdida)
        else:
            return True, 0

    def personajeVivo(self):
        return self.personaje.vivo()

    def restarStockConsumible(self, indice):
        objeto = self.consumibles[indice]
        objeto.restarStock()

    def stockCero(self, indice):
        objeto = self.consumibles[indice]
        return objeto.stockCero()

    def removerConsumible(self, indice):
        objeto = self.consumibles[indice]
        self.consumibles.remove(objeto)

    def removerEquipo(self, indice):
        objeto = self.equipo[indice]
        self.equipo.remove(objeto)

    def getEAtributo(self, indice):
        objeto = self.equipo[indice]
        return objeto.getAtributo()

    def getCAtributo(self, indice):
        objeto = self.consumibles[indice]
        return objeto.getAtributo()

    def getCosto(self, indice):
        objeto = self.consumibles[indice]
        return objeto.getCosto()

    def getMultiplicador(self, indice):
        objeto = self.equipo[indice]
        return objeto.getMultiplicador()

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

    def sumarStats(self, vida, destreza, resistencia, inteligencia, suerte):
        self.personaje.sumarStats()

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
        f = "Stats actuales: V {0} D {1} R {2} I {3} S {4}\nTiempo disponible: {5}"
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
        print self.tiempo
        print costo
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
        print costo
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
