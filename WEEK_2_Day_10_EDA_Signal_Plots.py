# Name: K.Santhosh Reddy
# Cohort: 4 Batch A2
# Mentor: Mr. Vamshi

import cv2
import os
import glob
import numpy as np
import matplotlib.pyplot as plt

def perform_eda(video_path):
    print(f"--- Week 2 Day 10: Extracting EDA for {os.path.basename(video_path)} ---\n")
    
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Failed to open {video_path}")
        return
        
    intensities = []
    frames_processed = 0
    
    # 1. Extract frames and Intensity-vs-Time
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Simple ROI Strategy: Find the absolute brightest spot (the LED)
        # Using a fixed 20x20 bounding box around the max intensity pixel
        (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(gray)
        
        x, y = maxLoc
        box_size = 10  # 20x20 total size
        
        # Ensure box is within frame boundaries
        y1 = max(0, y - box_size)
        y2 = min(gray.shape[0], y + box_size)
        x1 = max(0, x - box_size)
        x2 = min(gray.shape[1], x + box_size)
        
        roi = gray[y1:y2, x1:x2]
        
        if roi.size > 0:
            mean_intensity = np.mean(roi)
            intensities.append(mean_intensity)
        
        frames_processed += 1
        
        # For EDA purposes, just process the first 300 frames to analyze transitions clearly
        if frames_processed >= 300:
            break
            
    cap.release()
    
    # 2. Compare candidate ROI statistics and noise
    intensities = np.array(intensities)
    mean_overall = np.mean(intensities)
    std_dev = np.std(intensities)
    
    print("--- ROI Statistics & Noise ---")
    print(f"Total Frames Processed: {frames_processed}")
    print(f"Mean ROI Intensity: {mean_overall:.2f}")
    print(f"Standard Deviation (Noise/Variance): {std_dev:.2f}")
    
    # 3. Identify transitions and possible symbol periods
    # Simple thresholding based on mean to find transitions
    threshold = mean_overall
    binary_signal = (intensities > threshold).astype(int)
    
    transitions = np.sum(np.abs(np.diff(binary_signal)))
    print(f"\n--- Symbol Transitions ---")
    print(f"Identified Transitions (ON/OFF toggles): {transitions}")
    print(f"Estimated Frames per Symbol (approx): {frames_processed / max(1, transitions):.2f}")
    
    # 4. Document ambient-light/drift effects
    print("\n--- Ambient-Light & Drift Effects ---")
    # Check if the baseline drifts by comparing the first 50 frames to the last 50 frames
    first_50_mean = np.mean(intensities[:50])
    last_50_mean = np.mean(intensities[-50:])
    drift = abs(first_50_mean - last_50_mean)
    print(f"Intensity drift between start and end of sample: {drift:.2f}")
    if drift > 15:
        print("Significant ambient drift detected. Adaptive thresholding recommended.")
    else:
        print("Minimal ambient drift detected in this sample.")
        
    # Generate and save Signal Plot
    plt.figure(figsize=(10, 4))
    plt.plot(intensities, label='Raw Mean ROI Intensity', color='blue')
    plt.axhline(y=threshold, color='red', linestyle='--', label='Threshold')
    plt.title(f'Intensity vs Frame (First {frames_processed} Frames)')
    plt.xlabel('Frame Number')
    plt.ylabel('Mean Pixel Intensity (0-255)')
    plt.legend()
    plt.grid(True)
    
    plot_filename = 'EDA_signal_plot.png'
    plt.savefig(plot_filename)
    print(f"\nSaved signal plot to {plot_filename}")

if __name__ == "__main__":
    # Test with the first available video
    video_dir = 'Dataset/Videos/'
    video_files = glob.glob(os.path.join(video_dir, '*.mp4'))
    if video_files:
        perform_eda(video_files[0])
    else:
        print("No videos found to process.")
