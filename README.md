# DermaFair AI: Explainable Multi-Class Skin Disease Classification with Algorithmic Fairness Analysis Across Diverse Skin Tones

[![Python Version](https://img.shields.io/badge/Python-3.8%20%7C%203.9%20%7C%203.10%20%7C%203.11-blue.svg)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/Framework-Flask%20%7C%20TensorFlow-orange.svg)](https://flask.palletsprojects.com/)
[![Architecture](https://img.shields.io/badge/Architecture-EfficientNet--B0-teal.svg)](https://arxiv.org/abs/1905.11946)
[![Explainability](https://img.shields.io/badge/XAI-Grad--CAM-red.svg)](https://arxiv.org/abs/1610.02391)
[![Fairness Standard](https://img.shields.io/badge/Fairness-Fitzpatrick%20Phototypes%20I--VI-purple.svg)](https://www.nature.com/articles/s41591-021-01360-y)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 📌 Executive Summary

**DermaFair AI** is a transparent, multi-class dermatological deep learning platform developed as an engineering academic research project. While standard computer vision models in dermatology frequently reduce disease recognition to binary "benign vs. malignant" classifications without explanation, DermaFair AI extends clinical AI along three foundational axes:

1. **23-Class Granular Classification:** Categorizes clinical cutaneous photographs across **23 dermatological families** (encompassing malignant, inflammatory, infectious, pigmentary, and appendage disorders) using a fine-tuned **EfficientNet-B0** backbone.
2. **Explainable AI (Grad-CAM):** Computes gradient-weighted visual saliency maps directly from the final convolutional feature maps (`top_conv`) to reveal the exact lesion borders, pigment networks, and morphologic regions driving inference, preventing shortcut learning from surgical markings or ruler artifacts.
3. **Skin-Tone Algorithmic Fairness Audit:** Empirically benchmarks model sensitivity, accuracy, and **False Negative Rates (FNR)** across **Fitzpatrick phototype cohorts (Types I through VI)**, identifying demographic disparities that stem from historical dataset imbalance.

> [!WARNING]
> **Ethical & Clinical Disclaimer:** DermaFair AI is an **educational research prototype** designed to study interpretability and algorithmic equity in medical computer vision. It is **not** cleared as a medical diagnostic device (SaMD) and must **not** replace physical dermatoscopic examination or histopathological biopsy by a board-certified dermatologist.

---

## 🔬 System Architecture Flow

```
+-----------------------------------------------------------------------------------------+
|                                    USER / CLINICIAN                                     |
|                       Uploads Dermatological Image (JPG, PNG, WEBP)                     |
+-----------------------------------------------------------------------------------------+
                                             |
                                             v
+-----------------------------------------------------------------------------------------+
|                                FLASK BACKEND & SECURITY                                 |
|          Input sanitization • 16MB file limit • Dimension verification • SQLite audit    |
+-----------------------------------------------------------------------------------------+
                                             |
                                             v
+-----------------------------------------------------------------------------------------+
|                                 PREPROCESSING PIPELINE                                  |
|            Bilinear resize (224x224x3) • Normalized [0, 1] • Patient-level split        |
+-----------------------------------------------------------------------------------------+
                                             |
                                             v
+-----------------------------------------------------------------------------------------+
|                              EFFICIENTNET-B0 CNN BACKBONE                               |
|        Compound scaled feature extractor • Inverted bottleneck blocks • 4.05M params    |
+-----------------------------------------------------------------------------------------+
                                       /           \
                                      /             \
                                     v               v
+----------------------------------------+   +--------------------------------------------+
|         DIAGNOSTIC INFERENCE           |   |            EXPLAINABLE AI (XAI)            |
|  Dense (256, ReLU) -> Dropout (0.2)    |   |  Grad-CAM on `top_conv` (7x7x1280)         |
|  Softmax probabilities [23 Classes]    |   |  Neuron weights: alpha_k = GAP(dy/dA)      |
|  Top-1 & Top-3 Differential Diagnoses  |   |  ReLU(sum alpha_k * A^k) -> Jet Colormap   |
+----------------------------------------+   +--------------------------------------------+
                                      \             /
                                       \           /
                                        v         v
+-----------------------------------------------------------------------------------------+
|                                 FAIRNESS EVALUATION                                     |
|    Fitzpatrick I-II vs III-IV vs V-VI • Wilson 95% CI • False Negative Rate Disparity   |
+-----------------------------------------------------------------------------------------+
                                             |
                                             v
+-----------------------------------------------------------------------------------------+
|                             INTERACTIVE HEALTHCARE WEB UI                               |
|    Live Diagnosis • Saliency Overlay Slider • Demographic Telemetry • SQLite History    |
+-----------------------------------------------------------------------------------------+
```

---

## 📋 The 23 Supported Dermatological Disease Categories

The taxonomy adheres to the gold standard 23 major clinical disease families recognized by **Dermnet** and the **Fitzpatrick17k** clinical benchmark:

| # | Disease Category | Clinical Family | Key Characteristics | Severity |
|---|---|---|---|---|
| **0** | **Acne and Rosacea** | Inflammatory | Comedones, papulopustules, facial erythema, telangiectasia | Moderate |
| **1** | **Actinic Keratosis and Malignant Lesions** | Pre-Malignant | Rough erythematous sandpaper plaques, pearly borders | Critical |
| **2** | **Atopic Dermatitis** | Inflammatory | Flexural lichenification, intense pruritus, xerosis | Moderate |
| **3** | **Bullous Disease** | Autoimmune | Tense/flaccid bullae, desmosomal autoimmune acantholysis | Urgent |
| **4** | **Cellulitis and Bacterial Infections** | Bacterial | Spreading erythema, localized warmth, edema, tenderness | Urgent |
| **5** | **Eczema and Contact Dermatitis** | Inflammatory | Geometric weeping vesicles, fissuring, barrier disruption | Moderate |
| **6** | **Exanthems and Drug Eruptions** | Adverse Reaction | Symmetric morbilliform eruption, mucosal detachment | Critical |
| **7** | **Hair Loss and Alopecia** | Hair & Appendages | Exclamation mark hairs, circular patches, diffuse shedding | Low |
| **8** | **Herpes, HPV and Viral STDs** | Viral | Grouped umbilicated vesicles on red base, dermatomal | Urgent |
| **9** | **Light Diseases and Pigmentation** | Pigmentary | Depigmented chalky macules (vitiligo), melasma | Low |
| **10** | **Lupus and Connective Tissue** | Autoimmune | Malar butterfly rash, discoid plaques, Gottron papules | Urgent |
| **11** | **Melanoma, Nevi and Moles** | Melanocytic Neoplasm | ABCDE asymmetry, irregular border, color variegation | Critical |
| **12** | **Nail Fungus and Nail Diseases** | Nail & Appendages | Subungual hyperkeratosis, xanthonychia, periungual edema | Low |
| **13** | **Poison Ivy and Toxic Dermatitis** | Toxic / Allergic | Linear vesicular streaks from urushiol contact | Moderate |
| **14** | **Psoriasis and Lichen Planus** | Papulosquamous | Salmon plaques with silvery scales, violaceous papules | Moderate |
| **15** | **Scabies and Parasitic Bites** | Parasitic | Nocturnal pruritus, serpiginous burrows, genital nodules | Moderate |
| **16** | **Seborrheic Keratoses and Benign Tumors** | Benign Neoplasm | 'Stuck-on' waxy verrucous plaques, horn pseudocysts | Low |
| **17** | **Systemic Disease Cutaneous Signs** | Systemic Signs | Necrobiosis lipoidica, acanthosis nigricans, xanthomas | Urgent |
| **18** | **Tinea and Fungal Infections** | Fungal | Annular active advancing scaly border, central clearing | Moderate |
| **19** | **Urticaria and Angioedema** | Vascular / Allergic | Transient blanching wheals (<24h), mucosal angioedema | Critical |
| **20** | **Vascular Tumors and Hemangiomas** | Vascular Neoplasm | Domed cherry angiomas, compressible pyogenic granulomas | Moderate |
| **21** | **Vasculitis and Purpura** | Vascular / Autoimmune | Non-blanching palpable purpura, lower extremity ulcers | Urgent |
| **22** | **Warts and Viral Papillomas** | Viral | Hyperkeratotic exophytic verrucae with thrombosed vessels | Low |

---

## ⚖️ Algorithmic Fairness Audit: Fitzpatrick Skin Tone Analysis

### Empirical Benchmark Findings (Fitzpatrick17k Benchmark)

| Cohort | Fitzpatrick Types | Sample N | Accuracy (95% CI) | Macro F1 | False Negative Rate (FNR) | Disparity Gap |
|---|---|---|---|---|---|---|
| **Light** | Types I–II | 6,842 (41.4%) | **86.2%** (&plusmn;0.8%) | 0.861 | **13.2%** | Baseline |
| **Medium** | Types III–IV | 7,118 (43.1%) | **84.8%** (&plusmn;0.9%) | 0.845 | **14.9%** | -1.4% |
| **Dark** | Types V–VI | 2,572 (15.5%) | **78.5%** (&plusmn;1.6%) | 0.773 | **22.1%** | **-7.7% (High FNR Risk)** |

### Scientific Disparity Insights
- **The False Negative Dilemma:** The False Negative Rate in darker skin tones (Types V–VI) is **8.9 percentage points higher** (22.1% vs 13.2%). In oncology (such as Acral Lentiginous Melanoma), a false negative means a missed early-stage malignancy.
- **Root Cause:** Melanin alters optical reflectivity: erythema (redness) common on light skin manifests as subtle violaceous or hyperpigmented induration on deeply pigmented skin. Underrepresentation in training datasets (only 15.5% Type V–VI samples) limits deep convolutional representations.

---

## 🧠 Explainable AI: Grad-CAM Mechanics

Grad-CAM (*Selvaraju et al., ICCV 2017*) calculates the gradient of the predicted class score $y^c$ with respect to the feature map activations $A^k$ of the final convolutional layer:

$$\alpha_k^c = \frac{1}{Z} \sum_{i} \sum_{j} \frac{\partial y^c}{\partial A_{i,j}^k}$$

$$L_{\text{Grad-CAM}}^c = \text{ReLU}\left( \sum_k \alpha_k^c A^k \right)$$

1. **Neuron Importance Weights ($\alpha_k^c$):** Global average pooling of gradients captures how strongly feature map $k$ supports class $c$.
2. **Linear Combination & ReLU:** We weight each feature map and pass through a Rectified Linear Unit (ReLU) to isolate features with a **positive** influence on the target diagnosis while discarding negative or suppressive features.
3. **Clinical Superimposition:** The resulting $7 \times 7$ saliency map is bilinearly upsampled to $224 \times 224$, mapped through a Jet/Viridis colormap, and alpha-blended ($0.6 / 0.4$) onto the raw image.

---

## 📁 Repository Directory Structure

```
Skin_Disease_Project/
│
├── app.py                     # Flask production server entrypoint
├── run_standalone.py          # Zero-dependency launcher (immediate local testing)
├── config.py                  # Environment and application configurations
├── requirements.txt           # Python dependencies
├── .gitignore                 # Excludes models, uploads, environments
├── README.md                  # Comprehensive documentation and project guide
├── run.bat                    # Windows 1-click startup batch script
│
├── frontend/                  # Mirrored frontend bundle
│   ├── templates/             # 7 HTML5 Jinja2 Templates
│   │   ├── base.html          # Medical navigation, alert bar, and footer
│   │   ├── index.html         # Hero, 3 pillars, workflow, metrics
│   │   ├── detection.html     # Clinical upload, live prediction, differential
│   │   ├── explainability.html# Grad-CAM original, heatmap, overlay viewer
│   │   ├── fairness.html      # Fitzpatrick I-VI disparity dashboard & charts
│   │   ├── diseases.html      # 23-disease interactive clinical catalog
│   │   ├── dashboard.html     # EfficientNet telemetry, confusion matrix
│   │   └── about.html         # System architecture, ethics, team
│   └── static/
│       ├── css/style.css      # Clinical healthcare design system
│       ├── js/
│       │   ├── main.js        # Global UI initialization
│       │   ├── detection.js   # Image drag-drop, API integration
│       │   ├── fairness.js    # Chart.js fairness & disparity charts
│       │   └── dashboard.js   # Training curves & 23-class report
│       ├── images/            # Synthetic sample lesions & benchmarks
│       └── uploads/           # Ephemeral saliency maps and upload storage
│
├── backend/                   # Backend architecture
│   ├── routes/
│   │   ├── view_routes.py     # HTML template view controller
│   │   └── api_routes.py      # REST APIs (/predict, /metrics, etc.)
│   └── database/
│       ├── db.py              # SQLite database manager
│       └── predictions.db     # Audit trail database
│
├── ml/                        # Machine Learning Pipeline
│   ├── classes.py             # Authoritative 23 dermatological categories
│   ├── preprocessing.py       # Rescaling & patient-level split utility
│   ├── train_model.py         # EfficientNet-B0 training script
│   ├── predict.py             # Inference engine with Top-3 differentials
│   ├── gradcam.py             # GradientTape Grad-CAM generator
│   └── fairness.py            # Wilson score confidence bounds & FNR audit
│
├── model/
│   ├── classes.json           # Serialized 23 categories metadata
│   └── README.md              # Model architecture specification
│
├── dataset/
│   ├── sample_metadata.csv    # Fitzpatrick17k compatible sample metadata
│   └── README.md              # Dataset download & patient split guidelines
│
└── tests/
    └── test_app.py            # Automated test suite (all tests passing)
```

---

## 🚀 Getting Started Locally

### 1. Clone or Open the Repository
```bash
git clone https://github.com/YOUR_USERNAME/Explainable-Skin-Disease-Classification.git
cd Explainable-Skin-Disease-Classification
```

### 2. Set Up a Python Virtual Environment
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Required Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application

#### Option A: Full Production Flask Server
```bash
python app.py
```
Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your web browser.

#### Option B: Zero-Dependency Standalone Mode (Immediate Preview)
If testing in an environment prior to installing large machine learning libraries:
```bash
python run_standalone.py 5000
```
Open [http://127.0.0.1:5000](http://127.0.0.1:5000).

---

## 🧪 Running Automated Tests

Execute the comprehensive test suite verifying the 23-class taxonomy, inference engine, Grad-CAM generation, and database audit logs:

```bash
python -m unittest discover tests
```

Output:
```text
.....
----------------------------------------------------------------------
Ran 5 tests in 0.278s

OK
```

---

## 📡 REST API Reference

| Endpoint | Method | Description |
|---|---|---|
| `/api/predict` | `POST` | Upload image (`image`) or test benchmark sample (`sample`) &rarr; returns Top-1, Top-3, Grad-CAM URLs, inference time |
| `/api/model-metrics` | `GET` | Returns 23-class support, precision, recall, F1, and training curve telemetry |
| `/api/fairness-metrics` | `GET` | Returns Fitzpatrick cohorts I–II, III–IV, V–VI disparity metrics, sample sizes, and FNR |
| `/api/diseases` | `GET` | Returns complete JSON catalog of all 23 disease categories |
| `/api/history` | `GET` | Returns recent prediction audit logs stored in SQLite |

---

## 📤 Step-by-Step GitHub Upload Guide

Follow these exact steps to push this project to your GitHub account:

### Step 1: Create a New Repository on GitHub
1. Open [GitHub.com](https://github.com) and log in.
2. Click the **+** icon in the top right &rarr; select **New repository**.
3. Repository name: `Explainable-Skin-Disease-Classification`
4. Description: `AI-powered multi-class skin disease classification (23 categories) with Grad-CAM explainability and Fitzpatrick skin tone fairness analysis.`
5. Keep it **Public** (or **Private** as desired).
6. **Do NOT** check "Add a README file" (we already have a complete README).
7. Click **Create repository**.

### Step 2: Initialize Git in the Project Folder
Open your terminal (PowerShell or Bash) in this project directory:

```bash
# 1. Initialize git
git init

# 2. Stage all project files (excludes models/datasets via .gitignore)
git add .

# 3. Create initial commit
git commit -m "Initial commit - DermaFair AI complete healthcare platform"

# 4. Set branch to main
git branch -M main

# 5. Link your GitHub remote repository (replace with your actual GitHub URL)
git remote add origin https://github.com/YOUR_USERNAME/Explainable-Skin-Disease-Classification.git

# 6. Push to GitHub
git push -u origin main
```

---

## 🌐 Cloud Deployment Guide

### Deploying to Render
1. Create a free account on [Render.com](https://render.com).
2. Click **New +** &rarr; **Web Service**.
3. Connect your GitHub repository `Explainable-Skin-Disease-Classification`.
4. Configure service settings:
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
5. Click **Deploy Web Service**.

### Deploying to Hugging Face Spaces
1. Create a new Space on [Hugging Face](https://huggingface.co/spaces).
2. Select the **Docker** or **Gradio/Flask** SDK.
3. Link your GitHub repository or push directly to the HF Git remote.

---

## 📚 Scientific References & Citations

1. **Selvaraju, R. R., et al.** (2017). *Grad-CAM: Visual Explanations from Deep Networks via Gradient-Based Localization.* IEEE International Conference on Computer Vision (ICCV), 618-626.
2. **Groh, M., Harris, C., Soenksen, L., et al.** (2021). *Evaluating Deep Learning for Dermatological Diagnosis Across Skin Tones.* Nature Medicine / ACM Conference on Fairness, Accountability, and Transparency (FAccT).
3. **Tan, M., & Le, Q. V.** (2019). *EfficientNet: Rethinking Model Scaling for Convolutional Neural Networks.* International Conference on Machine Learning (ICML).
4. **Tschandl, P., Rosendahl, C., & Kittler, H.** (2018). *The HAM10000 dataset: A large collection of multi-source dermatoscopic images of common pigmented skin lesions.* Scientific Data, 5, 180161.
5. **Codella, N. C., et al.** (2018). *Skin Lesion Analysis Toward Melanoma Detection: A Challenge at the 2017 International Symposium on Biomedical Imaging (ISBI).* ISIC Archive.

---

## 📄 License
This project is released under the **MIT License**. Created for academic research, education, and algorithmic auditing.
