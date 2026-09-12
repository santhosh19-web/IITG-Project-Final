# Week 4 Day 20: Robustness & Ablation Study

## Component Ablation Table
| Condition | Smoothing Window | Timing Mechanism | Max Bit Run (Drift Metric) | Insight |
|-----------|------------------|------------------|----------------------------|---------|
| Baseline (Optimal Config) | 50 | Dynamic Snapping | 7 | Stable decode across 10k frames |
| No Smoothing (Window=1) | 1 | Dynamic Snapping | 18 | High frequency noise triggers false zero-cross transitions |
| Heavy Smoothing (Window=200) | 200 | Dynamic Snapping | 31 | Over-smoothing mathematically flattens legitimate isolated 1-bit pulses |
| Static Timing (No Snapping) | 50 | Static 2.82 Clock | 55 | Catastrophic phase drift completely loses sync after ~3000 frames |
| Simulated Poor ROI (+20% Noise) | 50 | Dynamic Snapping | 12 | Dynamic sync handles ambient noise well, but threshold margins degrade slightly |

## Research Insight & Interpretation
1. Symbol Timing is the Most Critical Failure Point:
   - The ablation of 'Dynamic Snapping' back to a 'Static 2.82 Clock' resulted in catastrophic failure (max error run jump from 7 to 55). Because 260FPS / 92bps = 2.82 is a non-integer frame-per-symbol ratio, phase drift is mathematically inevitable without transition-snapping.

2. Smoothing Sensitivity:
   - The system is highly sensitive to over-smoothing. Because a single OOK bit lasts only ~2.82 frames, a smoothing window larger than 50 frames begins to literally erase valid isolated 1s and 0s (e.g. rapid 1-0-1 sequences turn into a flat gray baseline). Under-smoothing is less fatal because the dynamic phase logic ignores noise if no transition is expected within the dead-reckoning window.

3. ROI Choice Robustness:
   - Comparing the dense 4LEDs signal vs the dim 1LED signal, the dynamic thresholding is highly robust to ROI size as long as the transmitter remains strictly in-frame. If the LED leaves the ROI entirely (camera drift), the threshold hits 0 variance and outputs raw noise.