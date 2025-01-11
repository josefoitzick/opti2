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
