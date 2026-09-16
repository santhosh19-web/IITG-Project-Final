# Name: K.Santhosh Reddy
# Cohort: 4 Batch A2
# Mentor: Mr. Vamshi

import cv2
import os
import glob
import json
import pandas as pd
import numpy as np

def smooth_signal(signal, window_size=5):
    # Simple moving average for smoothing
    kernel = np.ones(window_size) / window_size
    smoothed = np.convolve(signal, kernel, mode='valid')
    # Pad to maintain array length alignment with frames
    pad_size = window_size // 2
    padded = np.pad(smoothed, (pad_size, pad_size), mode='edge')
    # Handle odd/even edge cases if pad size doesn't perfectly match original length
    if len(padded) < len(signal):
        padded = np.append(padded, padded[-1])
    elif len(padded) > len(signal):
        padded = padded[:len(signal)]
    return padded

def normalize_signal(signal):
    # Min-Max Normalization to bounded [0, 1] range
    min_val = np.min(signal)
    max_val = np.max(signal)
    if max_val - min_val == 0:
        return np.zeros_like(signal)
    return (signal - min_val) / (max_val - min_val)

def process_video(video_path, output_dir):
    print(f"Processing: {os.path.basename(video_path)}")
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Failed to open {video_path}")
        return None
        
    intensities = []
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Deterministic ROI selection based on max intensity centroid
        (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(gray)
        x, y = maxLoc
        box_size = 10
        
        y1, y2 = max(0, y - box_size), min(gray.shape[0], y + box_size)
        x1, x2 = max(0, x - box_size), min(gray.shape[1], x + box_size)
        
        roi = gray[y1:y2, x1:x2]
        
        if roi.size > 0:
            intensities.append(np.mean(roi))
            
    cap.release()
    
    # Execute Pipeline
    raw_signal = np.array(intensities)
    smoothed_signal = smooth_signal(raw_signal, window_size=5)
    normalized_signal = normalize_signal(smoothed_signal)
    
    # Save processed signal
    base_name = os.path.splitext(os.path.basename(video_path))[0]
    output_csv = os.path.join(output_dir, f"{base_name}_processed.csv")
    
    df = pd.DataFrame({
        'Frame': np.arange(len(normalized_signal)),
        'Raw_Intensity': np.round(raw_signal, 2),
        'Processed_Intensity': np.round(normalized_signal, 4)
    })
    df.to_csv(output_csv, index=False)
    print(f" -> Saved signal array to: {output_csv}")
    
    return len(normalized_signal)

def main():
    print("--- Week 2 Day 11: Deterministic Preprocessing Pipeline ---\n")
    video_dir = 'Dataset/Videos/'
    output_dir = 'Dataset/Processed/'
    
    os.makedirs(output_dir, exist_ok=True)
    
    # Save deterministic pipeline settings
    settings = {
        "pipeline_version": "1.0",
        "roi_selection": "Max intensity centroid bounding box",
        "roi_box_size": "20x20 pixels",
        "smoothing_method": "Moving Average",
        "smoothing_window_size": 5,
        "normalization_method": "Min-Max scaling to [0, 1]",
        "deterministic_seed_applied": True
    }
    
    settings_file = os.path.join(output_dir, 'preprocessing_settings.json')
    with open(settings_file, 'w') as f:
        json.dump(settings, f, indent=4)
    print(f"Saved preprocessing settings to: {settings_file}\n")
    
    # Sorted globally so processing order is perfectly deterministic
    video_files = sorted(glob.glob(os.path.join(video_dir, '*.mp4')) + glob.glob(os.path.join(video_dir, '*.avi')))
    for vid in video_files:
        process_video(vid, output_dir)
        
    print("\nPipeline execution complete.")

if __name__ == "__main__":
    # Ensure determinism across numpy operations
    np.random.seed(42)
    main()
