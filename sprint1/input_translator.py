import matplotlib.pyplot as plt
import numpy as np

global scale, nconf, nchip, max_iter, n_pos, t_ext, tmax_chip, t_delta, tam
global chip_info, chip_pos
global filepath
chip_info = []
chip_pos  = []

def print_general_params():
    global scale, nconf, nchip, max_iter, n_pos, t_ext, tmax_chip, t_delta, tam
    print("scale is: {}".format(scale))
    print("nconf is: {}".format(nconf))
    print("nchip is: {}".format(nchip))
    print("t_ext is: {}".format(t_ext))
    print("tmax_chip is: {}".format(tmax_chip))
    print("t_delta is: {}".format(t_delta))
    print("max_iter is: {}".format(max_iter))
    print("n_pos is: {}".format(n_pos))
    print("tam is: {}".format(tam))

def read_params(filepath):
    global scale, nconf, nchip, max_iter, n_pos, t_ext, tmax_chip, t_delta, tam
    global chip_info, chip_pos
    file = open(filepath,'r')
    params = file.readline().split()
    scale    = int(params[0])
    nchip    = int(params[1])
    max_iter = int(params[5])
    n_pos    = int(params[6])
    nconf    = 1
    t_ext     = float(params[2])
    tmax_chip = float(params[3])
    t_delta   = float(params[4])
    tam = (100*scale)//n_pos
    
    file.readline()
    for i in range(nchip):
        chip_info_line = file.readline().split()
        h = int(chip_info_line[0])
        w = int(chip_info_line[1])
        tchip = float(chip_info_line[2])
        chip_info.append((h,w,tchip))
        
    file.readline()
    for _ in range(nconf):
        chip_pos.append(list())
        for __ in range(nchip):
            chip_position = file.readline().split()
            x = int(chip_position[0])
            y = int(chip_position[1])
            chip_pos[len(chip_pos)-1].append((x,y))
        file.readline()
        
def interactive_params():
    global scale, nconf, nchip, max_iter, n_pos, t_ext, tmax_chip, t_delta, tam
    global chip_info, chip_pos

    scale_tmp = input("scale: ")
    while not scale_tmp.isdigit() or int(scale_tmp)<1 or int(scale_tmp)>12:
        print("Not a integer between 1 and 12")
        scale_tmp = input("scale: ")
    scale = int(scale_tmp)
    
    nconf = 1
    
    # Por ahora un límite de 10 chips
    nchip_tmp = input("nchip: ")
    while not nchip_tmp.isdigit() or int(nchip_tmp)<1 or int(nchip_tmp)>10:
        print("Not a integer between 1 and 10")
        nchip_tmp = input("nchip: ")
    nchip = int(nchip_tmp)
    
    # Por ahora un límite de 1000 iteraciones para convergencia de fitness
    max_iter_tmp = input("max_iter: ")
    while not max_iter_tmp.isdigit() or int(max_iter_tmp)<1 or int(max_iter_tmp)>1000:
        print("Not a integer between 1 and 1000")
        max_iter_tmp = input("max_iter: ")
    max_iter = int(max_iter_tmp)
    
    n_pos_tmp = input("n_pos (divisor of {}): ".format(scale*100))
    while not n_pos_tmp.isdigit() or int(n_pos_tmp)<1 or ((scale*100)%int(n_pos_tmp) != 0):
        print("Must be positive integer divisor of {}".format(scale*100))
        n_pos_tmp = input("n_pos: ")
    n_pos = int(n_pos_tmp)
    
    tam = (scale*100)//n_pos
    
    # Por ahora un límite de 60 como temperatura inicial de la placa
    t_ext_tmp = input("t_ext: ")
    t_ext_tmp_check = t_ext_tmp.replace(".","")
    while not t_ext_tmp_check.isnumeric() or not ( 1 <= float(t_ext_tmp) <= 60.00):
        print("Not a float between 1 and 60")
        t_ext_tmp = input("t_ext: ")
        t_ext_tmp_check = t_ext_tmp.replace(".","")
    t_ext = float(t_ext_tmp)
    
    # Por ahora un límite de 200 como temperatura máxima de los chips
    tmax_chip_tmp = input("tmax_chip: ")
    tmax_chip_tmp_check = tmax_chip_tmp.replace(".","")
    while not tmax_chip_tmp_check.isnumeric() or not ( 1 <= float(tmax_chip_tmp) <= 200.00):
        print("Not a float between 1 and 200")
        tmax_chip_tmp = input("tmax_chip: ")
        tmax_chip_tmp_check = tmax_chip_tmp.replace(".","")
    tmax_chip = float(tmax_chip_tmp)
    
    # Por ahora un límite de 0.001 a 0.1 como t_delta
    t_delta_tmp = input("t_delta: ")
    t_delta_tmp_check = t_delta_tmp.replace(".","")
    while not t_delta_tmp_check.isnumeric() or not ( 0.001 <= float(t_delta_tmp) <= 0.1):
        print("Not a float between 0.001 and 0.1")
        t_delta_tmp = input("t_delta: ")
        t_delta_tmp_check = t_delta_tmp.replace(".","")
    t_delta = float(t_delta_tmp)
    
    for i in range(nchip):
        print("Enter info about chip {}".format(i))
        line = input("h w t_chip: ").split()
        h = line[0]
        w = line[1]
        t_chip = line[2]
        while not chip_correct(h,w,t_chip):
            print("Not correct values, h must be between 1 and {}; w must be bewteen 1 and {}, t_chip must be between 1 and {}".format(n_pos,2*n_pos,tmax_chip))
            line = input("h w t_chip: ").split()
            h = line[0]
            w = line[1]
            t_chip = line[2]
        chip_info.append((h,w,t_chip))
        
    for i in range(nconf):
        print("Enter info about conf {}".format(i))
        line = input("x y: ").split()
        x = line[0]
        y = line[1]
        while not position_correct(x,y):
            print("Not correct values, x must be between 1 and {}; y must be bewteen 1 and {}".format(n_pos,2*n_pos,))
            line = input("x y: ").split()
            x = line[0]
            y = line[1]
        chip_pos.append((h,w,t_chip))
            
        # Meter info del chip en la lista
    
