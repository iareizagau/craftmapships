import pandas as pd

df = pd.read_csv('oficios_geocodificados.csv')

df = df.drop(columns=['Latitud', 'Longitud'], errors='ignore')

df = df.rename(columns={
    'Pueblo exacto': 'Pueblo',
    'latitude': 'latitud',
    'longitude': 'longitud'
})

resumen = (
    df.groupby('Pueblo', as_index=False)
      .agg(
          numero_artesanos=('ID', 'size'),
          latitud=('latitud', 'first'),
          longitud=('longitud', 'first')
      )
)

resumen['ID'] = range(1, len(resumen) + 1)

resumen = resumen[['ID', 'Pueblo', 'latitud', 'longitud', 'numero_artesanos']]

resumen.to_csv('artesanos_por_pueblo.csv', index=False)

print("Archivo generado: artesanos_por_pueblo.csv")

