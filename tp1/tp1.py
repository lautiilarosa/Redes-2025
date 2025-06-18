import re
archivo = open("Tramas_802-15-4.log")
contenido = archivo.read()


tramasLC = []
tramasconS = []
tramasLI = []
tramas_checksum_incorrecto = []

#dividir las tramas
def split_tramas(text):
    tramas = re.split(r'(?<!7D)7E', text)
    tramas = ['7E' + trama for trama in tramas[1:]]
    tramas[-1] = tramas[-1].replace('\n', '')
    return tramas

#calcular longitud correcta
def longitud_correcta(tramas):
    tramaslongitudC = 0

    for i in range(len(tramas)):
        trama = tramas[i]
        # extraer la longitud de la trama y pasarla a decimal
        long = int(trama[2:6], 16)

        # extraer la longitud real de los datos (excluyendo el delimitador inicial, la longitud y el checksum)
        datos = trama[6:-2]
        if "7D7E" in datos:
            datos = datos.replace("7D7E", "7E")
            tramasconS.append(trama)

        long_real = len(datos) // 2

        # verificar si la longitud es correcta
        if long == long_real:
            tramaslongitudC += 1
            # agregar trama a la lista de tramas con longitud correcta
            tramasLC.append(trama)
        else:
            # agregar trama a la lista de tramas con longitud incorrecta
            tramasLI.append(trama)

    return tramaslongitudC

#calcular checksum
def checksum(tramasLC):
    checksumC = 0
    for i in range(len(tramasLC)):
        trama = tramasLC[i]
        # extraer los datos de la trama
        datos = trama[6:-2]
        if "7D7E" in datos:
            datos = datos.replace("7D7E", "7E")

        # calcular el checksum
        suma = 0
        k = 0
        while k < len(datos):
            byte = datos[k:k + 2]
            suma += int(byte, 16)
            k += 2

        # obtener el checksum de la trama (último byte)
        checksum_trama = int(trama[-2:], 16)

        # verificar si el checksum es correcto
        checksum_calculado = 0xFF - (suma & 0xFF)
        if checksum_trama == checksum_calculado:
            checksumC += 1
        else:
            tramas_checksum_incorrecto.append((i, trama))
    return checksumC




#1) contar tramas
tramas = split_tramas(contenido)
print("Nota: Los resultados son:")
print("Tramas Totales:",len(tramas))

#2) Indicar el número de tramas con longitud correcta y con longitud incorrecta.
x = longitud_correcta(tramas)
print("Tramas con longitud correcta:",x)
print("Tramas con longitud incorrecta:",len(tramas)-x)

#3) Para las tramas con longitud correcta, indicar el número de tramas con suma de verificación correcta y con suma de verificación incorrecta.
y = checksum(tramasLC)
print("Tramas con longitud correcta y checksum correcto:",y)
print("Tramas con longitud correcta y checksum incorrecto:",len(tramasLC)-y)

#4)Números de tramas que utilizan secuencia de escape.
print("Tramas con secuencia de escape:",len(tramasconS))

#5) Para cada línea con secuencia de escape, imprimir el número de línea y lalínea luego de retirar las secuencias de escape (las líneas se enumeran desde el 0)
print("")
print("Tramas con secuencia de escape:")
for i in range(len(tramasconS)):
    aux = tramasconS[i]
    if "7D7E" in aux:
        aux = aux.replace("7D7E", "7E")
    print(i+1,": ",aux)
print("")

#6) Para cada línea con longitud o checksum incorrecto, imprimir el número de línea y la línea incorrecta.
print("Tramas con longitud incorrecta:")
for i in range(len(tramasLI)):
    print(i+1,": ",tramasLI[i])
print("")
print("Tramas con checksum incorrecto:")
for i in range(len(tramas_checksum_incorrecto)):
    print(tramas_checksum_incorrecto[i][0]+1,": ",tramas_checksum_incorrecto[i][1])
