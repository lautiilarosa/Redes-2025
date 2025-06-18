with open("Tramas_802-15-4.log", "r") as archivo:
    contenido = archivo.read()

# Variables a utilizar
tramaslongitudC = 0
tramasconS = 0
checksumC = 0
tramas = 0
i = 0

# Listas para guardar las tramas con problemas
tramas_con_escape = []
tramas_longitud_incorrecta = []
tramas_checksum_incorrecto = []

# Función para analizar una trama
def analizartrama(inicio, fin, num_trama):
    global tramaslongitudC, tramasconS, checksumC

    # Verificar si hay secuencias de escape en la trama
    trama = contenido[inicio:fin]
    if "7D" in trama:
        tramasconS += 1
        tramas_con_escape.append((num_trama, trama.replace("7D7E", "7E").replace("7D7D", "7D")))

    # Extraer la longitud de la trama (bytes 2 y 3)
    long = contenido[inicio+2:inicio+6]
    long = int(long, 16)

    # Calcular la longitud real de los datos (excluyendo el delimitador inicial, la longitud y el checksum)
    datos = contenido[inicio+6:fin-2]
    datos = datos.replace("7D7E", "7E").replace("7D7D", "7D")  
    long_real = len(datos) // 2  

    # Verificar si la longitud es correcta
    if long == long_real:
        tramaslongitudC += 1

        # Calcular el checksum
        suma = 0
        k = 0
        while k < len(datos):
            byte = datos[k:k+2]
            suma += int(byte, 16)
            k += 2

        # Obtener el checksum de la trama (último byte)
        checksum_trama = int(contenido[fin-2:fin], 16)

        # Verificar si el checksum es correcto
        checksum_calculado = 0xFF - (suma & 0xFF)
        if checksum_trama == checksum_calculado:
            checksumC += 1
        else:
            tramas_checksum_incorrecto.append((num_trama, trama))
    else:
        tramas_longitud_incorrecta.append((num_trama, trama))

# Recorrer las tramas
while i < len(contenido):
    # Buscar el inicio de la trama (delimitador "7E")
    inicio = contenido.find("7E", i)
    if inicio == -1:
        break  # No hay más tramas

    # Buscar el final de la trama (siguiente "7E" que no esté escapado)
    fin = inicio + 2  # Empezar a buscar después del primer "7E"
    while fin < len(contenido):
        # Buscar el siguiente "7E"
        fin = contenido.find("7E", fin)
        if fin == -1:
            fin = len(contenido)  # Última trama
            break

        # Verificar si el "7E" está escapado (precedido por "7D")
        if fin >= 2 and contenido[fin-2:fin] == "7D":
            fin += 2  # Saltar el "7E" escapado y continuar buscando
        else:
            break  # Encontramos el final de la trama

    # Procesar la trama
    tramas += 1
    analizartrama(inicio, fin, tramas)

    # Mover el índice al final de la trama actual
    i = fin

# Resultados
print("La cantidad de tramas es: ", tramas)
print("La cantidad de tramas con longitud correcta es: ", tramaslongitudC)
print("La cantidad de tramas con longitud incorrecta es: ", (tramas - tramaslongitudC))
print("La cantidad de tramas con longitud correcta y checksum correcto es: ", checksumC)
print("La cantidad de tramas con longitud correcta y checksum incorrecto es: ", (tramaslongitudC - checksumC))
print("La cantidad de tramas con secuencia de escape es: ", tramasconS)

# Imprimir tramas con secuencia de escape
print("\nTramas con secuencia de escape:")
for num_trama, trama in tramas_con_escape:
    print(f"Trama {num_trama}: {trama}")

# Imprimir tramas con longitud incorrecta
print("\nTramas con longitud incorrecta:")
for num_trama, trama in tramas_longitud_incorrecta:
    print(f"Trama {num_trama}: {trama}")

# Imprimir tramas con checksum incorrecto
print("\nTramas con checksum incorrecto:")
for num_trama, trama in tramas_checksum_incorrecto:
    print(f"Trama {num_trama}: {trama}")