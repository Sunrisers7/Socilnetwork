Соціальна мережа з функціями:
- 👤 Профілі користувачів з аватарками
- 📝 Пости з фото
- 💬 Чати з темами та кастомізацією
- 👥 Друзі та групи
- 🔔 Сповіщення
- 🎨 Кастомні теми

## Встановлення

```bash
# Клонуйте репозиторій
git clone https://github.com/ВАШ_ЛОГІН/назва-репозиторію.git
cd socialnetwork

# Створіть віртуальне оточення
python -m venv .venv

# Активуйте
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Встановіть залежності
pip install -r requirements.txt

# Міграції
python manage.py makemigrations
python manage.py migrate

# Створіть суперкористувача
python manage.py createsuperuser

# Запустіть
python manage.py runserver