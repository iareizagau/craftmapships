# CraftMapShips

CraftMapShips es una aplicación web desarrollada con Django que visualiza datos de artesanos por localidad. El proyecto utiliza la librería `pandas` para procesar un archivo CSV y mostrar la información en una plantilla HTML.

## Características

- Visualización de datos de artesanos.
- Procesamiento de datos desde un archivo CSV.
- Estructura de proyecto Django escalable.

## Tecnologías Utilizadas

- **Backend:** Python, Django
- **Procesamiento de Datos:** pandas
- **Frontend:** HTML, (potencialmente CSS y JavaScript)
- **Base de Datos:** SQLite (configuración por defecto de Django)

## Estructura del Proyecto

El proyecto sigue una estructura estándar de Django, con una aplicación principal y directorios para plantillas y archivos estáticos.

```
craftmapships/
├── apps/
│   └── datosaccion/      # Aplicación principal para la visualización de datos
│       ├── migrations/
│       ├── templates/
│       │   └── datosaccion/
│       │       └── home.html # Plantilla para la página principal
│       ├── __init__.py
│       ├── admin.py
│       ├── apps.py
│       ├── models.py
│       ├── tests.py
│       ├── urls.py
│       └── views.py
├── craftmapships/        # Directorio de configuración del proyecto
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── static/
│   └── data/
│       └── datosaccion/
│           └── artesanos_por_pueblo.csv # Archivo de datos
├── templates/            # Directorio de plantillas globales
├── .gitignore
├── manage.py
└── README.md
```

## Instalación y Puesta en Marcha

Sigue estos pasos para configurar y ejecutar el proyecto en tu entorno local.

### 1. Clonar el Repositorio

```sh
git clone https://github.com/iareizagau/craftmapships.git
cd craftmapships
```

### 2. Crear y Activar un Entorno Virtual

Es una buena práctica utilizar un entorno virtual para gestionar las dependencias del proyecto.

```sh
# Crear el entorno virtual
python -m venv venv

# Activar en Windows
venv\Scripts\activate

# Activar en macOS/Linux
source venv/bin/activate
```

### 3. Instalar Dependencias

Instala las librerías necesarias. Primero, crea un archivo `requirements.txt` con el siguiente contenido:

```txt
Django
pandas
```

Luego, instala las dependencias:

```sh
pip install -r requirements.txt
```

### 4. Ejecutar las Migraciones

Aunque actualmente no hay modelos personalizados, es una buena práctica ejecutar las migraciones iniciales de Django.

```sh
python manage.py migrate
```

### 5. Iniciar el Servidor de Desarrollo

Ahora puedes iniciar el servidor de desarrollo de Django.

```sh
python manage.py runserver
```

Abre tu navegador y visita [http://127.0.0.1:8000/](http://127.0.0.1:8000/) para ver la aplicación en funcionamiento.

## Uso

La página principal de la aplicación muestra los datos procesados del archivo `artesanos_por_pueblo.csv`. Puedes modificar este archivo o la vista en `apps/datosaccion/views.py` para cambiar la lógica de visualización de datos.
