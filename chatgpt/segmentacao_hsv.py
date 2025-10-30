import cv2
import numpy as np
import sys

# definindo faixas HSV (valores típicos; ajuste conforme necessidade)
FAIXAS = {
    'vermelho1': ((0, 120, 70), (10, 255, 255)),
    'vermelho2': ((170,120,70), (180,255,255)),
    'verde': ((36, 50, 70), (89, 255, 255)),
    'azul': ((90, 50, 70), (130, 255, 255)),
    'amarelo': ((15, 100, 100), (35, 255, 255)),
}

if len(sys.argv) < 2:
    print("Uso: python identificar_cores_imagem.py <caminho_para_a_imagem>")
    sys.exit(1)
        
path = sys.argv[1]
img = cv2.imread(path)
if img is None:
    print(f"Erro: não foi possível carregar a imagem em {path}")
    sys.exit(1)
    
hdv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
mask_total = np.zeros(img.shape[:2], dtype=np.uint8)

for nome, (lower, upper) in FAIXAS.items(): 
    low = np.array(lower, dtype = np.uint8)
    up = np.array(upper, dtype = np.uint8)
    mask = cv2.inRange(hdv, low, up)
    if nome.startswith('vermelho'):
        mask_total = cv2.bitwise_or(mask, mask_total)
    else:
        mask_total = cv2.bitwise_or(mask, mask_total)
        
res = cv2.bitwise_and(img, img, mask=mask_total)


res = cv2.bitwise_and(img, img, mask=mask_total)
cv2.imshow('Original', img)
cv2.imshow('Mascara combinada', mask_total)
cv2.imshow('Resultado', res)
cv2.waitKey(0)
cv2.destroyAllWindows()