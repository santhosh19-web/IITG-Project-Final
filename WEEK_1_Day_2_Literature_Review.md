# Day 2: Literature Review and Candidate Methods
## Domain: Optical Camera Communication (OCC) Video Message Decoding

### 1. Core Domain Concepts
* **Computer Vision (CV):** Identifying and tracking the Light Emitting Diode (LED) or transmitting source in the video frames (Region of Interest - ROI selection). Handling varying lighting conditions and camera properties like exposure time and ISO.
* **Optical Communication:** The transmission of information using light. In OCC, the standard modulation scheme is On-Off Keying (OOK) where a "1" is represented by light ON and a "0" by light OFF.
* **Signal Processing:** Extracting the temporal intensity variation from the ROI across consecutive frames. Involves noise filtering (e.g., Moving Average, Gaussian filters), baseline wandering correction, and symbol synchronization.
* **AI-ML:** Using Machine Learning algorithms (like SVM, KNN) or Deep Learning (CNNs) to classify the extracted intensity signal as a "1" or "0", especially when ambient noise makes simple thresholding unreliable.

### 2. Method & Prior System Comparison Table

| Method / Approach | Modulation / Approach Type | Key Dataset / Input | Evaluation Metrics | Results / Pros | Limitations |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **1. Standard Thresholding (Global Shutter)** | Simple OOK | Low fps camera frames | BER, SNR | Very low computational cost; high accuracy in dark environments. | Fails heavily with ambient noise and distance fluctuations. |
| **2. Rolling Shutter (RS) OCC** | RS-OOK | CMOS camera capturing high-freq bands | Data Rate, BER | High data rates (> kbps); avoids flickering. | Requires strict camera exposure settings; distance limited. |
| **3. Adaptive Thresholding (Otsu's Method)** | CV-based Signal Processing | Moving transmitter videos | Accuracy, BER | Automatically adjusts to varying light intensities; no hardcoded threshold. | Struggles if background intensity is similar to LED intensity. |
| **4. Spatial-Temporal Matched Filters** | Signal Processing | Noisy OOK sequences | SNR improvement | Excellent noise suppression and synchronization. | Computationally heavier for real-time decoding on mobile. |
| **5. Support Vector Machine (SVM)** | ML-assisted Classifier | Labelled intensity features | F1-Score, BER | Strong boundary decision; robust against minor interference. | Requires labeled data; sensitive to scaling. |
| **6. k-Nearest Neighbors (k-NN)** | ML-assisted Classifier | Labelled signal segments | Accuracy, Inference time | Simple to implement; works well on small datasets. | Slow inference time on large test sets; sensitive to outliers. |
| **7. Convolutional Neural Net (CNN)** | Deep Learning | Raw Image Frames | Accuracy, Robustness | End-to-end transmitter localization and symbol classification. | Requires massive labeled datasets; high hardware requirements. |

### 3. Shortlisted Candidate Methods
Based on the literature review and the project constraints (offline software pipeline, OOK modulation), the following methods are shortlisted for implementation and comparison in upcoming weeks:

1. **Baseline 1: Fixed Thresholding (Signal Processing)**
   * **Approach:** Extract the mean intensity from the ROI and apply a fixed threshold value to classify 1s and 0s. 
   * **Why:** Simplest baseline to verify data extraction logic.

2. **Baseline 2: Adaptive Thresholding / Moving Average (Signal Processing)**
   * **Approach:** Apply Otsu's method or a Moving Average filter to dynamically calculate the threshold for the OOK signal over time.
   * **Why:** Robust against slow lighting changes and distance variations without needing labeled data.

3. **Advanced: ML-Assisted Symbol Classifier (AI/ML)**
   * **Approach:** Extract time-series features (mean, variance, peak intensity) from the synchronized symbols and use a lightweight ML model (e.g., Logistic Regression or SVM) for classification.
   * **Why:** Allows for better boundary definition when noise profiles are complex, assuming ground-truth labels are available or can be pseudo-labeled.
