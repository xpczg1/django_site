import os
import sys


def check_structure():
    print("=== ПРОВЕРКА СТРУКТУРЫ ПРОЕКТА ===")

    # Текущая директория
    current_dir = os.getcwd()
    print(f"Текущая директория: {current_dir}")

    # Содержимое корневой директории
    print("\nСодержимое корневой директории:")
    for item in os.listdir('.'):
        item_path = os.path.join('.', item)
        if os.path.isdir(item_path):
            print(f"  📁 {item}/")
        else:
            print(f"  📄 {item}")

    # Проверка папки mysite
    print("\nСодержимое папки 'mysite':")
    if os.path.exists('mysite') and os.path.isdir('mysite'):
        for item in os.listdir('mysite'):
            item_path = os.path.join('mysite', item)
            if os.path.isdir(item_path):
                print(f"  📁 {item}/")
            else:
                print(f"  📄 {item}")
    else:
        print("  ❌ Папка 'mysite' не существует!")

    # Проверка manage.py
    print(f"\nФайл manage.py существует: {os.path.exists('manage.py')}")

    # Проверка импорта
    print("\n=== ПРОВЕРКА ИМПОРТА ===")
    try:
        # Добавляем текущую директорию в путь
        sys.path.insert(0, current_dir)

        # Пытаемся импортировать settings
        from mysite import settings
        print("✅ Успешно импортирован mysite.settings")

        # Проверяем настройки Django
        os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'

        import django
        from django.conf import settings as django_settings

        django.setup()
        print("✅ Django успешно настроен")
        print(f"   DEBUG: {django_settings.DEBUG}")
        print(f"   ALLOWED_HOSTS: {django_settings.ALLOWED_HOSTS}")

    except ImportError as e:
        print(f"❌ Ошибка импорта: {e}")
    except Exception as e:
        print(f"❌ Ошибка: {e}")


if __name__ == '__main__':
    check_structure()