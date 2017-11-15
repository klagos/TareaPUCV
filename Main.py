from Clases import *

if __name__ == '__main__':
    # Crear Partida
    arch = open("base.txt")
    Partida = main.crearPartida(arch)
    arch.close()

    arch = open("texto.txt")
    Dialogo = Texto(arch)
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

    Partida.personaje.imprimirStatsIniciales()
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
        atributo = Partida.getAtributo(ingreso - 1)
        Partida.personaje.buffearAtributo(multiplicador, atributo)
        Partida.removerEquipo(ingreso - 1)
        Dialogo.imprimirEquipamiento(Partida.getEquipo())
        cantEquipados += 1
    Partida.personaje.imprimirStats()
    Dialogo.imprimirListadoCon(Partida.getConsumibles())
