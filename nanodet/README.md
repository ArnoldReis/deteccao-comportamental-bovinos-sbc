# NanoDet-Plus

Treinado no Google Colab (GPU T4) com o repositório oficial [RangiLyu/nanodet](https://github.com/RangiLyu/nanodet).

- **Backbone:** ShuffleNetV2 1.0x · **Neck:** GhostPAN · **Head:** NanoDetPlusHead (4,2 M parâmetros)
- **Entrada:** 320×320 · **Épocas:** 300 · **Batch:** 8 · **Otimizador:** AdamW (lr 0,001) com CosineAnnealing
- **Duração do treino:** ~2h30 (27/05/2025)
- **Melhor modelo:** época 300 — mAP@.50:.95 = 52,6% e AP50 = 74,1% na validação (`eval_results.txt`)

| Arquivo | Descrição |
|---|---|
| `nanodet_comportamento_gado.yml` | Configuração do modelo e do treino |
| `train.py` | Script de treino usado (baseado em `tools/train.py` do NanoDet) |
| `eval_results.txt` | Métricas do melhor modelo, por classe |
| `logs/treino_final_2025-05-27.txt` | Log completo das 300 épocas |

> A classe `Boi` (índice 0) é a supercategoria exportada pelo Roboflow, e não uma classe real. Por isso ela aparece como `nan` nas métricas.

## Pesos (na Release)

| Arquivo | Descrição |
|---|---|
| `nanodet_model_best.pth` | Pesos do melhor modelo (PyTorch) |
| `nanodet_comportamento_gado-sim.onnx` | Modelo exportado e simplificado em ONNX (5,5 MB) |

## Inferência rápida (ONNX, sem PyTorch)

```bash
cd scripts
python inferencia_nanodet_onnx.py --modelo nanodet_comportamento_gado-sim.onnx --imagem foto.jpg
```

A reavaliação com esse script reproduz as métricas do treino (AP50 = 74,2%), o que confirma que a decodificação está correta.

## Treinar novamente

```bash
git clone https://github.com/RangiLyu/nanodet.git && cd nanodet
pip install -r requirements.txt && python setup.py develop
# coloque o dataset (formato COCO) em data/gado/{train,valid}
python ../train.py ../nanodet_comportamento_gado.yml
```

Versões usadas no Colab: `torch 2.2.2`, `pytorch-lightning 1.9.0`, `torchmetrics 1.3.0`, `numpy 1.26.4`.
