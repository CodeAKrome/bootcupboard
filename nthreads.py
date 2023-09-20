#!env python3

import os
import psutil

def get_cpu_thread_count():
  """Returns the number of threads that can be run on the CPU.

  Works for ARM, Intel, and Apple CPUs.

  Returns:
    int: The number of threads that can be run on the CPU.
  """

  if psutil.WINDOWS:
    # Use the Windows API to get the number of logical processors.
    return os.cpu_count()
  elif psutil.LINUX:
    # Use the Linux /proc/cpuinfo file to get the number of logical processors.
    cpu_count = 0
    with open('/proc/cpuinfo', 'r') as f:
      for line in f:
        if line.startswith('processor'):
          cpu_count += 1
    return cpu_count
  elif psutil.OSX:
    # Use the macOS sysctl API to get the number of logical processors.
    import sysctl
    cpu_count = sysctl.sysctl('hw.logicalcpu')[0]
    return cpu_count
  else:
    # Unknown platform. Return None.
    return None

if __name__ == "__main__":
  print(get_cpu_thread_count())
