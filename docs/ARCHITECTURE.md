# Configuration System Architecture

## System Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                     FLASK APPLICATION START                      │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  1. Environment Detection (app/settings/envcommon.py)           │
│     - Read FLASK_ENV variable                                   │
│     - Determine which .env file to load                         │
│     - Load environment variables                                │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  2. Load Appropriate .env File                                  │
│                                                                  │
│     FLASK_ENV=development → .env.development                    │
│     FLASK_ENV=production  → .env.production                     │
│     Not Set               → .env (fallback)                     │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  3. Build Configuration (app/settings/base.py)                  │
│                                                                  │
│     ┌─────────────────┐                                         │
│     │  BaseConfig     │ ◄──── SecurityConfig (security.py)     │
│     │  (Foundation)   │ ◄──── DatabaseConfig (databases.py)    │
│     └────────┬────────┘                                         │
│              │                                                   │
│     ┌────────┴────────┬──────────────┬──────────────┐          │
│     │                 │              │              │          │
│     ▼                 ▼              ▼              ▼          │
│  Development      Production     Testing        Custom         │
│  Config           Config         Config         Config         │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  4. Initialize Flask App (app/__init__.py)                      │
│                                                                  │
│     app = Flask(__name__)                                       │
│     config_class = get_config()                                 │
│     app.config.from_object(config_class)                        │
│     config_class.init_app(app)                                  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  5. Application Ready                                           │
│     - All settings loaded                                       │
│     - Environment-specific initialization done                  │
│     - Ready to handle requests                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Configuration Inheritance

```
                    ┌──────────────────┐
                    │  SecurityConfig  │
                    │  (security.py)   │
                    └────────┬─────────┘
                             │
                             ├──────────────┐
                             │              │
                    ┌────────▼─────────┐    │
                    │ DatabaseConfig   │    │
                    │ (databases.py)   │    │
                    └────────┬─────────┘    │
                             │              │
                             ├──────────────┘
                             │
                    ┌────────▼─────────┐
                    │   BaseConfig     │
                    │   (base.py)      │
                    │                  │
                    │ - App settings   │
                    │ - Flask core     │
                    │ - Uploads        │
                    │ - Email          │
                    │ - Logging        │
                    │ - Features       │
                    └────────┬─────────┘
                             │
          ┌──────────────────┼──────────────────┐
          │                  │                  │
    ┌─────▼──────┐  ┌────────▼────────┐  ┌─────▼──────┐
    │Development │  │   Production    │  │  Testing   │
    │   Config   │  │     Config      │  │   Config   │
    │            │  │                 │  │            │
    │ DEBUG: ON  │  │  DEBUG: OFF     │  │ DEBUG: ON  │
    │ SQLite     │  │  PostgreSQL     │  │ In-Memory  │
    │ Relaxed    │  │  Strict         │  │ No CSRF    │
    └────────────┘  └─────────────────┘  └────────────┘
```

## Module Dependencies

```
run.py
  │
  └─► app/__init__.py (create_app)
        │
        └─► app/settings/__init__.py
              │
              ├─► app/settings/base.py
              │     │
              │     ├─► app/settings/security.py
              │     │     │
              │     │     └─► app/settings/envcommon.py
              │     │           │
              │     │           └─► python-dotenv
              │     │
              │     └─► app/settings/databases.py
              │           │
              │           └─► app/settings/envcommon.py
              │
              └─► app/settings/envcommon.py
```

## Environment Variable Flow

```
┌────────────────┐
│  .env files    │
│  .env          │
│  .env.dev      │
│  .env.prod     │
└────────┬───────┘
         │
         │ load_dotenv()
         ▼
┌────────────────┐
│  OS environ    │
│  variables     │
└────────┬───────┘
         │
         │ get_env()
         │ get_bool_env()
         │ get_int_env()
         ▼
┌────────────────┐
│  Config        │
│  Classes       │
│  (typed)       │
└────────┬───────┘
         │
         │ app.config.from_object()
         ▼
┌────────────────┐
│  Flask App     │
│  Config        │
└────────────────┘
```

## Configuration Access Patterns

```
Application Code:
┌─────────────────────────────────────┐
│  from flask import current_app      │
│  value = current_app.config['KEY']  │
└─────────────────────────────────────┘

Direct Import:
┌─────────────────────────────────────┐
│  from app.settings import get_env   │
│  value = get_env('KEY')             │
└─────────────────────────────────────┘

Template:
┌─────────────────────────────────────┐
│  {{ config.APP_NAME }}              │
│  {% if config.DEBUG %}...{% endif %}│
└─────────────────────────────────────┘
```

## Security Layers

```
┌─────────────────────────────────────────────────────────┐
│  Layer 1: Environment Files                             │
│  - .env files never committed to Git                    │
│  - Sensitive data stored as environment variables       │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│  Layer 2: Environment Validation                        │
│  - get_env() with required=True                         │
│  - Type conversion and validation                       │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│  Layer 3: Configuration Classes                         │
│  - Environment-specific security settings               │
│  - Production requires enhanced security                │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│  Layer 4: Flask Application                             │
│  - Runtime security enforcement                         │
│  - CSRF, sessions, rate limiting                        │
└─────────────────────────────────────────────────────────┘
```

## Configuration Priority

When multiple sources define the same setting:

```
1. Environment Variables (.env files)
   ↓ (highest priority)
2. Configuration Class Defaults
   ↓
3. Helper Function Defaults (get_env default parameter)
   ↓ (lowest priority)
```

Example:
```python
# In security.py
PASSWORD_MIN_LENGTH = get_int_env('PASSWORD_MIN_LENGTH', 8)

Priority:
1. If PASSWORD_MIN_LENGTH=10 in .env → uses 10
2. If not in .env, uses default → uses 8
```

## Adding New Configuration

```
Step 1: Decide Location
├─ General setting    → base.py (BaseConfig)
├─ Security setting   → security.py (SecurityConfig)
└─ Database setting   → databases.py (DatabaseConfig)

Step 2: Add Environment Variable
└─ Update .env.example, .env.development, .env.production

Step 3: Import and Use
└─ Access via app.config['SETTING_NAME']
```

## Common Patterns

### Pattern 1: Environment-Specific Values
```python
class BaseConfig:
    FEATURE_X = get_bool_env('FEATURE_X', False)

class DevelopmentConfig(BaseConfig):
    FEATURE_X = True  # Override for development

class ProductionConfig(BaseConfig):
    FEATURE_X = get_bool_env('FEATURE_X', required=True)
```

### Pattern 2: Computed Settings
```python
class BaseConfig:
    BASE_DIR = Path(__file__).parent.parent.parent
    UPLOAD_FOLDER = BASE_DIR / "uploads"
    DATABASE_URL = f"sqlite:///{BASE_DIR}/instance/app.db"
```

### Pattern 3: Conditional Defaults
```python
class ProductionConfig(BaseConfig):
    @classmethod
    def init_app(cls, app):
        # Production-specific initialization
        setup_logging(app)
        validate_required_settings(app)
```
