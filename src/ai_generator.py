"""
AI Test Generator - Version 2
Generador modular que usa Claude API con prompts organizados.
"""

import os
import logging
from typing import Dict, Optional
from anthropic import Anthropic
from dotenv import load_dotenv

from .prompts import (
    SYSTEM_PROMPT,
    get_gherkin_prompt,
    get_playwright_prompt,
)

from .validators import CodeValidator, ValidationResult

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Cargar variables de entorno
load_dotenv()



class AITestGenerator:
    """
    Generador de tests usando Claude API.
    
    Esta clase maneja el workflow completo:
    1. User Story → Gherkin (usando get_gherkin_prompt)
    2. Gherkin → Playwright Code (usando get_playwright_prompt)
    
    Example:
        >>> generator = AITestGenerator()
        >>> result = generator.generate_complete_test(user_story)
        >>> print(result["gherkin"])
        >>> print(result["code"])
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "claude-sonnet-4-20250514",
        max_tokens: int = 4000,
    ):
        """
        Inicializa el generador.
        
        Args:
            api_key: API key de Anthropic (opcional, usa .env si no se provee)
            model: Modelo de Claude a usar
            max_tokens: Tokens máximos en la respuesta
        """
        # Obtener API key
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        
        if not self.api_key:
            raise ValueError(
                "ANTHROPIC_API_KEY no encontrada. "
                "Configúrala en .env o pásala como argumento."
            )
        
        # Configuración
        self.model = model
        self.max_tokens = max_tokens
        
        # Cliente de Anthropic
        self.client = Anthropic(api_key=self.api_key)
        self.validator = CodeValidator()
        
        logger.info(f"✅ AITestGenerator inicializado con modelo: {self.model}")
        
    def _call_claude(self, user_prompt: str) -> str:
        """
        Método privado para llamar a Claude API.

        Args:
            user_prompt: El prompt a enviar
            
        Returns:
            La respuesta de Claude como texto
            
        Raises:
            Exception: Si hay error en la llamada
        """
        try:
            logger.info("🤖 Llamando a Claude API...")
            
            response = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                system=SYSTEM_PROMPT,  # ← Aquí se usa SYSTEM_PROMPT
                messages=[
                    {"role": "user", "content": user_prompt}
                ]
            )
            
            # Extraer el texto de la respuesta
            result = response.content[0].text
            
            logger.info("✅ Respuesta recibida de Claude")
            return result
            
        except Exception as e:
            logger.error(f"❌ Error llamando a Claude API: {e}")
            raise    
    
    def generate_gherkin(self, user_story: str) -> str:
        """
        Genera escenarios Gherkin desde una user story.
        
        Args:
            user_story: La user story como texto
            
        Returns:
            Escenarios Gherkin generados
            
        Example:
            >>> story = "As a user I want to login..."
            >>> gherkin = generator.generate_gherkin(story)
            >>> print(gherkin)
            Feature: User Login
              Scenario: Successful login
                Given I am on the login page
                ...
        """
        logger.info("📝 Generando Gherkin desde user story...")
        
        # 1. Crear el prompt usando la función de prompts.py
        prompt = get_gherkin_prompt(user_story)
        
        # 2. Llamar a Claude
        gherkin = self._call_claude(prompt)
        
        logger.info("✅ Gherkin generado exitosamente")
        return gherkin    

    def generate_playwright_code(self, gherkin_scenarios: str) -> str:
        """
        Genera código Playwright desde escenarios Gherkin.
        
        Args:
            gherkin_scenarios: Los escenarios Gherkin
            
        Returns:
            Código Playwright en Python
            
        Example:
            >>> gherkin = "Feature: Login\\nScenario: ..."
            >>> code = generator.generate_playwright_code(gherkin)
            >>> print(code)
            import pytest
            from playwright.async_api import async_playwright
            ...
        """
        logger.info("💻 Generando código Playwright desde Gherkin...")
        
        # 1. Crear el prompt usando la función de prompts.py
        prompt = get_playwright_prompt(gherkin_scenarios)
        
        # 2. Llamar a Claude
        code = self._call_claude(prompt)
        
        # 3. Limpiar markdown si existe
        code = self._clean_code_response(code)
        
        logger.info("✅ Código Playwright generado exitosamente")
        return code
    
    
    def _clean_code_response(self, code: str) -> str:
        """
        Limpia la respuesta de Claude removiendo markdown.
        
        Args:
            code: Código posiblemente con markdown
            
        Returns:
            Código limpio
        """
        # Remover bloques de código markdown
        if "```python" in code:
            code = code.split("```python")[1]
            code = code.split("```")[0]
        elif "```" in code:
            code = code.split("```")[1]
            code = code.split("```")[0]
        
        return code.strip()

    def generate_complete_test(self, user_story: str) -> Dict[str, str]:
        """
        Genera test completo: User Story → Gherkin → Playwright Code.
        
        Ahora incluye validación automática del código generado.
        """
        logger.info("🚀 Iniciando generación completa de test...")
        logger.info(f"📖 User Story: {user_story[:100]}...")
        
        # PASO 1: User Story → Gherkin
        gherkin = self.generate_gherkin(user_story)
        
        # PASO 2: Gherkin → Playwright Code
        code = self.generate_playwright_code(gherkin)
        
        # PASO 3: Validar código generado ← NUEVO
        logger.info("🔍 Validando código generado...")
        validation_result = self.validator.validate_code(code)
        
        # Mostrar resultados de validación
        if validation_result.is_valid:
            logger.info("✅ Código validado exitosamente")
        else:
            logger.warning("⚠️  Código generado tiene problemas")
        
        # Mostrar errores si hay
        if validation_result.errors:
            logger.error("🔴 ERRORES ENCONTRADOS:")
            for error in validation_result.errors:
                logger.error(f"  - {error}")
        
        # Mostrar advertencias si hay
        if validation_result.warnings:
            logger.warning("⚠️  ADVERTENCIAS:")
            for warning in validation_result.warnings:
                logger.warning(f"  - {warning}")
        
        # Mostrar sugerencias si hay
        if validation_result.suggestions:
            logger.info("💡 SUGERENCIAS:")
            for suggestion in validation_result.suggestions:
                logger.info(f"  - {suggestion}")
        
        logger.info("🎉 Test completo generado!")
        
        return {
            "user_story": user_story,
            "gherkin": gherkin,
            "code": code,
            "validation": validation_result,
        }
