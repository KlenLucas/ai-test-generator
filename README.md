# 🤖 AI Test Generator

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Playwright](https://img.shields.io/badge/playwright-1.40+-green.svg)
![Claude](https://img.shields.io/badge/claude-sonnet--4-orange.svg)

Sistema de generación automática de tests de Playwright usando Claude AI (Anthropic).

## 📋 Descripción

Este proyecto genera tests de Playwright automáticamente a partir de User Stories usando Claude AI. El sistema:

1. Lee una User Story (desde archivo o texto)
2. Genera escenarios Gherkin usando Claude AI
3. Convierte Gherkin a código Playwright
4. Valida el código automáticamente
5. Reporta problemas, advertencias y sugerencias

## ✨ Características

- 🤖 **Generación automática con Claude AI** - Usa el modelo Sonnet 4
- ✅ **Validación automática** - 5 validadores de calidad de código
- 🖥️ **CLI profesional** - Múltiples modos de input
- 📝 **Workflow de 2 pasos** - User Story → Gherkin → Code (mejor calidad)
- 🏗️ **Arquitectura modular** - Prompts, generador y validadores separados
- 📊 **Test suite incluido** - Verificación automática del sistema
- 📚 **Documentación exhaustiva** - 60+ páginas de conceptos y guías

## 🏗️ Arquitectura
```
User Story
    ↓
AI Generator (Claude) → Gherkin Scenarios
    ↓
AI Generator (Claude) → Playwright Code
    ↓
Validator → Reporte de calidad
    ↓
Test ejecutable
```

## 📁 Estructura del Proyecto
```
ai-test-generator/
├── src/
│   ├── __init__.py
│   ├── prompts.py              # Templates de prompts para Claude
│   ├── ai_generator.py         # Generador principal
│   └── validators.py           # Validadores de código
│
├── tests/                      # Tests generados
├── user_stories/               # User stories de ejemplo
│   ├── login.txt
│   ├── search.txt
│   ├── navigation.txt
│   └── form_submission.txt
│
├── cli.py                      # CLI principal
├── test_ai_generator.py        # Script de prueba simple
├── test_complete_workflow.py   # Test suite completo
│
├── .env                        # API keys (no commitear)
├── .gitignore                  # Archivos ignorados
├── requirements.txt            # Dependencias
│
├── README.md                   # Este archivo
├── USAGE.md                    # Guía de uso detallada
└── CONCEPTOS.md                # Documentación técnica (60 páginas)
```

## 🚀 Instalación

### 1. Clonar el repositorio
```bash
git clone https://github.com/TU-USUARIO/ai-test-generator.git
cd ai-test-generator
```

### 2. Crear entorno virtual
```bash
python -m venv venv
source venv/bin/activate  # En Mac/Linux
# venv\Scripts\activate   # En Windows
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
playwright install
```

### 4. Configurar API Key

Crea un archivo `.env` en la raíz del proyecto:
```bash
ANTHROPIC_API_KEY=tu_api_key_aqui
```

**Obtener API Key:**
1. Ir a https://console.anthropic.com/
2. Crear cuenta o iniciar sesión
3. Generar API key en Settings

### 5. Verificar instalación
```bash
python test_complete_workflow.py
```

Deberías ver: `✅ 5/5 tests pasados`

## 💻 Uso

### CLI (Forma Recomendada)

El proyecto incluye un CLI profesional con múltiples modos de input:
```bash
# Método 1: Desde archivo (RECOMENDADO para user stories largas)
python cli.py generate --file user_stories/login.txt

# Método 2: Directo en terminal (para textos cortos)
python cli.py generate "As a user I want to login to the system"

# Ver Gherkin generado
python cli.py generate --file user_stories/login.txt --show-gherkin

# Validar un test existente
python cli.py validate tests/test_example.py

# Ver información del sistema
python cli.py info

# Ayuda
python cli.py --help
python cli.py generate --help
```

#### Ejemplos de User Stories

El proyecto incluye 4 ejemplos en `user_stories/`:
- `login.txt` - Test de login
- `search.txt` - Test de búsqueda
- `navigation.txt` - Test de navegación
- `form_submission.txt` - Test de formulario
```bash
# Generar desde ejemplo
python cli.py generate --file user_stories/login.txt

# Ver output
ls tests/

# Ejecutar test generado
python -m pytest tests/test_*.py -v -s
```

### Uso Programático (Python)

También puedes usar el generador directamente en Python:
```python
from src.ai_generator import AITestGenerator

# Crear generador
generator = AITestGenerator()

# Tu user story
user_story = """
As a user
I want to visit example.com
So that I can see the page

Acceptance Criteria:
- User navigates to https://example.com
- User sees "Example Domain" in the page
"""

# Generar test completo
result = generator.generate_complete_test(user_story)

# Ver resultados
print(result['gherkin'])      # Escenarios Gherkin
print(result['code'])         # Código Playwright
print(result['validation'])   # Reporte de validación
```

### Ejecutar Tests Generados
```bash
# Test específico (con navegador visible)
python -m pytest tests/test_login.py -v -s

# Todos los tests (headless)
python -m pytest tests/ -v

# Con reporte detallado
python -m pytest tests/ -v --tb=short
```

## 🔍 Validaciones Automáticas

El sistema valida automáticamente el código generado:

- ✅ **Sintaxis Python** - Detecta errores de sintaxis con `ast.parse()`
- ✅ **Imports** - Verifica que estén pytest y playwright
- ✅ **Fixtures** - Valida que existan `browser` y `page`
- ✅ **Async/Await** - Verifica uso correcto de decoradores y await
- ✅ **Complejidad** - Detecta código innecesariamente complejo

### Ejemplo de validación:
```
🔍 VALIDACIÓN:
────────────────────────────────────────────────────────────
✅ Código validado exitosamente

💡 SUGERENCIAS:
  - Código bien estructurado y siguiendo mejores prácticas
```

## 📊 Componentes

### 1. Prompts (`src/prompts.py`)

Templates modulares para Claude:
- `SYSTEM_PROMPT` - Define el rol de Claude como experto en QA
- `GHERKIN_GENERATION_PROMPT` - Convierte User Story en Gherkin
- `PLAYWRIGHT_GENERATION_PROMPT` - Convierte Gherkin en código Playwright

### 2. AI Generator (`src/ai_generator.py`)

Clase principal que orquesta el proceso:
```python
class AITestGenerator:
    def generate_gherkin(user_story: str) -> str
        # User Story → Gherkin
        
    def generate_playwright_code(gherkin: str) -> str
        # Gherkin → Código Playwright
        
    def generate_complete_test(user_story: str) -> Dict
        # Workflow completo (2 pasos + validación)
```

### 3. Validators (`src/validators.py`)

Sistema de validación robusto:
```python
class CodeValidator:
    def validate_syntax(code: str) -> bool
    def validate_imports(code: str) -> bool
    def validate_fixtures(code: str) -> bool
    def validate_async_await(code: str) -> bool
    def validate_complexity(code: str) -> bool
    def validate_code(code: str) -> ValidationResult
```

### 4. CLI (`cli.py`)

Interfaz de línea de comandos profesional con:
- Múltiples modos de input
- Progress bars
- Colores y formato
- Validación integrada
- Generación automática de nombres de archivo

## 🎯 Ejemplo Completo

### Input (User Story):
```
As a user
I want to search on Google
So that I can find information

Acceptance Criteria:
- Navigate to https://www.google.com
- Enter search query "Playwright"
- Press Enter
- Verify results appear
```

### Output (Test Generado):
```python
import pytest
from playwright.async_api import async_playwright, Page

@pytest.fixture
async def browser():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        yield browser
        await browser.close()

@pytest.fixture
async def page(browser):
    page = await browser.new_page()
    yield page
    await page.close()

@pytest.mark.asyncio
async def test_user_searches_on_google(page: Page):
    # Given I navigate to Google
    await page.goto("https://www.google.com")
    
    # When I search for "Playwright"
    await page.fill('[name="q"]', "Playwright")
    await page.press('[name="q"]', "Enter")
    
    # Then I should see search results
    await page.wait_for_selector("#search")
    assert await page.locator("#search").is_visible()
```

## 💰 Costos

**Claude Sonnet 4 (claude-sonnet-4-20250514):**
- Input: $3 por millón de tokens
- Output: $15 por millón de tokens

**Estimado por test:** ~$0.003-0.005 USD

**100 tests:** ~$0.30-0.50 USD

## 🛠️ Tecnologías

- **Python 3.8+** - Lenguaje base
- **Playwright** - Automatización de navegador
- **Pytest** - Framework de testing
- **Claude API (Anthropic)** - Generación de código con IA
- **pytest-asyncio** - Soporte para tests asíncronos
- **Click** - Framework para CLI
- **python-dotenv** - Manejo de variables de entorno

## 📚 Documentación

Este proyecto incluye documentación exhaustiva:

### 📄 [README.md](README.md) (Este archivo)
- Overview del proyecto
- Instalación y configuración
- Uso básico con ejemplos

### 📘 [USAGE.md](USAGE.md)
Guía de uso completa con:
- Diferentes formas de generar tests
- Workflows comunes
- Ejemplos paso a paso
- Troubleshooting
- Tips y mejores prácticas

### 📖 [CONCEPTOS.md](CONCEPTOS.md)
Documentación técnica profunda (60 páginas):
- LLMs y Claude API
- Prompt Engineering
- Arquitectura de Sistemas AI
- Async/Await en Python
- Validación de Código AI
- Testing con Playwright
- CLI y UX
- Patrones de Diseño
- Mejores Prácticas

## 📈 Aprendizajes Clave

1. **Prompt Engineering es iterativo** - Mejoré los prompts 4-5 veces hasta obtener código simple
2. **LLMs no son perfectos** - La validación automática es esencial
3. **Arquitectura modular** - Separar prompts, generación y validación facilita mantenimiento
4. **Workflow de 2 pasos** - User Story → Gherkin → Code da mejor calidad que generación directa
5. **Async/Await** - Dentro de un test es secuencial, entre tests es paralelo

## 🔄 Workflow de Desarrollo
```bash
# 1. Activar entorno
source venv/bin/activate

# 2. Crear/editar user story
code user_stories/mi_feature.txt

# 3. Generar test
python cli.py generate --file user_stories/mi_feature.txt

# 4. Revisar código generado
code tests/test_mi_feature.py

# 5. Ejecutar test
python -m pytest tests/test_mi_feature.py -v -s

# 6. Iterar si es necesario
```

## 🧪 Testing del Sistema

Verifica que todo funciona correctamente:
```bash
python test_complete_workflow.py
```

Esto ejecuta 5 tests:
1. ✅ Inicialización del generador
2. ✅ Validador detecta errores
3. ✅ Generación completa funciona
4. ✅ CLI existe y es válido
5. ✅ Estructura del proyecto correcta

## ⚠️ Limitaciones Conocidas

- Claude a veces genera código más complejo de lo necesario (se controla con prompts específicos)
- La validación no cubre todos los casos edge posibles
- Costos de API se acumulan con uso frecuente
- Selectores CSS pueden requerir ajustes manuales según el sitio

## 🚧 Próximos Pasos

- [ ] Agregar modo interactivo (`--interactive`)
- [ ] Auto-corrección de problemas simples
- [ ] Soporte para más frameworks (Selenium, Cypress)
- [ ] Dashboard web para visualizar tests
- [ ] Integración con CI/CD
- [ ] Sistema de templates personalizables

## 🤝 Contribuciones

Este es un proyecto de aprendizaje. Mejoras y sugerencias son bienvenidas.

Para contribuir:
1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

MIT License - Uso educativo y personal

## 👤 Autor

**[Bryan Rodriguez]**
- GitHub: [@TU-USUARIO](https://github.com/bryan0422)
- LinkedIn: [Tu Perfil](www.linkedin.com/in/bryan-rodriguez-32a9a8211)

## 🙏 Agradecimientos

- [Anthropic](https://www.anthropic.com/) por Claude AI
- [Playwright](https://playwright.dev/) por el excelente framework de testing
- Comunidad de Python y testing

---

**⭐ Si este proyecto te fue útil, considera darle una estrella en GitHub**

**Creado como parte del aprendizaje de AI Engineering y Test Automation** 🤖✨