#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Clases import *

if __name__ == '__main__':
    # Crear Partida
    arch = open("base.txt")
    Partida = main.crearPartida(arch)
    arch.close()

    Dialogo.imprimirSaludo()
    Partida.personaje.nombre = raw_input("> ")
    print Dialogo.informarInicio(Partida.personaje)

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

    Partida.personaje.sumarStats(vida, destreza, resistencia, inteligencia, suerte)

    Partida.imprimirStatsIniciales()

    # Proceso de equipamiento
    Dialogo.imprimirListadoEq(Partida.equipo)
    ingreso = ""
    cantEquipados = 0
    while cantEquipados != 3:
        print ""
        ingreso = int(raw_input("> "))
        print ""
        if ingreso == -1:
            break
        multiplicador = Partida.getMultiplicador(ingreso - 1)
        atributo = Partida.getEAtributo(ingreso - 1)
        Partida.buffearAtributo(multiplicador, atributo)
        Partida.removerEquipo(ingreso - 1)
        Dialogo.imprimirEquipamiento(Partida.getEquipo())
        cantEquipados += 1
    Partida.personaje.imprimirStats()

    # Variable i para la cantidad de pruebas a enfrentar
    i = 0

    #Equipamiento de consumibles para el personaje y sus evaluaciones
    while (i+1 != 3):
        while True:
            Dialogo.imprimirListadoCon(Partida.getConsumibles())
            ingreso = int(raw_input("> "))
            if ingreso == -1 or len(Partida.getConsumibles()) == 0:
                break
            else:
                atributo = Partida.getCAtributo(ingreso-1)
                buff = Partida.getBuff(ingreso - 1)
                costo = Partida.getCosto(ingreso-1)
                print costo
                if (Partida.personaje.usarConsumible(atributo, buff, costo)):
                    Partida.restarStockConsumible(ingreso - 1)
                    if Partida.stockCero(ingreso - 1):
                        Partida.removerConsumible(ingreso - 1)
                else:
                    Dialogo.imprimirError3()
        Partida.imprimirStatsPersonaje()
        Dialogo.imprimirInterrogacion(Partida,i)

        # Inicio de evaluacion
        gana, hpPerdido = Partida.evaluacion(i)
        if not gana:
            Partida.daniarPersonaje(hpPerdido)

        # Si el personaje esta vivo, se imprime el dialogo de felicidades y se le
        # suma 1 a nuestro contador de pruebas. En el caso contrario el juego termina.
        if Partida.personajeVivo():
            Dialogo.imprimirFelicitaciones(hpPerdido)
            i += 1
        else:
            print "¡Perdiste!, los ramos eran muy dificiles..."
            break
