"""
Script de testing básico para verificar que todos los módulos funcionan correctamente.
Ejecutar: python test_app.py
"""
import sys
import os

# Fix encoding para Windows
if sys.platform == 'win32':
    os.system('chcp 65001 > nul')
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')


def test_imports():
    """Verifica que todas las dependencias se puedan importar"""
    print("🔍 Verificando imports...")

    try:
        import streamlit
        print("✅ Streamlit")
    except ImportError as e:
        print(f"❌ Streamlit: {e}")
        return False

    try:
        import psd_tools
        print("✅ psd-tools")
    except ImportError as e:
        print(f"❌ psd-tools: {e}")
        return False

    try:
        from PIL import Image
        print("✅ Pillow")
    except ImportError as e:
        print(f"❌ Pillow: {e}")
        return False

    try:
        import fitz
        print("✅ PyMuPDF")
    except ImportError as e:
        print(f"❌ PyMuPDF: {e}")
        return False

    return True


def test_modules():
    """Verifica que los módulos personalizados se puedan importar"""
    print("\n🔍 Verificando módulos personalizados...")

    try:
        import config
        print(f"✅ config.py (MAX_FILE_SIZE_MB: {config.MAX_FILE_SIZE_MB})")
    except ImportError as e:
        print(f"❌ config: {e}")
        return False

    try:
        from processors import psd_processor, ai_processor, image_utils
        print("✅ processors")
    except ImportError as e:
        print(f"❌ processors: {e}")
        return False

    try:
        from utils import file_validator, cache_manager
        print("✅ utils")
    except ImportError as e:
        print(f"❌ utils: {e}")
        return False

    return True


def test_config():
    """Verifica la configuración"""
    print("\n🔍 Verificando configuración...")

    import config

    print(f"   Tamaño máximo: {config.MAX_FILE_SIZE_MB}MB")
    print(f"   Preview size: {config.MAX_PREVIEW_SIZE}px")
    print(f"   Extensiones: {config.ALLOWED_EXTENSIONS}")
    print(f"   Cache TTL: {config.CACHE_TTL_SECONDS}s")
    print(f"   JPG Quality: {config.JPG_QUALITY}%")

    return True


def main():
    """Ejecuta todos los tests"""
    print("=" * 60)
    print("TESTING VISUALIZADOR PSD/AI")
    print("=" * 60)

    all_passed = True

    # Test imports
    if not test_imports():
        all_passed = False
        print("\n❌ Algunos imports fallaron. Ejecuta: pip install -r requirements.txt")

    # Test modules
    if not test_modules():
        all_passed = False
        print("\n❌ Algunos módulos personalizados fallaron")

    # Test config
    if not test_config():
        all_passed = False

    print("\n" + "=" * 60)
    if all_passed:
        print("✅ TODOS LOS TESTS PASARON")
        print("\nPara iniciar la aplicación:")
        print("  streamlit run app.py")
    else:
        print("❌ ALGUNOS TESTS FALLARON")
        print("\nPor favor, revisa los errores arriba")
        sys.exit(1)

    print("=" * 60)


if __name__ == "__main__":
    main()
