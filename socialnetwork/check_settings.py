import os
import sys

# Встановлюємо шлях до проекту
sys.path.insert(0, os.path.dirname(__file__))

# Пробуємо різні варіанти налаштувань
settings_modules = [
    'config.settings.dev',
    'config.settings',
    'config.settings.base',
]

for module in settings_modules:
    try:
        os.environ['DJANGO_SETTINGS_MODULE'] = module
        import django
        django.setup()
        from django.conf import settings
        print(f'✅ Працює з: {module}')
        print(f'   DEBUG: {settings.DEBUG}')
        print(f'   INSTALLED_APPS: {len(settings.INSTALLED_APPS)} додатків')
        break
    except Exception as e:
        print(f'❌ Помилка з {module}: {e}')