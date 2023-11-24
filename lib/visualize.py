import matplotlib.pyplot as plt

def visualizar_solucion(instance, solution):
    scale,nconf,nchip,max_iter,n_pos,t_ext,tmax_chip,t_delta,tam,chip_info = instance
    
    # Crear la figura y los ejes
    fig, ax = plt.subplots(figsize=(20, 10))  

    # Dibujar la placa
    for i in range(n_pos*2 + 1):
        y = i * tam
        ax.plot([0, scale * 100], [y, y], color='gray', linestyle='--', linewidth=0.5)

    for i in range(n_pos + 1):
        x = i * tam
        ax.plot([x, x], [0, scale * 200], color='gray', linestyle='--', linewidth=0.5)

    # Dibujar los chips en la placa
    for i in range(nchip):
        # Invertir las coordenadas
        y = solution[i*2] 
        x = solution[i*2+1]
        x_real = x * tam  # Usar alto_pos para el eje horizontal
        y_real = y * tam  # Usar ancho_pos para el eje vertical
        
        # Invertir las dimensiones
        alto = chip_info[i*3]
        ancho = chip_info[i*3+1]
        temperatura = chip_info[i*3+2]
        alto_real = alto * tam
        ancho_real = ancho * tam

        # Asignar un color diferente a cada chip
        color = plt.colormaps.get_cmap('tab10')(i)

        # Dibujar el rectángulo con el color y la etiqueta
        rect = plt.Rectangle((x_real, y_real), ancho_real, alto_real, linewidth=1, edgecolor='black', facecolor=color)
        ax.add_patch(rect)

        # Mostrar el nombre del chip y su temperatura 
        texto = f'C{i+1} - {temperatura}°C'
        ax.text(x_real + ancho_real / 2, y_real + alto_real / 2, texto, color='black',
                ha='center', va='center', fontsize=8, fontweight='bold')

    # Etiquetas y título
    ax.set_xlabel('Alto de la placa - x')  # Cambiar las etiquetas
    ax.set_ylabel('Ancho de la placa - y')
    ax.set_title("Placa TXISPA")

    # Mostrar la placa
    plt.show()

def print_general_params(instance):
    scale,nconf,nchip,max_iter,n_pos,t_ext,tmax_chip,t_delta,tam,chip_info = instance
    
    print("scale is: {}".format(scale))
    print("nconf is: {}".format(nconf))
    print("nchip is: {}".format(nchip))
    print("t_ext is: {}".format(t_ext))
    print("tmax_chip is: {}".format(tmax_chip))
    print("t_delta is: {}".format(t_delta))
    print("max_iter is: {}".format(max_iter))
    print("n_pos is: {}".format(n_pos))
    print("tam is: {}".format(tam))
    print("chip_info is: ",chip_info)