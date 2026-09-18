# YOLOv4-tiny e YOLOv7-tiny (Darknet)

Treinados no Google Colab com o [Darknet (AlexeyAB)](https://github.com/AlexeyAB/darknet), entrada 416×416, 7 classes.

| Arquivo | Descrição |
|---|---|
| `yolov4-tiny-custom.cfg` | Configuração do YOLOv4-tiny usada no treino |
| `yolov7-tiny-custom.cfg` | Configuração do YOLOv7-tiny usada no treino |
| `obj.names` | Nomes das 7 classes (na ordem dos índices do dataset) |
| `obj.data` | Arquivo de dados do Darknet (ajuste os caminhos para a sua máquina) |

## Pesos (na Release)

| Arquivo | Iterações | Observação |
|---|---|---|
| `yolov4-tiny-custom_best.weights` | ~12.900 | **Modelo final do YOLOv4-tiny** (melhor mAP na validação) |
| `yolov7-tiny-custom_30000.weights` | 30.000 | Melhor checkpoint do YOLOv7-tiny (ver limitações abaixo) |

## Treinar novamente

```bash
./darknet detector train obj.data yolov4-tiny-custom.cfg yolov4-tiny.conv.29 -dont_show -map
```

## Avaliar

```bash
./darknet detector map obj.data yolov4-tiny-custom.cfg yolov4-tiny-custom_best.weights
```

Ou, sem compilar o Darknet, use `scripts/avaliar_coco.py` (OpenCV DNN + pycocotools).

## Limitações conhecidas

- **`max_batches = 2000200`** nos dois `.cfg`. O valor recomendado pelo Darknet seria `classes × 2000 = 14000`, com `steps` em 80% e 90% desse valor. Com o valor usado, a taxa de aprendizado nunca é reduzida e o treino foi interrompido manualmente. Os arquivos foram mantidos exatamente como no treino, para fins de reprodutibilidade.
- **O YOLOv7-tiny não convergiu bem** (AP50 de 34% na validação, contra 73% do YOLOv4-tiny). Além do `max_batches`, o cfg usa `subdivisions=64` e `learning_rate=0.00261`, que podem ter contribuído.
- Houve experimentos preliminares (26/05/2025) com uma versão antiga do dataset e 8 classes. Eles não fazem parte dos resultados.
