import os
import pandas as pd
import numpy as np
import json

def adaptive_threshold(signal, window):
    pad_size = window // 2
    padded = np.pad(signal, (pad_size, pad_size), mode='edge')
    df_pad = pd.Series(padded)
    rolling_mean = df_pad.rolling(window, center=True).mean().bfill().ffill().values
    
    if len(rolling_mean) > len(signal):
        rolling_mean = rolling_mean[:len(signal)]
    elif len(rolling_mean) < len(signal):
        rolling_mean = np.append(rolling_mean, [rolling_mean[-1]] * (len(signal) - len(rolling_mean)))
    return (signal > rolling_mean).astype(int)

def dynamic_sync_decode(binary_signal, search_radius, frames_per_symbol=2.82):
    bits = []
    current_idx = frames_per_symbol / 2.0
    
    while int(current_idx) < len(binary_signal):
        idx = int(current_idx)
        bits.append(binary_signal[idx])
        
        start_search = max(0, idx + int(frames_per_symbol) - search_radius)
        end_search = min(len(binary_signal)-1, idx + int(frames_per_symbol) + search_radius)
        
        transition_found = False
        for i in range(start_search, end_search):
            if binary_signal[i] != binary_signal[i+1]:
                current_idx = i + (frames_per_symbol / 2.0)
                transition_found = True
                break
                
        if not transition_found:
            current_idx += frames_per_symbol
            
    return bits

def evaluate_consistency(bits):
    bit_string = "".join(map(str, bits))
    zero_runs = [len(s) for s in bit_string.replace('1', ' ').split()]
    one_runs = [len(s) for s in bit_string.replace('0', ' ').split()]
    max_run = max(max(zero_runs) if zero_runs else 0, max(one_runs) if one_runs else 0)
    return max_run

def main():
    print("--- Week 3 Day 19: Hyperparameter Tuning (Dynamic Sync Decoder) ---\n")
    
    target_csv = 'Dataset/Signal_V1/1LED_92bps_processed.csv'
    if not os.path.exists(target_csv):
        print("Error: Signal file not found.")
        return
        
    df = pd.read_csv(target_csv)
    signal = df['Processed_Intensity'].values
    
    # Split: Preamble/Train (0-2000), Validation (2000-5000), Test (5000+)
    # We use validation data for selection and keep test set untouched.
    val_signal = signal[2000:5000]
    print(f"Data Split: Using Validation Segment (Frames 2000 to 5000) for tuning.")
    print("Test Segment (Frames 5000+) is strictly untouched.\n")
    
    # Grid Search Parameters
    windows = [20, 50, 100]
    search_radii = [1, 2, 4]
    
    experiments = []
    best_config = None
    # We want to minimize the max_run (prevent clock drift) but keep it reasonable (not 0)
    best_score = float('inf')
    
    print("1. Systematic Grid Search Log:")
    print(f"{'Exp #':<6} | {'Window':<8} | {'Search Rad':<11} | {'Max Bit Run':<12} | {'Decoded Bits'}")
    print("-" * 65)
    
    exp_idx = 1
    for w in windows:
        for r in search_radii:
            bin_sig = adaptive_threshold(val_signal, window=w)
            bits = dynamic_sync_decode(bin_sig, search_radius=r, frames_per_symbol=2.82)
            
            max_run = evaluate_consistency(bits)
            decoded_len = len(bits)
            
            print(f"{exp_idx:<6} | {w:<8} | {r:<11} | {max_run:<12} | {decoded_len}")
            
            exp_dict = {
                "experiment_id": exp_idx,
                "window_size": w,
                "search_radius": r,
                "max_run": max_run,
                "decoded_bits_count": decoded_len
            }
            experiments.append(exp_dict)
            
            # Selection Criteria: Smallest max_run indicates tightest synchronization without dropping phase
            if max_run < best_score and max_run > 3: # Must have at least runs of 3 for valid data
                best_score = max_run
                best_config = exp_dict
                
            exp_idx += 1
            
    print("\n2. Saving Experiment Log and Tuned Candidate:")
    with open('Day_19_Experiment_Log.json', 'w') as f:
        json.dump(experiments, f, indent=4)
    print(" - Saved full log to Day_19_Experiment_Log.json")
    
    print(f"\n3. Best Validated Configuration:")
    print(f" - Best Adaptive Threshold Window: {best_config['window_size']} frames")
    print(f" - Best Dynamic Sync Search Radius: {best_config['search_radius']} frames")
    print(f" - Resulting Max Run in Validation Set: {best_config['max_run']}")
    print(" - Note: This optimized decoder is now frozen for the final blind test evaluation.")

if __name__ == "__main__":
    main()
