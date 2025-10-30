from sklearn.cluster import KMeans
import cv2
import numpy as np
import sys

def cor_dominante(img, k=3):
    data = img.reshape(-1, 3)
    kmeans = KMeans(n_clusters=k, random_state=42).fit(data)
    centers = kmeans.cluster_centers_.astype(int)
    labels, counts = np.unique(kmeans.labels_, return_counts=True)
    dominant = centers[counts.argmax()]
    return tuple(int(c) for c in dominant)

path = sys.argv[1]
img = cv2.imread(path)
if img is None:
    print(f"Erro: não foi possível carregar a imagem em {path}")
    sys.exit(1)
dom = cor_dominante(img, k=4)
print('Cor dominante (BGR):', dom, 'RGB:', (dom[2], dom[1], dom[0]))