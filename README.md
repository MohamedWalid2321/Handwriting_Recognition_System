# WritingPad: Pure Python Handwriting Recognition System

**WritingPad** is an educational and highly constrained software engineering project that implements a complete, end-to-end handwriting recognition system using **pure Python** from the ground up. 

Unlike typical modern applications that rely heavily on powerful third-party libraries, WritingPad takes a "from-scratch" architectural approach. It independently implements foundational computer vision techniques, mathematical feature extraction, and nearest-neighbor machine learning classification. The system demonstrates how complex image processing pipelines—such as 2D Gaussian convolutions, Otsu thresholding, morphological operations, and spatial moment calculations—can be built using only the Python standard library, basic arithmetic, and explicit nested loops.

This project serves as an interactive GUI application where users can draw handwritten symbols, run them through the custom CV pipeline, visualize the transformation steps, and train the system on their own hand-drawn templates. The only external dependency utilized in the entire project is `PyQt6`, exclusively for rendering the graphical user interface and drawing canvas.

## 🚀 Key Features

*   **Interactive Drawing Canvas:** A PyQt6-based drawing interface with configurable pen width and color.
*   **Custom Computer Vision Pipeline:**
    *   Grayscale conversion.
    *   **Gaussian Smoothing:** Manual 2D convolution with dynamically generated Gaussian kernels.
    *   **Otsu Thresholding:** Algorithmically calculated thresholding to binarize images.
    *   **Morphological Operations:** Custom erosion, dilation, opening, and closing using configurable structuring elements.
    *   **Connected Component Labeling:** Identifying and isolating shapes within the drawing canvas.
*   **Feature Extraction & Normalization:** Calculates spatial moments and geometric descriptors to capture scale- and translation-invariant features.
*   **Recognition Engine:** Utilizes nearest-neighbor algorithms over normalized feature vectors.
*   **Training & Persistence:** A built-in training manager allows you to draw new samples, assign labels, and save them persistently to a JSON template library with atomic writes for data safety.
*   **Tunable Settings System:** Externalized constants in `src/settings.py` for easily configuring application behavior (canvas size, pen settings, kernel size, sigma, etc.).


---

## 🛠️ Prerequisites

| Requirement | Version | Notes |
|-------------|---------|-------|
| Python      | ≥ 3.10  | Built with modern Python typing constraints. |
| pip         | any     | For installing PyQt6. |

---

## ⚙️ Installation & Setup

```bash
# 1. Clone the repository
git clone <repo-url>
cd handwriting-recognition-cv

# 2. Create a virtual environment
python -m venv .venv

# 3. Activate the environment
# Windows:
.venv\Scripts\activate
# macOS / Linux:
source .venv/bin/activate

# 4. Install dependencies (PyQt6 and testing libraries)
pip install -r requirements.txt

# 5. Verify the environment by running tests
python -m pytest tests/ -v
```

---

## 🏃 Running the Application

To launch the handwriting recognition GUI:

```bash
python -m src.ui.main_window
# Or simply:
python main.py
```

### Usage Instructions
1.  **Draw:** Use your mouse to draw a number or letter on the canvas in the left panel.
2.  **Recognize:** Click the "Recognize" button to run the CV pipeline and get a prediction with confidence scores.
3.  **Train:** To add a new symbol to the knowledge base, draw it, type a label (e.g., "A", "3") in the text box, and click "Save Sample". This updates the internal library.
4.  **Clear:** Use the "Clear" button to reset the canvas and visualization results.

---


---

## 🧪 Running Tests

The project includes a robust suite of tests designed to enforce strict dimension invariance and mathematical correctness for the custom algorithms.

```bash
# Run all tests
python -m pytest tests/ -v

# Run only unit tests
python -m pytest tests/unit/ -v
```

---

## 🏗️ Architecture Quick Reference

| Question | Answer |
|----------|--------|
| **May I use NumPy?** | **No** — The core constraint of this project is using pure Python nested loops and standard math. |
| **Where does a new CV module go?** | `src/cv/` |
| **Where do UI updates go?** | `src/ui/` |
| **What type must a pixel grid be?** | `list[list[int]]` or `list[list[tuple[int, int, int]]]` |
| **How do I adjust the pen or Gaussian kernel?** | Edit the constants directly in `src/settings.py`. |


