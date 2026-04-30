import os
import sys
import subprocess
import shutil

def build_exe():
    """Сборка EXE файла из main.py и logo.png"""
    
    if not os.path.exists("main.py"):
        print("❌ Ошибка: main.py не найден!")
        return False
    
    if not os.path.exists("logo.png"):
        print("❌ Ошибка: logo.png не найден!")
        print("💡 Положите logo.png в ту же папку, что и main.py")
        return False
    
    # Очистка старых сборок
    for folder in ["build", "dist"]:
        if os.path.exists(folder):
            print(f"🗑️  Удаляю {folder}/...")
            shutil.rmtree(folder)
    
    # Разделитель путей: ; для Windows, : для Linux/Mac
    sep = ";" if os.name == "nt" else ":"
    
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--windowed",
        "--name", "KeyGenerator",
        "--clean",
        "--noconfirm",
        "--add-data", f"logo.png{sep}.",  # Критично: встраиваем лого
        "main.py"
    ]
    
    print("🚀 Сборка EXE...")
    print(f"📦 logo.png будет встроен через --add-data")
    print(f"Команда: {' '.join(cmd)}\n")
    
    try:
        subprocess.run(cmd, check=True)
        
        exe_name = "KeyGenerator.exe" if os.name == "nt" else "KeyGenerator"
        exe_path = os.path.join("dist", exe_name)
        
        if os.path.exists(exe_path):
            size = os.path.getsize(exe_path) / (1024 * 1024)
            print(f"\n✅ Готово!")
            print(f"📁 {exe_path}")
            print(f"📏 {size:.2f} MB")
            return True
        return False
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Ошибка PyInstaller: {e}")
        return False
    except Exception as e:
        print(f"\n❌ Ошибка: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("  KEY GENERATOR — EXE BUILD")
    print("=" * 50 + "\n")
    success = build_exe()
    print("\n" + "=" * 50)
    print("Нажмите Enter..." if success else "❌ Проверьте ошибки выше")
    input()