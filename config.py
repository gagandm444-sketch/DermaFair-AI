import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dermafair-ai-academic-security-key-2026'
    
    # Upload configuration
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max upload
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}
    
    # Database
    DATABASE_PATH = os.path.join(BASE_DIR, 'backend', 'database', 'predictions.db')
    
    # Model configuration
    MODEL_DIR = os.path.join(BASE_DIR, 'model')
    MODEL_PATH = os.path.join(MODEL_DIR, 'skin_model.h5')
    CLASSES_PATH = os.path.join(MODEL_DIR, 'classes.json')
    
    # Dataset & Reports
    DATASET_DIR = os.path.join(BASE_DIR, 'dataset')
    REPORTS_DIR = os.path.join(BASE_DIR, 'reports')
