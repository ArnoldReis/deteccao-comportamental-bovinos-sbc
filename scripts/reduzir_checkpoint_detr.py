"""
Remove o estado do otimizador e do scheduler de um checkpoint do DETR,
mantendo apenas os pesos do modelo. Reduz o arquivo de ~500 MB para ~165 MB,
o que é suficiente para inferência (não serve para retomar o treino).

Uso (no Colab ou em qualquer máquina com PyTorch):
    python reduzir_checkpoint_detr.py checkpoint.pth detr_r50_gado.pth
"""
import sys
import torch

entrada, saida = sys.argv[1], sys.argv[2]
ck = torch.load(entrada, map_location="cpu", weights_only=False)
torch.save({"model": ck["model"], "args": ck.get("args"), "epoch": ck.get("epoch")}, saida)
print(f"Salvo em {saida} (época {ck.get('epoch')})")
