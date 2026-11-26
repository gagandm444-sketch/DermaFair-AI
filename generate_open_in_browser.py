# -*- coding: utf-8 -*-
import os, sys, base64, json

# 1. Load sample images as Base64
samples = [
    ('melanoma', 'Melanoma', 'Melanoma, Nevi and Moles', 'Malignant Neoplasm', 'static/images/sample_melanoma.png', '#ef4444', 'Asymmetric dark variegated macule with irregular borders (ABCDE positive).'),
    ('psoriasis', 'Psoriasis', 'Psoriasis and Lichen Planus', 'Papulosquamous', 'static/images/sample_psoriasis.png', '#f59e0b', 'Well-demarcated salmon-pink plaque with thick silvery micaceous scale.'),
    ('eczema', 'Eczema', 'Eczema and Contact Dermatitis', 'Inflammatory', 'static/images/sample_eczema.png', '#06b6d4', 'Erythematous weeping and excoriated eczematous rash with epidermal flaking.'),
    ('acne', 'Acne & Rosacea', 'Acne and Rosacea', 'Inflammatory', 'static/images/sample_acne.png', '#ec4899', 'Facial inflammatory erythema with follicular papules, pustules, and comedones.'),
    ('bcc', 'Basal Cell Carcinoma', 'Actinic Keratosis and Malignant Lesions', 'Pre-Malignant', 'static/images/sample_bcc.png', '#dc2626', 'Pearly translucent nodule with rolled borders and arborizing telangiectasia.'),
    ('tinea', 'Tinea (Ringworm)', 'Tinea and Fungal Infections', 'Fungal Infection', 'static/images/sample_tinea.png', '#10b981', 'Annular scaly erythematous plaque with elevated active border and central clearing.'),
    ('vitiligo', 'Vitiligo', 'Light Diseases and Pigmentation', 'Pigmentation', 'static/images/sample_vitiligo.png', '#6366f1', 'Sharply demarcated chalky porcelain-white depigmented macules with hyperpigmented halo.'),
    ('urticaria', 'Urticaria (Hives)', 'Urticaria and Angioedema', 'Vascular / Allergic', 'static/images/sample_urticaria.png', '#f97316', 'Evanescent raised pale edematous wheals surrounded by intense erythematous flares.'),
    ('seborrheic', 'Seborrheic Keratosis', 'Seborrheic Keratoses and Benign Tumors', 'Benign Neoplasm', 'static/images/sample_seborrheic.png', '#854d0e', 'Waxy verrucous hyperkeratotic brown stuck-on plaque with pseudohorn cysts.'),
    ('cellulitis', 'Cellulitis', 'Cellulitis and Bacterial Infections', 'Bacterial Infection', 'static/images/sample_cellulitis.png', '#b91c1c', 'Acute diffuse hot tender spreading scarlet erythema with cutaneous edema.')
]

sample_list = []
for sid, label, dname, group, pth, col, dsc in samples:
    b64 = ''
    if os.path.exists(pth):
        with open(pth, 'rb') as f:
            b64 = 'data:image/png;base64,' + base64.b64encode(f.read())
    sample_list.append({
        'id': sid,
        'label': label,
        'disease': dname,
        'group': group,
        'color': col,
        'desc': dsc,
        'image': b64
    })

# Read classes.json
with open('model/classes.json', 'r') as f:
    diseases_data = json.load(f)

# Write out OPEN_IN_BROWSER.html
print 'Building OPEN_IN_BROWSER.html with', len(sample_list), 'samples and', len(diseases_data), 'classes...'

# Append generator logic
