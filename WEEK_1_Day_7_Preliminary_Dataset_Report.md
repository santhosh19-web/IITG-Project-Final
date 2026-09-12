# Day 7: Preliminary Dataset Report
## Optical Camera Communication (OCC) Video Message Decoding

### 1. Raw-Data Archive Strategy
* **Preservation:** A strictly read-only raw copy of the dataset will be maintained in the `/data/raw/` folder. All preprocessing scripts will only read from this folder and write outputs to `/data/processed/`.
* **Versioning:** The original `.zip` or archive file provided by the faculty will be kept untouched as a backup to ensure zero accidental modification during the Exploratory Data Analysis (EDA) phase.

### 2. Initial Inspection & Coverage
*(This section summarizes the findings from the initial inspection notebook once the dataset is fully downloaded and parsed)*
* **Files Inspected:** Video sequences (`.mp4`/`.avi`) and mapping files (`.csv`).
* **Metadata Checks:** The generated Jupyter Notebook validates FPS (to ensure Nyquist compliance), resolution, and total video duration against expected parameters.
* **Target Coverage:** Checking the label file to ensure every video has a corresponding true transmitted binary sequence and decoded text message.

### 3. Inconsistencies and Invalid Data
* **Missing Data Risk:** The inspection notebook includes checks to identify videos with 0 bytes or videos where `cv2.VideoCapture` fails to open the stream.
* **Duplicates:** The notebook checks for duplicate `video_filename` entries in the ground-truth mapping to prevent double-counting in evaluation.
* **Class Imbalance:** By parsing the binary targets (e.g., `10110010`), the distribution of `1`s vs `0`s will be plotted to flag extreme imbalances that could disrupt moving average threshold calculations.

### 4. Next Steps
* Execute the generated Jupyter Notebook (`WEEK_1_Day_7_Initial_Inspection.ipynb`) locally once the dataset download finishes.
* Document any video corruption or label mismatch directly into the Experiment Log before starting Week 2's intensive preprocessing.
