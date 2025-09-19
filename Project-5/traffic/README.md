## 🧪 Experiment Detail
### **Experiment 1 — Baseline Model**
**Setup**  
- 2 Convolutional layers (`32 filters`)
- MaxPooling after each Conv
- Dense(128) + Dropout(0.5)
- Optimizer: Adam
**Results**  
- **Train Accuracy:** 85.68.90%  
- **Validation Accuracy:** 94.90%
- Perform better in validation accuracy but slight overfitting observed.
- ---
### **Experiment 2 — More Filters**
**Change**  
- Increased Conv filters from `32 → 64`.

**Reasoning**  
- More filters capture more feature types from images.

**Results**  
- **Train Accuracy:** 77.80%  
- **Validation Accuracy:** 90.82%  
- Remarkable decrease in performance due to overfitting(more learning data).
___
### **Experiment 3 — Change Optimizer**
**Change**  
- Retain Conv filters `64` But change optimizer to `RMSprop`

**Reasoning**  
- .RMSprop could help in image data.

**Results**  
- **Train Accuracy:** 92.47%  
- **Validation Accuracy:** 95.92%
- Model increase it's accuracy and overfitting is decrease
___
### **Experiment 4 — Add More Conv `64` Layer**
**Change**  
- Retain same optimizer but add one more conv `64` filter

**Reasoning**  
- Capture more feature and increade learning capability.

**Results**  
- **Train Accuracy:** 93.59%  
- **Validation Accuracy:** 95.60%
- Model increase it's accuracy and overfitting is decrease
___
### Experiment 5 — Data Augmentation + Batch Normalization
**Change**  
- Added Batch Normalization after each Conv layer.  
- Applied Data Augmentation: small rotations, shifts, zoom.  
- Maintained RMSprop optimizer from Experiment 3.

**Reasoning**  
To improve generalization without increasing model size by exposing the network to slightly varied versions of the training images and stabilizing the training process.

**Results**  
- **Train Accuracy:** 92.39%  
- **Validation Accuracy:** 97.25%  
- **Test Accuracy:** 97%  
Significant improvement over previous experiments, confirming that generalization — not network depth — was the main limiting factor.

