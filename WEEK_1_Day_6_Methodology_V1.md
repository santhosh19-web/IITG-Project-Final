# Day 6: Methodology V1 and Data-Readiness Package
## Optical Camera Communication (OCC) Video Message Decoding

### 1. Literature & Data-Readiness Package Summary
**Literature Foundation:** Our approach builds on robust Computer Vision (CV) Region of Interest (ROI) extraction and Signal Processing (Moving Average/Otsu thresholding) methodologies. Given the problem constraint of no physical hardware integration, offline software pipelines provide the highest reliability for On-Off Keying (OOK) modulation.
**Data Readiness:**
* The raw dataset will consist of video sequences and a ground-truth mapping file.
* Before ingestion, videos will be validated for Nyquist compliance (FPS > 2x baud rate).
* A strict Group-by-Video methodology is enforced to prevent temporal data leakage.

### 2. Proposed Preprocessing, Modelling, and Evaluation Plan
**A. Preprocessing (CV):**
* **Frame Extraction:** Read video sequence frame-by-frame via OpenCV.
* **Transmitter Localization:** Identify the brightest stable region (the LED/transmitter) and extract a bounding box (ROI).
* **Intensity Extraction:** Calculate the mean pixel intensity across the ROI for every frame to generate a 1D time-series signal.

**B. Modelling (Signal Processing & AI/ML):**
* **Baseline Method:** Apply a dynamic threshold (Moving Average) to the 1D signal to classify ON (`1`) and OFF (`0`) states.
* **Advanced Method:** Extract local statistical features and train an SVM classifier to differentiate signal from complex ambient noise.

**C. Evaluation (Decoding & Metrics):**
* **Timing Recovery:** Synchronize the classified symbols to account for camera frame-drops.
* **Reconstruction:** Group binary sequences and map them to standard character encodings (e.g., ASCII).
* **Metrics:** Evaluated primarily on Bit Error Rate (BER), exact Decoded-Message Correctness, and execution time per sequence.

### 3. Split Strategy & Constraints
* **Split Strategy:** 70% Train, 15% Validation, 15% Test. The split is performed entirely at the **video level**. Shuffling individual frames is strictly prohibited due to temporal leakage.
* **Constraints:** Offline decoding only; no real-time stream decoding is required in Phase 1. Fluctuating ambient light and rolling-shutter artifacts are expected constraints that the models must mitigate.

### 4. Mentor Corrections & Updated Experiment Plan
*(The following updates have been incorporated into Methodology V1 based on mentor feedback)*

**Feedback & Corrections Received:**
1. *Constraint Check:* Ensure that the moving average window size is dynamically parameterized rather than hardcoded, as different videos may have varying camera FPS.
2. *Metric Addition:* Add "Synchronization Robustness" (measuring maximum frame drift) as a core metric alongside BER.
3. *Split Validation:* The mentor approved the video-level split strategy and explicitly warned against any cross-video frame pollution.

**Updated Experiment Plan Action Items:**
* [x] Parameterize the temporal smoothing window size in the baseline script.
* [x] Update the evaluation script to calculate maximum allowable frame drift.
* [x] Finalize `Methodology V1` and freeze the theoretical design phase. 
