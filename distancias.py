import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import cv2

def medir_disparidad_anaglifo(anaglyph_path):
    """
    Permite medir distancias en píxeles entre versiones roja y cian
    de objetos en una imagen anaglifo usando clics del mouse.
    """
    # Cargar imagen
    img = cv2.imread(anaglyph_path)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    objetos = ['A (Cercano)', 'B (Medio)', 'C (Fondo)']
    resultados = {}

    for obj in objetos:
        print(f"\n{'='*50}")
        print(f"OBJETO {obj}")
        print(f"{'='*50}")

        fig, ax = plt.subplots(figsize=(14, 8))
        ax.imshow(img_rgb)
        ax.set_title(f"Objeto {obj}\nClic 1: punto en capa ROJA | Clic 2: mismo punto en capa CIAN", fontsize=12)
        ax.axis('on')

        # Cuadrícula para facilitar lectura
        ax.grid(True, color='white', alpha=0.3, linewidth=0.5)

        print(f"Da clic en el punto ROJO del objeto {obj}")
        print(f"Luego da clic en el mismo punto en la capa CIAN")

        # Capturar 2 puntos por objeto
        puntos = plt.ginput(2, timeout=30, show_clicks=True)
        plt.close()

        if len(puntos) == 2:
            x1, y1 = puntos[0]
            x2, y2 = puntos[1]

            # Calcular distancia euclidiana
            distancia = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
            disparidad_x = abs(x2 - x1)  # La más relevante (eje horizontal)
            disparidad_y = abs(y2 - y1)

            resultados[obj] = {
                'rojo': (round(x1, 1), round(y1, 1)),
                'cian': (round(x2, 1), round(y2, 1)),
                'disparidad_x': round(disparidad_x, 2),
                'disparidad_y': round(disparidad_y, 2),
                'distancia_euclidiana': round(distancia, 2)
            }

            print(f"\n Resultado Objeto {obj}:")
            print(f"   Punto Rojo  → x1={x1:.1f}, y1={y1:.1f}")
            print(f"   Punto Cian  → x2={x2:.1f}, y2={y2:.1f}")
            print(f"   Disparidad horizontal (Δx): {disparidad_x:.2f} px")
            print(f"   Disparidad vertical   (Δy): {disparidad_y:.2f} px")
            print(f"   Distancia euclidiana:       {distancia:.2f} px")
        else:
            print(f"⚠️  No se capturaron suficientes puntos para Objeto {obj}")

    # Resumen final con visualización
    print(f"\n{'='*50}")
    print("RESUMEN FINAL - DISPARIDADES")
    print(f"{'='*50}")
    
    fig, ax = plt.subplots(figsize=(14, 8))
    ax.imshow(img_rgb)
    
    colores_marcadores = {'A (Cercano)': 'yellow', 'B (Medio)': 'lime', 'C (Fondo)': 'white'}

    for obj, datos in resultados.items():
        print(f"\nObjeto {obj}:")
        print(f"  (x1,y1) Rojo = {datos['rojo']}")
        print(f"  (x2,y2) Cian = {datos['cian']}")
        print(f"  Δx = {datos['disparidad_x']} px")
        print(f"  Δy = {datos['disparidad_y']} px")
        print(f"  Distancia = {datos['distancia_euclidiana']} px")

        # Dibujar puntos y línea en la imagen resumen
        x1, y1 = datos['rojo']
        x2, y2 = datos['cian']
        color = colores_marcadores[obj]

        ax.plot(x1, y1, 'o', color='red', markersize=10)
        ax.plot(x2, y2, 'o', color='cyan', markersize=10)
        ax.plot([x1, x2], [y1, y2], '-', color=color, linewidth=2,
                label=f"Obj {obj}: {datos['distancia_euclidiana']}px")
        ax.annotate(f"{obj}\nΔx={datos['disparidad_x']}px",
                    xy=((x1+x2)/2, (y1+y2)/2),
                    color=color, fontsize=9,
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='black', alpha=0.6))

    ax.set_title("Resumen de disparidades medidas", fontsize=13)
    ax.legend(loc='upper right', facecolor='black', labelcolor='white')
    plt.tight_layout()
    plt.show()

    return resultados


resultados = medir_disparidad_anaglifo("anaglyph.png")