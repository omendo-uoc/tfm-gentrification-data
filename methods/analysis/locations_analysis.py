import pandas as pd


file_path = 'data/processed/locations_processed.csv'
data = pd.read_csv(file_path)

activity_mapping = {
    'Optica Ortopedia Audicion': ['optica ortopedia audicion'],
    'Deporte y Ocio': [
        'actividades deporte ocio', 'articulos deportivos', 'sala de fiestas',
        'salon recreativo', 'parques infantiles', 'parque deporte urbano',
        'puerto deportivo', 'playa mascotas'
    ],
    'Cafetería y Restauración': [
        'cafeteria', 'tasca', 'restaurante', 'bar cafeteria', 'bar', 'bar cafeteria zumeria',
        'bar cafeteria hamburgueseria', 'restaurante pizzeria', 'bar cerveceria',
        'bar cibercafe', 'bar cafeteria arepera', 'guachinche', 'bar terraza', 'restaurante buffet',
        'bar taberna', 'bar churreria chocolateria', 'bar kiosco', 'café', 'bar piscina',
        'restaurante bodega', 'bar pasteleria', 'bar cafeteriapasteleria', 'barchurreria',
        'barclub', 'restaurante meson', 'bar cafeteria creperia', 'bar croissanteria',
        'alimentacion productos especializados herbolario', 'bar cafeteriachurreria',
        'autobar', 'bardulceria'
    ],
    'Comercio General': [
        'comercio otro tipo', 'bazar electronica', 'bazar multitienda estanco',
        'compraventa productos segunda mano', 'comercio almacen deposito',
        'compraventa oro'
    ],
    'Tecnología y Electrónica': [
        'informatica telecomunicaciones', 'electricidad electronica', 'telefonia',
        'centro comercial hogar informatica telecomunicaciones', 'industria editorial periodicos'
    ],
    'Moda y Complementos': [
        'moda complementos', 'zapateria calzado', 'zapateria calzado taller',
        'perfumeria estetica complementos', 'hogar textil', 'moda complementos infantil',
        'moda complementos taller', 'bisuteria complementos', 'joyeria relojeria',
        'joyeria relojeria taller'
    ],
    'Hogar y Decoración': [
        'hogar muebles electrodomesticos decoracion', 'ferreteria', 'centro comercial hogar construccion',
        'centro comercial hogar moda'
    ],
    'Agencias y Alojamientos': [
        'agencia de viajes', 'vivienda vacacional', 'alojamiento extrahotelero',
        'alojamiento hotelero', 'informador turistico', 'oficina de turismo'
    ],
    'Entretenimiento y Cultura': [
        'discoteca club', 'jugueteria', 'estudio fotografia', 'discoteca',
        'videoclub', 'libreria papeleria discoteca', 'articulos musicales', 'locutorio'
    ],
    'Otros': [
        'mascotas', 'concesionario exposicion automocion', 'residencia mascotas',
        'parque mascotas', 'centro comercial', 'mercados y ferias', 'representacion distribucion comercial',
        'cerrado sin actividad', 'tabaqueria licoreria', 'parafarmacia productos naturales', 'kiosco prensa'
    ]
}


reverse_mapping = {activity: category for category, activities in activity_mapping.items() for activity in activities}
data['nueva_actividad'] = data['actividad_tipo'].map(reverse_mapping)

output_file_path = 'data/final/locations_categorized.csv'
data.to_csv(output_file_path, index=False)
