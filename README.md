# Blockchain Demo - Aplicación de Demostración

Una aplicación de demostración de blockchain desarrollada en Python con Flet framework, que implementa una cadena de bloques funcional con interfaz gráfica multiplataforma.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Flet](https://img.shields.io/badge/Flet-Latest-cyan.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## 📋 Descripción

Este proyecto es un prototipo educativo que demuestra los conceptos fundamentales de blockchain:

- **Criptografía SHA-256**: Cada bloque se asegura con hash criptográfico
- **Inmutabilidad**: Los datos no pueden modificarse sin romper la cadena
- **Validación de integridad**: Verificación completa de la cadena
- **Patrones de diseño**: Implementación de Singleton, Factory Method, Chain of Responsibility y Observer

## ✨ Características

### Funcionalidades Principales

- ✅ **Creación automática de bloque génesis**
- ✅ **Agregar bloques con transacciones**
- ✅ **Validación de integridad de la cadena**
- ✅ **Simulación de ataques** para demostrar inmutabilidad
- ✅ **Exportar/Importar blockchain** en formato JSON
- ✅ **Búsqueda de bloques** por contenido
- ✅ **Estadísticas en tiempo real**
- ✅ **Interfaz gráfica atractiva** con tema personalizado
- ✅ **Vista educativa de agregar bloques** con visualización paso a paso

### Arquitectura

```
blockchain_app/
├── main.py                    # Punto de entrada
├── src/
│   ├── models/               # Modelos de datos
│   │   ├── transaccion.py   # Clase Transaccion
│   │   ├── bloque.py        # Clase Bloque (Factory Method)
│   │   └── blockchain.py    # Clase CadenaDeBloques (Singleton)
│   ├── views/               # Vistas de la interfaz
│   │   ├── home_view.py
│   │   ├── agregar_bloque_view.py
│   │   └── visualizar_cadena_view.py
│   ├── controllers/         # Lógica de negocio
│   │   └── blockchain_controller.py
│   ├── utils/              # Utilidades
│   │   ├── hash_utils.py   # Funciones SHA-256
│   │   └── validators.py   # Validadores (Chain of Responsibility)
│   └── components/         # Componentes UI reutilizables
│       ├── bloque_card.py
│       ├── agregar_bloque_educativo.py  # Vista educativa de agregar bloques
│       └── navigation.py
└── README.md
```

## 🚀 Instalación

### Requisitos Previos

- Python 3.10 o superior
- pip (gestor de paquetes de Python)

### Pasos de Instalación

1. **Clonar o descargar el proyecto**

```bash
cd blockchain_app
```

2. **Instalar dependencias**

```bash
pip install flet
```

3. **Ejecutar la aplicación**

```bash
python main.py
```

## 📖 Uso

### Pantalla Principal (Home)

- Visualiza todos los bloques de la cadena
- Panel de estadísticas con métricas en tiempo real
- Botones para validar cadena y simular ataques
- Indicadores visuales de validez (verde/rojo)

### Agregar Bloque

1. Completa el formulario con:
   - **Emisor**: Nombre o dirección del emisor
   - **Receptor**: Nombre o dirección del receptor
   - **Cantidad**: Monto a transferir (debe ser > 0)
   - **Descripción**: Información adicional (opcional)

2. Haz clic en "Agregar Bloque"
3. El nuevo bloque se agregará a la cadena automáticamente

### Visualizar Blockchain

- **Búsqueda**: Filtra bloques por contenido
- **Exportar**: Guarda la blockchain en archivo JSON
- **Importar**: Carga una blockchain desde archivo JSON
- **Actualizar**: Refresca la vista

### Simular Ataque

1. En la vista principal, haz clic en "Simular Ataque"
2. Ingresa el índice del bloque a modificar
3. Los datos se modificarán sin recalcular el hash
4. La validación detectará la manipulación

### Agregar Bloque (Educativo)

**Nueva funcionalidad educativa** que combina agregar bloques con visualización paso a paso:

1. Navega a "Agregar (Edu)" en el menú lateral
2. Completa el formulario con los datos de la transacción:
   - **Emisor**: Nombre del emisor
   - **Receptor**: Nombre del receptor
   - **Cantidad**: Monto (número)
   - **Descripción**: Información adicional (opcional)
3. Observa cómo se actualiza en tiempo real:
   - 📝 **Paso 1**: Datos de la transacción en formato JSON
   - ⚙️ **Paso 2**: Metadatos del bloque (índice, timestamp)
   - 🔗 **Paso 3**: Hash del bloque anterior (conexión con la cadena)
   - 🔐 **Paso 4**: Cálculo del hash SHA-256 del nuevo bloque
4. Haz clic en "Agregar Bloque a la Cadena"
5. Observa el mensaje de confirmación con detalles del bloque agregado

**Beneficio educativo**: Esta vista permite comprender visualmente cómo se construye un bloque desde cero, cómo se conecta con el bloque anterior mediante el hash, y cómo se calcula el hash final del bloque.

## 🎨 Patrones de Diseño

### 1. Singleton Pattern

**Ubicación**: `src/models/blockchain.py`

```python
blockchain = CadenaDeBloques.get_instance()
```

Garantiza una única instancia de la blockchain en toda la aplicación.

### 2. Factory Method Pattern

**Ubicación**: `src/models/bloque.py`

```python
bloque = Bloque.crear_bloque(indice, datos, hash_previo)
genesis = Bloque.crear_bloque_genesis()
```

Encapsula la lógica de creación de bloques.

### 3. Chain of Responsibility Pattern

**Ubicación**: `src/utils/validators.py`

```python
validador = ValidadorTransaccion()
validador.establecer_siguiente(ValidadorBloque())
es_valido, mensaje = validador.validar(datos)
```

Validación en cadena de transacciones y bloques.

### 4. Observer Pattern

**Ubicación**: `src/controllers/blockchain_controller.py`

```python
controller.agregar_observador(callback)
controller.notificar_observadores()
```

Las vistas se actualizan automáticamente cuando cambia la blockchain.

## 🔐 Seguridad y Validación

### Hash SHA-256

Cada bloque calcula su hash combinando:
- Índice del bloque
- Timestamp
- Datos almacenados
- Hash del bloque anterior
- Nonce (para proof-of-work)

### Validación de Integridad

La aplicación valida:
1. Hash individual de cada bloque
2. Enlaces correctos entre bloques consecutivos
3. Estructura del bloque génesis
4. Índices consecutivos

## 📊 Estadísticas

La aplicación muestra:

- **Total de bloques**: Número de bloques en la cadena
- **Estado**: Válida/Inválida
- **Tamaño**: Tamaño total en KB
- **Tiempo promedio**: Tiempo promedio entre bloques

## 🎯 Casos de Uso Educativos

### Demostrar Inmutabilidad

1. Agrega varios bloques
2. Usa "Simular Ataque" para modificar un bloque antiguo
3. Valida la cadena para ver cómo se detecta la manipulación

### Exportar/Importar

1. Crea una blockchain con varios bloques
2. Exporta a JSON
3. Reinicia la aplicación
4. Importa el archivo JSON para restaurar la cadena

### Búsqueda de Transacciones

1. Agrega bloques con diferentes emisores/receptores
2. En "Visualizar", busca por nombre de emisor
3. Observa cómo se filtran los bloques

### Aprender a Agregar Bloques

1. Navega a "Agregar (Edu)" en el menú lateral
2. Completa el formulario paso a paso
3. Observa en tiempo real:
   - Cómo se estructuran los datos de la transacción
   - Qué metadatos se agregan al bloque
   - Cómo se obtiene el hash del bloque anterior
   - Cómo se calcula el hash SHA-256 del nuevo bloque
4. Agrega el bloque y verifica en "Inicio" que fue agregado correctamente
5. Experimenta modificando ligeramente los datos y observa cómo cambia el hash completamente

## 🛠️ Tecnologías Utilizadas

- **Python 3.10+**: Lenguaje de programación
- **Flet**: Framework de UI multiplataforma
- **hashlib**: Cálculo de hashes SHA-256
- **json**: Serialización de datos
- **datetime**: Gestión de timestamps
- **logging**: Sistema de logs

## 📝 Código de Calidad

El proyecto sigue:

- ✅ **PEP 8**: Estándar de estilo de Python
- ✅ **Type hints**: Anotaciones de tipo en todas las funciones
- ✅ **Docstrings**: Documentación en formato Google
- ✅ **Separación de responsabilidades**: Arquitectura MVC/MVVM
- ✅ **Código en español**: Variables, funciones y comentarios
- ✅ **Modularidad**: Archivos < 200 líneas

## 🐛 Solución de Problemas

### Error al importar Flet

```bash
pip install --upgrade flet
```

### La aplicación no inicia

Verifica que estés usando Python 3.10 o superior:

```bash
python --version
```

### Error al exportar/importar

Asegúrate de tener permisos de escritura en el directorio seleccionado.

## 🤝 Contribuciones

Este es un proyecto educativo. Siéntete libre de:

- Reportar bugs
- Sugerir mejoras
- Agregar nuevas funcionalidades
- Mejorar la documentación

## 📄 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

## 👨‍💻 Autor

Desarrollado como demostración educativa de blockchain con Python y Flet.

## 🔗 Enlaces Útiles

- [Documentación de Flet](https://flet.dev)
- [Python hashlib](https://docs.python.org/3/library/hashlib.html)
- [Blockchain Basics](https://en.wikipedia.org/wiki/Blockchain)

---

**¡Disfruta explorando el mundo de blockchain!** 🚀🔗
