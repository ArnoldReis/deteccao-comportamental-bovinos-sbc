# Single Board Computers (SBCs)

Esta pasta descreve os dispositivos avaliados no TCC e os resultados de desempenho obtidos em cada um. Os detalhes completos estão nas Seções 3.3 a 4 do [texto do TCC](../docs/TCC_Arnold_Zago_dos_Reis.pdf).

## Dispositivos

| SBC | Processador | RAM | GPU | Custo (US$) | Sistema / bibliotecas | Situação |
|---|---|---|---|---|---|---|
| Raspberry Pi Zero | ARM1176JZF-S, 1 GHz | 512 MB | Não | ~10 | Raspberry Pi OS | ❌ desligava durante a instalação das dependências |
| Banana Pi M2 Zero | Allwinner H2+, quad-core Cortex-A7, 1 GHz | 512 MB | Não | ~15 | Armbian (Debian), kernel 5.15 ([Qengineering](https://github.com/Qengineering/BananaPi-M2-Zero-OV5640)), OpenCV 4.5.5 | ✅ (exceto DETR) |
| Raspberry Pi 3 Model B | ARM Cortex-A53, 1,2 GHz | 1 GB | Não | ~35 | Raspberry Pi OS 64-bit, OpenCV 4.5.5 | ✅ (exceto DETR) |
| NVIDIA Jetson Nano | ARM Cortex-A57, 1,4 GHz | 4 GB | Maxwell, 128 núcleos CUDA | 100–130 | JetPack 4.6 (CUDA, cuDNN, TensorRT), OpenCV com GPU | ✅ todos os modelos |

O DETR não pôde ser executado no Banana Pi M2 Zero nem no Raspberry Pi 3, porque as versões das bibliotecas exigidas pelo modelo não são compatíveis com esses dispositivos.

## Protocolo

- **Dataset:** 115 imagens de bovinos ([Cattle Detection, loliktry — Roboflow](https://universe.roboflow.com/loliktry/cattle_detection-060yo/dataset/1))
- **Repetições:** 5 execuções completas por modelo em cada dispositivo
- **Monitoramento:** `sysstat` (CPU e memória) e `procps` (tempo por imagem)
- **Critérios de aceitação:** latência < 30 s por inferência e consumo de memória < 80%

## Tempo médio por imagem (segundos)

| Modelo | Banana Pi M2 Zero | Raspberry Pi 3 | Jetson Nano |
|---|---:|---:|---:|
| YOLOv4-tiny | 21,59 | 24,50 | 5,86 |
| YOLOv7-tiny | 21,60 | 20,65 | 6,69 |
| **NanoDet** | **4,00** | **4,80** | **1,44** |
| DETR | – | – | 1,45 |

## Consumo de recursos durante a inferência

| Modelo | Recurso | Banana Pi M2 Zero | Raspberry Pi 3 | Jetson Nano |
|---|---|---:|---:|---:|
| YOLOv4-tiny | CPU | 19,60% | 17,70% | 18,00% |
| | Memória | 0,34% | 4,50% | 3,64% |
| YOLOv7-tiny | CPU | 20,42% | 18,57% | 18,00% |
| | Memória | 0,32% | 4,87% | 3,07% |
| NanoDet | CPU | 21,00% | 19,03% | 18,00% |
| | Memória | 0,22% | 4,19% | 4,24% |
| DETR | CPU | – | – | 43,05% |
| | Memória | – | – | 9,29% |

Fonte: Tabelas 2 e 3 do TCC.
