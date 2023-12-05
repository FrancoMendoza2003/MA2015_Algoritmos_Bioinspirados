import sys
import pandas as pd
import time

lugares=pd.read_csv("actividad2.csv",index_col=0)
tuple_list = [tuple(x) for x in lugares.to_records(index=False)]

def distancia(ciudad1, ciudad2):
    # Función para calcular la distancia euclidiana entre dos ciudades
    return (tuple_list[ciudad1-1][ciudad2-1])

def distancia_total(ruta):
    # Función para calcular la distancia total de una ruta
    distancia_total = 0
    for i in range(len(ruta)-1):
        distancia_total += distancia(ruta[i], ruta[i+1])
    return distancia_total

def heuristico_insercion(ciudades):
    # Inicializar la ruta con las dos primeras ciudades
    ruta = [ciudades[0], ciudades[1],ciudades[0]] #La ruta es una lista de tuplas

    # Iterar sobre las ciudades restantes y agregarlas a la ruta
    for i in range(2, len(ciudades)):
        mejor_distancia = sys.maxsize
        mejor_posicion = 0
        print(ciudades[i])
        # Encontrar la mejor posición para insertar la ciudad actual
        for j in range(len(ruta)-1):
            d = distancia(ciudades[i], ruta[j]) + distancia(ciudades[i], ruta[j + 1]) - distancia(ruta[j], ruta[j + 1]) #El menos es porque es la distancia que sustituye
            print(j,":",d)
            if d < mejor_distancia:
                mejor_distancia = d
                mejor_posicion = j + 1

        # Insertar la ciudad en la mejor posición encontrada
        ruta.insert(mejor_posicion, ciudades[i])
        print("Ruta:",ruta)

    return ruta

# Record the start time
start_time = time.time()


# Ejemplo de uso para 7 nodos
numbers_vector = list(range(1, 8))
# Ejemplo de uso para 5 nodos
#ciudades_ejemplo = [1,2,3,4,5]
ruta_optima = heuristico_insercion(numbers_vector)
costo=distancia_total(ruta_optima)



print("Ruta óptima:", ruta_optima)
print("Costo:", costo)


# Record the end time
end_time = time.time()

# Calculate the elapsed time
elapsed_time = end_time - start_time

# Print the elapsed time
print(f"Time of execution: {elapsed_time} seconds")
