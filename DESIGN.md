# Diseño de la cola de triaje

`TriageQueue` mantiene tres `deque`, una por nivel. Encolar y retirar de cada
nivel cuesta O(1); para llamar al siguiente basta revisar los niveles en orden
1, 2 y 3. Cada `deque` conserva el orden FIFO de los pacientes de ese nivel.
Una sola `deque` necesitaría insertar pacientes críticos en medio de la cola,
y una lista ordenada puede requerir desplazar elementos en cada inserción.

Las operaciones que leen o modifican las colas usan el mismo `Lock`. Si un
worker encola un paciente crítico mientras otro llama al siguiente, el lock
serializa ambas operaciones: si el encolado ocurre primero, el paciente
crítico queda disponible para la siguiente llamada; si la extracción ocurre
primero, esa llamada retira exactamente al paciente que encabezaba la cola y
el crítico queda primero para la próxima. Así no se puede extraer dos veces
el mismo paciente.