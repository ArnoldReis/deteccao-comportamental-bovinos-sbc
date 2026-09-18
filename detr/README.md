# DETR (ResNet-50)

Fine-tuning do [DETR original (facebookresearch/detr)](https://github.com/facebookresearch/detr) no Google Colab.

No TCC, o DETR alcançou Precision 0,94, Recall 0,69 e F1-Score 0,79. Ele só pôde ser executado no **NVIDIA Jetson Nano** (1,45 s por imagem, 43% de CPU), pois as dependências não eram compatíveis com o Banana Pi M2 Zero e o Raspberry Pi 3.

Configuração salva no checkpoint: backbone ResNet-50, 100 queries, `lr = 1e-4`, `lr_backbone = 1e-5`, batch 2, 150 épocas planejadas, dataset em formato COCO.

## Situação dos arquivos

- O checkpoint do treino principal (`detr_dataset/outputs/box_model/checkpoint.pth`, ~500 MB) e o respectivo `log.txt` estão no Google Drive do autor e **ainda não foram reavaliados** neste repositório.
- Um segundo checkpoint (`detr_weights/checkpoint.pth`, 29/05/2025) registra apenas a época 0, ou seja, é de uma execução interrompida no início. Por isso não foi publicado.
- O notebook de treino (`detr_custom_training_tutorial.ipynb`) deve ser adicionado em `notebooks/`.

## Publicando o peso

O checkpoint completo inclui o estado do otimizador, desnecessário para inferência. Para reduzi-lo a ~165 MB antes de subir na Release:

```bash
python scripts/reduzir_checkpoint_detr.py checkpoint.pth detr_r50_gado.pth
```
