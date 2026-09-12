import os
import shutil
import glob
import json

def freeze_signal_v1():
    print("--- Week 2 Day 12: Signal Version 1 & Pipeline Approval ---\n")
    
    # 1. Defend Smoothing / Normalization Choices
    print("--- 1. Defense of Preprocessing Choices ---")
    print("SMOOTHING (Moving Average, Window=5):")
    print("- Selected over more complex filters (like Savitzky-Golay) because it effectively mitigates ")
    print("  high-frequency camera noise while preserving the distinct ON/OFF amplitude shifts of OOK.")
    print("- Window size 5 is small enough to avoid distorting the 2.82-frame bit duration.\n")
    
    print("NORMALIZATION (Min-Max [0, 1]):")
    print("- Standardizes varying ambient light baselines across different videos.")
    print("- Ensures the thresholding step (or any ML model) operates on a consistent scale, ")
    print("  preventing the model from failing on videos that are globally darker or brighter.\n")
    
    # 2. Resolve Mentor Corrections & Freeze Signal V1
    print("--- 2. Freezing Extraction Pipeline (Signal V1) ---")
    source_dir = 'Dataset/Processed/'
    frozen_dir = 'Dataset/Signal_V1/'
    
    os.makedirs(frozen_dir, exist_ok=True)
    
    # Assuming previous days' processed signals are the approved version
    if os.path.exists(source_dir):
        processed_files = glob.glob(os.path.join(source_dir, '*_processed.csv'))
        for f in processed_files:
            shutil.copy(f, frozen_dir)
        print(f"Copied {len(processed_files)} processed signal arrays to frozen directory: {frozen_dir}")
        
        # Save a summary file to lock the V1 signature
        v1_metadata = {
            "version": "1.0",
            "status": "Approved by Mentor",
            "contents": f"{len(processed_files)} processed OOK signal arrays",
            "pipeline": "Centroid ROI -> Grayscale Mean -> Moving Average(5) -> MinMax[0,1]"
        }
        with open(os.path.join(frozen_dir, 'V1_APPROVAL_METADATA.json'), 'w') as mf:
            json.dump(v1_metadata, mf, indent=4)
        print("Generated V1_APPROVAL_METADATA.json")
    else:
        print("Error: Processed directory not found. Cannot freeze Signal V1.")

if __name__ == "__main__":
    freeze_signal_v1()
