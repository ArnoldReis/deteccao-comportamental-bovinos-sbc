# RF-DETR Base

> **Experimento adicional, não incluído nos resultados do TCC.**

Modelo [RF-DETR](https://github.com/roboflow/rf-detr) (Roboflow) treinado em 15/06/2025. Pelos caminhos registrados no checkpoint (`/train/cache/...`), o treino parece ter sido feito na infraestrutura de treino da Roboflow, e não no Colab.

Configuração salva no checkpoint (`weights.pt`):

| Parâmetro | Valor |
|---|---|
| Encoder | DINOv2 (windowed small) |
| Resolução | 616 × 616 |
| Queries | 300 |
| Épocas | 100 (com early stopping, paciência 15) |
| Batch | 2 × 8 (acúmulo de gradiente) |
| lr / lr do encoder | 1e-4 / 1.5e-4 |
| EMA | sim |
| Multi-scale | sim |
| Classes | Bebendo, Comendo, Deitado, Em pe, Escondido, Outro, Pastando |

## Peso (na Release)

`rf-detr_base_gado.pt` (arquivo `weights.pt` original, 128 MB).

## Inferência

```python
from rfdetr import RFDETRBase
from PIL import Image

modelo = RFDETRBase(pretrain_weights="rf-detr_base_gado.pt")
deteccoes = modelo.predict(Image.open("foto.jpg"), threshold=0.5)
```

> Este modelo ainda não foi avaliado neste repositório.
