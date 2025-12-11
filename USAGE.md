# 📘 GUÍA DE USO - AI Test Generator

Guía práctica con ejemplos para usar el generador de tests.

---

## 🚀 INICIO RÁPIDO

### 1. Setup Inicial
```bash
# Activar entorno virtual
source venv/bin/activate

# Verificar que todo funciona
python test_complete_workflow.py
```

---

## 💻 FORMAS DE GENERAR TESTS

### Opción 1: Desde Archivo (RECOMENDADO)

**Mejor para:** User stories largas y complejas
```bash
# 1. Ver ejemplos disponibles
ls user_stories/

# 2. Generar test
python cli.py generate --file user_stories/login.txt

# 3. Ejecutar test
python -m pytest tests/test_*.py -v -s
```

---

### Opción 2: Modo Interactivo

**Mejor para:** Escribir user stories en el momento
```bash
# Abre tu editor automáticamente
python cli.py generate --interactive

# Escribe tu user story, guarda y cierra
```

---

### Opción 3: Modo Rápido

**Mejor para:** Prototipos y tests simples
```bash
python cli.py generate --quick "visit homepage"
python cli.py generate --quick "search for items"
python cli.py generate --quick "submit form"
```

---

### Opción 4: Directo en Terminal

**Mejor para:** User stories muy cortas
```bash
python cli.py generate "As a user I want to login"
```

---

## 🎯 EJEMPLOS PRÁCTICOS

### Ejemplo 1: Test de Login
```bash
python cli.py generate --file user_stories/login.txt --show-gherkin
```

### Ejemplo 2: Test de Búsqueda
```bash
python cli.py generate --file user_stories/search.txt
```

### Ejemplo 3: Generar todos los ejemplos
```bash
for file in user_stories/*.txt; do
    python cli.py generate --file "$file"
done
```

---

## 🔍 VALIDAR TESTS
```bash
# Validar un test específico
python cli.py validate tests/test_login.py

# Validar todos los tests
for file in tests/test_*.py; do
    python cli.py validate "$file"
done
```

---

## 🧪 EJECUTAR TESTS

### Test Individual
```bash
# Con navegador visible
python -m pytest tests/test_workflow_example.py -v -s

# Headless (sin ver navegador)
python -m pytest tests/test_workflow_example.py -v
```

### Todos los Tests
```bash
# Secuencial
python -m pytest tests/ -v

# En paralelo (más rápido)
python -m pytest tests/ -v -n 3
```

---

## 📊 VER INFORMACIÓN DEL SISTEMA
```bash
python cli.py info
```

---

## 🛠️ WORKFLOWS COMUNES

### Workflow 1: Generar y Ejecutar
```bash
# 1. Generar
python cli.py generate --file user_stories/login.txt

# 2. Ejecutar
python -m pytest tests/test_*.py -v -s
```

### Workflow 2: Iteración Rápida
```bash
# 1. Generar rápido
python cli.py generate --quick "test idea"

# 2. Revisar código
code tests/test_*.py

# 3. Ejecutar
python -m pytest tests/test_*.py -v -s
```

---

## ⚙️ OPCIONES AVANZADAS

### Ver Gherkin Generado
```bash
python cli.py generate --file user_stories/login.txt --show-gherkin
```

### Personalizar Nombre de Archivo
```bash
python cli.py generate --file user_stories/login.txt --filename test_custom.py
```

### Cambiar Directorio de Salida
```bash
python cli.py generate --file user_stories/login.txt --output custom_tests/
```

---

## 🐛 TROUBLESHOOTING

### Error: API Key no encontrada
```bash
# Verificar .env
cat .env

# Debe contener:
ANTHROPIC_API_KEY=sk-ant-...
```

### Error: Import error
```bash
# Reinstalar dependencias
pip install -r requirements.txt
```

### Tests fallan al ejecutar
```bash
# Instalar browsers de Playwright
playwright install
```

---

## 💡 TIPS

1. **User Stories Claras** - Más detalles = mejores tests
2. **Una Acción por Test** - Tests simples y enfocados
3. **Usar Archivos** - Más cómodo que escribir en terminal
4. **Validar Siempre** - Verificar calidad del código generado

---

**Última actualización:** Diciembre 2025