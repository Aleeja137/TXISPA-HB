global scale, nconf, nchip, max_iter, n_pos, t_ext, tmax_chip, t_delta
global chip_info, chip_pos
chip_info = []
chip_pos  = []

def print_general_params():
    global scale, nconf, nchip, max_iter, n_pos, t_ext, tmax_chip, t_delta
    print("scale is: {}".format(scale))
    print("nconf is: {}".format(nconf))
    print("nchip is: {}".format(nchip))
    print("t_ext is: {}".format(t_ext))
    print("tmax_chip is: {}".format(tmax_chip))
    print("t_delta is: {}".format(t_delta))
    print("max_iter is: {}".format(max_iter))
    print("n_pos is: {}".format(n_pos))

def read_params(filepath):
    global scale, nconf, nchip, max_iter, n_pos, t_ext, tmax_chip, t_delta
    global chip_info, chip_pos
    file = open(filepath,'r')
    params = file.readline().split()
    scale    = int(params[0])
    nconf    = int(params[1])
    nchip    = int(params[2])
    max_iter = int(params[6])
    n_pos    = int(params[7])
    t_ext     = float(params[3])
    tmax_chip = float(params[4])
    t_delta   = float(params[5])
    
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
    
filepath = 'input2'
read_params(filepath)
print_general_params()
print(chip_info)
print(chip_pos)
write_card_file('test')


