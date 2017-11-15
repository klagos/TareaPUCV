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

class Texto:
    def __init__(self, arch):
        lista = arch.readlines()
        self.empezarEvaluacion = lista[10:13]
        self.Logrado = lista[13:15]

    # Esta funcion imprime el saludo del inicio del programa
    def imprimirSaludo(self):
        print "¡Bienvenido a la simulación de pruebas!"
        print "Por favor escribe el nombre de tu personaje:"

    # Imprime la vida, tiempo y stats iniciales a repartir del personaje
    def informarInicio(self, personaje):
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

    # Esta funcion imprimira el error al intentar agregar stats que exceden de los que posee el personaje
    def imprimirError1(self):
        print "Lo siento, esa cantidad excede lo que tienes disponible."
        print "Empezaremos de nuevo por si te equivocaste al repartir."

    # Esta funcion imprimira que sobraron stats al agregarselos al personaje.
    def imprimirError2(self):
        print "¡Te sobran puntos! Dadas tus malas matemáticas, te las asignaremos a Suerte (puede que la necesites)."

    # Esta funcion imprime la lista de consumibles que posee el personaje
    def imprimirConsumibles(self, lista):
        f = "{0}.- ({1}) {2}: {3} de tiempo, {4} de {5}"
        contador = 1
        for consumible in lista:
            linea = f.format(contador, consumible.getStock(), consumible.getNombre(), consumible.getCosto(), consumible.getBuff(),
                             consumible.getAtributo())
            contador += 1
            print linea

    # Imprime el texto relacionado con los consumibles y luego se imprime el listado de consumibles
    def imprimirListadoCon(self, lista):
        print "Aquí están los consumibles, selecciona el número del objeto que deseas."
        print "Para comenzar la evaluación ingresa -1."
        self.imprimirConsumibles(lista)

    # Esta funcion imprime la lista de equipamiento que posee el personaje
    def imprimirEquipamiento(self, lista):
        f = "{0}.- {1}: Bonificador {2} a {3}"
        contador = 1
        for equipamiento in lista:
            linea = f.format(contador, equipamiento.getNombre(), equipamiento.getMultiplicador(), equipamiento.getAtributo())
            contador += 1
            print linea

    # Esta funcion imprime el texto relacionado con los equipos y luego se imprime el listado de equipamiento
    def imprimirListadoEq(self, lista):
        print "Aquí está el listado de todos los equipamientos que hay, elige un número para equiparlo."
        print "En caso de que ya no quieras equiparte más ingresa -1."
        self.imprimirEquipamiento(lista)


class Simulacion:
    def __init__(self, consumibles, equipo, pruebas, personaje):
        self.consumibles = consumibles
        self.equipo = equipo
        self.pruebas = pruebas
        self.personaje = personaje
        self.copyPersonaje = copy.deepcopy(personaje)

    def removerEquipo(self, indice):
        objeto = self.equipo[indice]
        self.equipo.remove(objeto)

    def getAtributo(self, indice):
        objeto = self.equipo[indice]
        return objeto.getAtributo()

    def getMultiplicador(self, indice):
        objeto = self.equipo[indice]
        return objeto.getMultiplicador()

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