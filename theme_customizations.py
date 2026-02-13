"""
Personalizaciones y temas adicionales para el Dashboard.
Archivo opcional para experimentos y variaciones de diseño.
"""


class ThemePresets:
    """Colecciones predefinidas de temas profesionales"""
    
    @staticmethod
    def get_corporate_theme():
        """Tema corporativo azul"""
        return {
            "primary": "#0066CC",
            "secondary": "#E8F0FE",
            "accent": "#1E40AF",
            "success": "#10B981",
            "danger": "#EF4444",
        }
    
    @staticmethod
    def get_tech_theme():
        """Tema tech/startup con neón"""
        return {
            "primary": "#00D4FF",
            "secondary": "#0A0E27",
            "accent": "#FFD60A",
            "success": "#52B788",
            "danger": "#E63946",
        }
    
    @staticmethod
    def get_elegant_theme():
        """Tema elegante y minimalista"""
        return {
            "primary": "#6366F1",
            "secondary": "#F8FAFC",
            "accent": "#4F46E5",
            "success": "#059669",
            "danger": "#DC2626",
        }


class DesignPatterns:
    """Patrones de diseño reutilizables"""
    
    CARD_SHADOW = "0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)"
    CARD_SHADOW_HOVER = "0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)"
    
    TRANSITION_SMOOTH = "all 300ms cubic-bezier(0.4, 0, 0.2, 1)"
    TRANSITION_BOUNCE = "all 300ms cubic-bezier(0.34, 1.56, 0.64, 1)"
    
    BORDER_RADIUS_SM = "4px"
    BORDER_RADIUS_MD = "8px"
    BORDER_RADIUS_LG = "12px"
    BORDER_RADIUS_XL = "16px"
    
    SPACING_XS = "0.25rem"
    SPACING_SM = "0.5rem"
    SPACING_MD = "1rem"
    SPACING_LG = "1.5rem"
    SPACING_XL = "2rem"


class Iconsets:
    """Conjuntos de iconos para diferentes contextos"""
    
    STATUS_ICONS = {
        "new": "🆕",
        "in_progress": "⏳",
        "won": "✅",
        "closed": "🔒",
        "pending": "⏸️",
        "urgent": "🚨"
    }
    
    PRIORITY_ICONS = {
        "Low": "📊",
        "Medium": "⚠️",
        "High": "🔴",
        "Critical": "🔥"
    }
    
    ACTION_ICONS = {
        "edit": "✏️",
        "delete": "🗑️",
        "save": "💾",
        "cancel": "❌",
        "refresh": "🔄",
        "search": "🔍",
        "filter": "⚙️",
        "export": "📤",
        "import": "📥"
    }
    
    SECTION_ICONS = {
        "description": "📝",
        "notes": "📋",
        "status": "📊",
        "priority": "⚡",
        "timeline": "📅",
        "team": "👥",
        "settings": "⚙️",
        "report": "📈"
    }


class Typography:
    """Estilos de tipografía profesionales"""
    
    FONT_FAMILY_PRIMARY = "'Segoe UI', 'Helvetica Neue', sans-serif"
    FONT_FAMILY_MONO = "'JetBrains Mono', 'Courier New', monospace"
    
    # Tamaños
    SIZE_XS = "0.75rem"
    SIZE_SM = "0.875rem"
    SIZE_BASE = "1rem"
    SIZE_LG = "1.125rem"
    SIZE_XL = "1.25rem"
    SIZE_2XL = "1.5rem"
    SIZE_3XL = "1.875rem"
    SIZE_4XL = "2.25rem"
    
    # Pesos
    WEIGHT_LIGHT = "300"
    WEIGHT_NORMAL = "400"
    WEIGHT_MEDIUM = "500"
    WEIGHT_SEMIBOLD = "600"
    WEIGHT_BOLD = "700"
    
    # Line heights
    LINE_HEIGHT_TIGHT = "1.25"
    LINE_HEIGHT_NORMAL = "1.5"
    LINE_HEIGHT_RELAXED = "1.75"


class AnimationLibrary:
    """Animaciones CSS reutilizables"""
    
    FADE_IN = """
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    """
    
    SLIDE_IN_TOP = """
    @keyframes slideInTop {
        from {
            opacity: 0;
            transform: translateY(-10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    """
    
    SLIDE_IN_LEFT = """
    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-10px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    """
    
    PULSE = """
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.8; }
    }
    """
    
    BOUNCE = """
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }
    """
    
    SHINE = """
    @keyframes shine {
        0% { background-position: -200%; }
        100% { background-position: 200%; }
    }
    """


class ResponsiveBreakpoints:
    """Breakpoints responsive profesionales"""
    
    MOBILE = "480px"
    TABLET = "768px"
    DESKTOP = "1024px"
    WIDE = "1280px"
    ULTRAWIDE = "1536px"
    
    @staticmethod
    def get_responsive_rule(mobile, tablet, desktop):
        """Genera reglas CSS responsive"""
        return f"""
        /* Mobile */
        @media (max-width: {ResponsiveBreakpoints.TABLET}) {{
            {mobile}
        }}
        /* Tablet */
        @media (min-width: {ResponsiveBreakpoints.TABLET}) and (max-width: {ResponsiveBreakpoints.DESKTOP}) {{
            {tablet}
        }}
        /* Desktop */
        @media (min-width: {ResponsiveBreakpoints.DESKTOP}) {{
            {desktop}
        }}
        """


class AccessibilityUtilities:
    """Utilidades para mejorar accesibilidad (WCAG 2.1)"""
    
    FOCUS_OUTLINE = "outline: 2px solid currentColor; outline-offset: 2px;"
    
    SKIP_TO_CONTENT = """
    <a href="#main-content" class="skip-link" style="
        position: absolute;
        top: -9999px;
        left: -9999px;
    ">Ir al contenido principal</a>
    """
    
    HIGH_CONTRAST_MODE = """
    @media (prefers-contrast: more) {
        * {
            border-width: 2px;
        }
    }
    """
    
    REDUCED_MOTION = """
    @media (prefers-reduced-motion: reduce) {
        * {
            animation-duration: 0.01ms !important;
            animation-iteration-count: 1 !important;
            transition-duration: 0.01ms !important;
        }
    }
    """
