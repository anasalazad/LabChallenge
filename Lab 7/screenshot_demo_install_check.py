"""
Lab 7 - check that TensorFlow and PyTorch are both installed on my laptop.
Run from a terminal in this folder:   python screenshot_demo_install_check.py
(One screen of output = one easy screenshot for the worklog.)

Each library is checked in its own subprocess, because importing/training
TensorFlow and PyTorch in the same Python process can crash on some machines.
"""
import platform
import subprocess
import sys

TF_CHECK = r"""
import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
import tensorflow as tf
print(f"TensorFlow  : {tf.__version__}  (Keras {tf.keras.__version__})")
gpus = tf.config.list_physical_devices("GPU")
print(f"  GPU       : {gpus if gpus else 'none - CPU only (fine for this unit)'}")
x = tf.constant([[1.0, 2.0], [3.0, 4.0]])
print(f"  test      : tf.matmul(x, x) = {tf.matmul(x, x).numpy().tolist()}")
"""

TORCH_CHECK = r"""
import torch
print(f"PyTorch     : {torch.__version__}")
print(f"  CUDA GPU  : {torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'none - CPU only (fine for this unit)'}")
x = torch.tensor([[1.0, 2.0], [3.0, 4.0]])
print(f"  test      : x @ x = {(x @ x).tolist()}")
"""


def check(name, code, pip_hint):
    result = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True)
    if result.returncode == 0:
        print(result.stdout.rstrip())
        return True
    last = (result.stderr.strip().splitlines() or ["unknown error"])[-1]
    print(f"{name:<12}: NOT WORKING -> {last}")
    print(f"  fix       : {pip_hint}")
    return False


print("=" * 60)
print(" COS30018 Lab 7 - TensorFlow + PyTorch install check")
print("=" * 60)
print(f"Python      : {sys.version.split()[0]}  ({platform.system()} {platform.release()})")
print("-" * 60)
ok_tf = check("TensorFlow", TF_CHECK, "pip install tensorflow")
print("-" * 60)
ok_torch = check("PyTorch", TORCH_CHECK,
                 "use the command from https://pytorch.org/get-started/locally/")
print("-" * 60)
print("Both frameworks work - ready for Lab 7!" if ok_tf and ok_torch
      else "Something's missing - see the fix lines above.")
