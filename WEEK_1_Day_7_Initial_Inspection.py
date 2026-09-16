# Name: K.Santhosh Reddy
# Cohort: 4 Batch A2
# Mentor: Mr. Vamshi

import cv2
import os
import pandas as pd
import glob

def inspect_dataset():
    print("--- Initial Dataset Inspection ---")
    video_dir = 'Dataset/Videos/'
    
    # Verify directory exists
    if not os.path.exists(video_dir):
        print(f"Error: Directory '{video_dir}' not found.")
        return
        
    video_files = glob.glob(os.path.join(video_dir, '*.mp4')) + glob.glob(os.path.join(video_dir, '*.avi'))
    print(f"Found {len(video_files)} raw video files.\n")
    
    data = []
    for vid in video_files:
        cap = cv2.VideoCapture(vid)
        if cap.isOpened():
            fps = cap.get(cv2.CAP_PROP_FPS)
            frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            
            data.append({
                'Video_Name': os.path.basename(vid),
                'FPS': round(fps, 2),
                'Total_Frames': frames,
                'Resolution': f"{width}x{height}"
            })
        cap.release()
    
    if data:
        df = pd.DataFrame(data)
        print("Dataset Metadata:")
        print(df.to_string(index=False))
    else:
        print("No metadata extracted.")

if __name__ == "__main__":
    inspect_dataset()

"""
--- EXPECTED OUTPUT ---
--- Initial Dataset Inspection ---
Found 4 raw video files.

Dataset Metadata:
     Video_Name    FPS  Total_Frames Resolution
 1LED_92bps.mp4  29.97          1052  1920x1080
2LEDs_92bps.mp4  29.97          1052  1920x1080
3LEDs_92bps.mp4  29.97          1052  1920x1080
4LEDs_92bps.mp4  29.97          1052  1920x1080
"""
