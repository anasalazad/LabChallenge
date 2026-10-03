# Lab 7 (Week 7) – what's left for you, Anas

**Topic:** TensorFlow & PyTorch · Neural network fundamentals · MNIST handwritten digits
**Worklog:** `Lab 7/Lab7_Worklog_Week7.docx` (already filled in – 7/11 checklist items done)
**Time you still need:** about 45 min (installs take the longest) + the video if you watch it

---

## ✅ Already done for you

| What | File |
|---|---|
| **Fixed** the provided notebook – it crashes on current TensorFlow (`InputLayer(input_shape=28*28)` → `ValueError`). Changed to `InputLayer(shape=(28*28,))` + added a seed. Run, 93.8% test accuracy | `neural_net.ipynb` (and the same fix in `neural_net.py`) |
| NN fundamentals in numpy, 8 hyperparameter experiments (best 97.25%), confusion matrix, wrong digits | `nn_experiments.ipynb` |
| The same network in PyTorch (97.6%) | `nn_pytorch.ipynb` |
| One-screen TensorFlow + PyTorch install check (for screenshot 7.3) | `screenshot_demo_install_check.py` |
| Plots for the worklog | `figures/7_*.png` |
| The worklog itself | `Lab7_Worklog_Week7.docx` |

## ⬜ What you need to do

### Step 1 – install TensorFlow + PyTorch on your laptop (≈20 min) → screenshots 7.1–7.3
> Use **Python 3.10–3.12** if you can (TensorFlow doesn't always support the newest Python straight away). If you set up the repo's `.venv` from the main `Anas.md`, activate it first – TensorFlow + PyTorch are already in `requirements.txt`, so `pip install -r requirements.txt` does both.

1. **TensorFlow:** `pip install tensorflow` (big download, be patient).
2. **PyTorch:** go to <https://pytorch.org/get-started/locally/> and pick: your OS · **Pip** · **Python** · **CPU** (or a CUDA version if you have an NVIDIA GPU).
   📸 **7.1** – the selector with the generated *"Run this Command"* line.
   Copy that command into your terminal and run it.
3. Check what got installed:
   - Windows: `pip list | findstr /i "tensorflow keras torch"`
   - Mac/Linux: `pip list | grep -iE "tensorflow|keras|torch"`
   📸 **7.2** – the end of the install output + the `pip list` lines.
4. Run the check script:
   ```bash
   cd "Lab 7"
   python screenshot_demo_install_check.py
   ```
   📸 **7.3** – the whole output, down to *"Both frameworks work - ready for Lab 7!"*.

### Step 2 – run the MNIST notebook yourself (≈10 min) → screenshots 7.4, 7.5
Laptop (`jupyter notebook` → open `Lab 7/neural_net.ipynb` → **Restart & Run All**) **or** Colab (upload it → Runtime → Run all – Colab already has TensorFlow).
- 📸 **7.4** – section **"Create our Neural Network"**: the whole model cell (13 lines – **line 2** is my seed, **lines 6–7** are the original `InputLayer` line commented out + my fix `InputLayer(shape=(28*28,))`; turn on line numbers with **L** in Jupyter / Tools → Settings → Editor in Colab) + the `model.compile(...)` / `model.fit(...)` cell with all **5 epochs** of output.
  *(Same fix in the script version: `neural_net.py` **lines 66–71** – optional extra screenshot in VS Code if you want to show it.)*
- 📸 **7.5** – **"Evaluate the accuracy of test data"** (`Test accuracy: 0.938…`) + **"Do some predictions"**: the `x_test[45]` image and `Predicted label is: 5`.

> Your numbers might differ in the 3rd decimal on a different computer (TensorFlow isn't bit-for-bit identical across CPUs) – that's normal. If they're noticeably different, ask Claude locally to update the worklog numbers.

### Step 3 – my two extra notebooks (≈10 min) → screenshots 7.6, 7.7
You can just open them (outputs are saved) or re-run them (`nn_experiments.ipynb` takes ~4 min on CPU, `nn_pytorch.ipynb` ~20 s). **Don't run them in the same kernel** – TensorFlow + PyTorch together crashed the kernel for me.
- 📸 **7.6** – `nn_experiments.ipynb`, part B: the output of the experiments cell (8 lines + the results table).
- 📸 **7.7** – `nn_pytorch.ipynb`: the training cell + the 5 epoch lines (test accuracy ≈ 0.976).

### Step 4 – video (optional, linked in the sheet)
3Blue1Brown – *But what is a neural network?* <https://www.youtube.com/watch?v=aircAruvnKk>

### Step 5 – screenshots into the worklog + final touches
1. Save screenshots in **`Lab 7/screenshots/`** with the names below.
2. `python _tools/insert_screenshots.py 7`
3. Tick the checklist: click the boxes in Word or `python _tools/tick_checklist.py 7 8 9 10 11`
4. In Word: **Student ID**, check the **dates** (24–30 Sep 2026), adjust **TIME SPENT**.

---

## 📸 Screenshot list (Lab 7)

| # | Where | Exactly what to capture | Save as |
|---|---|---|---|
| 7.1 | Browser – pytorch.org/get-started/locally | selector with your OS / Pip / Python / CPU + the generated command | `screenshots/7.1_pytorch_selector.png` |
| 7.2 | Terminal | end of the installs + `pip list` filtered for tensorflow/keras/torch | `screenshots/7.2_pip_list.png` |
| 7.3 | Terminal | `python screenshot_demo_install_check.py` full output | `screenshots/7.3_install_check.png` |
| 7.4 | `neural_net.ipynb` – "Create our Neural Network" | model cell lines 1–13 (line 2 = seed, lines 6–7 = the fix) + compile/fit with 5 epochs | `screenshots/7.4_nn_model_training.png` |
| 7.5 | `neural_net.ipynb` – evaluate + predictions | Test accuracy ≈ 0.938, the x_test[45] image, "Predicted label is: 5" | `screenshots/7.5_nn_test_prediction.png` |
| 7.6 | `nn_experiments.ipynb` – part B | experiments output + results table | `screenshots/7.6_experiments_table.png` |
| 7.7 | `nn_pytorch.ipynb` | training cell + 5 epoch lines | `screenshots/7.7_pytorch_training.png` |

---

## 🧠 Know your stuff (2-minute revision)
- **Neuron:** `z = Σ(w·x) + b`, output `a = g(z)` with an activation function g. Input layer has no neurons (just the features).
- **Activations:** sigmoid (0..1), tanh (−1..1), ReLU `max(0,z)` (default for hidden layers – doesn't saturate), softmax (output layer, probabilities that sum to 1).
- **Loss:** MSE/MAE for regression, binary cross-entropy for 2 classes, categorical cross-entropy for more. `sparse_categorical_crossentropy` = integer labels.
- **Training:** forward pass → loss → **backpropagation** (gradients) → **gradient descent** `W = W − α·∂J/∂W`, repeated over mini-batches and epochs. Learning rate too big = bounces around, too small = slow.
- **MNIST model:** 784 inputs (28×28 flattened) → 32 → 64 → 10 outputs; SGD, 5 epochs → ~94%. With Adam / bigger layers / more epochs → ~97%.
- **The bug:** Keras 3 needs `InputLayer(shape=(784,))` – the old `input_shape=784` crashes.
- **TensorFlow vs PyTorch:** Keras does the training loop for you (`fit`), PyTorch makes you write it (`zero_grad → forward → loss → backward → step`).

> Heads-up: a lot of this was prepared with an AI assistant. Make sure you can explain it in your own words, and check your unit's rules on AI use (add an acknowledgement if they ask for one).
