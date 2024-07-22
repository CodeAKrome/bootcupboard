#!env python
import torch

def grafix_device():
    """Return device to use for GPU"""
    device = "cpu"
    if torch.backends.mps.is_available():
        device = "mps"
    if torch.cuda.is_available():
        device = "cuda"
    return device
        
def mps_built():
    """Is mps support available"""
    if torch.backends.mps.is_built():
        print(
            "MPS not available because the current MacOS version is not 12.3+ "
            "and/or you do not have an MPS-enabled device on this machine."
        )
    else:
        print(
            "MPS not available because the current PyTorch install was not "
            "built with MPS enabled."
            )
        
print(f"Using {grafix_device()} device")
