# -*- coding: utf-8 -*-
"""
Generate sample benchmark metadata CSV conforming to Fitzpatrick17k schema.
"""
import os
import random

def generate_sample_metadata():
    out_path = os.path.join(os.path.dirname(__file__), "dataset", "sample_metadata.csv")
    d_dir = os.path.dirname(out_path)
    if not os.path.exists(d_dir):
        os.makedirs(d_dir)

    classes = [
        "Acne and Rosacea", "Actinic Keratosis and Malignant Lesions", "Atopic Dermatitis",
        "Bullous Disease", "Cellulitis and Bacterial Infections", "Eczema and Contact Dermatitis",
        "Exanthems and Drug Eruptions", "Hair Loss and Alopecia", "Herpes, HPV and Viral STDs",
        "Light Diseases and Pigmentation", "Lupus and Connective Tissue", "Melanoma, Nevi and Moles",
        "Nail Fungus and Nail Diseases", "Poison Ivy and Toxic Dermatitis", "Psoriasis and Lichen Planus",
        "Scabies and Parasitic Bites", "Seborrheic Keratoses and Benign Tumors", "Systemic Disease Cutaneous Signs",
        "Tinea and Fungal Infections", "Urticaria and Angioedema", "Vascular Tumors and Hemangiomas",
        "Vasculitis and Purpura", "Warts and Viral Papillomas"
    ]

    fitz_types = [1, 2, 3, 4, 5, 6]
    # Realistic distribution weights: Types I-IV more common, Types V-VI underrepresented
    weights = [0.20, 0.22, 0.24, 0.18, 0.10, 0.06]

    random.seed(42)
    rows = ["image_id,patient_id,fitzpatrick_scale,fitzpatrick_group,label_id,disease_class"]

    for i in range(1, 101):
        img_id = "img_{:05d}.jpg".format(i)
        pat_id = "PAT_{:03d}".format((i % 35) + 1) # ~35 unique patients for 100 images
        # Weighted choice for phototype
        r = random.random()
        cum = 0
        scale = 1
        for ft, w in zip(fitz_types, weights):
            cum += w
            if r <= cum:
                scale = ft
                break

        if scale in (1, 2):
            fg = "Fitzpatrick I-II"
        elif scale in (3, 4):
            fg = "Fitzpatrick III-IV"
        else:
            fg = "Fitzpatrick V-VI"

        lbl_id = i % 23
        d_name = classes[lbl_id]
        rows.append("{},{},{},{},{},\"{}\"".format(img_id, pat_id, scale, fg, lbl_id, d_name))

    with open(out_path, "w") as f:
        f.write("\n".join(rows) + "\n")

    print("Generated {} with {} samples.".format(out_path, len(rows) - 1))

if __name__ == "__main__":
    generate_sample_metadata()
