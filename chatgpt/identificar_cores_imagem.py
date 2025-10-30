import cv2
import numpy as np
import webcolors
from scipy.spatial import KDTree

# Obter a lista de nomes de cores CSS3 de forma compatível
css3_names = list(webcolors.names(spec='css3'))

# Pré-computar as cores CSS3 em uma estrutura de dados eficiente
css3_names_to_rgb = {
    name: webcolors.name_to_rgb(name, spec='css3') for name in css3_names
}
rgb_values = list(css3_names_to_rgb.values())
kdt_db = KDTree(rgb_values)

def rgb_to_name(rgb_tuple):
    """
    Converte um tuplo RGB para o nome da cor CSS3 mais próximo.
    Usa uma KDTree pré-computada para eficiência.
    """
    try:
        # Tenta obter o nome exato usando a função apropriada
        return webcolors.rgb_to_name(rgb_tuple, spec='css3')
    except ValueError:
        # Encontra o nome mais próximo usando a KDTree
        distance, index = kdt_db.query(rgb_tuple)
        return css3_names[index]

# Exemplo de uso
rgb_teste = (190, 53, 25)
nome_da_cor = rgb_to_name(rgb_teste)
print(f"O nome da cor para {rgb_teste} é: {nome_da_cor}")
def on_mouse(event, x,y, flags, param):
    img = param['img']
    b,g,r = img[y,x]
    rgb = (int(b), int(g), int(r))
    # pixel_bgr = np.uint8([[ [b, g, r] ]])
    pixel_bgr = np.array([[ [b, g, r] ]], dtype=np.uint8)


    # hsv = cv2.cvtColor(np.uint8([[ [b,g,r] ]]), cv2.COLOR_BGR2HSV)[0][0]
    pixel_hsv = cv2.cvtColor(pixel_bgr, cv2.COLOR_BGR2HSV)
    hsv = pixel_hsv[0][0]
    name = rgb_to_name(rgb)
    print(f"Pos: ({x},{y})  RGB: {rgb}  HSV: {tuple(int(v) for v in hsv)}  Nome aproximado: {name}")
    
    overlay = img.copy()
    
    cv2.rectangle(overlay, (10, 10), (210, 80), (int(b), int(g), int(r)), -1)
    cv2.putText(overlay, f"{name}", (220,40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2)
    cv2.imshow("Imagem", overlay)
  

    
    


    # hsv = cv2.cvtColor(np.uint8([[b,g,r]]), cv2.COLOR_BGR2HSV)[0][0]
    
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Uso: python identificar_cores_imagem.py <caminho_para_a_imagem>")
        sys.exit(1)
        
    path = sys.argv[1]
    img = cv2.imread(path)
    if img is None:
        print(f"Erro: Não foi possível carregar a imagem em {path}")
        sys.exit(1)
        
        
    cv2.namedWindow("Imagem", cv2.WINDOW_NORMAL)
    cv2.setMouseCallback("Imagem", on_mouse, param={'img': img})
    while True:
        cv2.imshow("Imagem", img)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
    