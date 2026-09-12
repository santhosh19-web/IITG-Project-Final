import os
import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def estimate_clock_and_sync(csv_path):
    print(f"--- Week 3 Day 13: Synchronisation & Clock Estimation ---")
    print(f"Analyzing: {os.path.basename(csv_path)}\n")
    
    df = pd.read_csv(csv_path)
    signal = df['Processed_Intensity'].values
    
    # 1. Estimate symbol duration using transitions (Zero-crossing logic on mean-subtracted signal)
    mean_val = np.mean(signal)
    binary_signal = (signal > mean_val).astype(int)
    
    # Find indices where the signal toggles (0 to 1 or 1 to 0)
    transitions = np.where(np.diff(binary_signal) != 0)[0]
    
    # Calculate the distance (in frames) between consecutive transitions
    transition_distances = np.diff(transitions)
    
    # The minimum distance between transitions likely represents a single bit (1 symbol)
    # We use a percentile or median of the smaller distances to avoid noise
    if len(transition_distances) > 0:
        candidate_bit_length = np.percentile(transition_distances, 10)
    else:
        candidate_bit_length = 2.82 # Fallback theoretical: 260 FPS / 92 bps
        
    print(f"--- 1. Candidate Timing & Boundaries ---")
    print(f"Total Transitions Detected: {len(transitions)}")
    print(f"Estimated Frames per Symbol (Clock Rate): {candidate_bit_length:.2f} frames")
    
    # 2. Define candidate bit boundaries (Sync Markers)
    # Start the clock from the first detected transition
    first_transition = transitions[0] if len(transitions) > 0 else 0
    num_symbols = int((len(signal) - first_transition) / candidate_bit_length)
    
    sync_markers = [first_transition + int(i * candidate_bit_length) for i in range(num_symbols)]
    
    # 3. Visualise sync markers over the signal (Zoom in on the first 150 frames)
    plt.figure(figsize=(12, 5))
    zoom_limit = min(200, len(signal))
    plt.plot(signal[:zoom_limit], label='Processed Signal', color='blue', linewidth=1.5)
    
    # Plot vertical sync markers
    for marker in sync_markers:
        if marker < zoom_limit:
            plt.axvline(x=marker, color='red', linestyle='--', alpha=0.6)
            
    plt.title(f'Symbol Synchronisation Markers (First {zoom_limit} Frames)')
    plt.xlabel('Frame Number')
    plt.ylabel('Normalized Intensity')
    plt.legend(['Processed Signal', 'Candidate Bit Boundary'])
    plt.grid(True)
    
    plot_path = 'Sync_Markers.png'
    plt.savefig(plot_path)
    print(f"\n--- 2. Visualisation ---")
    print(f"Saved synchronization visualization to {plot_path}")
    
    # 4. Document uncertainty / alternate hypotheses
    print("\n--- 3. Uncertainty & Alternate Hypotheses ---")
    print("Uncertainty 1: Rolling Shutter Effect.")
    print("  - Hypothesis: CMOS cameras scan line-by-line. High-frequency LED toggles may cause partial exposure bands within a single frame, blurring the exact transition frame.")
    print("Uncertainty 2: Frame Drops / Clock Drift.")
    print("  - Hypothesis: If the camera drops a frame, the strict addition of ~2.82 frames per symbol will drift completely out of phase. A Phase-Locked Loop (PLL) or dynamic transition-snapping may be required later.")
    print("Uncertainty 3: Non-Integer Boundaries.")
    print("  - Hypothesis: 260 / 92 = 2.82. Since frames are discrete integers, sampling exactly at the bit center requires dynamic interpolation rather than static indexing.")
    
if __name__ == "__main__":
    target_csv = 'Dataset/Signal_V1/1LED_92bps_processed.csv'
    if os.path.exists(target_csv):
        estimate_clock_and_sync(target_csv)
    else:
        # Fallback to grab any processed CSV
        files = glob.glob('Dataset/Signal_V1/*_processed.csv')
        if files:
            estimate_clock_and_sync(files[0])
        else:
            print("Error: No processed signals found in Dataset/Signal_V1/")
