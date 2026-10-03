"""
Lab 5 - quick check that Python + scikit-learn are installed properly on my laptop.
Run it from a terminal (in this folder):   python screenshot_demo_setup_check.py
Everything fits on one screen, so it's an easy screenshot for the worklog.
"""
import platform
import sys

print("=" * 52)
print(" COS30018 Lab 5 - local Python / sklearn setup check")
print("=" * 52)
print(f"Python          : {sys.version.split()[0]}  ({platform.system()} {platform.release()})")

missing = []
for pkg, import_name in [("numpy", "numpy"), ("pandas", "pandas"),
                         ("scikit-learn", "sklearn"), ("matplotlib", "matplotlib"),
                         ("jupyter notebook", "notebook")]:
    try:
        mod = __import__(import_name)
        print(f"{pkg:<16}: {mod.__version__}")
    except ImportError:
        print(f"{pkg:<16}: NOT INSTALLED  ->  pip install {pkg.replace('jupyter ', '')}")
        missing.append(pkg)

if "scikit-learn" not in missing and "numpy" not in missing:
    import numpy as np
    from sklearn.linear_model import LinearRegression

    area = np.array([[3456], [2089], [1416]])   # the 3 houses from the lab sheet
    price = np.array([600, 395, 232])
    model = LinearRegression().fit(area, price)
    print("-" * 52)
    print("Quick test - LinearRegression on the lab-sheet houses")
    print(f"  price = {model.coef_[0]:.4f} * area + {model.intercept_:.2f}")
    print(f"  predicted price of a 2500 sq.ft house: ${model.predict([[2500]])[0]:.1f}k")

print("-" * 52)
print("All good - ready for the lab!" if not missing else f"Missing: {', '.join(missing)}")
