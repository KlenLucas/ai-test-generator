# 🤖 AI Test Generator

Generador automático de tests de Playwright usando Claude AI.

## 📋 Descripción

Este proyecto genera tests de Playwright automáticamente a partir de User Stories usando Claude AI (Anthropic). El sistema:

1. Lee una User Story
2. Genera escenarios Gherkin
3. Convierte Gherkin a código Playwright
4. Valida el código automáticamente
5. Reporta problemas y sugerencias

## 🏗️ Arquitectura
```
User Story
    ↓
AI Generator (Claude) → Gherkin Scenarios
    ↓
AI Generator (Claude) → Playwright Code
    ↓
Validator → Reporte de calidad
```

## 📁 Estructura del Proyecto
```
ai-test-generator/
├── src/
│   ├── prompts.py          # Templates de prompts para Claude
│   ├── ai_generator.py     # Generador principal
│   └── validators.py       # Validadores de código
├── tests/                  # Tests generados
├── test_ai_generator.py   # Script de prueba
├── .env                    # API keys (no commitear)
├── requirements.txt        # Dependencias
└── README.md              # Este archivo
```

## 🚀 Instalación

### 1. Clonar/Descargar el proyecto
```bash
cd ~/Documents/ai-test-generator
```

### 2. Crear entorno virtual
```bash
python -m venv venv
source venv/bin/activate  # En Mac/Linux
```

### 3. Instalar dependencias
```bash
pip install anthropic python-dotenv playwright pytest pytest-asyncio
playwright install
```

### 4. Configurar API Key

Crea un archivo `.env`:
```bash
ANTHROPIC_API_KEY=tu_api_key_aqui
```

## 💻 Uso

### Generar un test completo
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

# Generar test
result = generator.generate_complete_test(user_story)

# Ver resultados
print(result['gherkin'])      # Escenarios Gherkin
print(result['code'])         # Código Playwright
print(result['validation'])   # Reporte de validación
```

### Usar el script de prueba
```bash
python test_ai_generator.py
```

Esto generará automáticamente:
- Escenarios Gherkin
- Código Playwright
- Validación del código
- Archivo en `tests/test_google_search.py`

### Ejecutar tests generados
```bash
# Ejecutar un test específico
python -m pytest tests/test_google_search.py -v

# Ver el navegador (headed mode)
python -m pytest tests/test_google_search.py -v -s

# Ejecutar todos los tests
python -m pytest tests/ -v
```

## 🔍 Validaciones Automáticas

El sistema valida automáticamente:

- ✅ **Sintaxis Python:** Detecta errores de sintaxis
- ✅ **Imports:** Verifica que estén pytest y playwright
- ✅ **Fixtures:** Valida que existan browser y page
- ✅ **Async/Await:** Verifica uso correcto
- ✅ **Complejidad:** Detecta código innecesariamente complejo

### Ejemplo de validación:
```
✅ VALIDACIÓN EXITOSA

⚠️  ADVERTENCIAS:
  - Se generaron 3 tests. Considera simplificar a 1-2 tests principales.

💡 SUGERENCIAS:
  - Código bien estructurado y siguiendo mejores prácticas.
```

## 📊 Componentes

### 1. Prompts (`src/prompts.py`)

Templates modulares para Claude:
- `SYSTEM_PROMPT`: Define el rol de Claude
- `GHERKIN_GENERATION_PROMPT`: User Story → Gherkin
- `PLAYWRIGHT_GENERATION_PROMPT`: Gherkin → Code

### 2. AI Generator (`src/ai_generator.py`)

Clase principal:
```python
class AITestGenerator:
    def generate_gherkin(user_story)         # Genera Gherkin
    def generate_playwright_code(gherkin)    # Genera código
    def generate_complete_test(user_story)   # Workflow completo
```

### 3. Validators (`src/validators.py`)

Sistema de validación:
```python
class CodeValidator:
    def validate_syntax(code)       # Valida sintaxis
    def validate_imports(code)      # Valida imports
    def validate_fixtures(code)     # Valida fixtures
    def validate_async_await(code)  # Valida async/await
    def validate_complexity(code)   # Valida complejidad
    def validate_code(code)         # Ejecuta todas
```

## 🎯 Ejemplos

### User Story Simple
```python
user_story = """
As a user
I want to search on Google
So that I can find information

Acceptance Criteria:
- Navigate to https://www.google.com
- Enter search query
- Verify results appear
"""

result = generator.generate_complete_test(user_story)
```

### Test Generado
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
async def test_search_on_google(page: Page):
    await page.goto("https://www.google.com")
    await page.fill('[name="q"]', "Playwright Python")
    await page.press('[name="q"]', "Enter")
    await page.wait_for_selector("#search")
    assert await page.locator("#search").is_visible()
```

## 💰 Costos

**Claude Sonnet 4:**
- Input: $3 por millón de tokens
- Output: $15 por millón de tokens

**Estimado por test generado:** ~$0.003-0.005 USD

## 🛠️ Tecnologías

- **Python 3.8+**
- **Playwright** - Automatización de navegador
- **Pytest** - Framework de testing
- **Claude API (Anthropic)** - Generación de código con IA
- **pytest-asyncio** - Soporte para tests async

## 📚 Aprendizajes Clave

1. **Async/Await:** Tests usan API asíncrona de Playwright
2. **Prompt Engineering:** Los prompts necesitan ser muy específicos
3. **Validación:** Código generado por IA debe validarse
4. **Iteración:** Mejorar prompts es un proceso iterativo

## 🔄 Workflow de Desarrollo
```bash
# 1. Activar entorno
source venv/bin/activate

# 2. Modificar prompts (si es necesario)
code src/prompts.py

# 3. Generar tests
python test_ai_generator.py

# 4. Ejecutar tests
python -m pytest tests/ -v

# 5. Iterar según resultados
```

## ⚠️ Limitaciones Conocidas

- Claude a veces genera más tests de los necesarios
- Prompts requieren refinamiento continuo
- Validación no cubre todos los casos edge
- Costos de API se acumulan con uso frecuente

## 🚀 Próximos Pasos

- [ ] CLI para generar tests desde terminal
- [ ] Auto-corrección de código con problemas
- [ ] Integración con CI/CD
- [ ] Soporte para más frameworks (Selenium, Cypress)
- [ ] Dashboard para visualizar tests generados

## 📝 Notas

**Proyecto:** AI Test Generator v1.0  
**Semanas:** 3-4 de 8  
**Stack:** Python, Playwright, Claude API  
**Estado:** Funcional con validación automática  

## 🤝 Contribuciones

Este es un proyecto de aprendizaje. Mejoras y sugerencias son bienvenidas.

## 📄 Licencia

MIT License - Uso educativo y personal

---

**Creado como parte del aprendizaje de AI Testing y Automation** 🤖✨