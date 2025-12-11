"""
Test completo del workflow de generación de tests
Verifica que todo el sistema funciona correctamente
"""

import os
import sys
from pathlib import Path
from src.ai_generator import AITestGenerator
from src.validators import CodeValidator

def print_section(title):
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60 + "\n")

def test_generator_initialization():
    """Test 1: Inicialización del generador"""
    print_section("TEST 1: Inicialización")
    
    try:
        generator = AITestGenerator()
        print("✅ Generador inicializado correctamente")
        return True
    except Exception as e:
        print(f"❌ Error al inicializar: {e}")
        return False

def test_validator():
    """Test 2: Validador funciona"""
    print_section("TEST 2: Validador")
    
    # Código con errores intencionales
    bad_code = """
    async def test_example():
        page.goto("https://example.com")
    """
    
    validator = CodeValidator()
    result = validator.validate_code(bad_code)
    
    if not result.is_valid and len(result.errors) > 0:
        print("✅ Validador detecta errores correctamente")
        print(f"   Errores detectados: {len(result.errors)}")
        return True
    else:
        print("❌ Validador NO detectó errores esperados")
        return False

def test_simple_generation():
    """Test 3: Generación simple"""
    print_section("TEST 3: Generación Simple")
    
    user_story = """
    As a user
    I want to visit example.com
    So that I can see the page
    
    Acceptance Criteria:
    - User navigates to https://example.com
    - User sees "Example Domain" on the page
    """
    
    try:
        print("⏳ Generando test (esto tomará ~30 segundos)...")
        generator = AITestGenerator()
        result = generator.generate_complete_test(user_story)
        
        # Verificaciones
        checks = []
        
        # Check 1: Tiene Gherkin
        if result.get('gherkin'):
            checks.append("✅ Gherkin generado")
        else:
            checks.append("❌ Falta Gherkin")
        
        # Check 2: Tiene código
        if result.get('code'):
            checks.append("✅ Código generado")
        else:
            checks.append("❌ Falta código")
        
        # Check 3: Tiene validación
        if result.get('validation'):
            checks.append("✅ Validación ejecutada")
        else:
            checks.append("❌ Falta validación")
        
        # Check 4: Código tiene fixtures
        code = result.get('code', '')
        if 'async def browser' in code and 'async def page' in code:
            checks.append("✅ Fixtures presentes")
        else:
            checks.append("❌ Faltan fixtures")
        
        # Check 5: Código tiene test
        if 'async def test_' in code:
            checks.append("✅ Función de test presente")
        else:
            checks.append("❌ Falta función de test")
        
        # Mostrar resultados
        for check in checks:
            print(f"   {check}")
        
        # Guardar ejemplo
        output_file = "tests/test_workflow_example.py"
        with open(output_file, 'w') as f:
            f.write(code)
        print(f"\n   📁 Test guardado en: {output_file}")
        
        all_passed = all("✅" in check for check in checks)
        return all_passed
        
    except Exception as e:
        print(f"❌ Error durante generación: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_cli_exists():
    """Test 4: CLI existe y es ejecutable"""
    print_section("TEST 4: CLI")
    
    cli_path = Path("cli.py")
    
    if cli_path.exists():
        print("✅ cli.py existe")
        
        # Verificar que tenga contenido
        with open(cli_path) as f:
            content = f.read()
            if 'click' in content and '@cli.command' in content:
                print("✅ CLI tiene estructura correcta")
                return True
            else:
                print("⚠️  CLI existe pero estructura incorrecta")
                return False
    else:
        print("❌ cli.py no encontrado")
        return False

def test_structure():
    """Test 5: Estructura del proyecto"""
    print_section("TEST 5: Estructura del Proyecto")
    
    required_files = {
        "src/prompts.py": "Templates de prompts",
        "src/ai_generator.py": "Generador AI",
        "src/validators.py": "Validadores",
        "cli.py": "CLI",
        "README.md": "Documentación",
        "CONCEPTOS.md": "Guía de conceptos",
        ".env": "Configuración",
    }
    
    required_dirs = {
        "src/": "Código fuente",
        "tests/": "Tests generados",
        "user_stories/": "User stories",
    }
    
    all_good = True
    
    print("Archivos:")
    for file, desc in required_files.items():
        if Path(file).exists():
            print(f"   ✅ {file:25} {desc}")
        else:
            print(f"   ❌ {file:25} {desc}")
            all_good = False
    
    print("\nDirectorios:")
    for dir, desc in required_dirs.items():
        if Path(dir).exists():
            print(f"   ✅ {dir:25} {desc}")
        else:
            print(f"   ⚠️  {dir:25} {desc} (se creará si es necesario)")
    
    return all_good

def main():
    print("\n")
    print("╔═══════════════════════════════════════════════════════╗")
    print("║        🧪 TEST COMPLETO DEL SISTEMA                  ║")
    print("║        AI Test Generator v1.0                        ║")
    print("╚═══════════════════════════════════════════════════════╝")
    
    results = []
    
    # Ejecutar tests
    results.append(("Inicialización", test_generator_initialization()))
    results.append(("Validador", test_validator()))
    results.append(("Generación", test_simple_generation()))
    results.append(("CLI", test_cli_exists()))
    results.append(("Estructura", test_structure()))
    
    # Resultados finales
    print_section("RESULTADOS FINALES")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {status:10} {name}")
    
    print(f"\n   Total: {passed}/{total} tests pasados")
    
    if passed == total:
        print("\n   🎉 ¡SISTEMA COMPLETAMENTE FUNCIONAL!")
        print("   ✅ Proyecto 1 al 100%")
        return 0
    else:
        print(f"\n   ⚠️  {total - passed} test(s) fallaron")
        print("   Revisa los errores arriba")
        return 1

if __name__ == "__main__":
    sys.exit(main())