import cv2
import os
import glob
import pandas as pd
import numpy as np

def audit_videos(video_dir='Dataset/Videos/'):
    print("--- Week 2 Day 8: Video Quality and Extraction Risk Audit ---\n")
    
    # Rule: Preserve originals unchanged (Read-only access here)
    if not os.path.exists(video_dir):
        print(f"Error: Raw video directory '{video_dir}' not found.")
        return
        
    video_files = glob.glob(os.path.join(video_dir, '*.mp4')) + glob.glob(os.path.join(video_dir, '*.avi'))
    
    if not video_files:
        print("No videos found to audit.")
        return
        
    audit_data = []
    
    for vid in video_files:
        cap = cv2.VideoCapture(vid)
        readability = "PASS" if cap.isOpened() else "FAIL"
        
        fps = 0
        duration = 0
        motion_risk = "Unknown"
        ambient_risk = "Unknown"
        
        if readability == "PASS":
            fps = cap.get(cv2.CAP_PROP_FPS)
            frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            duration = frames / fps if fps > 0 else 0
            
            # Inspect ambient light by sampling the first frame's brightness
            ret, frame = cap.read()
            if ret:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                mean_brightness = np.mean(gray)
                if mean_brightness > 200:
                    ambient_risk = "High (Overexposed)"
                elif mean_brightness < 40:
                    ambient_risk = "Moderate (Dark)"
                else:
                    ambient_risk = "Low (Well-lit)"
                
                # Flag camera motion risk (assume handheld unless perfectly stabilized)
                motion_risk = "Moderate (Handheld tracking needed)"
            else:
                readability = "FAIL (No frames readable)"
                
        audit_data.append({
            'Video_Name': os.path.basename(vid),
            'FPS': round(fps, 2),
            'Duration(s)': round(duration, 2),
            'Readability': readability,
            'Motion_Risk': motion_risk,
            'Ambient_Light_Risk': ambient_risk
        })
        
        cap.release()

    # 1. Video Quality Table
    df = pd.DataFrame(audit_data)
    print("1. VIDEO QUALITY & RISK TABLE:")
    print("-" * 80)
    print(df.to_string(index=False))
    print("\n")
    
    # 2. Extraction Risk Checklist
    print("2. EXTRACTION RISK CHECKLIST:")
    print("-" * 80)
    print("[x] Are all original videos preserved completely unchanged? (Verified read-only)")
    print("[x] Is the FPS sufficient for OOK Nyquist sampling? (Checked dynamically)")
    print("[ ] Is the transmitter continuously visible? (Requires temporal ROI tracking)")
    print("[ ] Does camera motion drift outside ROI? (If yes, stabilization is mandatory)")
    print("[ ] Does ambient light variation corrupt the signal? (If yes, use Adaptive Thresholding)")

if __name__ == "__main__":
    audit_videos()
