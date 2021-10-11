import re
import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from pathlib import Path
from fast_histogram import histogram2d

vertices = {'C':np.array((0,1)), 'G':np.array((1,1)), 'A':np.array((1,0)), 'T':np.array((0,0))}
anot = {0:('right', 'top'), 1:('left', 'bottom')}
verticesF = {'C':np.array((0,0)), 'G':np.array((499,0)), 'A':np.array((499,499)), 'T':np.array((0,499))}
anotF = {499:('left', 'top'), 0:('right', 'bottom')}
start = np.random.random(size=2)

def fill_coordinates(seq):
    coords = [start]
    for i, letra in enumerate(seq):
        if not i%100000:
            print(f"Iteración número {i} de {len(seq)} -- {round(100*i/len(seq),2)}%", end='\r')
        coords.append(0.5 * (vertices[letra] + coords[-1]))
    print(f"Iteración número {i} de {len(seq)} -- {round(100*i/len(seq),2)}%")
    return zip(*coords)

def save_figure(x, y, path, titulo):
    Path(path).mkdir(parents=True, exist_ok=True)
    plt.figure(figsize=(15,15), facecolor = 'black')
    plt.scatter(x,y, s=1000/len(x), c="0.15")
    plt.xticks([])
    plt.yticks([])
    plt.title(titulo,fontsize=40, color='grey', )
    for key, vals in vertices.items():
        plt.annotate(key, xy=vals, xytext=vals, ha=anot[vals[0]][0], va=anot[vals[1]][1], fontsize=20, color="darkblue")
    plt.savefig(path+'fractal.png')
    #with open(path+'coords.json', 'w') as f:
    #    json.dump({'x':x, 'y':y}, f)
    
def save_figureF(x, y, path, titulo):
    Path(path).mkdir(parents=True, exist_ok=True)
    bounds = [[min(y), max(y)],[min(x), max(x)]]
    h = histogram2d(y, x, range=bounds, bins=500)[::-1,:]
    plt.figure(figsize=(15,15), facecolor = 'black')
    plt.imshow(h, norm=colors.LogNorm(vmin=1, vmax=h.max()), cmap="Greys")
    plt.xticks([])
    plt.yticks([])
    plt.title("De la cosa",fontsize=40, color='grey', )
    plt.axis('off')
    plt.title(titulo,fontsize=40, color='grey', )
    for key, vals in verticesF.items():
        plt.annotate(key, xy=vals, xytext=vals, ha=anotF[vals[0]][0], va=anotF[vals[1]][1], fontsize=20, color="white")
    plt.savefig(path+'fractal.png')
    #with open(path+'coords.json', 'w') as f:
    #    json.dump({'x':x, 'y':y}, f)
    
def reader(path, filas):
    with open(path) as f:
        if filas:
            lineas = [next(f).upper() for _ in range(filas)]
        else:
            lineas = [x.upper() for x in f.readlines()]
    limpias = [re.sub(r'[^CGAT]','',x) for x in lineas if re.fullmatch(r'[A-Z]*',x.strip('\n'))]
    return ''.join(limpias)

if __name__ == "__main__":
    archivo = input('Ruta del archivo:\n')
    titulo = input('Introduzca el nombre:\n')
    filas = int(input('Número máximo de renglones:\n'))
    fast = input('Modo [veloz] o [lento]?\n').lower()
    while fast not in ['veloz','lento']:
        fast = input('Modo [veloz] o [lento]?\n').lower()
    if not titulo:
        titulo = archivo.split('.')[0]
    seq = reader(archivo, filas)
    x, y = fill_coordinates(seq)
    if fast == 'veloz':
        save_figureF(x,y, f'output/{"_".join(titulo.split())}/', titulo)
    else:
        save_figure(x,y, f'output/{"_".join(titulo.split())}/', titulo)
    print('End of code')