# Problem Understanding Note: OCC Video Message Decoding

## 1. Technical Problem Statement Rewrite
The objective of this project is to decode digital messages transmitted via Optical Camera Communication (OCC). The transmitting source uses an On-Off Keying (OOK) modulation scheme to encode binary data into temporal light-intensity variations. Our goal is to develop a robust, offline, software-based computer vision and signal processing pipeline. This pipeline must process recorded video data to localize the transmitting light source, extract the time-series intensity signals across frames, synchronize the symbol timing, and ultimately reconstruct the original transmitted binary sequence and text message, all without requiring any physical hardware integration.

## 2. Inputs and Outputs
**Inputs:**
- Raw video sequences capturing the transmitting light source.
- Video frames containing the temporal light-intensity variations (the physical layer signals).

**Outputs/Targets:**
- The intermediate extracted temporal light-intensity variation time-series signal.
- The decoded transmitted binary sequence (1s and 0s).
- The final reconstructed human-readable decoded message.

## 3. End-to-End Software Pipeline

```text
[Raw Video Input]
       |
       v
[Frame Extraction]
       |
       v
[Transmitter Localization / ROI Selection]
       |
       v
[Temporal Light Intensity Extraction]
       |
       v
[Signal Preprocessing & Smoothing]
       |
       v
[Thresholding / Symbol Classification]
       |
       v
[Symbol Synchronization & Timing Recovery]
       |
       v
[Binary Sequence Reconstruction]
       |
       v
[Message Decoding]
       |
       v
[Performance Evaluation & BER Calculation]
```

**Success Criteria:**
- **Accuracy:** High accuracy in decoding the final message, primarily measured by Bit Error Rate (BER) when reference ground truth is available.
- **Robustness:** The pipeline must handle varying Region of Interest (ROI) selections, noise, and ambient lighting fluctuations without complete failure.
- **Synchronization:** Accurate timing recovery to prevent symbol drift over time.
- **Reproducibility:** The software pipeline must be completely reproducible, modular, and not heavily hardcoded for a single specific video.

## 4. Technical Questions & Assumptions

**Assumptions:**
1. **Sampling Rate:** The camera's frame rate is strictly greater than the Nyquist rate (at least twice the transmitter's blinking frequency) to avoid aliasing and reliably capture the OOK states.
2. **Spatial Stability:** The transmitting light source remains relatively stationary within the camera's field of view throughout the duration of the video.
3. **Modulation Scheme:** The modulation is strictly standard On-Off Keying (OOK) without complex pulse-width modulation (PWM) or multi-level intensity modulation.

**Technical Questions Requiring Clarification:**
4. What is the expected transmission baud rate (blinking frequency) of the light source, and is it uniform across all provided videos in the dataset?
5. Are there significant rolling-shutter effects present in the videos (resulting in bright/dark bands across a single frame), and should our pipeline utilize these effects for higher-frequency decoding?
6. Does the transmitted binary sequence include standard start/stop bits, preambles, or synchronization headers to help identify the beginning of a message?
7. What character encoding standard (e.g., ASCII, UTF-8, Manchester encoding) is used to map the binary sequences to the final decoded text messages?
8. Do the video environments contain competing ambient light sources, reflections, or optical noise that might severely interfere with transmitter localization and intensity extraction?
