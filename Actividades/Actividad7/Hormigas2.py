from random import seed
from random import random
import time
# Parámetros del algoritmo de colonia de hormigas
num_hormigas = 4
iteraciones = 100
# Caminos es la matriz de parámetros del problema	
Caminos = [["0-1","0-2","0-3","1-2","1-3","1-4","2-3","2-4","3-4"],[4000,5400,9800,4300,6200,8700,4800,7100,4900]]
convenencia=[]
for i in range(len(Caminos[1])):
    convenencia.append(1/Caminos[1][i])
#Agregar convenencia
Caminos.append(convenencia)
#Agregar tao (feromonas)
Caminos.append([0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1])

alpha=0.1
beta=10


# Record the start time
start_time = time.time()
for i in range(iteraciones):
    Hormigas=[]
    for i in range(num_hormigas):
        cam_final=[]
        opciones_disponibles=[0,1,2]
        for i in range(4):  # Planificación a 3 años
            #Guardar el valor de convenencia*feromona
            nT=[]
            for i in (opciones_disponibles):
                nT.append((Caminos[2][i]**alpha)*(Caminos[3][i]**beta))
            #Guardar el valor de probabilidad acumulada para ver cual decisión tomar
            Pij=[0]
            for i in range(len(nT)):
                Pij.append((nT[i]/sum(nT))+Pij[i])
            del Pij[0]
            #print(Pij)
            P=random()
            #print(P)
            #Escoger una opción
            for i in range(len(opciones_disponibles)):
                if P<Pij[i]:
                    cam_sel=(opciones_disponibles[i])
                    break
            #print(Caminos[0][cam_sel])
            #Dar opciones disponibles para la siguiente iteración
            cam_final.append(cam_sel)
            if cam_sel==0:
                opciones_disponibles=[3,4,5]
            elif cam_sel==1:
                opciones_disponibles=[6,7]
            elif cam_sel==2:
                opciones_disponibles=[8]
            elif cam_sel==3:
                opciones_disponibles=[6,7]
            elif cam_sel==4:
                opciones_disponibles=[8]
            elif cam_sel==6:
                opciones_disponibles=[8]
            elif cam_sel==5 or cam_sel==7 or cam_sel==8:
                break

        costo_solucion=0
        cam_hormiga=[]
        for i in cam_final:
            cam_hormiga.append(Caminos[0][i])
            costo_solucion+=Caminos[1][i]
        sol_hormiga=[cam_final,cam_hormiga,costo_solucion]
        Hormigas.append(sol_hormiga)

    #Ejemplo de clase
    #Hormigas=[[[0, 4, 8], ['0-1', '1-3', '3-4'], 15100], [[1, 7], ['0-2' ,'2-4'], 12500]]
    #Ejemplo de presentación
    #Hormigas=[[[0, 5], ['0-1', '1-4'], 12700], [[1, 7], ['0-2' ,'2-4'], 12500]]
    
    deltas=[]
    # Generar k vectores con ceros
    for i in range(len(Hormigas)):
        deltas.append([0] * 9)
    # Buscar que caminos tomo cada hormiga (deltas)
    for i in range(len(deltas)):
        for j in (Hormigas[i][0]):
            deltas[i][j]=1/Hormigas[i][2]

    # Sumar los k deltas
    Deltas=[0]*9
    for i in range(len(deltas)):
        for j in range(len(deltas[i])):
            Deltas[j]+=deltas[i][j]

    # Actualización global de feromonas
    for i in range(len(Caminos[3])):
        Caminos[3][i]=Caminos[3][i]*0.9+Deltas[i]
    
    print(Hormigas)
    print(Caminos[3])
    
# Record the end time
end_time = time.time()

# Calculate the elapsed time
elapsed_time = end_time - start_time

# Print the elapsed time
print(f"Time of execution: {elapsed_time} seconds")
    




        

