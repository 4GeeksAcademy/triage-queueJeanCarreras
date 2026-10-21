from collections import deque
from dataclasses import dataclass, field
from datetime import datetime
from threading import Lock
from typing import Deque, Dict, List


@dataclass(frozen=True)
class Patient:
    name: str
    triage_level: int
    arrived_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("El nombre del paciente no puede estar vacío.")
        if self.triage_level not in (1, 2, 3):
            raise ValueError("El nivel de triaje debe ser 1, 2 o 3.")


class TriageQueue:
    def __init__(self) -> None:
        self._queues: Dict[int, Deque[Patient]] = {
            level: deque() for level in (1, 2, 3)
        }
        self._lock = Lock()

    def enqueue(self, patient: Patient) -> None:
        with self._lock:
            self._queues[patient.triage_level].append(patient)

    def dequeue(self) -> Patient:
        with self._lock:
            for level in (1, 2, 3):
                if self._queues[level]:
                    return self._queues[level].popleft()
        raise IndexError("No hay pacientes en espera para llamar.")

    def peek(self) -> Patient:
        with self._lock:
            for level in (1, 2, 3):
                if self._queues[level]:
                    return self._queues[level][0]
        raise IndexError("No hay pacientes en espera.")

    def list_queue(self) -> List[Patient]:
        with self._lock:
            return [
                patient
                for level in (1, 2, 3)
                for patient in self._queues[level]
            ]

    def stats(self) -> Dict[int, int]:
        with self._lock:
            return {level: len(self._queues[level]) for level in (1, 2, 3)}


def _print_patient(patient: Patient) -> None:
    print(
        f"{patient.name} | nivel {patient.triage_level} | "
        f"llegada {patient.arrived_at.isoformat(timespec='seconds')}"
    )


def main() -> None:
    queue = TriageQueue()
    while True:
        print("\nGestor de triaje")
        print("1. Añadir paciente")
        print("2. Llamar al siguiente paciente")
        print("3. Ver cola")
        print("4. Ver estadísticas")
        print("5. Salir")
        try:
            choice = input("Selecciona una opción: ").strip()
            if choice == "1":
                name = input("Nombre del paciente: ").strip()
                triage_level = int(input("Nivel de triaje (1-3): ").strip())
                patient = Patient(name=name, triage_level=triage_level)
                queue.enqueue(patient)
                print(f"Paciente añadido: {patient.name}.")
            elif choice == "2":
                try:
                    patient = queue.dequeue()
                    print("Llamando a:")
                    _print_patient(patient)
                except IndexError as error:
                    print(error)
            elif choice == "3":
                patients = queue.list_queue()
                if not patients:
                    print("La cola está vacía.")
                else:
                    for patient in patients:
                        _print_patient(patient)
            elif choice == "4":
                print("Pacientes en espera por nivel:")
                for level, count in queue.stats().items():
                    print(f"Nivel {level}: {count}")
            elif choice == "5":
                print("Saliendo del gestor de triaje.")
                return
            else:
                print("Opción inválida. Elige un número del 1 al 5.")
        except ValueError as error:
            print(f"Entrada inválida: {error}")
        except EOFError:
            print("\nEntrada finalizada. Saliendo del gestor de triaje.")
            return


if __name__ == "__main__":
    main()