def chip_correct(h,w,t_chip):
    global n_pos,tmax_chip
    t_chip_check = t_chip.replace(".","")
    return h.isdigit() or w.isdigit() or (1<=int(h)<=n_pos) or (1<=int(w)<=2*n_pos) or t_chip_check.isnumeric() or (1 <= float(t_chip) <= tmax_chip)
    
#//scale, nconf, nchip, t_ext,tmax_chip, t_delta, max_iter
def write_card_file(filepath):
    global scale, nconf, nchip, max_iter, n_pos, t_ext, tmax_chip, t_delta
    global chip_info, chip_pos
    
    file = open(filepath,'w')
    file.write("{} {} {} {} {} {} {}\n\n".format(scale,nconf,nchip,t_ext,tmax_chip,t_delta,max_iter))
    
    tam = (100*scale)//n_pos
    
    for (h,w,tchip) in chip_info:
        file.write("{} {} {}\n".format(h*tam,w*tam,tchip))
    
    file.write("\n")
    
    for configuration in chip_pos:
        for (x,y) in configuration:
            file.write("{} {}\n".format(x*tam,y*tam))
        file.write("\n")
    
def visualizar_placa(conf_ind : int):
    global scale, nconf, nchip, max_iter, n_pos, t_ext, tmax_chip, t_delta, tam
    global chip_info, chip_pos
    global filepath
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
    for i, (chip, posicion) in enumerate(zip(chip_info, chip_pos[conf_ind])):
        y, x = posicion  # Invertir las coordenadas
        x_real = x * tam  # Usar alto_pos para el eje horizontal
        y_real = y * tam  # Usar ancho_pos para el eje vertical
        alto, ancho, temperatura = chip  # Invertir las dimensiones
        alto_real = alto * tam
        ancho_real = ancho * tam

        # Asignar un color diferente a cada chip
        color = plt.cm.get_cmap('tab10')(i)

        # Dibujar el rectángulo con el color y la etiqueta
        rect = plt.Rectangle((x_real, y_real), ancho_real, alto_real, linewidth=1, edgecolor='black', facecolor=color)
        ax.add_patch(rect)

        # Mostrar el nombre del chip y su temperatura dentro del rectángulo
        texto = f'C{i+1} - {temperatura}°C'
        ax.text(x_real + ancho_real / 2, y_real + alto_real / 2, texto, color='black',
                ha='center', va='center', fontsize=8, fontweight='bold')

    # Configurar etiquetas y título
    ax.set_xlabel('Alto de la placa - x')  # Cambiar las etiquetas
    ax.set_ylabel('Ancho de la placa - y')
    ax.set_title("Placa del fichero {}".format(filepath))

    # Mostrar la placa
    plt.show()

def valid_solution(solution : list, chip_info : list, n_pos : int, scale : int, tam : int):
    n_filas = n_pos*2
    n_columnas = n_pos
    n_chips = len(solution)

    # Verificar que ningún chip se salga de la placa
    for i in range(n_chips):
        x, y = solution[i]
        ancho, alto, _ = chip_info[i]

        if x < 0 or x + ancho > n_filas or y < 0 or y + alto > n_columnas:
            return False  # El chip se sale de la placa

    # Verificar que ningún chip solape con otro chip
    for i in range(n_chips - 1):
        x1, y1 = solution[i]
        ancho1, alto1, _= chip_info[i]

        for j in range(i + 1, n_chips):
            x2, y2 = solution[j]
            ancho2, alto2, _ = chip_info[j]

            if (x1 < x2 + ancho2 and x1 + ancho1 > x2 and
                y1 < y2 + alto2 and y1 + alto1 > y2):
                return False  # Los chips se solapan

    return True  # Todas las condiciones son válidas

filepath = 'data/input3'
read_params(filepath)
print_general_params()
print(chip_info)
print(chip_pos)
# write_card_file('data/card_test')
visualizar_placa(0)
print(valid_solution(chip_pos[0],chip_info,n_pos,scale,tam))

# interactive_params()
# print_general_params()


# Cosas pendientes:
# Meter la configuración de los chips de manera interactiva, aunque solo haya una configuración, se necesitan dos bulces, uno para conf, otro para chips
# Crear una función de vecindad
# Implementar random search, implementar local search
# Plantearle la idea de multiobjetivo con wirelength
# Escribir el documento sobre todo esto para el viernes