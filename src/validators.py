"""
Code Validators
Valida código Playwright generado para detectar problemas comunes.
"""

import ast
import re
from typing import Dict, List, Tuple
from dataclasses import dataclass

@dataclass
class ValidationResult:
    """Resultado de una validación."""
    is_valid: bool
    errors: List[str]
    warnings: List[str]
    suggestions: List[str]
    
    def __str__(self):
        """Formato legible del resultado."""
        lines = []
        
        if self.is_valid:
            lines.append("✅ VALIDACIÓN EXITOSA")
        else:
            lines.append("❌ VALIDACIÓN FALLIDA")
        
        if self.errors:
            lines.append("\n🔴 ERRORES:")
            for error in self.errors:
                lines.append(f"  - {error}")
        
        if self.warnings:
            lines.append("\n⚠️  ADVERTENCIAS:")
            for warning in self.warnings:
                lines.append(f"  - {warning}")
        
        if self.suggestions:
            lines.append("\n💡 SUGERENCIAS:")
            for suggestion in self.suggestions:
                lines.append(f"  - {suggestion}")
        
        return "\n".join(lines)
    
class CodeValidator:
    """Validador principal de código Playwright."""
    
    def __init__(self):
        """Inicializa el validador."""
        self.errors = []
        self.warnings = []
        self.suggestions = []
    
    def validate_syntax(self, code: str) -> bool:
        """
        Valida que el código tenga sintaxis Python correcta.
        
        Args:
            code: El código a validar
            
        Returns:
            True si la sintaxis es válida
        """
        try:
            ast.parse(code) ## AST = Abstract Syntax Tree (Árbol de Sintaxis Abstracta). Python convierte el código a un árbol para verificar sintaxis
            return True
        except SyntaxError as e:
            self.errors.append(
                f"Error de sintaxis en línea {e.lineno}: {e.msg}"
            )
            return False
        except Exception as e:
            self.errors.append(f"Error al parsear código: {str(e)}")
            return False   
        
    def validate_imports(self, code: str) -> bool:
        """
        Valida que estén todos los imports necesarios.
        
        Args:
            code: El código a validar
            
        Returns:
            True si los imports son válidos
        """
        required_imports = {
            "pytest": False,
            "playwright": False,
        }
        
        # Buscar imports en el código
        for line in code.split("\n"):
            if "import pytest" in line:
                required_imports["pytest"] = True
            if "from playwright" in line or "import playwright" in line:
                required_imports["playwright"] = True
        
        # Verificar que estén todos
        all_present = True
        for lib, present in required_imports.items():
            if not present:
                self.errors.append(f"Falta import requerido: {lib}")
                all_present = False
        
        return all_present
    
    def validate_fixtures(self, code: str) -> bool:
        """
        Valida que existan las fixtures necesarias (browser, page).
        
        Args:
            code: El código a validar
            
        Returns:
            True si las fixtures están presentes
        """
        has_browser_fixture = "@pytest.fixture" in code and "async def browser" in code
        has_page_fixture = "@pytest.fixture" in code and "async def page" in code
        
        all_present = True
        
        if not has_browser_fixture:
            self.errors.append("Falta fixture 'browser'")
            all_present = False
        
        if not has_page_fixture:
            self.errors.append("Falta fixture 'page'")
            all_present = False
        
        return all_present    
    
    def validate_async_await(self, code: str) -> bool:
        """
        Valida el uso correcto de async/await.
        
        Args:
            code: El código a validar
            
        Returns:
            True si async/await se usa correctamente
        """
        issues_found = False
        
        # Verificar que tests tengan @pytest.mark.asyncio
        test_functions = re.findall(r'async def (test_\w+)', code)
        
        for test_name in test_functions:
            # Buscar si tiene el decorador antes
            pattern = rf'@pytest\.mark\.asyncio\s+async def {test_name}'
            if not re.search(pattern, code):
                self.warnings.append(
                    f"Test '{test_name}' es async pero falta @pytest.mark.asyncio"
                )
                issues_found = True
        
        # Verificar uso de await en operaciones de Playwright
        playwright_methods = [
            'goto', 'click', 'fill', 'screenshot', 'title',
            'wait_for_selector', 'locator', 'get_by_'
        ]
        
        for method in playwright_methods:
            # Buscar uso sin await
            pattern = rf'page\.{method}\('
            if re.search(pattern, code):
                # Verificar si tiene await antes
                pattern_with_await = rf'await\s+page\.{method}\('
                if not re.search(pattern_with_await, code):
                    self.warnings.append(
                        f"Método 'page.{method}()' debería usar 'await'"
                    )
        
        return not issues_found
    
    def validate_complexity(self, code: str) -> bool:
        """
        Valida que el código no sea innecesariamente complejo.
        
        Args:
            code: El código a validar
            
        Returns:
            True si la complejidad es aceptable
        """
        lines = code.split("\n")
        non_empty_lines = [line for line in lines if line.strip()]
        line_count = len(non_empty_lines)
        
        # Contar tests
        test_count = len(re.findall(r'async def test_\w+', code))
        
        # Verificar complejidad
        complexity_ok = True
        
        # Advertencia si hay demasiados tests
        if test_count > 3:
            self.warnings.append(
                f"Se generaron {test_count} tests. "
                f"Considera simplificar a 1-3 tests principales."
            )
            complexity_ok = False
        
        # Advertencia si el código es muy largo
        expected_lines = test_count * 20  # ~20 líneas por test
        if line_count > expected_lines * 2:
            self.warnings.append(
                f"Código muy extenso ({line_count} líneas para {test_count} tests). "
                f"Esperado: ~{expected_lines} líneas. "
                f"Considera simplificar."
            )
            complexity_ok = False
        
        # Detectar Page Object Model innecesario
        if "class " in code and "Page" in code:
            if test_count <= 2:
                self.suggestions.append(
                    "Detectado Page Object Model. "
                    "Para tests simples, considera usar código inline más simple."
                )
        
        # Detectar tests parametrizados innecesarios
        if "@pytest.mark.parametrize" in code:
            self.suggestions.append(
                "Detectado test parametrizado. "
                "Verifica si es realmente necesario o si complica innecesariamente."
            )
        
        return complexity_ok
    
    def validate_code(self, code: str) -> ValidationResult:
        """
        Ejecuta todas las validaciones.
        
        Args:
            code: El código Playwright a validar
            
        Returns:
            ValidationResult con todos los resultados
        """
        # Limpiar resultados previos
        self.errors = []
        self.warnings = []
        self.suggestions = []
        
        # Ejecutar todas las validaciones
        syntax_valid = self.validate_syntax(code)
        imports_valid = self.validate_imports(code)
        fixtures_valid = self.validate_fixtures(code)
        async_valid = self.validate_async_await(code)
        complexity_ok = self.validate_complexity(code)
        
        # Determinar si el código es válido
        # Errores = NO válido
        # Warnings/Suggestions = Válido pero mejorable
        is_valid = len(self.errors) == 0
        
        return ValidationResult(
            is_valid=is_valid,
            errors=self.errors.copy(),
            warnings=self.warnings.copy(),
            suggestions=self.suggestions.copy()
        )