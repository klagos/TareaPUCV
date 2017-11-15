#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Clases import *
import math

# Esta funcion crea todos los objetos y posteriormente los almacena en la simulacion
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




# Esta funcion imprime la lista de consumibles que posee el personaje
def imprimirConsumibles(lista):
    f = "{0}.- ({1}) {2}: {3} de tiempo, {4} de {5}"
    contador = 1
    for consumible in lista:
        linea = f.format(contador, consumible.stock, consumible.nombre, consumible.costo, consumible.buff,
                         consumible.atributo)
        contador += 1
        print linea

# Imprime el texto relacionado con los consumibles y luego se imprime el listado de consumibles
def imprimirListadoCon(Dialogo, lista):
    print Dialogo.consumibles[0] + Dialogo.consumibles[1]
    imprimirConsumibles(lista)

# Esta funcion imprime la lista de equipamiento que posee el personaje
def imprimirEquipamiento(lista):
    f = "{0}.- {1}: Bonificador {2} a {3}"
    contador = 1
    for equipamiento in lista:
        linea = f.format(contador, equipamiento.nombre, equipamiento.multiplicador, equipamiento.atributo)
        contador += 1
        print linea

# Esta funcion imprime el texto relacionado con los equipos y luego se imprime el listado de equipamiento
def imprimirListadoEq(Dialogo, lista):
    print Dialogo.equipamiento[0] + Dialogo.equipamiento[1]
    imprimirEquipamiento(lista)

# Esta funcion imprime los stats actuales del personaje
def imprimirStats(personaje):
    f = "Stats actuales: V {0} D {1} R {2} I {3} S {4}\nTiempo disponible: {5}"
    print f.format(personaje.vida, personaje.destreza, personaje.resistencia, personaje.inteligencia, personaje.suerte,
                   personaje.tiempo)

# Esta funcion usa el consumible, modificando los stats del personaje
def usarConsumible(personaje, atributo, buff):
    atributo = atributo
    if atributo == "destreza":
        personaje.destreza += buff
    elif atributo == "resistencia":
        personaje.resistencia += buff
    elif atributo == "inteligencia":
        personaje.resistencia += buff
    else:
        personaje.suerte += buff

# Esta funcion usa el equipamiento, modificando los stats del personaje
def usarEquipable(personaje, atributo, buff):
    if atributo == "destreza":
        personaje.destreza += buff
    elif atributo == "resistencia":
        personaje.resistencia += buff
    elif atributo == "inteligencia":
        personaje.resistencia += buff
    else:
        personaje.suerte += buff

# Esta funcion modifica los stats del personaje al inicio.
def sumarStats(personaje, vida, destreza, resistencia, inteligencia, suerte):
    personaje.vida += vida
    personaje.destreza += destreza
    personaje.resistencia += resistencia
    personaje.inteligencia += inteligencia
    personaje.suerte += suerte

'''
def equipar(personaje, equipamiento):
'''
