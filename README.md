# opti2
Proyecto 2 - Métodos de optimización


Parámetros de la instancia

# areas:

Significado: Lista de identificadores únicos para las áreas que deben ser visitadas. Cada área representa un lugar donde los fiscalizadores deben realizar tareas de mantenimiento o inspección.

Ejemplo: "areas": [1, 2, 3, 4, 5] significa que hay 5 áreas que deben ser atendidas.


# vehiculos:

Significado: Lista de identificadores únicos para los vehículos disponibles. Cada vehículo se utiliza para transportar a los fiscalizadores y cubrir las áreas asignadas.

Ejemplo: "vehiculos": [1, 2, 3] indica que hay 3 vehículos disponibles para realizar las visitas.


# fiscalizadores:

Significado: Lista de identificadores únicos para los fiscalizadores disponibles. Los fiscalizadores son las personas responsables de realizar las tareas en cada área.

Ejemplo: "fiscalizadores": [1, 2, 3, 4] significa que hay 4 fiscalizadores disponibles.


# TMax:

Significado: Tiempo máximo, en minutos, que un vehículo puede operar en un día. Esto incluye los tiempos de traslado y el tiempo requerido para realizar las tareas en las áreas asignadas.

Ejemplo: "TMax": 480 significa que cada vehículo puede operar hasta 480 minutos en un día.

# Tij:

Significado: Matriz que indica el tiempo necesario (en minutos) para que un vehículo visite un área específica. Las claves externas representan las áreas y las internas representan los vehículos.

Ejemplo: "Tij": {
    "1": {"1": 30, "2": 40},
    "2": {"1": 45, "2": 50}
}

Esto significa que el vehículo 1 tarda 30 minutos en visitar el área 1 y 45 minutos en visitar el área 2, mientras que el vehículo 2 tarda 40 minutos en el área 1 y 50 minutos en el área 2.

# Cap:

Significado: Capacidad máxima de supervisores que puede transportar un vehículo al mismo tiempo.

Ejemplo: "Cap": 4 significa que cada vehículo puede llevar hasta 4 fiscalizadores.


# a:

Significado: Número mínimo de salidas que debe realizar un fiscalizador durante la semana.

Ejemplo: "a": 2 significa que cada fiscalizador debe realizar al menos 2 salidas semanales.


# b:

Significado: Número máximo de salidas que puede realizar un fiscalizador durante la semana.

Ejemplo: "b": 6 significa que un fiscalizador no puede realizar más de 6 salidas semanales.

# Cost:

Significado: Costos fijos asociados al uso de cada vehículo. Este costo incluye combustible, mantenimiento y otros gastos operativos diarios.

Ejemplo: "Cost": {
    "1": 25,
    "2": 20,
    "3": 15
}

Esto significa que el costo diario de operar el vehículo 1 es 25 unidades, el del vehículo 2 es 20 unidades, y el del vehículo 3 es 15 unidades.

# Comb:

Representa el costo promedio del combustible (en CLP) que consume cada vehículo 𝑘 k al visitar el área 𝑖.

Por ejemplo: "Comb": { "1": {"1": 3000, "2": 4000, "3": 5000} } significa que:

El vehículo 1 gasta 3,000 CLP en combustible para el área 1.

El vehículo 2 gasta 4,000 CLP en combustible para el área 1.

El vehículo 3 gasta 5,000 CLP en combustible para el área 1.


