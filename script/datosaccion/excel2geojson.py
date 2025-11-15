import json
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter


def generate_geojson():
    """
    Genera un archivo GeoJSON a partir de un archivo CSV geocodificado.
    """
    csv_path = r'C:\Users\imanol\projects\imanol\maps\scripts\datosaccion\oficios_geocodificados.csv'
    geojson_path = r'C:\Users\imanol\projects\imanol\maps\static\data\datosaccion\artesanos_bizkaia.geojson'
    
    try:
        df = pd.read_csv(csv_path)
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {csv_path}. Ejecuta get_lat_lng() primero.")
        return

    features = []
    for index, row in df.iterrows():
        # Asegurarse de que la latitud y longitud no son nulas
        if pd.notna(row['latitude']) and pd.notna(row['longitude']):
            try:
                geometry = {
                    "type": "Point",
                    "coordinates": [row['longitude'], row['latitude']]
                }
                
                # Limpiar las propiedades para evitar valores NaN que no son JSON válidos
                properties = {
                    "id": row.get('ID'),
                    "pueblo": row.get('Pueblo exacto'),
                    "oficio": row.get('Tipo de oficio'),
                    "descripcion": row.get('Descripción'),
                    "email": row.get('Email'),
                    "telefono": row.get('Teléfono'),
                    "enlace": row.get('Enlace'),
                    "imagenes": row.get('Enlace imágenes')
                }
                
                cleaned_properties = {k: v if pd.notna(v) else None for k, v in properties.items()}

                features.append({
                    "type": "Feature",
                    "geometry": geometry,
                    "properties": cleaned_properties
                })
            except Exception as e:
                print(f"Error procesando la fila {index}: {e}")
        else:
            print(f"Fila {index} sin coordenadas, saltando.")

    geojson_data = {
        "type": "FeatureCollection",
        "features": features
    }

    with open(geojson_path, 'w', encoding='utf-8') as f:
        json.dump(geojson_data, f, indent=4, ensure_ascii=False)

    print(f"Archivo GeoJSON generado en '{geojson_path}'.")
    return geojson_path


def get_lat_lng():
    file_path = r'C:\Users\imanol\projects\imanol\maps\static\data\datosaccion\artesanos_bizkaia.csv'
    # --------------------------
    # Cargar CSV original
    # --------------------------
    df = pd.read_csv(file_path)

    # Limpieza del nombre del pueblo (por si hay espacios)
    df["Pueblo exacto"] = df["Pueblo exacto"].astype(str).str.strip()

    # --------------------------
    # Configurar geocoder
    # --------------------------
    geolocator = Nominatim(user_agent="mi_app_geocodificacion")
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)   # 1 seg por petición

    def get_lat_lon(place_name):
        try:
            location = geocode(place_name + ", España")
            if location:
                print(f"Coordenadas encontradas para {place_name}: ({location.latitude}, {location.longitude})")
                return location.latitude, location.longitude
            else:
                print(f"No se encontraron coordenadas para {place_name}")
                return None, None
        except Exception as e:
            print(f"Error geocodificando {place_name}: {e}")
            return None, None

    # --------------------------
    # Aplicar geocodificación
    # --------------------------
    df['latitude'] = None
    df['longitude'] = None
    for index, row in df.iterrows():
        pueblo = row.get('Pueblo exacto')
        if pueblo and pd.notna(pueblo) and pueblo.lower() != 'nan':
            lat, lng = get_lat_lon(pueblo)
            df.at[index, 'latitude'] = lat
            df.at[index, 'longitude'] = lng
        else:
            print(f"Fila {index} sin 'Pueblo exacto', saltando.")


    # --------------------------
    # Guardar CSV resultante
    # --------------------------
    output_filename = "oficios_geocodificados.csv"
    df.to_csv(output_filename, index=False)

    print(f"Geocodificación completada y guardada en '{output_filename}'.")


if __name__ == '__main__':
    # Primero, asegúrate de que el archivo con coordenadas exista
    # get_lat_lng() 
    
    # Luego, genera el GeoJSON
    generate_geojson()
