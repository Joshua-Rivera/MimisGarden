import torch

print(torch.__version__)
print("Is CUDA available:", torch.cuda.is_available())

if (torch.cuda.is_available()):
    device = torch.device("cuda")
    print("Using GPU:", torch.cuda.get_device_name(device))