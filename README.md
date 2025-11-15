# Documentación del Proyecto: Datos para la Acción

Este documento detalla la estructura y el propósito de los datos y scripts utilizados en la aplicación `datosaccion`.

## 1. Datos Utilizados

Los datos de la aplicación se encuentran en el directorio `static/data/datosaccion/`.

### Archivos Principales:

*   **`artesanos_bizkaia.csv`**:
    *   **Descripción**: Archivo CSV original obtenido mediante scraping. Contiene el listado de artesanos de Bizkaia con detalles sobre su oficio, pueblo y otros datos de contacto.
    *   **Uso**: Es la fuente de datos primaria para el resto del procesamiento.

*   **`oficios_geocodificados.csv`**:
    *   **Descripción**: Un archivo CSV intermedio generado por `excel2geojson.py`. Es una copia de `artesanos_bizkaia.csv` pero con dos columnas adicionales: `latitude` y `longitude`.
    *   **Uso**: Sirve como paso previo para la creación del archivo `artesanos_bizkaia.geojson`.

*   **`artesanos_por_pueblo.csv`**:
    *   **Descripción**: Archivo CSV generado por `Limpieza_agrupacion.py`. Agrupa a los artesanos por pueblo y cuenta cuántos hay en cada uno.
    *   **Uso**: Se carga en la vista de Django para pasar al frontend los datos necesarios para visualizar los círculos en el mapa.

*   **`artesanos_bizkaia.geojson`**:
    *   **Descripción**: Archivo GeoJSON generado a partir de `oficios_geocodificados.csv`. Contiene la información de los artesanos en un formato geográfico estándar.
    *   **Uso**: Se carga directamente en el mapa de la página `home.html` para visualizar la ubicación de cada artesano individualmente.

*   **`variacion_pob_2014_2023/`**:
    *   **Descripción**: Este directorio contiene varios archivos GeoJSON que segmentan los municipios según la variación de su población entre 2014 y 2023.
    *   **Uso**: Estos archivos se cargan en el mapa como capas superpuestas para visualizar tendencias demográficas.

## 2. Scripts de Procesamiento

Los scripts utilizados para generar y limpiar los datos se encuentran en `scripts/datosaccion/`.

### Archivos de Script:

*   **`scraping_artesanos.py`**:
    *   **Descripción**: Script de Python que realiza web scraping para extraer la información de los artesanos y la guarda en `artesanos_bizkaia.csv`.
    *   **Uso**: Es el primer paso para obtener los datos crudos.

*   **`excel2geojson.py`**:
    *   **Descripción**: Script de Python que realiza dos funciones clave:
        1.  **Geocodificación (`get_lat_lng`)**: Lee `artesanos_bizkaia.csv`, utiliza `geopy` para obtener las coordenadas (latitud y longitud) de cada pueblo y guarda el resultado en `oficios_geocodificados.csv`.
        2.  **Generación de GeoJSON (`generate_geojson`)**: Lee `oficios_geocodificados.csv` y lo convierte al formato GeoJSON (`artesanos_bizkaia.geojson`).
    *   **Uso**: Procesa los datos iniciales para prepararlos para su visualización en el mapa.

*   **`Limpieza_agrupacion.py`**:
    *   **Descripción**: Script de Python que lee el archivo `oficios_geocodificados.csv`, agrupa los artesanos por pueblo, cuenta el número de artesanos en cada uno y genera el archivo `artesanos_por_pueblo.csv`.
    *   **Uso**: Prepara los datos agregados necesarios para la visualización de los círculos en el mapa.
