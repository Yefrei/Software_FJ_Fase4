# Software FJ – Sistema Integral de Gestión

## Descripción
Aplicación de consola desarrollada en Python para gestionar clientes, servicios y reservas sin utilizar bases de datos. La información se conserva en listas durante la ejecución y los eventos/errores se registran en `logs/sistema.log`.

## Requisitos
- Python 3.10 o superior.
- Visual Studio Code (opcional).

## Ejecución
1. Abrir esta carpeta en Visual Studio Code.
2. Abrir la terminal integrada.
3. Ejecutar:

```bash
python main.py
```

En Windows también puede ser necesario:

```bash
py main.py
```

## Módulos
- `entidades.py`: clase abstracta Entidad.
- `clientes.py`: clase Cliente y validaciones.
- `servicios.py`: clase abstracta Servicio y tres servicios especializados.
- `reservas.py`: creación, confirmación y cancelación de reservas.
- `excepciones.py`: excepciones personalizadas.
- `gestor.py`: listas en memoria y registro de logs.
- `main.py`: demostración de operaciones y pruebas.

## Consideración sobre la sobrecarga
Python no implementa sobrecarga tradicional por firma como otros lenguajes. En este proyecto se demuestra una variante equivalente mediante parámetros opcionales en `calcular_costo`: permite calcular con valores predeterminados o indicar impuesto y descuento.
