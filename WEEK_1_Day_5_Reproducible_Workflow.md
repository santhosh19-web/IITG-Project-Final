# Day 5: Reproducible Workflow and Experiment Design
## Optical Camera Communication (OCC) Video Message Decoding

### 1. Reproducible Pipeline Flowchart
To ensure full reproducibility, the end-to-end workflow is automated from raw data ingestion to final evaluation without manual intervention per video.

```text
[Raw Data: Videos & Ground Truth]
           |
           v
[Preprocessing Pipeline]
   - Frame Extraction
   - ROI (Transmitter) Localization
   - Temporal Intensity Extraction
           |
           v
[Dataset Splitting]
   - Group-by Video Split (Train/Val/Test)
           |
           v
[Model / Method Execution]  <---(Hyperparameter Tuning)
   - Baseline: Fixed/Adaptive Thresholding
   - Advanced: ML-Assisted Classifier (e.g., SVM/CNN)
           |
           v
[Symbol Synchronization & Message Decoding]
   - Timing Recovery
   - Binary Sequence Reconstruction
   - Text Decoding (OOK Demodulation)
           |
           v
[Final Evaluation]
   - BER, Accuracy, Execution Time
```

### 2. Experiment Plan
**Baseline Method:**
* **Fixed/Adaptive Thresholding:** Extract the mean pixel intensity from the localized light source. Apply a dynamic threshold (e.g., Moving Average or Otsu's method) to classify a frame as `1` (ON) or `0` (OFF).

**Advanced Methods:**
* **ML-Assisted Symbol Classifier:** Extract statistical time-series features (variance, local peaks/troughs) and train a lightweight Machine Learning model (e.g., Support Vector Machine or Logistic Regression) to handle noisy environments where thresholding fails.

**Project-Specific Experiment:**
* **Sensitivity Analysis:** Test the robustness of both methods across:
  1. **ROI Choice:** How does a slightly misaligned bounding box affect decoding?
  2. **Smoothing:** Varying the window size of the moving average filter.
  3. **Symbol Timing:** Evaluating performance when the camera FPS fluctuates slightly vs. a perfectly stable frame rate.

### 3. Tentative Evaluation Criteria
1. **Decoded-Message Correctness:** Exact string matching accuracy of the final decoded text vs. the expected text.
2. **Bit Error Rate (BER):** Percentage of incorrectly decoded bits in the binary sequence (where reference truth is available).
3. **Synchronization Robustness:** The maximum allowable frame drift or FPS fluctuation before the decoder drops/adds a false bit.
4. **Execution Time:** Computation time required to decode a 10-second video sequence (important for offline processing scalability).

### 4. Experiment Log Template
Every experiment iteration must be recorded in this format before being accepted into the `main` branch.

| Exp ID | Method/Model | ROI Size | Smoothing Window | Hyperparameters | Val BER | Exec Time (s) | Notes & Failure Cases |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| EXP_001 | Fixed Threshold | 20x20 | None | Threshold = 127 | N/A | N/A | Initial baseline test |
| EXP_002 | Adaptive (Otsu) | 20x20 | 5-Frame MA | Window=5 | N/A | N/A | Testing moving average |
| EXP_003 | SVM Classifier | 10x10 | None | C=1.0, Kernel=RBF | N/A | N/A | Advanced method test |

### 5. Repository / Folder Structure
To maintain reproducibility, the final project workspace will strictly adhere to the following architecture:

```text
IITG-Project-Final/
│
├── data/
│   ├── raw/                 # Unchanged original video sequences
│   ├── processed/           # Extracted intensities (.csv or .npy)
│   └── ground_truth/        # Mapping and labels
│
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_preprocessing.ipynb
│   └── 03_baseline_evaluation.ipynb
│
├── src/
│   ├── preprocessing.py     # Functions for ROI and intensity extraction
│   ├── models.py            # Thresholding and ML models
│   └── evaluation.py        # BER and synchronization metrics
│
├── reports/                 
│   ├── figures/             # EDA plots and accuracy graphs
│   └── experiment_log.csv   # Living document tracking all runs
│
├── requirements.txt         # Python dependencies
└── README.md                # Reproducibility instructions
```
