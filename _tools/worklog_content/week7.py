# Week 7 worklog content - Lab 7 (TensorFlow/PyTorch, NN fundamentals, MNIST)
# Markup: **bold**, `code`. Edit text here, then: python _tools/build_worklogs.py 7

SPEC = {
    "week": 7,
    "dates": "24-30 September 2026",
    "student_name": "Anas Al Azad",
    "student_id": "",
    "title": "Week 7 – TensorFlow & PyTorch, Neural Network fundamentals, MNIST digit recogniser",
    "intro": "My checklist for this week – ticked = done (notebooks, plots and scripts are in the "
             "**Lab 7** folder of my repo), unticked = still on my to-do list.",
    "checklist": [
        ("Read the Week 7 tutorial (DL frameworks + neural network fundamentals)", True),
        ("Installed TensorFlow 2.21 + PyTorch 2.14 and checked both work "
         "(`screenshot_demo_install_check.py`)", True),
        ("NN fundamentals in numpy: activation functions + one neuron trained with backprop "
         "(`nn_experiments.ipynb` part A)", True),
        ("Ran `neural_net.ipynb` – fixed the Keras 3 `InputLayer` error – **93.8%** test accuracy", True),
        ("8 hyperparameter experiments (neurons, activation, optimiser, learning rate, batch size, epochs) "
         "– best **97.25%**", True),
        ("Confusion matrix + looked at the digits the network gets wrong", True),
        ("Same network in PyTorch (`nn_pytorch.ipynb`) – 97.6%", True),
        ("Install TensorFlow + PyTorch on my own laptop (pytorch.org selector) and run the install check", False),
        ("Run `neural_net.ipynb` myself (Colab or laptop) and take the screenshots", False),
        ("Watch the 3Blue1Brown neural network video linked in the sheet", False),
        ("Add my screenshots (yellow boxes below)", False),
    ],
    "rows": [
        {
            "task": "DL frameworks: TensorFlow + PyTorch",
            "task_note": "Lab sheet section 1",
            "did": [
                "Read about both: TensorFlow (Google Brain, 2015) and PyTorch (Facebook AI Research, 2017).",
                "Installed **TensorFlow 2.21** (comes with Keras 3.15) with `pip install tensorflow`, and "
                "**PyTorch 2.14** with pip, then checked `pip list` + imported both.",
                "Wrote `screenshot_demo_install_check.py` – prints both versions, whether a GPU is "
                "found and does a tiny matrix multiply in each library.",
                "Still to do: same install on my own laptop using the pytorch.org selector (screenshots 7.1–7.3).",
            ],
            "time": "1 h",
            "learning": [
                "Colab has both preinstalled; locally it's pip.",
                "The PyTorch install command depends on OS + compute platform (CPU vs a CUDA version) "
                "– CUDA builds let you train on an NVIDIA GPU.",
            ],
            "problems": [
                "The CPU-only PyTorch download server (`download.pytorch.org`) was blocked on the cloud "
                "machine I first used, so I installed the normal PyPI wheel – which is the CUDA "
                "build and pulled in a few GB of NVIDIA libraries even though there's no GPU.",
            ],
        },
        {
            "task": "Neural network fundamentals",
            "task_note": "Lab sheet section 2, `nn_experiments.ipynb` part A",
            "did": [
                "Went through layers, neurons, weights & bias, z = Σ(w·x) + b, activation "
                "functions, loss functions (MSE, MAE, binary/categorical cross-entropy), backprop and "
                "gradient descent.",
                "Plotted sigmoid / tanh / ReLU and tried softmax on [2, 1, 0.1] → [0.659, 0.242, "
                "0.099] (Fig 7.1).",
                "Trained **one neuron by hand in numpy** on the AND gate: forward pass → binary "
                "cross-entropy → backprop → gradient descent. Loss 0.694 → 0.0087, "
                "weights [8.82, 8.82], bias −13.4, predicts [0, 0, 0, 1] ✔.",
            ],
            "time": "1.5 h",
            "learning": [
                "Without a non-linear activation the whole network is just one linear function.",
                "Sigmoid/tanh go flat at the ends (tiny gradients) → ReLU for hidden layers, "
                "softmax for the multi-class output.",
                "For sigmoid + cross-entropy the backprop gradient simplifies to (a − y).",
            ],
            "problems": [],
        },
        {
            "task": "MNIST neural network",
            "task_note": "`neural_net.ipynb`",
            "did": [
                "MNIST: 60,000 train / 10,000 test images, 28×28, pixels 0–255 → scaled to "
                "0–1 and flattened to 784.",
                "Network 784 → 32 → 64 → 10 (ReLU, softmax), SGD + "
                "`sparse_categorical_crossentropy`, 5 epochs: train acc 93.8%, **test acc 93.80%**, "
                "test loss 0.2045 (tutor's run: 93.87%).",
                "Prediction for `x_test[45]`: **5** with 93.8% probability (correct).",
                "Added `tf.keras.utils.set_random_seed(42)` so my results are reproducible.",
            ],
            "time": "1 h",
            "learning": [
                "`sparse_categorical_crossentropy` = integer labels, `categorical_crossentropy` = one-hot labels.",
                "Scaling inputs to 0–1 helps gradient descent converge.",
                "The output is 10 probabilities – `np.argmax` picks the digit.",
            ],
            "problems": [
                "**The provided code crashes on current TensorFlow (Keras 3)**: "
                "`InputLayer(input_shape=28*28)` → *ValueError: Cannot convert '784' to a shape*. "
                "Fixed with `InputLayer(shape=(28*28,))` (`input_shape` is deprecated and it has to be "
                "a tuple). Fixed the same line in `neural_net.py`.",
                "The comments say 64 / 128 units but the code actually uses 32 / 64.",
            ],
        },
        {
            "task": "Extra – hyperparameter experiments",
            "task_note": "`nn_experiments.ipynb` parts B–C",
            "did": [
                "The notebook says to try combinations, so I ran **8 configs** (same seed, 10% of the "
                "training set held out for validation) (Fig 7.2, 7.3):",
                "Adam **96.8%** vs SGD 93.8% with the same network; SGD with lr = 0.1 → 96.5%; "
                "sigmoid instead of ReLU → only 76.6%; batch size 256 → 87.8%; "
                "best = Adam, 256-128, 10 epochs → **97.25%**.",
                "Confusion matrix of the best model: most mix-ups are 2→3, 4→9, 7→3, "
                "9→8; plotted some wrong digits – mostly messy ones (Fig 7.4, 7.5).",
            ],
            "time": "2 h",
            "learning": [
                "Optimiser / learning rate made the biggest difference, then size + epochs.",
                "Bigger batch = fewer weight updates per epoch, so it needs more epochs.",
                "The biggest model's validation loss starts going back up around epoch 9–10 "
                "while training loss keeps falling → overfitting.",
            ],
            "problems": [
                "Every run takes 15–60 s on CPU (no GPU), so I kept it to 8 experiments instead of "
                "a full grid search.",
            ],
        },
        {
            "task": "Extra – PyTorch version",
            "task_note": "`nn_pytorch.ipynb`",
            "did": [
                "Rebuilt the network (784 → 128 → 64 → 10) in PyTorch with my own training "
                "loop: `zero_grad → forward → loss → backward → step`.",
                "Adam, 5 epochs: **97.6% test accuracy** in 18 s on CPU – about the same as Keras.",
            ],
            "time": "1 h",
            "learning": [
                "Keras hides the loop in `fit()`, PyTorch makes you write it – more code but you see "
                "every step from the lab sheet.",
                "`nn.CrossEntropyLoss` already includes the softmax, so no softmax layer at the end.",
            ],
            "problems": [
                "Running TensorFlow training and PyTorch training in the **same** Jupyter kernel crashed "
                "it (segfault – the two libraries clash). Moved PyTorch into its own notebook and "
                "loaded MNIST straight from the `.npz` file with numpy so it doesn't need TensorFlow.",
            ],
        },
    ],
    "total_time": "6.5 h",
    "total_note": "+ ~45 min laptop install & screenshots",
    "screenshots_intro": "Figures 7.1–7.6 come straight out of my `nn_experiments.ipynb`. The yellow "
                         "boxes are screenshots I still need to grab from my laptop.",
    "figures": [
        {"path": "Lab 7/figures/7_1_activation_functions.png", "width": 5.8,
         "caption": "the activation functions from the lab sheet"},
        {"path": "Lab 7/figures/7_2_hyperparameter_results.png", "width": 5.0,
         "caption": "test accuracy of my 8 hyperparameter experiments (orange = lab baseline, green = best)"},
        {"path": "Lab 7/figures/7_3_learning_curves.png", "width": 5.8,
         "caption": "learning curves – sigmoid learns slowly, Adam is fastest, the biggest model starts "
                    "overfitting at the end"},
        {"path": "Lab 7/figures/7_4_confusion_matrix.png", "width": 3.8,
         "caption": "confusion matrix of my best model (97.25% test accuracy)"},
        {"path": "Lab 7/figures/7_5_misclassified.png", "width": 5.8,
         "caption": "some of the test digits my best model gets wrong"},
        {"path": "Lab 7/figures/7_6_prediction_45.png", "width": 4.6,
         "caption": "the notebook's example digit x_test[45] and my best model's softmax output"},
    ],
    "screenshots": [
        {"id": "7.1", "title": "pytorch.org – install command for my laptop",
         "what": "the “Start Locally” selector on https://pytorch.org/get-started/locally/ with "
                 "your OS, Package = Pip, Language = Python, Compute Platform = CPU (or your CUDA) and "
                 "the generated “Run this Command” line.",
         "file": "Lab 7/screenshots/7.1_pytorch_selector.png"},
        {"id": "7.2", "title": "Terminal – installed packages",
         "what": "the end of `pip install tensorflow` + the PyTorch command, then `pip list` filtered "
                 "for tensorflow / keras / torch (Windows: `pip list | findstr /i \"tensorflow keras torch\"`).",
         "file": "Lab 7/screenshots/7.2_pip_list.png"},
        {"id": "7.3", "title": "Terminal – install check script",
         "what": "full output of `python screenshot_demo_install_check.py` down to "
                 "“Both frameworks work - ready for Lab 7!”.",
         "file": "Lab 7/screenshots/7.3_install_check.png"},
        {"id": "7.4", "title": "neural_net.ipynb – model + training",
         "what": "the “Create our Neural Network” cell, all 13 lines (**line 2** = my seed, **lines 6–7** = "
                 "the original `InputLayer` line commented out + my fix `InputLayer(shape=(28*28,))`) and the "
                 "`model.compile`/`model.fit` cell with all 5 epochs.",
         "file": "Lab 7/screenshots/7.4_nn_model_training.png"},
        {"id": "7.5", "title": "neural_net.ipynb – test accuracy + prediction",
         "what": "the evaluate cells (Test accuracy ≈ 0.938) and the prediction section: the "
                 "x_test[45] image and “Predicted label is: 5”.",
         "file": "Lab 7/screenshots/7.5_nn_test_prediction.png"},
        {"id": "7.6", "title": "nn_experiments.ipynb – my experiment results",
         "what": "the output of the experiments cell (the 8 lines + the results table).",
         "file": "Lab 7/screenshots/7.6_experiments_table.png"},
        {"id": "7.7", "title": "nn_pytorch.ipynb – PyTorch training",
         "what": "the training cell and its output (5 epochs, test accuracy ≈ 0.976).",
         "file": "Lab 7/screenshots/7.7_pytorch_training.png"},
    ],
}
