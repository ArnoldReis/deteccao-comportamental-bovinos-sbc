"""
Inferência do NanoDet-Plus (comportamento de gado) usando o modelo ONNX.
Não precisa de PyTorch nem do repositório do NanoDet: só onnxruntime, opencv e numpy.

Uso:
    python inferencia_nanodet_onnx.py --modelo nanodet_comportamento_gado-sim.onnx --imagem foto.jpg
"""
import argparse
import cv2
import numpy as np
import onnxruntime as ort

CLASSES = ["Boi", "Bebendo", "Comendo", "Deitado", "Em pe", "Escondido", "Outro", "Pastando"]
INPUT = 320
STRIDES = [8, 16, 32, 64]
REG_MAX = 7
MEAN = np.array([103.53, 116.28, 123.675], dtype=np.float32)  # BGR
STD = np.array([57.375, 57.12, 58.395], dtype=np.float32)


def preprocessar(img_bgr):
    img = cv2.resize(img_bgr, (INPUT, INPUT)).astype(np.float32)
    img = (img - MEAN) / STD
    return img.transpose(2, 0, 1)[None]


def centros():
    pts = []
    for s in STRIDES:
        n = int(np.ceil(INPUT / s))
        ys, xs = np.meshgrid(np.arange(n), np.arange(n), indexing="ij")
        pts.append(np.stack([xs.ravel() * s, ys.ravel() * s, np.full(n * n, s)], 1))
    return np.concatenate(pts).astype(np.float32)


CENTROS = centros()


def detectar(sessao, img_bgr, conf=0.35, iou=0.6):
    h, w = img_bgr.shape[:2]
    saida = sessao.run(None, {sessao.get_inputs()[0].name: preprocessar(img_bgr)})[0][0]
    nc = len(CLASSES)
    scores = saida[:, :nc]                      # já passam por sigmoid no export
    reg = saida[:, nc:].reshape(-1, 4, REG_MAX + 1)
    reg = np.exp(reg - reg.max(-1, keepdims=True))
    reg = reg / reg.sum(-1, keepdims=True)
    dist = (reg * np.arange(REG_MAX + 1)).sum(-1) * CENTROS[:, 2:3]
    cx, cy = CENTROS[:, 0], CENTROS[:, 1]
    caixas = np.stack([cx - dist[:, 0], cy - dist[:, 1], cx + dist[:, 2], cy + dist[:, 3]], 1)
    caixas = np.clip(caixas, 0, INPUT) * np.array([w / INPUT, h / INPUT] * 2, dtype=np.float32)

    resultados = []
    for c in range(nc):
        sel = scores[:, c] > conf
        if not sel.any():
            continue
        b, s = caixas[sel], scores[sel, c]
        xywh = np.c_[b[:, :2], b[:, 2:] - b[:, :2]]
        idx = cv2.dnn.NMSBoxes(xywh.tolist(), s.tolist(), conf, iou)
        for i in np.array(idx).flatten():
            resultados.append((CLASSES[c], float(s[i]), b[i].tolist()))
    return resultados


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--modelo", default="nanodet_comportamento_gado-sim.onnx")
    ap.add_argument("--imagem", required=True)
    ap.add_argument("--saida", default="resultado_nanodet.jpg")
    ap.add_argument("--conf", type=float, default=0.35)
    a = ap.parse_args()

    sessao = ort.InferenceSession(a.modelo, providers=["CPUExecutionProvider"])
    img = cv2.imread(a.imagem)
    for nome, score, (x1, y1, x2, y2) in detectar(sessao, img, a.conf):
        print(f"{nome:10s} {score:.2f}  [{x1:.0f}, {y1:.0f}, {x2:.0f}, {y2:.0f}]")
        cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), (0, 200, 0), 2)
        cv2.putText(img, f"{nome} {score:.2f}", (int(x1), int(y1) - 4),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 200, 0), 1)
    cv2.imwrite(a.saida, img)
    print("Imagem salva em", a.saida)


if __name__ == "__main__":
    main()
