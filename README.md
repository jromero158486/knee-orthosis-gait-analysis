# Análisis de Marcha con Órtesis usando Landmarks y Simulación CAD

Este repositorio contiene el análisis cuantitativo de la marcha con y sin órtesis mediante visión por computadora (MediaPipe) y el análisis estructural del diseño de una órtesis de rodilla modelada en Fusion 360.

## Descripción del Análisis de Marcha

Se procesaron videos de sujetos caminando con y sin órtesis para extraer métricas biomecánicas usando **MediaPipe Pose**.

### Métricas extraídas:
- **Ángulo de rodilla izquierda y derecha** (flexión/extensión)
- **Desviación de la línea media corporal** (alineación postural)
- [En desarrollo: Ancho de paso y cadencia]

### 🛠 Herramientas:
- Python + OpenCV + MediaPipe
- Matplotlib y SciPy para visualizaciones y análisis estadístico

---

## 🧪 Resultados

Se generaron visualizaciones automáticas:
- Diagramas de caja (boxplots) para comparar condiciones
- Series temporales
- Estadísticas de media y desviación estándar
- Pruebas t pareadas para análisis de significancia

Todos los resultados están en `data/outputs/`.
---

## 🧱 Análisis Estructural de la Órtesis

Se utilizó **Autodesk Fusion 360** para:
- Modelar la órtesis en PLA
- Asignar restricciones y cargas realistas (peso parcial, contacto corporal)
- Simular el esfuerzo estático y factor de seguridad

## Instrucciones de uso

1. Instalar dependencias:
```bash
pip install -r requirements.txt

- Colocar tus videos en data/videos/ con los nombres:

sin_ortesis.mp4
con_ortesis.mp4

- Visualizar puntos y ángulos

python src/view_landmarks.py

- Extraer métricas de marcha:

python src/analyze_gait.py

- Analizar y visualizar resultados:

python src/analyze_results.py