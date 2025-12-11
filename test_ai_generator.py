"""
Script de prueba para AITestGenerator
"""

from src.ai_generator import AITestGenerator

def main():
    print("=" * 60)
    print("🚀 TEST: AI Test Generator v2")
    print("=" * 60)
    print()
    
    # 1. Crear el generador
    print("📦 Inicializando generador...")
    generator = AITestGenerator()
    print()
    
    # 2. User story de prueba
    user_story = """
As a user
I want to visit example.com
So that I can see the page

Acceptance Criteria:
- User navigates to https://example.com
- User sees "Example Domain" in the page
"""
    
    print("📖 User Story:")
    print(user_story)
    print()
    
    # 3. Generar test completo
    print("⏳ Generando test completo (esto tomará ~30 segundos)...")
    print()
    
    result = generator.generate_complete_test(user_story)
    
    # 4. Mostrar resultados
    print("=" * 60)
    print("✅ RESULTADOS")
    print("=" * 60)
    print()
    
    print("📝 GHERKIN GENERADO:")
    print("-" * 60)
    print(result['gherkin'])
    print()
    
    print("💻 CÓDIGO PLAYWRIGHT GENERADO:")
    print("-" * 60)
    print(result['code'])
    print()
    
    # Mostrar validación ← NUEVO
    print("🔍 VALIDACIÓN DEL CÓDIGO:")
    print("-" * 60)
    print(result['validation'])
    print()     
    
    # 5. Guardar el código generado
    output_file = "tests/test_google_search.py"
    with open(output_file, 'w') as f:
        f.write(result['code'])
    
    print("=" * 60)
    print(f"✅ Código guardado en: {output_file}")
    print("=" * 60)
    print()
    print("🎯 Siguiente paso: ejecuta el test con:")
    print(f"   python -m pytest {output_file} -v")
    print()

if __name__ == "__main__":
    main()