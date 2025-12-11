"""
AI Test Generator - Versión Inicial Simple
Este es tu punto de partida. Lo iremos mejorando juntos.
"""

import os
from anthropic import Anthropic
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()


def generate_test_from_story(user_story: str) -> str:
    """
    Genera un test de Playwright desde una user story.
    
    Args:
        user_story: La historia de usuario en texto
        
    Returns:
        Código Python del test generado
    """
    
    # 1. Inicializar cliente de Claude
    client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    
    # 2. Crear el prompt (simple por ahora)
    prompt = f"""You are an expert QA Engineer. Generate a Playwright test in Python.

User Story:
{user_story}

Requirements:
- Use pytest framework
- Use async/await with Playwright
- Include proper imports at the top
- Add clear assertions with good error messages
- Include comments explaining each step
- Use explicit waits (wait_for_selector) where needed
- Follow Python best practices

Output ONLY the Python code, no explanations."""
    
    # 3. Llamar a Claude API
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2000,
        messages=[
            {
                "role": "user", 
                "content": prompt
            }
        ]
    )
    
    # 4. Extraer el código generado
    generated_code = response.content[0].text
    
    # 5. Limpiar markdown si viene con ```python
    if "```python" in generated_code:
        generated_code = generated_code.split("```python")[1].split("```")[0].strip()
    elif "```" in generated_code:
        generated_code = generated_code.split("```")[1].split("```")[0].strip()
    
    return generated_code


def main():
    """
    Función principal - Tu primer generador funcionando!
    """
    
    print("\n" + "="*60)
    print("🤖 AI TEST GENERATOR - Versión 0.1")
    print("="*60 + "\n")
    
    # Leer la user story
    story_file = "examples/user_stories/simple_login.txt"
    
    try:
        with open(story_file, "r") as f:
            user_story = f.read()
        
        print(f"📖 Leyendo user story de: {story_file}")
        print(f"📝 User story:")
        print("-" * 60)
        print(user_story)
        print("-" * 60 + "\n")
        
        # Generar el test
        print("🤖 Generando test con Claude AI...")
        generated_code = generate_test_from_story(user_story)
        
        # Guardar el test generado
        #output_file = "tests/test_generated_simple.py"
        from pathlib import Path
        story_name = Path(story_file).stem  # Obtiene "simple_login" de "simple_login.txt"
        output_file = f"tests/test_{story_name}.py"
        with open(output_file, "w") as f:
            f.write(generated_code)
        
        print(f"✅ Test generado exitosamente!")
        print(f"📁 Guardado en: {output_file}\n")
        
        # Mostrar preview del código
        print("📄 Preview del código generado:")
        print("=" * 60)
        lines = generated_code.split("\n")
        for i, line in enumerate(lines[:25], 1):  # Primeras 25 líneas
            print(f"{i:3d} | {line}")
        
        if len(lines) > 25:
            print(f"... ({len(lines) - 25} líneas más)")
        print("=" * 60)
        
        # Instrucciones para ejecutar
        print("\n🚀 Para ejecutar el test generado:")
        print(f" python -m pytest {output_file} -v --headed")
        print("\n" + "="*60)
        
    except FileNotFoundError:
        print(f"❌ Error: No se encontró el archivo {story_file}")
        print("💡 Crea el archivo con tu user story primero")
    
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n💡 Verifica que tu API key esté configurada en .env")


if __name__ == "__main__":
    main()
