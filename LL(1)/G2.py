CADENA_VACIA = None
FIN_DE_CADENA = '$'

def crear_conjuntos(reglas):
    conjuntos_primeros = {}
    conjuntos_siguientes = {}
    conjuntos_prediccion = {}

    for regla in reglas:
        izquierda = regla['left']
        conjuntos_primeros[izquierda] = []
        conjuntos_siguientes[izquierda] = []

    def union(arr1, arr2):
        return list(set(arr1) | set(arr2))

    def es_no_terminal(item):
        return item in conjuntos_primeros

    def almacenar_conjuntos(conjunto_inicial, items, conjunto_adicional):
        conjunto = conjunto_inicial.copy()

        for index, item in enumerate(items):
            if es_no_terminal(item):
                conjunto = union(conjunto, [i for i in conjuntos_primeros[item] if i != CADENA_VACIA])

                if CADENA_VACIA in conjuntos_primeros[item]:
                    if index + 1 < len(items):
                        continue
                    conjunto = union(conjunto, conjunto_adicional)
            else:
                conjunto = union(conjunto, [item])
            break

        return conjunto

    def calcular_primeros():
        cambio_de_conjunto = True

        while cambio_de_conjunto:
            cambio_de_conjunto = False

            for regla in reglas:
                izquierda = regla['left']
                derecha = regla['right']
                conjunto = conjuntos_primeros[izquierda].copy()
                conjunto = union(conjunto, almacenar_conjuntos(conjunto, derecha, [CADENA_VACIA]))

                if len(conjuntos_primeros[izquierda]) != len(conjunto):
                    conjuntos_primeros[izquierda] = conjunto
                    cambio_de_conjunto = True

        return conjuntos_primeros

    def calcular_siguientes():
        conjuntos_siguientes[reglas[0]['left']].append(FIN_DE_CADENA)

        cambio_de_conjunto = True

        while cambio_de_conjunto:
            cambio_de_conjunto = False

            for regla in reglas:
                izquierda = regla['left']
                derecha = regla['right']

                for index, item in enumerate(derecha):
                    if not es_no_terminal(item):
                        continue

                    conjunto = conjuntos_siguientes[item].copy()

                    if index + 1 < len(derecha):
                        conjunto = union(conjunto, almacenar_conjuntos(conjunto, derecha[index + 1:], conjuntos_siguientes[izquierda]))
                    else:
                        conjunto = union(conjunto, conjuntos_siguientes[izquierda])

                    if len(conjuntos_siguientes[item]) != len(conjunto):
                        conjuntos_siguientes[item] = conjunto
                        cambio_de_conjunto = True

        return conjuntos_siguientes

    def calcular_conjuntos_prediccion():
        for indice_regla, regla in enumerate(reglas, start=1):
            izquierda = regla['left']
            derecha = regla['right']
            conjunto = []

            if es_no_terminal(derecha[0]):
                conjunto = union(conjunto, almacenar_conjuntos(conjunto, derecha, conjuntos_siguientes[izquierda]))
            elif derecha[0] == CADENA_VACIA:
                conjunto = [item for item in conjuntos_siguientes[izquierda] if item != FIN_DE_CADENA]
            else:
                conjunto.append(derecha[0])

            conjuntos_prediccion[indice_regla] = conjunto

        return conjuntos_prediccion

    conjuntos_primeros = calcular_primeros()
    conjuntos_siguientes = calcular_siguientes()
    conjuntos_prediccion = calcular_conjuntos_prediccion()

    return {'conjuntos_primeros': conjuntos_primeros, 'conjuntos_siguientes': conjuntos_siguientes, 'conjuntos_prediccion': conjuntos_prediccion}

reglas = [
    {'left': 'S', 'right': ['A', 'B', 'uno']},
    {'left': 'A', 'right': ['dos', 'B']},
    {'left': 'A', 'right': [CADENA_VACIA]},
    {'left': 'B', 'right': ['C', 'D']},
    {'left': 'B', 'right': ['tres']},
    {'left': 'B', 'right': [CADENA_VACIA]},
    {'left': 'C', 'right': ['cuatro', 'A', 'B']},
    {'left': 'C', 'right': ['cinco']},
    {'left': 'D', 'right': ['seis']},
    {'left': 'D', 'right': [CADENA_VACIA]}
]

def imprimir_conjuntos(conjuntos):
    for nombre_conjunto, diccionario_conjunto in conjuntos.items():
        print("\n{}:".format(nombre_conjunto))
        for clave, valor in diccionario_conjunto.items():
            valores_cadena = [str(v) if v is not None else 'epsilon' for v in valor]
            if nombre_conjunto == 'conjuntos_prediccion':
                regla = reglas[clave - 1]  
                elementos_regla = [str(r) if r is not None else 'epsilon' for r in regla['right']]
                print("  {} -> {}: {{{}}}".format(regla['left'], ' '.join(elementos_regla), ', '.join(valores_cadena)))
            else:
                print("  {}: {}".format(clave, ', '.join(valores_cadena)))

conjuntos = crear_conjuntos(reglas)
imprimir_conjuntos(conjuntos)
