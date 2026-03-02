
## Proyecto: ADV - Analizador de Depreciacion Vehicular

Aplicación en python con streamlit para analizar el comportamiento del precio de vehiculos usados en funcion de:

- Antiguedad  
- Kilometraje  
- OEM / Fabricante  
- Distribución y dispersión de precios  

## Objetivo
Simular un escenario de análisis de precios y responder preguntas clave de negocio como el impacto en la antiguedad en el valor de reventa, correlacion media entre el kilometraje y el precio.

## Aplicabilidad

Este tipo de analisis es aplicable para:
- Lotes de autos usados    
- Análisis automotriz  
- Evaluación de activos
- Aseguradoras  

## Principales Hallazgos (Patrones Esperados)

- La depreciación no es lineal
- Algunos OEM conservan mejor su valor relativo.
- El aumento en el kilometraje aumenta la caída del precio.
- Los vehículos más antiguos presentan mayor dispersión de precios.

## Dataset
- ds/vehicles_us.csv

## Herramientas Empleadas
- Python
- Pandas – Limpieza y transformación de datos  
- Plotly Express – Visualizaciones interactivas  
- Streamlit – Desarrollo de aplicación web  
  
## Estructura del proyecto

```
Sp07-ADV/
├── app.py                # Aplicación Streamlit
├── ds/
│   └── vehicles_us.csv   # Dataset original
├── notebooks/
│   └── EDA.ipynb         # Análisis exploratorio
├── requirements.txt      # Dependencias
└── README.md             # Documentación
```
## Creditos / Autor

Adrian Gil

Data Scientist | Engineering Background 

- https://github.com/adriangil007

- https://www.linkedin.com/in/adriangilr/
