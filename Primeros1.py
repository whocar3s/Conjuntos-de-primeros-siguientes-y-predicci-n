def calcular_primeros(gramatica):
    primeros = {}

    # Función para verificar si un símbolo es terminal
    def es_terminal(simbolo):
        return simbolo.islower()

    # Función recursiva para calcular los primeros de un símbolo
    def calcular_primeros_rec(simbolo):
        # Si ya se ha calculado el conjunto de primeros para este símbolo, retornarlos
        if simbolo in primeros:
            return primeros[simbolo]

        primeros[simbolo] = set()

        for produccion in gramatica[simbolo]:
            primer_simbolo = produccion[0]

            # Caso 1: Si la producción es epsilon, añadirlo a los primeros del símbolo actual
            if primer_simbolo == ' ':
                primeros[simbolo].add(' ')
            # Caso 2: Si el primer símbolo es terminal, añadirlo a los primeros del símbolo actual
            elif es_terminal(primer_simbolo):
                primeros[simbolo].add(primer_simbolo)
            # Caso 3: Si el primer símbolo es no terminal, calcular los primeros de ese no terminal y añadirlos
            else:
                todos_epsilon = True
                for simbolo_primero in produccion:
                    # Verificar si es un no terminal
                    if not es_terminal(simbolo_primero):
                        primeros_simbolo = calcular_primeros_rec(simbolo_primero)
                        # Agregar los primeros del no terminal al conjunto de primeros del símbolo actual
                        primeros[simbolo].update(primeros_simbolo - {' '})  # Agregar todos los primeros menos el epsilon
                        # Si el no terminal no produce epsilon, marcar que no todos los símbolos producen epsilon
                        if ' ' not in primeros_simbolo:
                            todos_epsilon = False
                            break
                    else:
                        primeros[simbolo].add(simbolo_primero)
                        todos_epsilon = False
                        break

                # Si todos los no terminales en la producción producen epsilon, agregar epsilon al conjunto de primeros del símbolo actual
                if todos_epsilon:
                    primeros[simbolo].add(' ')

        return primeros[simbolo]

    # Calcular primeros para cada símbolo de la gramática
    for simbolo in gramatica.keys():
        calcular_primeros_rec(simbolo)

    return primeros

# Ejemplo de gramática
gramatica = {
    'A': [['B', 'C'], ['ant', 'B', 'all']],
    'B': [['big', 'C'], ['bus', 'A', 'boss'], [' ']],
    'C': [['cat'], ['cow']]
}

conjunto_primeros = calcular_primeros(gramatica)
for no_terminal, primeros in conjunto_primeros.items():
    print(f'Primeros de {no_terminal}: {primeros}')
