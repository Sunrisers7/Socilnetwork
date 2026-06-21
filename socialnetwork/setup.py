#!/usr/bin/env python
"""
Setup script for Social Network Django project
"""
import os
import sys
import django
from pathlib import Path


def setup_environment():
    """Setup the environment variables"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
    os.environ.setdefault('DEBUG', 'True')
    os.environ.setdefault('ALLOWED_HOSTS', 'localhost,127.0.0.1')

    # Add the project root to Python path
    BASE_DIR = Path(__file__).resolve().parent
    sys.path.insert(0, str(BASE_DIR))


def check_dependencies():
    """Check if all required packages are installed"""
    required_packages = [
        'django',
        'pillow',
        'crispy_forms',
        'channels',
        'redis',
    ]

    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)

    if missing_packages:
        print(f"Missing packages: {', '.join(missing_packages)}")
        print("Install them with: pip install -r requirements.txt")
        return False
    return True


def create_directories():
    """Create required directories if they don't exist"""
    directories = [
        'media/profile_pics',
        'media/post_images',
        'media/group_avatars',
        'media/chat_files',
        'static/css',
        'static/js',
        'static/img',
        'staticfiles',
    ]

    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✓ Created directory: {directory}")


def check_configuration():
    """Check Django configuration"""
    import django.conf as conf

    if not conf.settings.configured:
        print("❌ Django settings are not configured!")
        return False

    checks = []

    # Check DEBUG
    checks.append(('DEBUG', f"DEBUG = {conf.settings.DEBUG}",
                   conf.settings.DEBUG is not None))

    # Check ALLOWED_HOSTS
    allowed_hosts = conf.settings.ALLOWED_HOSTS
    checks.append(('ALLOWED_HOSTS', f"ALLOWED_HOSTS = {allowed_hosts}",
                   bool(allowed_hosts) if not conf.settings.DEBUG else True))

    # Check SECRET_KEY
    checks.append(('SECRET_KEY', 'SECRET_KEY is set',
                   bool(conf.settings.SECRET_KEY)))

    # Check DATABASES
    checks.append(('DATABASES', f"Using {conf.settings.DATABASES['default']['ENGINE']}",
                   True))

    # Print results
    all_passed = True
    for check_name, message, passed in checks:
        status = '✓' if passed else '❌'
        print(f"{status} {check_name}: {message}")
        if not passed:
            all_passed = False

    return all_passed


def main():
    """Main setup function"""
    print("\n" + "=" * 50)
    print("Social Network Django Project Setup")
    print("=" * 50 + "\n")

    # Setup environment
    print("Setting up environment...")
    setup_environment()

    # Create directories
    print("\nCreating directories...")
    create_directories()

    # Initialize Django
    print("\nInitializing Django...")
    django.setup()

    # Check configuration
    print("\nChecking configuration...")
    if not check_configuration():
        print("\n❌ Configuration check failed!")
        print("\nPlease fix the following:")
        print("1. Make sure DEBUG=True in your .env file or settings")
        print("2. Set ALLOWED_HOSTS in your .env file: ALLOWED_HOSTS=localhost,127.0.0.1")
        print("3. Generate a SECRET_KEY or set it in .env file")
        sys.exit(1)

    # Run migrations
    print("\nRunning migrations...")
    from django.core.management import call_command

    try:
        call_command('makemigrations', verbosity=0)
        call_command('migrate', verbosity=0)
        print("✓ Migrations completed")
    except Exception as e:
        print(f"❌ Migration error: {e}")
        sys.exit(1)

    print("\n" + "=" * 50)
    print("Setup completed successfully!")
    print("=" * 50)
    print("\nYou can now run the server with:")
    print("  python manage.py runserver")
    print("\nOr create a superuser with:")
    print("  python manage.py createsuperuser")


if __name__ == '__main__':
    main()