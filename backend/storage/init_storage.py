"""
Storage Directory Initialization

Creates all required directories for data storage and logging.
Ensures proper structure exists before application starts.
"""

import os
from pathlib import Path


def init_storage(config):
    """
    Initialize all storage directories required by the application.
    
    Args:
        config: Configuration object with directory paths
    """
    directories = [
        # Data directories
        config.DATA_DIR,
        config.USERS_DIR,
        config.PATIENTS_DIR,
        config.DOCTORS_DIR,
        config.ADMIN_DIR,
        config.DIAGNOSES_DIR,
        config.WALLETS_DIR,
        config.TRANSACTIONS_DIR,
        config.CONFIG_DIR,
        config.ASSISTANT_DIR,
        config.SESSIONS_DIR,
        config.UPLOADS_DIR,
        config.UPLOADS_DIR / 'diagnoses',
        config.UPLOADS_DIR / 'doctors',
        config.UPLOADS_DIR / 'patients',
        
        # Log directories
        config.LOGS_DIR,
        config.LOGS_DIR / 'api',
        config.LOGS_DIR / 'ai',
        config.LOGS_DIR / 'auth',
        config.LOGS_DIR / 'errors',
        config.LOGS_DIR / 'audit',
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    
    # Initialize default configuration files if they don't exist
    _init_default_configs(config)


def _init_default_configs(config):
    """Create default configuration files if they don't exist"""
    import json
    from datetime import datetime
    
    # Default diseases configuration
    diseases_path = config.CONFIG_DIR / 'diseases.json'
    if not diseases_path.exists():
        default_diseases = {
            "version": 1,
            "last_updated": datetime.now().isoformat(),
            "categories": [
                {
                    "id": "infectious",
                    "name": {"en": "Infectious Diseases", "ar": "الأمراض المعدية"},
                    "subcategories": [
                        {"id": "bacterial", "name": {"en": "Bacterial", "ar": "بكتيرية"}},
                        {"id": "viral", "name": {"en": "Viral", "ar": "فيروسية"}},
                        {"id": "fungal", "name": {"en": "Fungal", "ar": "فطرية"}},
                        {"id": "parasitic", "name": {"en": "Parasitic", "ar": "طفيلية"}}
                    ]
                },
                {
                    "id": "inflammatory",
                    "name": {"en": "Inflammatory Diseases", "ar": "الأمراض الالتهابية"},
                    "subcategories": [
                        {"id": "eczema", "name": {"en": "Eczema", "ar": "أكزيما"}},
                        {"id": "psoriasis", "name": {"en": "Psoriasis", "ar": "صدفية"}},
                        {"id": "dermatitis", "name": {"en": "Dermatitis", "ar": "التهاب الجلد"}}
                    ]
                },
                {
                    "id": "neoplastic",
                    "name": {"en": "Neoplastic (Tumors)", "ar": "الأورام"},
                    "subcategories": [
                        {"id": "benign", "name": {"en": "Benign", "ar": "حميدة"}},
                        {"id": "malignant", "name": {"en": "Malignant", "ar": "خبيثة"}},
                        {"id": "premalignant", "name": {"en": "Pre-malignant", "ar": "ما قبل السرطان"}}
                    ]
                },
                {
                    "id": "allergic",
                    "name": {"en": "Allergic Reactions", "ar": "ردود الفعل التحسسية"},
                    "subcategories": [
                        {"id": "urticaria", "name": {"en": "Urticaria", "ar": "الشرى"}},
                        {"id": "contact", "name": {"en": "Contact Allergy", "ar": "حساسية التلامس"}}
                    ]
                },
                {
                    "id": "autoimmune",
                    "name": {"en": "Autoimmune Diseases", "ar": "أمراض المناعة الذاتية"},
                    "subcategories": [
                        {"id": "lupus", "name": {"en": "Lupus", "ar": "الذئبة"}},
                        {"id": "vitiligo", "name": {"en": "Vitiligo", "ar": "البهاق"}}
                    ]
                },
                {
                    "id": "pigmentary",
                    "name": {"en": "Pigmentary Disorders", "ar": "اضطرابات التصبغ"},
                    "subcategories": []
                },
                {
                    "id": "genetic",
                    "name": {"en": "Genetic/Hereditary", "ar": "الأمراض الوراثية"},
                    "subcategories": []
                }
            ],
            "diseases": [
                {
                    "id": "tinea_corporis",
                    "name": {"en": "Ringworm (Tinea Corporis)", "ar": "السعفة الجسدية"},
                    "category": "infectious",
                    "subcategory": "fungal",
                    "severity_range": ["mild", "moderate", "severe"],
                    "urgency": "routine",
                    "description": {
                        "en": "A common fungal infection causing ring-shaped rashes",
                        "ar": "عدوى فطرية شائعة تسبب طفح جلدي على شكل حلقة"
                    }
                },
                {
                    "id": "psoriasis_plaque",
                    "name": {"en": "Plaque Psoriasis", "ar": "الصدفية اللويحية"},
                    "category": "inflammatory",
                    "subcategory": "psoriasis",
                    "severity_range": ["mild", "moderate", "severe"],
                    "urgency": "routine",
                    "description": {
                        "en": "Chronic autoimmune condition causing raised, red, scaly patches",
                        "ar": "حالة مناعية ذاتية مزمنة تسبب بقع حمراء مرتفعة ومتقشرة"
                    }
                },
                {
                    "id": "atopic_dermatitis",
                    "name": {"en": "Atopic Dermatitis (Eczema)", "ar": "التهاب الجلد التأتبي"},
                    "category": "inflammatory",
                    "subcategory": "eczema",
                    "severity_range": ["mild", "moderate", "severe"],
                    "urgency": "routine",
                    "description": {
                        "en": "Chronic skin condition causing itchy, inflamed skin",
                        "ar": "حالة جلدية مزمنة تسبب حكة والتهاب الجلد"
                    }
                },
                {
                    "id": "melanoma",
                    "name": {"en": "Melanoma", "ar": "سرطان الجلد الميلانومي"},
                    "category": "neoplastic",
                    "subcategory": "malignant",
                    "severity_range": ["early", "advanced"],
                    "urgency": "urgent",
                    "description": {
                        "en": "Serious form of skin cancer developing from melanocytes",
                        "ar": "نوع خطير من سرطان الجلد يتطور من الخلايا الصباغية"
                    }
                },
                {
                    "id": "acne_vulgaris",
                    "name": {"en": "Acne Vulgaris", "ar": "حب الشباب"},
                    "category": "inflammatory",
                    "subcategory": "dermatitis",
                    "severity_range": ["mild", "moderate", "severe", "cystic"],
                    "urgency": "routine",
                    "description": {
                        "en": "Common skin condition causing pimples and inflammation",
                        "ar": "حالة جلدية شائعة تسبب البثور والالتهاب"
                    }
                },
                {
                    "id": "vitiligo",
                    "name": {"en": "Vitiligo", "ar": "البهاق"},
                    "category": "autoimmune",
                    "subcategory": "vitiligo",
                    "severity_range": ["localized", "generalized", "universal"],
                    "urgency": "routine",
                    "description": {
                        "en": "Condition causing loss of skin color in patches",
                        "ar": "حالة تسبب فقدان لون الجلد في بقع"
                    }
                },
                {
                    "id": "herpes_simplex",
                    "name": {"en": "Herpes Simplex", "ar": "الهربس البسيط"},
                    "category": "infectious",
                    "subcategory": "viral",
                    "severity_range": ["mild", "moderate", "recurrent"],
                    "urgency": "routine",
                    "description": {
                        "en": "Viral infection causing blisters on skin or mucous membranes",
                        "ar": "عدوى فيروسية تسبب بثور على الجلد أو الأغشية المخاطية"
                    }
                },
                {
                    "id": "basal_cell_carcinoma",
                    "name": {"en": "Basal Cell Carcinoma", "ar": "سرطان الخلايا القاعدية"},
                    "category": "neoplastic",
                    "subcategory": "malignant",
                    "severity_range": ["superficial", "nodular", "infiltrative"],
                    "urgency": "urgent",
                    "description": {
                        "en": "Most common form of skin cancer, usually slow-growing",
                        "ar": "أكثر أنواع سرطان الجلد شيوعًا، عادة ما يكون بطيء النمو"
                    }
                },
                {
                    "id": "contact_dermatitis",
                    "name": {"en": "Contact Dermatitis", "ar": "التهاب الجلد التماسي"},
                    "category": "allergic",
                    "subcategory": "contact",
                    "severity_range": ["mild", "moderate", "severe"],
                    "urgency": "routine",
                    "description": {
                        "en": "Skin reaction from contact with irritants or allergens",
                        "ar": "رد فعل جلدي من التلامس مع مهيجات أو مسببات الحساسية"
                    }
                },
                {
                    "id": "scabies",
                    "name": {"en": "Scabies", "ar": "الجرب"},
                    "category": "infectious",
                    "subcategory": "parasitic",
                    "severity_range": ["typical", "crusted"],
                    "urgency": "routine",
                    "description": {
                        "en": "Itchy skin condition caused by tiny mites",
                        "ar": "حالة جلدية مسببة للحكة بسبب عث صغير"
                    }
                }
            ]
        }
        with open(diseases_path, 'w', encoding='utf-8') as f:
            json.dump(default_diseases, f, ensure_ascii=False, indent=2)
    
    # Default specialties configuration
    specialties_path = config.CONFIG_DIR / 'specialties.json'
    if not specialties_path.exists():
        default_specialties = {
            "version": 1,
            "last_updated": datetime.now().isoformat(),
            "specialties": [
                {
                    "id": "general_dermatology",
                    "name": {"en": "General Dermatology", "ar": "طب الجلدية العام"},
                    "handles_categories": ["infectious", "inflammatory", "allergic", "pigmentary"],
                    "description": {"en": "General skin conditions and diseases", "ar": "الحالات والأمراض الجلدية العامة"}
                },
                {
                    "id": "pediatric_dermatology",
                    "name": {"en": "Pediatric Dermatology", "ar": "طب جلدية الأطفال"},
                    "handles_categories": ["infectious", "inflammatory", "genetic"],
                    "age_range": {"min": 0, "max": 18},
                    "description": {"en": "Skin conditions in children", "ar": "الحالات الجلدية لدى الأطفال"}
                },
                {
                    "id": "dermatologic_oncology",
                    "name": {"en": "Dermatologic Oncology", "ar": "أورام الجلد"},
                    "handles_categories": ["neoplastic"],
                    "priority": "high",
                    "description": {"en": "Skin cancers and tumors", "ar": "سرطانات وأورام الجلد"}
                },
                {
                    "id": "cosmetic_dermatology",
                    "name": {"en": "Cosmetic Dermatology", "ar": "طب الجلد التجميلي"},
                    "handles_categories": ["pigmentary"],
                    "description": {"en": "Cosmetic skin treatments", "ar": "علاجات الجلد التجميلية"}
                },
                {
                    "id": "immunodermatology",
                    "name": {"en": "Immunodermatology", "ar": "مناعة الجلد"},
                    "handles_categories": ["autoimmune", "allergic"],
                    "description": {"en": "Immune-related skin conditions", "ar": "الحالات الجلدية المتعلقة بالمناعة"}
                }
            ]
        }
        with open(specialties_path, 'w', encoding='utf-8') as f:
            json.dump(default_specialties, f, ensure_ascii=False, indent=2)
    
    # Default pricing configuration
    pricing_path = config.CONFIG_DIR / 'pricing.json'
    if not pricing_path.exists():
        default_pricing = {
            "version": 1,
            "last_updated": datetime.now().isoformat(),
            "currency": "USD",
            "diagnosis_prices": {
                "ai_only": {
                    "price": 10.00,
                    "description": {"en": "AI diagnosis only", "ar": "تشخيص الذكاء الاصطناعي فقط"}
                },
                "ai_doctor_review": {
                    "price": 50.00,
                    "description": {"en": "AI + Doctor review", "ar": "ذكاء اصطناعي + مراجعة طبيب"}
                },
                "urgent": {
                    "multiplier": 1.5,
                    "description": {"en": "Urgent case multiplier", "ar": "مضاعف الحالات العاجلة"}
                }
            },
            "revenue_split": {
                "platform_percentage": 30,
                "doctor_percentage": 70,
                "description": "Platform takes 30%, doctor receives 70% of doctor review fees"
            },
            "wallet": {
                "min_deposit": 10.00,
                "max_deposit": 1000.00,
                "min_balance_for_diagnosis": 10.00
            }
        }
        with open(pricing_path, 'w', encoding='utf-8') as f:
            json.dump(default_pricing, f, ensure_ascii=False, indent=2)
    
    # Default AI routing configuration
    ai_routing_path = config.CONFIG_DIR / 'ai_routing.json'
    if not ai_routing_path.exists():
        default_ai_routing = {
            "version": 1,
            "last_updated": datetime.now().isoformat(),
            "providers": {
                "internal": {
                    "enabled": True,
                    "priority": 1,
                    "description": "Internal trained models"
                },
                "openrouter": {
                    "enabled": True,
                    "priority": 2,
                    "model": "anthropic/claude-3-haiku",
                    "timeout_ms": 30000,
                    "description": "OpenRouter LLM API"
                },
                "gemini": {
                    "enabled": True,
                    "priority": 3,
                    "model": "gemini-1.5-flash",
                    "timeout_ms": 30000,
                    "description": "Google Gemini Vision API"
                },
                "groq": {
                    "enabled": True,
                    "priority": 4,
                    "model": "llama-3.1-70b-versatile",
                    "timeout_ms": 15000,
                    "description": "Groq Fast Inference API"
                }
            },
            "stage_routing": {
                "stage0_validation": {
                    "primary": ["internal", "gemini"],
                    "description": "Image validation gate"
                },
                "stage1_normal_abnormal": {
                    "primary": ["internal", "openrouter"],
                    "fallback": ["gemini", "groq"],
                    "description": "Normal vs abnormal classification"
                },
                "stage2_category": {
                    "primary": ["openrouter", "gemini"],
                    "fallback": ["groq", "internal"],
                    "description": "Disease category classification"
                },
                "stage3_diagnosis": {
                    "primary": ["openrouter", "gemini"],
                    "fallback": ["groq"],
                    "description": "Fine-grained diagnosis"
                },
                "stage4_fusion": {
                    "primary": ["openrouter"],
                    "fallback": ["groq"],
                    "description": "AI fusion and explanation"
                }
            },
            "fallback_behavior": {
                "max_retries": 3,
                "retry_delay_ms": 1000,
                "exponential_backoff": True,
                "fail_open": False,
                "description": "If all providers fail, reject gracefully"
            }
        }
        with open(ai_routing_path, 'w', encoding='utf-8') as f:
            json.dump(default_ai_routing, f, ensure_ascii=False, indent=2)
    
    # Default admin user
    admin_path = config.ADMIN_DIR / 'admin.json'
    if not admin_path.exists():
        import bcrypt
        default_password = bcrypt.hashpw('admin123'.encode(), bcrypt.gensalt()).decode()
        default_admin = {
            "users": [
                {
                    "id": "admin-001",
                    "email": "admin@skindiagnosis.app",
                    "password_hash": default_password,
                    "role": "super_admin",
                    "name": "System Administrator",
                    "created_at": datetime.now().isoformat(),
                    "last_login": None
                }
            ]
        }
        with open(admin_path, 'w', encoding='utf-8') as f:
            json.dump(default_admin, f, ensure_ascii=False, indent=2)
