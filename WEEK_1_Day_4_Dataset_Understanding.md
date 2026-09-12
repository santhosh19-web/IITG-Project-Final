# Day 4: Dataset Understanding and Risk Assessment
## Optical Camera Communication (OCC) Video Message Decoding

### 1. Expected Dataset Schema, Structure & Metadata
Before ingesting the final raw dataset, we anticipate the following structure based on the problem statement requirements for OOK video decoding:

**Expected Files:**
* `videos/`: A directory containing raw video sequences (e.g., `.mp4`, `.avi`, or `.mov`) capturing the transmitting light source.
* `ground_truth.csv` or `labels.json`: A mapping file containing the true transmitted messages for evaluation.

**Expected Columns / Targets (in the mapping file):**
* `video_filename`: Unique identifier for the video sequence.
* `transmitted_binary`: The exact sequence of 1s and 0s (e.g., `10110010`) expected to be decoded from the video.
* `decoded_message`: The human-readable text corresponding to the binary sequence.

**Important Metadata to Extract:**
* **Frames Per Second (FPS):** Crucial for determining if the Nyquist rate criteria is met relative to the transmitter's baud rate.
* **Resolution (Width x Height):** Impacts the computational cost of localization and Region of Interest (ROI) extraction.
* **Duration/Total Frames:** Required for temporal signal synchronization and mapping binary sequence length to frame counts.

---

### 2. Identified Dataset Risks
Given the nature of temporal Computer Vision and Signal Processing tasks, the following risks must be mitigated:

* **Missing/Invalid Data:** Dropped frames during video capture or videos that are completely corrupted/unreadable.
* **Annotation/Labeling Errors:** Misalignment between the provided ground truth binary sequence and the actual video (e.g., a missed start bit in the label).
* **Class Imbalance:** If the transmitted messages contain heavily skewed distributions of 1s (light ON) vs 0s (light OFF), statistical thresholding (like moving average) might bias towards the majority class.
* **Temporal Leakage:** If machine learning models are used, randomly shuffling frames across the train and test sets will cause massive data leakage. The model would "memorize" ambient background lighting rather than learning the temporal OOK signal.
* **Environmental Variance:** Differences in ambient lighting, camera distance, or slight camera shaking across different videos.

---

### 3. Correct Train/Validation/Test Split Strategy
To preserve the integrity of the evaluation and prevent temporal leakage, the dataset split **must strictly occur at the video/sequence level, never at the frame level.**
* **Preservation:** A correct split must preserve the entire contiguous temporal sequence of a video within a single set. 
* **Methodology:** If we have 20 videos, we allocate 14 videos entirely to the Training set, 3 entirely to Validation, and 3 entirely to Testing. We cannot take the first half of Video A for training and the second half for testing, as the environment and lighting parameters would leak.

---

### 4. Dataset-Risk Checklist
Before beginning the Exploratory Data Analysis (EDA) and Preprocessing, the following checklist must be cleared:

- [ ] **Completeness:** Do all videos in the dataset folder have a corresponding entry in the ground truth mapping file?
- [ ] **Playability:** Can all videos be successfully opened and read frame-by-frame using `cv2.VideoCapture`?
- [ ] **Nyquist Validation:** Is the video FPS at least twice the expected transmitter blinking frequency?
- [ ] **Temporal Integrity:** Are there any noticeable skipped or duplicated frames in the raw recordings?
- [ ] **Split Verification:** Has the data splitting logic been strictly defined to group by `video_filename`?
- [ ] **Label Sanity:** Do the lengths of the `transmitted_binary` targets mathematically align with the total frame counts and expected baud rates?
