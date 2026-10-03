# Week 5 worklog content - Lab 5 (Python intro, Google Colab, sklearn, Linear Regression)
# Markup: **bold**, `code`. Edit text here, then: python _tools/build_worklogs.py 5

SPEC = {
    "week": 5,
    "dates": "10-16 September 2026",
    "student_name": "Anas Al Azad",
    "student_id": "",  # <- put your student ID here (or type it in Word)
    "title": "Week 5 – Python intro, Google Colab, scikit-learn & Linear Regression",
    "intro": "My checklist for this week – ticked = done (notebooks and plots are all in the "
             "**Lab 5** folder of my repo), unticked = still on my to-do list.",
    "checklist": [
        ("Read the Week 5 tutorial sheet + the \u201cGoogle Colab introduction\u201d PDF", True),
        ("Python basics – ran every example from the sheet + my own variations "
         "(`python_basics_practice.ipynb`)", True),
        ("Made a Colab walkthrough notebook that follows the Colab PDF step by step "
         "(`colab_walkthrough.ipynb`)", True),
        ("Went through `Linear_Regression.ipynb` and matched each step to the theory "
         "(load → train → weights → predict → MSE)", True),
        ("Extra: 3-house example + **gradient descent from scratch** + learning-rate experiment "
         "(`linear_regression_extras.ipynb`)", True),
        ("Extra: proper train/test split (diabetes dataset)", True),
        ("Wrote a setup-check script for my laptop (`screenshot_demo_setup_check.py`)", True),
        ("Log into Google Colab and run `colab_walkthrough.ipynb` on a GPU runtime", False),
        ("Run `Linear_Regression.ipynb` myself in Colab", False),
        ("Install scikit-learn + Jupyter on my laptop and `import sklearn` in a new notebook", False),
        ("Run part D of the extras notebook (California Housing train/test split) "
         "somewhere with internet", False),
        ("Add my screenshots (yellow boxes below)", False),
    ],
    "rows": [
        {
            "task": "Python introduction",
            "task_note": "Lab sheet section 1",
            "did": [
                "Went through every example in the sheet: variables, operators "
                "(`+ - * / // % **`), string concat/repeat, implicit + explicit type conversion, "
                "if/else, if/elif/else, functions, while + for loops, `range()`, `import math`.",
                "Put it all in `python_basics_practice.ipynb` with a **“my try”** cell after "
                "each topic – e.g. looped over all the “try these variations” numbers at once "
                "instead of editing them by hand, caught the error from `123 + \"456\"`, "
                "used f-strings and `enumerate()`.",
                "Wrote a small `predict_price()` function (y = m·x + b) so the Python part links "
                "to the linear regression part.",
            ],
            "time": "1.5 h",
            "learning": [
                "Python is dynamically typed – int→float happens automatically but "
                "int + str doesn't, you have to cast.",
                "`/` always gives a float, `//` floors, `%` is the remainder; `range(10)` stops at 9.",
                "Indentation **is** the block structure.",
            ],
            "problems": [
                "The sheet's loop examples use `sum` as a variable name, which hides the built-in "
                "`sum()` (calling it afterwards gives *'int' object is not callable*). Renamed it to "
                "`total` / used `del sum`.",
            ],
        },
        {
            "task": "Google Colab intro",
            "task_note": "“Google Colab introduction” PDF",
            "did": [
                "Read the Colab PDF and built `colab_walkthrough.ipynb` that follows it: code + text "
                "cells, runtime type GPU/TPU, `tf.test.gpu_device_name()`, TPU check, `!pip install`, "
                "`!git clone`, file hierarchy, `files.upload()` and `drive.mount()`.",
                "Added `!nvidia-smi` and a second TPU check with `tf.config.list_logical_devices('TPU')`.",
                "Still to do: run it in Colab on a T4 GPU runtime (screenshots 5.1–5.4).",
            ],
            "time": "1 h",
            "learning": [
                "Colab = Jupyter in the browser with the ML libraries preinstalled + free (time-limited) GPU/TPU.",
                "`!` runs a shell command from a cell.",
                "Session storage gets wiped when the runtime resets – mount Google Drive to keep files.",
            ],
            "problems": [
                "The sheet's TPU check relies on the `COLAB_TPU_ADDR` variable, which (as far as I can "
                "tell) the newer TPU runtimes don't set, so I added the TensorFlow check as a backup.",
            ],
        },
        {
            "task": "scikit-learn + Jupyter set-up",
            "task_note": "Lab sheet section 3",
            "did": [
                "Worked out the local set-up from the sheet: `pip install scikit-learn`, then "
                "`jupyter notebook`, new notebook, `import sklearn`.",
                "Wrote `screenshot_demo_setup_check.py` – prints the Python/numpy/pandas/sklearn/"
                "matplotlib/notebook versions and fits a tiny LinearRegression so I can check "
                "everything works in one go.",
                "Still to do: install it on my laptop + screenshot 5.5.",
            ],
            "time": "0.5 h",
            "learning": [
                "sklearn = the “classic ML” library (regression, classification, clustering, "
                "dimensionality reduction) with the same `fit()` / `predict()` interface for everything.",
            ],
            "problems": [
                "Easy to mix up: the pip package is **scikit-learn** but you `import sklearn` "
                "(the old `pip install sklearn` package name is deprecated).",
            ],
        },
        {
            "task": "Linear Regression notebook",
            "task_note": "`Linear_Regression.ipynb`",
            "did": [
                "California Housing: 20,640 houses × 8 features, target = median house value "
                "(in $100k).",
                "`LinearRegression().fit()` → looked at the 8 learned weights (`coef_`, e.g. "
                "MedInc +0.437, AveBedrms +0.645, Latitude/Longitude about −0.42/−0.43) "
                "and the intercept (−36.94).",
                "Predicted house #5: 2.675 vs true 2.697 – pretty close. MSE = **0.524**, and "
                "the numpy version `np.mean((pred - y)**2)` gives exactly the same number.",
                "Matched it to the theory: y = w0 + w1x1 + … + w8x8, cost J(w) = ½Σ(ŷ − y)².",
            ],
            "time": "1 h",
            "learning": [
                "Training = finding the weights that minimise the cost function.",
                "The sign of a weight shows if a feature pushes the price up or down.",
                "The notebook measures the MSE on the same data it trained on, which is a bit optimistic "
                "(so I tried a proper test split in my extras).",
            ],
            "problems": [
                "The dataset download (`fetch_california_housing`) got a **403 Forbidden** from the "
                "figshare link on the cloud machine I first used – the network there blocks it. "
                "Works in Colab, so I'm re-running it there.",
            ],
        },
        {
            "task": "Extra – my own experiments",
            "task_note": "`linear_regression_extras.ipynb`",
            "did": [
                "Fitted the 3-house example from the sheet: price = 0.1759 × area + 0.76, so a "
                "2500 sq.ft house ≈ **$440.6k** (Fig 5.1).",
                "Coded **gradient descent from scratch** with the sheet's cost function and update rule "
                "– got exactly the same m and b as sklearn (final J = 555.3).",
                "Learning-rate test: α = 0.005 too slow, 0.05 / 0.3 converge, 0.65 oscillates, "
                "0.7 **diverges** (Fig 5.2).",
                "Proper 80/20 train/test split on sklearn's diabetes data: train R² 0.528, test "
                "R² 0.453, test MSE ≈ 2900 (Fig 5.3). Same idea for California Housing is "
                "part D (needs the download).",
            ],
            "time": "2 h",
            "learning": [
                "Feature scaling is basically required for gradient descent.",
                "GD only converges when α is below a limit (here 2/3); sklearn doesn't need "
                "α because it solves least squares directly.",
                "Test error > training error, so always keep a test set.",
            ],
            "problems": [
                "GD on the raw areas (~1000s) blew up to 1e205 / nan within 20 iterations. Fixed by "
                "standardising the feature (z-score) and converting the weights back afterwards.",
            ],
        },
    ],
    "total_time": "6 h",
    "total_note": "+ about 45 min still to do in Colab",
    "screenshots_intro": "Figures 5.1–5.3 come straight out of my `linear_regression_extras.ipynb`. "
                         "The yellow boxes are screenshots I still need to grab from Colab / my laptop.",
    "figures": [
        {"path": "Lab 5/figures/5_1_toy_regression_line.png", "width": 4.6,
         "caption": "regression line for the 3 houses from the lab sheet (dashed = errors the cost function adds up)"},
        {"path": "Lab 5/figures/5_2_learning_rate.png", "width": 4.9,
         "caption": "my gradient descent with different learning rates – too small is slow, too big diverges"},
        {"path": "Lab 5/figures/5_3_diabetes_pred_vs_true.png", "width": 3.6,
         "caption": "train/test split on the diabetes dataset – predicted vs true on the 20% test set"},
        {"path": "Lab 5/figures/5_4_california_pred_vs_true.png", "width": 3.6, "optional": True,
         "caption": "California Housing test set – predicted vs true (part D of my extras)"},
    ],
    "screenshots": [
        {"id": "5.1", "title": "Colab – my walkthrough notebook running",
         "what": "the whole browser window with `colab_walkthrough.ipynb` open in Colab: the first code "
                 "cell's output (“Hello from Google Colab!”) and the text cell under it, with your "
                 "Google account icon visible top-right.",
         "file": "Lab 5/screenshots/5.1_colab_first_cells.png"},
        {"id": "5.2", "title": "Colab – changing the runtime type to GPU",
         "what": "Runtime → Change runtime type dialog with **T4 GPU** selected (before you press Save).",
         "file": "Lab 5/screenshots/5.2_colab_runtime_gpu.png"},
        {"id": "5.3", "title": "Colab – GPU check",
         "what": "the `tf.test.gpu_device_name()` cell showing `'/device:GPU:0'` and the `!nvidia-smi` "
                 "table underneath it.",
         "file": "Lab 5/screenshots/5.3_colab_gpu_check.png"},
        {"id": "5.4", "title": "Colab – pip install, git clone and the Files pane",
         "what": "the `!pip install pandas` and `!git clone` cells with their output, with the Files "
                 "pane (folder icon on the left) open showing the `Testing-and-Debugging-Tools` folder "
                 "(and `drive` if you mounted it).",
         "file": "Lab 5/screenshots/5.4_colab_pip_clone_files.png"},
        {"id": "5.5", "title": "My laptop – scikit-learn installed",
         "what": "terminal after `pip install scikit-learn notebook` and then "
                 "`python screenshot_demo_setup_check.py` – the whole output down to "
                 "“All good - ready for the lab!”.",
         "file": "Lab 5/screenshots/5.5_local_sklearn_setup.png"},
        {"id": "5.6", "title": "Linear_Regression.ipynb in Colab – training",
         "what": "the “3 - Train a model” section: the `lin_reg.fit(...)` cell, the `coef_` "
                 "array and the intercept (−36.94…).",
         "file": "Lab 5/screenshots/5.6_linreg_train.png"},
        {"id": "5.7", "title": "Linear_Regression.ipynb in Colab – testing",
         "what": "the “4 - Test a model” section: predict for sample 5 (2.675), the true value "
                 "(2.697) and both MSE cells (0.5243…).",
         "file": "Lab 5/screenshots/5.7_linreg_test_mse.png"},
    ],
}
