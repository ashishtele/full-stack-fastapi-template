def generate_dot_code(files):
    dependencies = {}
    
    # Extracting dependencies from the provided data
    for file_path, import_statement in files.items():
        module_name = file_path.split("/")[-1].split(".")[0]
        dependencies[module_name] = []
        if import_statement.startswith("from"):
            imported_module = import_statement.split("from ")[-1].split(" import ")[0]
            if "," in imported_module:
                imported_modules = imported_module.split(", ")
                for mod in imported_modules:
                    dependencies[module_name].append(mod)
            else:
                dependencies[module_name].append(imported_module)
        elif import_statement.startswith("import"):
            imported_modules = import_statement.split("import ")[-1]
            if "," in imported_modules:
                imported_modules = imported_modules.split(", ")
                for mod in imported_modules:
                    dependencies[module_name].append(mod)
            else:
                dependencies[module_name].append(imported_modules)
    
    # Generating DOT code
    dot_code = "digraph G {\n"
    for module, imports in dependencies.items():
        for imp in imports:
            dot_code += f'    "{module}" -> "{imp}"\n'
    dot_code += "}"
    
    return dot_code

# Test the function with the provided data
files = {
    "backend/app/backend_pre_start.py": "from app.core.db import engine",
    "backend/app/crud.py": "from app.core.security import get_password_hash, verify_password\nfrom app.models import Item, ItemCreate, User, UserCreate, UserUpdate",
    "backend/app/initial_data.py": "from app.core.db import engine, init_db",
    "backend/app/main.py": "from app.api.main import api_router\nfrom app.core.config import settings",
    "backend/app/models.py": "from sqlmodel import Field, Relationship, SQLModel",
    "backend/app/tests_pre_start.py": "from app.core.db import engine",
    "backend/app/utils.py": "from app.core.config import settings",
    "backend/app/api/deps.py": "from app.models import TokenPayload, User\nfrom app.core import security\nfrom app.core.config import settings\nfrom app.core.db import engine",
    "backend/app/api/main.py": "from app.api.routes import items, login, users, utils",
    "backend/app/api/routes/items.py": "from app.api.deps import CurrentUser, SessionDep\nfrom app.models import Item, ItemCreate, ItemOut, ItemsOut, ItemUpdate, Message",
    "backend/app/api/routes/login.py": "from app import crud\nfrom app.api.deps import CurrentUser, SessionDep, get_current_active_superuser\nfrom app.core import security\nfrom app.core.config import settings\nfrom app.core.security import get_password_hash\nfrom app.models import Message, NewPassword, Token, UserOut\nfrom app.utils import generate_password_reset_token, generate_reset_password_email, send_email, verify_password_reset_token",
    "backend/app/api/routes/users.py": "from app import crud\nfrom app.api.deps import CurrentUser, SessionDep, get_current_active_superuser\nfrom app.core.config import settings\nfrom app.core.security import get_password_hash, verify_password\nfrom app.models import Item, Message, UpdatePassword, User, UserCreate, UserCreateOpen, UserOut, UsersOut, UserUpdate, UserUpdateMe\nfrom app.utils import generate_new_account_email, send_email",
    "backend/app/api/routes/utils.py": "from app.api.deps import get_current_active_superuser\nfrom app.models import Message\nfrom app.utils import generate_test_email, send_email",
    "backend/app/core/config.py": "from typing import Annotated, Any, Literal\nfrom pydantic import AnyUrl, BeforeValidator, HttpUrl, PostgresDsn, computed_field, model_validator\nfrom pydantic_core import MultiHostUrl\nfrom pydantic_settings import BaseSettings, SettingsConfigDict\nfrom typing_extensions import Self",
    "backend/app/core/db.py": "from app import crud\nfrom app.core.config import settings\nfrom sqlmodel import Session, create_engine, select\nfrom app.models import User, UserCreate",
    "backend/app/core/security.py": "from jose import jwt\nfrom datetime import datetime, timedelta\nfrom typing import Any\nfrom passlib.context import CryptContext\nfrom app.core.config import settings",
    "backend/app/tests/conftest.py": "import pytest\nfrom fastapi.testclient import TestClient\nfrom sqlmodel import Session, delete\nfrom app.core.config import settings\nfrom app.core.db import engine, init_db\nfrom app.main import app\nfrom app.models import Item, User\nfrom app.tests.utils.user import authentication_token_from_email\nfrom app.tests.utils.utils import get_superuser_token_headers",
    "backend/app/tests/api/routes/test_items.py": "from fastapi.testclient import TestClient\nfrom sqlmodel import Session\nfrom app.core.config import settings\nfrom app.tests.utils.item import create_random_item",
    "backend/app/tests/api/routes/test_login.py": "from unittest.mock import patch\nfrom fastapi.testclient import TestClient\nfrom app.core.config import settings\nfrom app.utils import generate_password_reset_token",
    "backend/app/tests/api/routes/test_users.py": "from unittest.mock import patch\nfrom fastapi.testclient import TestClient\nfrom sqlmodel import Session\nfrom app import crud\nfrom app.core.config import settings\nfrom app.models import UserCreate\nfrom app.tests.utils.utils import random_email, random_lower_string",
    "backend/app/tests/crud/test_user.py": "from fastapi.encoders import jsonable_encoder\nfrom sqlmodel import Session\nfrom app import crud\nfrom app.core.security import verify_password\nfrom app.models import User, UserCreate, UserUpdate\nfrom app.tests.utils.utils import random_email, random_lower_string",
    "backend/app/tests/scripts/test_backend_pre_start.py": "from unittest.mock import MagicMock, patch\nfrom sqlmodel import select\nfrom app.backend_pre_start import init, logger",
    "backend/app/tests/scripts/test_test_pre_start.py": "from unittest.mock import MagicMock, patch\nfrom sqlmodel import select\nfrom app.tests_pre_start import init, logger",
    "backend/app/tests/utils/item.py": "from sqlmodel import Session\nfrom app import crud\nfrom app.models import Item, ItemCreate\nfrom app.tests.utils.user import create_random_user\nfrom app.tests.utils.utils import random_lower_string",
    "backend/app/tests/utils/user.py": "from fastapi.testclient import TestClient\nfrom sqlmodel import Session\nfrom app import crud\nfrom app.core.config import settings\nfrom app.models import User, UserCreate, UserUpdate\nfrom app.tests.utils.utils import random_email, random_lower_string",
    "backend/app/tests/utils/utils.py": "import random\nimport string\nfrom fastapi.testclient import TestClient\nfrom app.core.config import settings"
}

dot_code = generate_dot_code(files)
print(dot_code)
