"""
Inferência do YOLOv4-tiny (Darknet) com OpenCV DNN - não precisa compilar o Darknet.

Uso:
    python inferencia_yolo_opencv.py --cfg ../darknet/yolov4-tiny-custom.cfg \
        --pesos yolov4-tiny-custom_best.weights --imagem foto.jpg
"""
import argparse
import cv2
import numpy as np

CLASSES = ["Bebendo", "Comendo", "Deitado", "Em pe", "Escondido", "Outro", "Pastando"]


def carregar(cfg, pesos, tamanho=416):
    rede = cv2.dnn.readNetFromDarknet(cfg, pesos)
    modelo = cv2.dnn_DetectionModel(rede)
    modelo.setInputParams(size=(tamanho, tamanho), scale=1 / 255.0, swapRB=True)
    return modelo


def detectar(modelo, img_bgr, conf=0.25, nms=0.45):
    ids, scores, caixas = modelo.detect(img_bgr, confThreshold=conf, nmsThreshold=nms)
    resultados = []
    for c, s, (x, y, w, h) in zip(np.array(ids).flatten(), np.array(scores).flatten(), caixas):
        resultados.append((CLASSES[int(c)], float(s), [float(x), float(y), float(x + w), float(y + h)]))
    return resultados


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cfg", default="../darknet/yolov4-tiny-custom.cfg")
    ap.add_argument("--pesos", default="yolov4-tiny-custom_best.weights")
    ap.add_argument("--imagem", required=True)
    ap.add_argument("--saida", default="resultado_yolo.jpg")
    ap.add_argument("--conf", type=float, default=0.25)
    a = ap.parse_args()

    modelo = carregar(a.cfg, a.pesos)
    img = cv2.imread(a.imagem)
    for nome, score, (x1, y1, x2, y2) in detectar(modelo, img, a.conf):
        print(f"{nome:10s} {score:.2f}  [{x1:.0f}, {y1:.0f}, {x2:.0f}, {y2:.0f}]")
        cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), (255, 140, 0), 2)
        cv2.putText(img, f"{nome} {score:.2f}", (int(x1), int(y1) - 4),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 140, 0), 1)
    cv2.imwrite(a.saida, img)
    print("Imagem salva em", a.saida)


if __name__ == "__main__":
    main()
