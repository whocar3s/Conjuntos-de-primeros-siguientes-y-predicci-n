def calcular_primeros(gramatica):
    primeros = {}

    def es_terminal(simbolo):
        return simbolo.islower()

    def calcular_primeros_rec(simbolo, procesados=set()):
        if simbolo in primeros:
            return primeros[simbolo]

        primeros[simbolo] = set()

        for produccion in gramatica[simbolo]:
            primer_simbolo = produccion[0]

            # Caso 1: Si la producción es epsilon añadirlo a los primeros del símbolo actual
            if primer_simbolo == '':
                if len(produccion) == 1:
                    primeros[simbolo].add('')
            # Caso 2: Si el primer símbolo es terminal añadirlo a los primeros del símbolo actual
            elif es_terminal(primer_simbolo):
                primeros[simbolo].add(primer_simbolo)
            # Caso 3: Si el primer símbolo es no terminal calcular los primeros de ese no terminal y añadirlos
            else:
                todos_epsilon = True
                for simbolo_primero in produccion:
                    if not es_terminal(simbolo_primero):
                        primeros_simbolo = calcular_primeros_rec(simbolo_primero)
                        primeros[simbolo].update(primeros_simbolo - {''})  
                        if '' not in primeros_simbolo:
                            todos_epsilon = False
                            break
                    else:
                        primeros[simbolo].add(simbolo_primero)
                        todos_epsilon = False
                        break

                if todos_epsilon:
                    primeros[simbolo].add('')

        return primeros[simbolo]

    for simbolo in gramatica.keys():
        calcular_primeros_rec(simbolo)

    return primeros


def calcular_primeros_secuencia(gramatica, secuencia):
    conjunto_primeros = set()
    for simbolo in secuencia:
        if simbolo.islower():
            conjunto_primeros.add(simbolo)
            break
        elif simbolo != '':
            primeros_simbolo = calcular_primeros(gramatica)[simbolo] 
            conjunto_primeros |= primeros_simbolo - {''}
            if '' not in primeros_simbolo:
                break
    return conjunto_primeros

def calcular_siguientes(gramatica, conjunto_primeros):
    siguientes = {no_terminal: set() for no_terminal in gramatica.keys()}

    def es_terminal(simbolo):
        return simbolo.islower()

    procesados = set()

    def calcular_siguientes_rec(no_terminal, procesados=set()):

        if no_terminal in procesados:
            return siguientes[no_terminal]

        procesados.add(no_terminal)

        for nt, producciones in gramatica.items():
            for produccion in producciones:
                for i, simbolo in enumerate(produccion):
                    if simbolo == no_terminal:
                        if i == len(produccion) - 1:
                            # Caso 3: Añadir a SIGUIENTE(B) los elementos de SIGUIENTE(A)
                            siguientes[no_terminal].update(calcular_siguientes_rec(nt, procesados))
                        elif produccion[i + 1] == '':
                            # Caso 3: Añadir a SIGUIENTE(B) los elementos de SIGUIENTE(A)
                            siguientes[no_terminal].update(calcular_siguientes_rec(nt, procesados))
                            # Remover epsilon si se encuentra en los siguientes de A
                            if '' in siguientes[nt]:
                                siguientes[no_terminal].remove('')
                        else:
                            siguiente_simbolo = produccion[i + 1]
                            if es_terminal(siguiente_simbolo):
                                # Caso 2: Añadir a SIGUIENTE(B) el terminal siguiente_simbolo
                                siguientes[no_terminal].add(siguiente_simbolo)
                            elif siguiente_simbolo != '':
                                # Caso 2: Añadir a SIGUIENTE(B) los elementos de PRIMERO(β)
                                primeros_beta = calcular_primeros_secuencia(gramatica, produccion[i + 1:])
                                if '' in primeros_beta:
                                    siguientes[no_terminal].update(primeros_beta - {''})
                                    siguientes[no_terminal].update(calcular_siguientes_rec(siguiente_simbolo, procesados))
                                else:
                                    siguientes[no_terminal].update(primeros_beta)
                                # Si hay un simbolo siguiente, agregarlo tambien
                                siguientes[no_terminal].update(calcular_siguientes_rec(siguiente_simbolo, procesados))

        return siguientes[no_terminal]

    for no_terminal in gramatica.keys():
        calcular_siguientes_rec(no_terminal)

    return siguientes

def calcular_conjunto_prediccion(gramatica, conjunto_primeros, conjunto_siguientes):
    conjunto_prediccion_completo = {}

    for no_terminal, producciones in gramatica.items():
        conjunto_prediccion_completo[no_terminal] = {}

        for produccion in producciones:
            conjunto_prediccion = set()

            primeros_produccion = calcular_primeros_secuencia(gramatica, produccion)

            if produccion == ['']:
                if '' in conjunto_primeros:
                    conjunto_prediccion.update((conjunto_primeros[''] - {''}) | conjunto_siguientes[no_terminal])
                else:
                    conjunto_prediccion.update(conjunto_siguientes[no_terminal])
            else:
                conjunto_prediccion.update(primeros_produccion - {''})

            conjunto_prediccion_completo[no_terminal][tuple(produccion)] = conjunto_prediccion

    return conjunto_prediccion_completo



# Ejemplo de gramática
gramatica = {
    'A': [['B', 'C'], ['ant', 'A', 'all']],
    'B': [['big', 'C'], ['bus', 'A', 'boss'], ['']],
    'C': [['cat'], ['cow']]
}


conjunto_primeros = calcular_primeros(gramatica)
conjunto_siguientes = calcular_siguientes(gramatica, conjunto_primeros)

for no_terminal, primeros in conjunto_primeros.items():
    print(f'Primeros de {no_terminal}: {primeros}')

for no_terminal, siguientes in conjunto_siguientes.items():
    print(f'Siguientes de {no_terminal}: {siguientes}')

conjunto_prediccion_completo = calcular_conjunto_prediccion(gramatica, conjunto_primeros, conjunto_siguientes)

for no_terminal, producciones in conjunto_prediccion_completo.items():
    for produccion, conjunto_prediccion in producciones.items():
        print(f"Conjunto de prediccion de {no_terminal} -> {' '.join(produccion)} : {conjunto_prediccion}")


