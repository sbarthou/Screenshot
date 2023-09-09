import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


original_image = mpimg.imread('screenshots/imagen13.png')
image = np.dot(original_image[..., :3], [0.2989, 0.5870, 0.1140])


# valor más repetido
def mas_repetido(image, value=None, delta=None):   # value: 'min' | 'max'
    minimo = image.min()
    maximo = image.max()
    
    if value == None:
        valores, conteos = np.unique(image, return_counts=True)
        rep = valores[np.argmax(conteos)]
        return rep
    elif value == 'min':   # min: mas oscuros
        rango_min = minimo + delta
        rango = image[(image >= minimo) & (image <= rango_min)]
        valores, conteos = np.unique(rango, return_counts=True)
        rep = valores[np.argmax(conteos)]
        return rep
    elif value == 'max':   # min: mas claros
        rango_max = maximo - delta
        rango = image[(image <= maximo) & (image >= rango_max)]
        valores, conteos = np.unique(rango, return_counts=True)
        rep = valores[np.argmax(conteos)]
        return rep

    
# Detectar si es similar a rep
def rep_to_color(valor, rep, delta):
    if abs(valor - rep) <= delta: return True
    else: return False

    
# dividir matriz en sub matrices
def dividir(matrix, n):
    sub_matrices = []
    
    for i in range(0, matrix.shape[0], n):
        for j in range(0, matrix.shape[1], n):
            submatriz = matrix[i:i+n, j:j+n]
            sub_matrices.append(submatriz)
    return sub_matrices


def convert(image, delta1, delta2):
    rep = mas_repetido(image, 'min', delta1)
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            if rep_to_color(image[i, j], rep, delta2):
                image[i, j] = 0

    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            if image[i, j] != 0:
                image[i, j] = 1
                
    if np.all(image == 0):
        image = np.ones(image.shape)
        
    return image


dim = 300
sub_images = dividir(image, dim)

images = []
for i in range(len(sub_images)):
    imagen = convert(sub_images[i], 0.05, 0.3)
    images.append(imagen)
    

n_row = int(np.ceil(image.shape[0]/dim))
n_col = int(np.ceil(image.shape[1]/dim))

stacked_rows = []
m = 1
for i in range(n_row):
    stack_row = np.hstack(images[(n_col*i):n_col*m])
    stacked_rows.append(stack_row)
    m += 1

stacked = np.vstack(stacked_rows)

plt.imshow(stacked, cmap='gray', vmin=0, vmax=1)
plt.axis('off')
plt.tight_layout()
plt.show()