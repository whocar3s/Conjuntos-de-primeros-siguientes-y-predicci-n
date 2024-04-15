CADENA_VACIA = None
FIN_DE_CADENA = '$'

def crear_conjuntos(reglas):
    conjuntos_primeros = {}
    conjuntos_siguientes = {}
    conjuntos_prediccion = {}

    # Inicializar los conjuntos de primeros y siguientes para cada no terminal
    for regla in reglas:
        izquierda = regla['left']
        conjuntos_primeros[izquierda] = []
        conjuntos_siguientes[izquierda] = []

    # Función para unir dos listas sin duplicados
    def union(arr1, arr2):
        return list(set(arr1) | set(arr2))

    # Función para verificar si un elemento es un no terminal
    def es_no_terminal(item):
        return item in conjuntos_primeros

    # Función para recolectar los elementos de los conjuntos de primeros y siguientes
    def almacenar_conjuntos(conjunto_inicial, items, conjunto_adicional):
        conjunto = conjunto_inicial.copy()

        for index, item in enumerate(items):
            if es_no_terminal(item):
                # Regla: Si el item es un no terminal, añadimos los primeros de ese no terminal al conjunto
                conjunto = union(conjunto, [i for i in conjuntos_primeros[item] if i != CADENA_VACIA])

                if CADENA_VACIA in conjuntos_primeros[item]:
                    if index + 1 < len(items):
                        continue
                    # Regla: Si el no terminal puede derivar en cadena vacía, añadimos el conjunto adicional al conjunto
                    conjunto = union(conjunto, conjunto_adicional)
            else:
                # Regla: Si el item es un terminal, lo añadimos al conjunto
                conjunto = union(conjunto, [item])
            break

        return conjunto

    # Función para crear los conjuntos de primeros
    def calcular_primeros():
        cambio_de_conjunto = True

        while cambio_de_conjunto:
            cambio_de_conjunto = False

            for regla in reglas:
                izquierda = regla['left']
                derecha = regla['right']
                conjunto = conjuntos_primeros[izquierda].copy()
                # Regla: Para cada producción, añadimos los primeros de la parte derecha al conjunto de primeros de la parte izquierda
                conjunto = union(conjunto, almacenar_conjuntos(conjunto, derecha, [CADENA_VACIA]))

                if len(conjuntos_primeros[izquierda]) != len(conjunto):
                    conjuntos_primeros[izquierda] = conjunto
                    cambio_de_conjunto = True

        return conjuntos_primeros

    # Función para crear los conjuntos de siguientes
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
                        # Regla: Si hay un no terminal seguido de otros símbolos, añadimos los primeros de esos símbolos al conjunto de siguientes del no terminal
                        conjunto = union(conjunto, almacenar_conjuntos(conjunto, derecha[index + 1:], conjuntos_siguientes[izquierda]))
                    else:
                        # Regla: Si el no terminal es el último símbolo de la producción, añadimos los siguientes de la parte izquierda al conjunto de siguientes del no terminal
                        conjunto = union(conjunto, conjuntos_siguientes[izquierda])

                    if len(conjuntos_siguientes[item]) != len(conjunto):
                        conjuntos_siguientes[item] = conjunto
                        cambio_de_conjunto = True

        return conjuntos_siguientes

    # Función para crear los conjuntos de predicción
    def calcular_conjuntos_prediccion():
        for indice_regla, regla in enumerate(reglas, start=1):
            izquierda = regla['left']
            derecha = regla['right']
            conjunto = []

            if es_no_terminal(derecha[0]):
                # Regla: Si la producción comienza con un no terminal, añadimos los primeros de ese no terminal al conjunto de predicción
                conjunto = union(conjunto, almacenar_conjuntos(conjunto, derecha, conjuntos_siguientes[izquierda]))
            elif derecha[0] == CADENA_VACIA:
                # Regla: Si la producción deriva en cadena vacía, añadimos los siguientes de la parte izquierda al conjunto de predicción
                conjunto = [item for item in conjuntos_siguientes[izquierda] if item != FIN_DE_CADENA]
            else:
                # Regla: Si la producción comienza con un terminal, añadimos ese terminal al conjunto de predicción
                conjunto.append(derecha[0])

            conjuntos_prediccion[indice_regla] = conjunto

        return conjuntos_prediccion

    conjuntos_primeros = calcular_primeros()
    conjuntos_siguientes = calcular_siguientes()
    conjuntos_prediccion = calcular_conjuntos_prediccion()

    return {'conjuntos_primeros': conjuntos_primeros, 'conjuntos_siguientes': conjuntos_siguientes, 'conjuntos_prediccion': conjuntos_prediccion}

reglas = [
    {'left': 'A', 'right': ['B', 'C']},
    {'left': 'A', 'right': ['ant', 'A', 'all']},
    {'left': 'B', 'right': ['big', 'C']},
    {'left': 'B', 'right': ['bus', 'A', 'boss']},
    {'left': 'B', 'right': [CADENA_VACIA]},
    {'left': 'C', 'right': ['cat']},
    {'left': 'C', 'right': ['cow']}
]

def imprimir_conjuntos(conjuntos):
    for nombre_conjunto, diccionario_conjunto in conjuntos.items():
        print("\n{}:".format(nombre_conjunto))
        for clave, valor in diccionario_conjunto.items():
            # Convertir los elementos a cadenas antes de unirlos
            valores_cadena = [str(v) if v is not None else 'epsilon' for v in valor]
            if nombre_conjunto == 'conjuntos_prediccion':
                # Imprimir la regla en lugar del número
                regla = reglas[clave - 1]  # Restamos 1 porque los índices en Python comienzan en 0
                # Convertir los elementos de la regla a cadenas antes de unirlos
                elementos_regla = [str(r) if r is not None else 'epsilon' for r in regla['right']]
                print("  {} -> {}: {{{}}}".format(regla['left'], ' '.join(elementos_regla), ', '.join(valores_cadena)))
            else:
                print("  {}: {}".format(clave, ', '.join(valores_cadena)))

conjuntos = crear_conjuntos(reglas)
imprimir_conjuntos(conjuntos)
