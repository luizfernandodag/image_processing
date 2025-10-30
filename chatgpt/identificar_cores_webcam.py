import cv2
import numpy as np
import webcolors
from scipy.spatial import KDTree

# Tenta obter a lista de nomes de cores CSS3.
# Esta abordagem funciona em versões mais recentes e é robusta.
try:
    css3_names = list(webcolors.names(spec='css3'))
except AttributeError:
    # Se a função 'names' não for encontrada (como em versões muito antigas),
    # usa uma lista de nomes pré-definida.
    css3_names = [
        'black', 'white', 'red', 'green', 'blue', 'yellow', 'cyan', 'magenta',
        'gray', 'silver', 'maroon', 'olive', 'lime', 'navy', 'purple', 'teal'
    ]

# Pré-computar as cores CSS3 em uma estrutura de dados eficiente
try:
    # Mapeia nomes para valores RGB usando as funções da biblioteca
    css3_names_to_rgb = {
        name: webcolors.name_to_rgb(name, spec='css3') for name in css3_names
    }
except ValueError:
    # Se a especificação 'css3' não for encontrada em 'name_to_rgb',
    # tentamos com 'html4' ou lidamos com o caso.
    css3_names_to_rgb = {
        name: webcolors.name_to_rgb(name, spec='html4') for name in css3_names
    }
    
rgb_values = list(css3_names_to_rgb.values())

# Verifica se a lista rgb_values não está vazia antes de criar a KDTree
if rgb_values:
    kdt_db = KDTree(rgb_values)
else:
    print("Erro: A lista de valores RGB está vazia. Não é possível criar a KDTree.")
    # Saia ou trate o erro apropriadamente
    exit()


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


# Lógica para encontrar o índice correto da câmera
cap = None
for i in range(5):
    temp_cap = cv2.VideoCapture(i)
    if temp_cap.isOpened():
        print(f"✅ Câmera encontrada no índice {i}")
        cap = temp_cap
        break
    else:
        print(f"❌ Índice {i} não funciona")

if cap is None or not cap.isOpened():
    print("Erro: Não foi possível acessar a câmera.")
    raise RuntimeError("Não foi possível abrir a câmera. Verifique o índice ou drivers.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Erro: Não foi possível capturar um frame da câmera.")
        break
    
    h, w = frame.shape[:2]
    cx, cy = w // 2, h // 2
    
    b, g, r = frame[cy, cx]
    rgb = (int(r), int(g), int(b))
    
    nome = rgb_to_name(rgb)
    
    # Desenha o quadrado central
    cv2.rectangle(frame, (cx - 30, cy - 30), (cx + 30, cy + 30), (int(b), int(g), int(r)), 2)
    # Desenha o quadrado para a cor e o texto
    cv2.rectangle(frame, (10, 10), (230, 70), (int(b), int(g), int(r)), -1)
    
    cv2.putText(frame, f"{nome} RGB{rgb}", (12, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    
    cv2.imshow("Webcam - pressione q para sair", frame)
    
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
