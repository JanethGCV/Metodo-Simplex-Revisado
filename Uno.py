import numpy as np

# Leer y procesar el archivo único
archivo = 'Problema.txt'  # Nombre del archivo
with open(archivo, 'r') as f:
    lineas = f.readlines()

# Extraer la función objetivo
funcion_objetivo = lineas[1].strip().split('=')[1].strip()
c = np.array([float(x.split('x')[0]) for x in funcion_objetivo.split('+')])

# Extraer las restricciones
restricciones = []
b = []
for linea in lineas[4:]:
    if "<=" in linea:
        coeficientes, lado_derecho = linea.split("<=")
        restricciones.append([float(x.split('x')[0]) for x in coeficientes.strip().split('+')])
        b.append(float(lado_derecho.strip()))
    elif "=" in linea:  # Si hubiera restricciones de igualdad
        coeficientes, lado_derecho = linea.split("=")
        restricciones.append([float(x.split('x')[0]) for x in coeficientes.strip().split('+')])
        b.append(float(lado_derecho.strip()))

A = np.array(restricciones)
b = np.array(b)

# Preparar matriz en forma estándar
num_restricciones, num_variables = A.shape
A_estandar = np.hstack((A, np.eye(num_restricciones)))  # Agregar variables de holgura
c_estandar = np.concatenate((c, np.zeros(num_restricciones)))  # Ampliar vector de costos

# Inicialización de las variables básicas y no básicas
variables_basicas_indices = list(range(num_variables, num_variables + num_restricciones))
variables_no_basicas_indices = list(range(num_variables))
B_inv = np.eye(num_restricciones)  # Inversa inicial de la matriz base
Cb = c_estandar[variables_basicas_indices]
Cn = c
e = np.zeros(num_restricciones)
E = np.eye(num_restricciones)

# Mostrar información del problema
print("Problema en forma estándar:")
print("Maximizar Z =", " + ".join(f"{c_estandar[i]}x{i+1}" for i in range(len(c_estandar))))
print("\nSujeto a:")
for i in range(num_restricciones):
    print(" + ".join(f"{A_estandar[i, j]}x{j+1}" for j in range(A_estandar.shape[1])), "=", b[i])

# Mostrar matrices procesadas
print("\nDatos del problema en forma estándar:")
print("Vector de costos c:\n", c_estandar)
print("Matriz A:\n", A_estandar)
print("Vector b:\n", b)
print("\nVariables básicas iniciales (XB):")
for i in variables_basicas_indices:
    print(f"[x{i+1}]")
print("\nVariables no básicas iniciales (Cn):")
print([f"x{i+1}" for i in variables_no_basicas_indices])
print("\nMatriz (An):\n", A)
print("\nCostos básicos (Cb):\n", Cb)
print("Matriz inversa inicial (B⁻¹):\n", B_inv)
print("Vector de costos reducidos inicial (e):\n", e)
print("Matriz identidad inicial (E):\n", E)
