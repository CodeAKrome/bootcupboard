import torch
import timeit
a_cpu = torch.rand(250, device='cpu')
b_cpu = torch.rand((250, 250), device='cpu')
a_mps = torch.rand(250, device='mps')
b_mps = torch.rand((250, 250), device='mps')

print('cpu', timeit.timeit(lambda: a_cpu @ b_cpu, number=100_000))
print('mps', timeit.timeit(lambda: a_mps @ b_mps, number=100_000))
