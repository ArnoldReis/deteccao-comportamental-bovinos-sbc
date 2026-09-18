"""
Avaliação COCO padronizada (mAP@.50:.95, AP50, AP75 e AP50 por classe)
para os modelos NanoDet-Plus (ONNX) e YOLO (Darknet via OpenCV).

Foi com este script que os números de `resultados/metricas_coco.json` foram gerados,
usando o mesmo avaliador (pycocotools) para todos os modelos.

Exemplos:
    python avaliar_coco.py --dataset caminho/gado/valid --tipo nanodet \
        --pesos nanodet_comportamento_gado-sim.onnx
    python avaliar_coco.py --dataset caminho/gado/valid --tipo yolo \
        --cfg ../darknet/yolov4-tiny-custom.cfg --pesos yolov4-tiny-custom_best.weights

O dataset deve estar no formato COCO exportado pelo Roboflow
(pasta com as imagens e o arquivo _annotations.coco.json).
"""
import argparse
import contextlib
import io
import os

import cv2
from pycocotools.coco import COCO
from pycocotools.cocoeval import COCOeval


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset", required=True)
    ap.add_argument("--tipo", choices=["nanodet", "yolo"], required=True)
    ap.add_argument("--pesos", required=True)
    ap.add_argument("--cfg", help="arquivo .cfg (apenas para YOLO)")
    a = ap.parse_args()

    with contextlib.redirect_stdout(io.StringIO()):
        gt = COCO(os.path.join(a.dataset, "_annotations.coco.json"))
    nome_para_id = {c["name"]: c["id"] for c in gt.dataset["categories"]}

    if a.tipo == "nanodet":
        import onnxruntime as ort
        import inferencia_nanodet_onnx as m
        modelo = ort.InferenceSession(a.pesos, providers=["CPUExecutionProvider"])
        detectar = lambda img: m.detectar(modelo, img, conf=0.01)
    else:
        import inferencia_yolo_opencv as m
        modelo = m.carregar(a.cfg, a.pesos)
        detectar = lambda img: m.detectar(modelo, img, conf=0.005)

    deteccoes = []
    for im in gt.dataset["images"]:
        img = cv2.imread(os.path.join(a.dataset, im["file_name"]))
        for classe, score, (x1, y1, x2, y2) in detectar(img):
            deteccoes.append({"image_id": im["id"], "category_id": nome_para_id[classe],
                              "bbox": [x1, y1, x2 - x1, y2 - y1], "score": score})

    ev = COCOeval(gt, gt.loadRes(deteccoes), "bbox")
    ev.evaluate(); ev.accumulate(); ev.summarize()

    print("\nAP50 por classe (classes sem instâncias no conjunto são ignoradas):")
    for i, cid in enumerate(ev.params.catIds):
        p = ev.eval["precision"][0, :, i, 0, 2]
        p = p[p > -1]
        if len(p):
            print(f"  {gt.cats[cid]['name']:10s} {p.mean() * 100:5.1f}%")


if __name__ == "__main__":
    main()
