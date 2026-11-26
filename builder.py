# -*- coding: utf-8 -*-
"""
Builder script to generate OPEN_IN_BROWSER.html
A 100% self-contained standalone prototype for DermaFair AI with DermaBot AI and dynamic image analysis.
"""
import os, sys, base64, json

# 1. Load samples
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

# 2. Load diseases
with open('model/classes.json', 'r') as f:
    diseases = json.load(f)

# Clinical guidance mapping for all 23 diseases
GUIDANCE = {
    "Acne and Rosacea": {
        "healing": "Apply 2% Salicylic Acid (BHA) for clogged pores, 2.5-5% Benzoyl Peroxide for inflammatory bacterial papules, or 10% Azelaic Acid to reduce erythema and rosacea flushing. Use soothing Zinc PCA and Niacinamide 2-4%. Avoid pore-clogging comedogenic oils and harsh physical scrubs.",
        "morning": "1. Gentle pH-balanced foaming cleanser -> 2. Niacinamide / Azelaic acid serum -> 3. Oil-free gel moisturizer with ceramides -> 4. Broad-spectrum SPF 50+ mineral/hybrid sunscreen (non-comedogenic).",
        "evening": "1. Gentle double cleanse (micellar water + cleanser) -> 2. Treatment: Topical Retinoid (Adapalene 0.1%) or Benzoyl Peroxide 2.5% spot treatment -> 3. Lightweight barrier repair cream.",
        "diet": "Reduce high-glycemic index foods and skim dairy spikes which stimulate IGF-1 sebum production. Eat antioxidant-rich berries, green tea, and omega-3 fatty acids (salmon, walnuts, flaxseed). Hydrate with 2.5L water daily.",
        "red_flags": "Deep painful nodulocystic lesions, scarring tracts, sudden widespread outbreak, or burning eyes / eyelid inflammation (ocular rosacea requires ophthalmic evaluation)."
    },
    "Actinic Keratosis and Malignant Lesions": {
        "healing": "Pre-cancerous and malignant lesions require formal dermatological evaluation. Medical treatments include prescription topical 5-Fluorouracil (5-FU), Imiquimod cream, photodynamic therapy (PDT), or surgical cryotherapy / Mohs micrographic excision.",
        "morning": "1. Ultra-gentle non-irritating cleanser -> 2. High-dose broad-spectrum SPF 50+ with high UVA protection (essential) -> 3. Broad-brimmed sun-protective hat and UV sunglasses outdoors.",
        "evening": "1. Gentle lukewarm water cleanse -> 2. Dermatologist-prescribed therapeutic agent as directed -> 3. Barrier-supporting squalane or ceramide soothing cream.",
        "diet": "Antioxidant-rich Mediterranean diet with polyphenol-rich green tea, leafy greens, tomatoes (lycopene for photoprotection), and nicotinamide (Vitamin B3 500mg daily shown to reduce non-melanoma skin cancer recurrence).",
        "red_flags": "Rapid induration, persistent non-healing sore older than 6 weeks, spontaneous ulceration or bleeding, pearly translucent nodule with telangiectasia."
    },
    "Atopic Dermatitis": {
        "healing": "Focus on stratum corneum barrier repair: Ceramide-dominant emollients applied within 3 minutes of bathing (the 'soak and seal' method). For active flares, low-to-mid potency topical corticosteroids or topical calcineurin inhibitors (Tacrolimus/Pimecrolimus) as prescribed.",
        "morning": "1. Soap-free, fragrance-free gentle hydrating wash -> 2. Hyaluronic acid on damp skin -> 3. Thick ceramide barrier cream -> 4. Physical mineral SPF 50+ (Zinc Oxide is soothing).",
        "evening": "1. Lukewarm 5-10 minute bath/shower -> 2. Pat dry gently (leave skin damp) -> 3. Apply prescribed anti-inflammatory ointment to active plaques -> 4. Generous occlusive barrier balm (petrolatum/ceramides) all over.",
        "diet": "Anti-inflammatory diet rich in omega-3 fatty acids, probiotics (fermented kefir/yogurt), and quercetin (apples, red onions). Avoid known individual dietary allergen triggers.",
        "red_flags": "Superimposed painful vesicular clusters (Eczema Herpeticum is a medical emergency), yellow honey-colored weeping crusts (secondary Staph impetigo), or fever."
    },
    "Bullous Disease": {
        "healing": "Autoimmune blistering dermatoses (Pemphigoid/Pemphigus) require urgent systemic dermatological management (systemic corticosteroids, Rituximab, Dapsone). Keep blisters clean, intact whenever possible, and apply non-adherent silicone dressings.",
        "morning": "1. Sterile saline or chlorhexidine gentle rinse -> 2. Non-adherent sterile dressing over de-roofed blisters -> 3. Prescribed systemic medication.",
        "evening": "1. Careful dressing change avoiding shear stress -> 2. Prescribed topical antiseptic or steroid ointment -> 3. Protective soft loose cotton clothing.",
        "diet": "Soft, non-acidic, room-temperature foods if oral mucosal erosions are present. High protein diet to support re-epithelialization of de-roofed skin.",
        "red_flags": "Widespread epidermal peeling, Nikolsky sign positive (skin slides off with light rubbing), mouth/throat blisters impairing swallowing or breathing (immediate emergency department admission required)."
    },
    "Cellulitis and Bacterial Infections": {
        "healing": "Bacterial infection of deep dermis and subcutaneous tissues requires prompt oral or intravenous antibiotics (e.g., Cephalexin, Flucloxacillin, or Clindamycin). Elevate affected limb to reduce edema. Mark borders with a pen to track spreading.",
        "morning": "1. Strict hand hygiene -> 2. Take prescribed antibiotics on schedule with water -> 3. Keep area elevated and rested -> 4. Clean cool compresses for pain relief.",
        "evening": "1. Inspect margins against pen line -> 2. Take evening antibiotic dose -> 3. Elevate limb on two pillows during sleep -> 4. Avoid tight bandages.",
        "diet": "Hydration with electrolyte-rich fluids, Vitamin C, and zinc to support immune phagocytosis and tissue healing. Complete entire prescribed antibiotic course.",
        "red_flags": "Rapidly advancing redness, systemic fever/chills, bullae formation, crepitus (crackling beneath skin), or confusion (signs of sepsis or necrotizing fasciitis require immediate ER evaluation)."
    },
    "Eczema and Contact Dermatitis": {
        "healing": "Identify and remove offending allergen or irritant (fragrance, nickel, harsh detergents, latex). Apply cool compresses and over-the-counter 1% Hydrocortisone cream for 5-7 days. Restore lipid mantle with ceramide-cholesterol-fatty acid barrier creams.",
        "morning": "1. Rinse with lukewarm water or soapless cleanser -> 2. Apply soothing colloidal oatmeal or panthenol (Vitamin B5) serum -> 3. Rich barrier cream -> 4. Fragrance-free mineral sunscreen.",
        "evening": "1. Very gentle cleanser -> 2. Apply thin layer of hydrocortisone or soothing zinc cream to affected areas -> 3. Seal with thick ointment (pure petrolatum or ceramide ointment) under cotton gloves/socks if hands/feet.",
        "diet": "Hydration and anti-inflammatory nutrition with turmeric, ginger, and wild-caught fish. Avoid alcohol and spicy foods that cause cutaneous vasodilatation during flares.",
        "red_flags": "Severe facial or periorbital edema, widespread blistering, pustular secondary infection, or occupational incapacitation."
    },
    "Exanthems and Drug Eruptions": {
        "healing": "Immediately review all recently started prescription medications, supplements, and OTC drugs (started within past 2-8 weeks). Discontinue suspected causative drugs under medical supervision. Calamine lotion, oral non-sedating antihistamines (Cetirizine) for pruritus.",
        "morning": "1. Cool shower with soap-free cleanser -> 2. Calamine or colloidal oatmeal soothing lotion -> 3. Loose cotton clothing.",
        "evening": "1. Cool compress -> 2. Oral antihistamine to prevent nocturnal scratch cycles -> 3. Emollient moisturizing.",
        "diet": "Bland, easily digestible diet with plenty of fluids to maintain renal excretion of drug metabolites.",
        "red_flags": "Mucosal erosion (lips, eyes, genitals), facial edema, skin pain, epidermal detachment (Stevens-Johnson Syndrome / TEN), fever, or lymphadenopathy (DRESS syndrome - emergency!)."
    },
    "Hair Loss and Alopecia": {
        "healing": "Non-scarring: Topical Minoxidil 5% for androgenetic thinning, intralesional triamcinolone injections by dermatologist for Alopecia Areata, stress reduction and nutritional correction (ferritin, Vitamin D, zinc) for Telogen Effluvium.",
        "morning": "1. Gentle scalp massage with fingertips -> 2. Sulfate-free anti-hairfall shampoo (Ketoconazole 2% 2-3x/week) -> 3. Scalp UV sunscreen.",
        "evening": "1. Apply Minoxidil 5% solution/foam to dry scalp -> 2. Peptide scalp serum -> 3. Silk/satin pillowcase to minimize friction breakage.",
        "diet": "Adequate daily protein (collagen, eggs, lentils), iron-rich leafy greens, pumpkin seeds (zinc), biotin, and Vitamin D3 supplementation.",
        "red_flags": "Follicular erythema, scale, loss of follicular openings (scarring cicatricial alopecia requires urgent dermatologist biopsy to prevent permanent baldness)."
    },
    "Herpes, HPV and Viral STDs": {
        "healing": "For Herpes simplex/zoster: Early prescription oral antiviral therapy (Valacyclovir, Acyclovir) initiated within 72 hours of symptom onset drastically shortens duration and prevents post-herpetic neuralgia. Keep lesions dry and clean.",
        "morning": "1. Gently cleanse with saline or chlorhexidine -> 2. Take prescribed oral antiviral with water -> 3. Apply cool drying compresses (Domeboro solution).",
        "evening": "1. Cleanse gently, avoid touching lesions with bare hands -> 2. Apply zinc oxide drying paste -> 3. Rest and sleep.",
        "diet": "Diet high in L-lysine (fish, chicken, beans) and lower in L-arginine (nuts, chocolate) during active viral flares. Boost Vitamin C and zinc.",
        "red_flags": "Lesions near the tip or side of nose and eye (Hutchinson sign indicates Herpes Zoster Ophthalmicus - risk of blindness, see ophthalmologist immediately) or immunocompromised patients."
    },
    "Light Diseases and Pigmentation": {
        "healing": "For Vitiligo: Topical calcineurin inhibitors, topical JAK inhibitors (Ruxolitinib), and targeted narrowband UVB phototherapy. For Melasma/PIH: Strict mineral sunscreen (iron oxide blocks visible light), Azelaic acid 10-20%, Tranexamic acid, and Vitamin C.",
        "morning": "1. Gentle brightening cleanser -> 2. Vitamin C (L-ascorbic acid 15%) + Ferulic acid -> 3. Tinted mineral sunscreen with Iron Oxides and SPF 50+ (crucial for pigment).",
        "evening": "1. Double cleanse -> 2. Azelaic acid 10% or Tranexamic acid 3% serum -> 3. Ceramide night cream with Niacinamide 4% (inhibits melanosome transfer).",
        "diet": "Antioxidant-dense nutrition: citrus fruits, carrots/sweet potatoes (beta-carotene), spinach, and polyphenol-rich green tea. Supplement Vitamin D3 if avoiding sun exposure.",
        "red_flags": "Sudden appearance of dark, variegated, asymmetric spots with irregular borders, or rapidly advancing depigmentation accompanied by autoimmune thyroid symptoms."
    },
    "Lupus and Connective Tissue": {
        "healing": "Strict photoprotection is mandatory (UV radiation triggers cutaneous and systemic lupus flares). Prescription topical corticosteroids, topical calcineurin inhibitors, and systemic Hydroxychloroquine managed by rheumatologist/dermatologist.",
        "morning": "1. Ultra-gentle cleanser -> 2. Prescribed non-steroidal topical agent -> 3. Broad-spectrum SPF 50+ with high UVA-PF rating reapplied every 2 hours.",
        "evening": "1. Lukewarm cleanse -> 2. Calming barrier repair cream containing madecassoside or ceramides -> 3. Avoid temperature extremes.",
        "diet": "Anti-inflammatory Mediterranean diet. Avoid alfalfa sprouts and echinacea (which stimulate immune flare-ups). Ensure adequate Vitamin D3.",
        "red_flags": "Chest pain, shortness of breath, dark urine, severe joint swelling, or digital ulceration with color changes (Raynaud phenomenon with tissue necrosis)."
    },
    "Melanoma, Nevi and Moles": {
        "healing": "Malignant melanoma CANNOT be treated with creams or home remedies. Suspicious pigmented lesions require immediate surgical excisional biopsy by a board-certified dermatologist or surgical oncologist. Early detection at Stage I has >99% 5-year survival.",
        "morning": "1. Gentle cleansing -> 2. Daily broad-spectrum SPF 50+ to all exposed skin -> 3. Monthly full-body skin self-exam using ABCDE criteria.",
        "evening": "1. Cleanse gently -> 2. Hydrate skin normally -> 3. Avoid picking, scratching, or applying caustic home remedies to any mole.",
        "diet": "Protective antioxidant nutrition rich in selenium, Vitamin E, beta-carotene, and polyphenols. Maintain normal Vitamin D levels.",
        "red_flags": "ABCDE: Asymmetry, Border irregularity, Color variegation (black, brown, blue, red, white), Diameter >6mm, Evolving (changing size, shape, elevation, bleeding, itching, or 'ugly duckling' appearance) - URGENT dermatological biopsy required."
    },
    "Nail Fungus and Nail Diseases": {
        "healing": "Onychomycosis: Prescription oral Terbinafine (often 6-12 weeks under liver monitoring) or topical lacquers (Amorolfine, Ciclopirox, Efinaconazole) for mild distal cases. Keep feet thoroughly dry, disinfect footwear with antifungal spray.",
        "morning": "1. Wash and thoroughly towel-dry toes -> 2. Apply topical antifungal nail lacquer or antifungal powder in socks -> 3. Wear breathable cotton/wool socks.",
        "evening": "1. File thickened nail plate down gently with disposable emery board -> 2. Apply antifungal solution to nail bed and hyponychium -> 3. Allow to dry completely.",
        "diet": "Biotin, zinc, and high-quality protein to support new healthy keratinized nail plate outgrowth. Adequate iron intake.",
        "red_flags": "Single dark longitudinal brown/black stripe on nail plate (longitudinal melanonychia - rule out subungual melanoma), or spreading periungual erythema, throbbing pain, and pus (acute paronychia/felon)."
    },
    "Poison Ivy and Toxic Dermatitis": {
        "healing": "Immediately wash exposed skin within 30 minutes with soap and cold water or specialized urushiol wash (Zanfel/Tecnu) to remove plant resins. Cool astringent compresses (aluminum acetate / Domeboro), calamine lotion, and oral antihistamines.",
        "morning": "1. Cool shower (never hot water, which spreads resins) -> 2. Calamine lotion to weeping vesicular streaks -> 3. Clean light cotton gauze.",
        "evening": "1. Cool compress for 15 minutes -> 2. High-potency topical steroid cream (if prescribed) -> 3. Oral Diphenhydramine or Cetirizine for nocturnal sleep comfort.",
        "diet": "Cool hydrating fluids, fresh fruits, vegetables. Avoid touching contaminated gardening tools, pets, or outdoor footwear until washed.",
        "red_flags": "Facial or periorbital swelling, involvement of genital area, rash covering >25% of body surface area, or inhalation of smoke from burning brush (medical emergency)."
    },
    "Psoriasis and Lichen Planus": {
        "healing": "Keratolytic agents (Salicylic acid 3-5%, Urea 10-20%) to dissolve micaceous scale, followed by topical high-potency corticosteroids combined with Vitamin D3 analogues (Calcipotriol). Systemic biologics (IL-17, IL-23, TNF inhibitors) for moderate-severe disease.",
        "morning": "1. Moisturizing shower with soap-free oil wash -> 2. Keratolytic urea/salicylic cream on thick plaques -> 3. Rich emollient ointment -> 4. Sun exposure (controlled 10-15 mins natural UV).",
        "evening": "1. Lukewarm bath with Epsom salts -> 2. Apply prescribed Calcipotriol / topical corticosteroid to plaques -> 3. Occlusive barrier balm (petrolatum).",
        "diet": "Anti-inflammatory Mediterranean diet with omega-3 fatty acids (reduces systemic inflammation). Avoid alcohol and smoking which are known major psoriasis flare triggers. Maintain healthy BMI.",
        "red_flags": "Sudden eruption of sterile pustules covering large body surface areas with fever (von Zumbusch Generalized Pustular Psoriasis) or red peeling over >90% body (Erythrodermic Psoriasis) - requires emergency hospitalization."
    },
    "Scabies and Parasitic Bites": {
        "healing": "Prescription topical Permethrin 5% cream applied from jawline to soles of feet, left on for 8-14 hours, and repeated in 7 days. Oral Ivermectin for resistant or institutional outbreaks. Wash all clothing, towels, and bedding in hot water (60°C) and dry on high heat.",
        "morning": "1. Shower off Permethrin cream after overnight application -> 2. Apply soothing calamine lotion -> 3. Put on freshly laundered clothes.",
        "evening": "1. Cool compress -> 2. Oral antihistamine to suppress severe nocturnal itching -> 3. Trim fingernails short to prevent bacterial superinfection from scratching.",
        "diet": "Normal balanced diet. All household members and intimate contacts must be treated simultaneously, regardless of whether they have symptoms.",
        "red_flags": "Bulls-eye target rash with expanding red ring (Erythema Migrans indicates Lyme Disease), secondary honey-colored impetigo infection, or thick crusted scales (Norwegian/Crusted scabies in immunocompromised patients)."
    },
    "Seborrheic Keratoses and Benign Tumors": {
        "healing": "Seborrheic keratoses are completely benign and do not require medical intervention unless irritated by clothing friction or cosmetically bothersome. Dermatologist treatments include cryotherapy with liquid nitrogen, light electrodessication, or curettage.",
        "morning": "1. Normal gentle cleansing -> 2. Regular hydration -> 3. Daily broad-spectrum SPF 50+.",
        "evening": "1. Normal cleansing -> 2. Mild exfoliation with lactic acid or urea cream -> 3. Do NOT attempt to scratch, shave, or burn off stuck-on lesions at home.",
        "diet": "Healthy balanced diet rich in micronutrients and antioxidants.",
        "red_flags": "Sudden explosive eruption of dozens or hundreds of seborrheic keratoses over a few weeks (Sign of Leser-Trélat - potential paraneoplastic marker of internal malignancy), or bleeding/ulceration."
    },
    "Systemic Disease Cutaneous Signs": {
        "healing": "Cutaneous signs (e.g. Acanthosis Nigricans, Necrobiosis Lipoidica, Xanthomas) indicate underlying systemic endocrine, metabolic, or vascular pathology (Insulin resistance, diabetes, hyperlipidemia). Primary focus is medical management of the internal disorder.",
        "morning": "1. Gentle cleansing -> 2. Urea 10-20% or Ammonium Lactate 12% lotion to velvety hyperkeratotic zones -> 3. Broad-spectrum SPF 50+.",
        "evening": "1. Lukewarm wash -> 2. Prescribed topical agent or mild retinol -> 3. Barrier hydration cream.",
        "diet": "Strict low-glycemic, whole-food diet to reverse insulin resistance and lower HbA1c. Reduce refined carbohydrates and saturated fats. Daily exercise 30 minutes.",
        "red_flags": "Palpable non-blanching purple spots (vasculitis), rapidly enlarging painful necrotic ulcers with ragged undermined purple edges (Pyoderma Gangrenosum), or diabetic foot ulcers with numbness."
    },
    "Tinea and Fungal Infections": {
        "healing": "Topical antifungal creams containing Terbinafine 1%, Clotrimazole 1%, Ketoconazole 2%, or Miconazole applied twice daily for 2-4 weeks (continue 1 week after rash clears). Keep affected skin thoroughly clean, dry, and cool. Wear loose breathable cotton garments.",
        "morning": "1. Wash area with antibacterial/antifungal zinc pyrithione bar -> 2. Dry thoroughly with a separate clean towel -> 3. Apply Terbinafine cream 2cm beyond the active red border.",
        "evening": "1. Cleanse and dry thoroughly -> 2. Second application of antifungal cream -> 3. Antifungal powder in shoes/groin folds.",
        "diet": "Lower sugar and refined carbohydrate intake. Support immune health with garlic, probiotics, and zinc.",
        "red_flags": "Fungal infection involving scalp with hair loss and boggy swelling (Kerion), fungal invasion deep into hair follicles (Majocchi Granuloma), or infection not responding to 2 weeks of OTC topical antifungals."
    },
    "Urticaria and Angioedema": {
        "healing": "First-line therapy: High-dose second-generation non-sedating H1 antihistamines (Cetirizine 10-20mg, Fexofenadine 180mg, Levocetirizine, or Bilastine). Avoid non-steroidal anti-inflammatory drugs (NSAIDs, Aspirin, Ibuprofen) which can provoke mast cell degranulation.",
        "morning": "1. Cool lukewarm shower -> 2. Morning H1 antihistamine dose as prescribed -> 3. Wear loose, light, non-restrictive clothing.",
        "evening": "1. Cool compress to itchy wheals (avoid ice direct to skin) -> 2. Evening antihistamine dose -> 3. Keep bedroom cool and well-ventilated.",
        "diet": "Low-histamine diet during acute flares (avoid aged cheeses, cured meats, wine, fermented foods, canned fish). Keep a food-and-symptom diary to trace specific triggers.",
        "red_flags": "Swelling of lips, tongue, throat, difficulty breathing, wheezing, dizziness, or lightheadedness (Anaphylaxis is an immediate life-threatening emergency requiring intramuscular Epinephrine / 911)."
    },
    "Vascular Tumors and Hemangiomas": {
        "healing": "Cherry angiomas and benign hemangiomas require no medical therapy unless bleeding or cosmetically undesirable. Dermatologist treatments include pulsed dye laser (PDL), electrodessication, or shave excision. Infantile hemangiomas may be treated with oral Propranolol.",
        "morning": "1. Gentle cleansing with minimal friction -> 2. Sun protection SPF 50+.",
        "evening": "1. Gentle cleanse -> 2. Hydration -> 3. Avoid scratching or picking at vascular papules to prevent persistent bleeding.",
        "diet": "Standard healthy balanced nutrition.",
        "red_flags": "Lesion that bleeds spontaneously and profusely upon trivial trauma (Pyogenic Granuloma), rapid painful enlargement, or periorbital lesions obstructing vision in infants."
    },
    "Vasculitis and Purpura": {
        "healing": "Requires comprehensive medical investigation (urinalysis for renal involvement, CBC, inflammatory markers, autoimmune serologies). Rest, leg elevation, compression stockings (for mild cases), and systemic corticosteroids or immunosuppressive agents as prescribed by specialist.",
        "morning": "1. Gentle wash avoiding friction -> 2. Apply gentle barrier cream -> 3. Leg elevation whenever sitting -> 4. Wear graduated compression stockings if prescribed.",
        "evening": "1. Lukewarm rinse -> 2. Soft cotton protective socks/dressings -> 3. Elevate legs on pillows overnight.",
        "diet": "Hydration and anti-inflammatory whole-food diet. Avoid prolonged standing or walking during active purpuric flares.",
        "red_flags": "Abdominal pain, blood in urine or stools, persistent fevers, numbness/tingling/weakness in feet or hands (mononeuritis multiplex), or rapidly spreading necrotic ulcers."
    },
    "Warts and Viral Papillomas": {
        "healing": "Salicylic acid 17-40% topical paint applied daily after soaking in warm water and paring down hyperkeratotic scale with disposable emery board. Dermatologist options include liquid nitrogen cryotherapy, Cantharidin, Candida antigen immunotherapy, or pulsed-dye laser.",
        "morning": "1. Wash hands with soap -> 2. Keep wart covered with adhesive bandage to prevent viral transmission and auto-inoculation -> 3. Do not bite or pick.",
        "evening": "1. Soak wart in warm water for 5 minutes -> 2. Gently pare dead skin with disposable board -> 3. Apply Salicylic acid paint precisely on lesion -> 4. Cover with tape overnight.",
        "diet": "Immune-boosting nutrition: Vitamin C, zinc, and Vitamin A to help cell-mediated immunity fight HPV.",
        "red_flags": "Anogenital warts (HPV strains with oncogenic potential require gynecologic/urologic exam), lesions that bleed easily or fail to respond after 12 weeks of treatment."
    }
}

# Attach guidance to diseases
for d in diseases:
    nm = d['name']
    g = GUIDANCE.get(nm, {})
    d['healing'] = g.get('healing', 'Consult a dermatologist for individualized therapeutic management.')
    d['morning'] = g.get('morning', 'Gentle cleanser -> Hydrating serum -> Barrier moisturizer -> SPF 50+.')
    d['evening'] = g.get('evening', 'Gentle cleanse -> Prescribed treatment cream -> Ceramide night repair.')
    d['diet'] = g.get('diet', 'Anti-inflammatory diet rich in antioxidants, omega-3 fatty acids, and optimal hydration.')
    d['red_flags'] = g.get('red_flags', d.get('red_flags', 'Rapid change in size, shape, bleeding, or intense pain.'))

print 'All 23 diseases populated with comprehensive clinical healing and routine guidance!'

# Output builder script
with open('builder_data.py', 'w') as f:
    f.write('# Auto-generated data\n')
    f.write('SAMPLES_JSON = ' + json.dumps(sample_list) + '\n')
    f.write('DISEASES_JSON = ' + json.dumps(diseases) + '\n')

print 'Saved builder_data.py successfully!'
