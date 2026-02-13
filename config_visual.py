"""
Configuración visual del Dashboard - Cambia el tema y estilos fácilmente.
"""

from enum import Enum


class VisualConfig:
    """Configuración visual centralizada del Dashboard"""
    
    # Tema activo
    ACTIVE_THEME = "dark"  # dark, corporate, tech, elegant
    
    # Animaciones
    ENABLE_ANIMATIONS = True
    ANIMATION_SPEED = "0.3s"  # fast, 0.3s, 0.5s, slow
    
    # Colores
    PRIMARY_COLOR = "#3B82F6"
    ACCENT_COLOR = "#06B6D4"
    SUCCESS_COLOR = "#10B981"
    WARNING_COLOR = "#F59E0B"
    DANGER_COLOR = "#EF4444"
    
    # Spacing
    CARD_PADDING = "0.85rem"
    MODAL_PADDING = "1.5rem 1.75rem"
    SECTION_SPACING = "1.5rem"
    
    # Border radius
    BORDER_RADIUS_SMALL = "8px"
    BORDER_RADIUS_MEDIUM = "12px"
    BORDER_RADIUS_LARGE = "16px"
    
    # Sombras
    SHADOW_LIGHT = "0 2px 4px rgba(0, 0, 0, 0.1)"
    SHADOW_MEDIUM = "0 4px 12px rgba(0, 0, 0, 0.15)"
    SHADOW_HEAVY = "0 20px 40px -12px rgba(0, 0, 0, 0.4)"
    
    # Efectos
    ENABLE_GRADIENT = True
    ENABLE_BLUR = True
    ENABLE_GLOW = True
    
    # Grid
    GRID_COLUMNS = 3
    GRID_GAP = "small"
    
    # Tipografía
    FONT_SIZE_BASE = "0.95rem"
    FONT_WEIGHT_NORMAL = "400"
    FONT_WEIGHT_MEDIUM = "500"
    FONT_WEIGHT_BOLD = "700"


class ThemeConfig(Enum):
    """Configuraciones de tema predefinidas"""
    
    DARK = {
        "name": "Oscuro",
        "bg_primary": "#0A0C10",
        "bg_secondary": "#111316",
        "bg_card": "#16181C",
        "text_primary": "#E8E9EA",
        "text_secondary": "#8B8E94",
        "accent": "#3B82F6",
        "description": "Tema oscuro profesional (predeterminado)"
    }
    
    CORPORATE = {
        "name": "Corporativo",
        "bg_primary": "#F8FAFC",
        "bg_secondary": "#E2E8F0",
        "bg_card": "#FFFFFF",
        "text_primary": "#0F172A",
        "text_secondary": "#475569",
        "accent": "#0066CC",
        "description": "Tema claro corporativo"
    }
    
    TECH = {
        "name": "Tech",
        "bg_primary": "#0F0F1E",
        "bg_secondary": "#1A1A2E",
        "bg_card": "#16213E",
        "text_primary": "#EAEAEA",
        "text_secondary": "#A8A8A8",
        "accent": "#00D4FF",
        "description": "Tema tech con neón"
    }
    
    MINT = {
        "name": "Mint",
        "bg_primary": "#F0FDFA",
        "bg_secondary": "#CCFBF1",
        "bg_card": "#F2F9F7",
        "text_primary": "#0D3B3B",
        "text_secondary": "#4B7776",
        "accent": "#14B8A6",
        "description": "Tema mint fresco"
    }


class ComponentsConfig:
    """Configuración específica de componentes"""
    
    # Tickets
    TICKET_CARD_HEIGHT = "auto"
    TICKET_TITLE_LINES = 2  # máximo de líneas
    SHOW_TICKET_ICONS = True
    
    # Modal
    MODAL_WIDTH = "large"  # small, medium, large
    MODAL_MAX_HEIGHT = "90vh"
    MODAL_BLUR_BACKDROP = True
    
    # Badges
    BADGE_SIZE = "small"  # tiny, small, medium
    BADGE_SHOW_ICONS = True
    BADGE_ANIMATION = True
    
    # Botones
    BUTTON_RADIUS = "8px"
    BUTTON_ANIMATION = True
    BUTTON_SHOW_ICONS = True
    
    # Formularios
    FORM_BORDER_RADIUS = "12px"
    FORM_FOCUS_GLOW = True
    FORM_TRANSITION_SPEED = "0.3s"


class PerformanceConfig:
    """Configuración de performance"""
    
    # CSS Cache
    CSS_CACHE_ENABLED = True
    
    # Animaciones
    ANIMATIONS_ENABLED = True
    REDUCE_MOTION_RESPECT = True  # Respetar preferencia del usuario
    
    # Efectos
    BLUR_EFFECTS = True
    SHADOW_EFFECTS = True
    GRADIENT_EFFECTS = True
    
    # Renderizado
    LAZY_LOAD_IMAGES = False
    OPTIMIZE_SCROLLBAR = True


class AccesibilityConfig:
    """Configuración de accesibilidad"""
    
    # WCAG Level
    WCAG_LEVEL = "AA"  # A, AA, AAA
    
    # Contraste
    ENFORCE_HIGH_CONTRAST = False
    MIN_CONTRAST_RATIO = 4.5  # 1:4.5 para AA
    
    # Navegación
    KEYBOARD_NAVIGATION = True
    SKIP_TO_CONTENT = True
    
    # Focus
    SHOW_FOCUS_INDICATORS = True
    FOCUS_INDICATOR_WIDTH = "2px"
    
    # Motion
    RESPECT_PREFERS_REDUCED_MOTION = True


class ResponsiveConfig:
    """Configuración responsiva"""
    
    # Breakpoints
    BREAKPOINT_MOBILE = "480px"
    BREAKPOINT_TABLET = "768px"
    BREAKPOINT_DESKTOP = "1024px"
    BREAKPOINT_WIDE = "1280px"
    
    # Grid adaptativo
    COLUMNS_MOBILE = 1
    COLUMNS_TABLET = 2
    COLUMNS_DESKTOP = 3
    COLUMNS_WIDE = 4
    
    # Padding adaptativo
    PADDING_MOBILE = "0.5rem"
    PADDING_TABLET = "0.75rem"
    PADDING_DESKTOP = "1rem"


def get_active_theme():
    """Obtiene la configuración del tema activo"""
    theme_name = VisualConfig.ACTIVE_THEME.upper()
    try:
        theme = ThemeConfig[theme_name]
        return theme.value
    except KeyError:
        # Default a DARK si no existe
        return ThemeConfig.DARK.value


def get_css_variables():
    """Genera variables CSS basadas en la configuración"""
    theme = get_active_theme()
    
    return f"""
    :root {{
        --bg-primary: {theme['bg_primary']};
        --bg-secondary: {theme['bg_secondary']};
        --bg-card: {theme['bg_card']};
        --text-primary: {theme['text_primary']};
        --text-secondary: {theme['text_secondary']};
        --accent: {theme['accent']};
        
        --radius-sm: {VisualConfig.BORDER_RADIUS_SMALL};
        --radius-md: {VisualConfig.BORDER_RADIUS_MEDIUM};
        --radius-lg: {VisualConfig.BORDER_RADIUS_LARGE};
        
        --shadow-light: {VisualConfig.SHADOW_LIGHT};
        --shadow-medium: {VisualConfig.SHADOW_MEDIUM};
        --shadow-heavy: {VisualConfig.SHADOW_HEAVY};
        
        --animation-speed: {VisualConfig.ANIMATION_SPEED};
        --card-padding: {VisualConfig.CARD_PADDING};
        --section-spacing: {VisualConfig.SECTION_SPACING};
    }}
    """


def apply_user_preferences():
    """Aplica preferencias del usuario (contraste alto, sin animaciones, etc.)"""
    import streamlit as st
    
    preferences = {
        "high_contrast": False,
        "reduce_motion": False,
        "font_size": "normal"  # small, normal, large
    }
    
    # Estas preferencias pueden guardarse en session_state
    if "visual_prefs" not in st.session_state:
        st.session_state.visual_prefs = preferences
    
    return st.session_state.visual_prefs


# ============================================================================
# EJEMPLOS DE USO
# ============================================================================

"""
Ejemplo 1: Cambiar tema
    VisualConfig.ACTIVE_THEME = "tech"

Ejemplo 2: Cambiar color primario
    VisualConfig.PRIMARY_COLOR = "#F59E0B"

Ejemplo 3: Deshabilitar animaciones
    VisualConfig.ENABLE_ANIMATIONS = False

Ejemplo 4: Aumentar grid columns
    VisualConfig.GRID_COLUMNS = 4

Ejemplo 5: Obtener tema activo
    tema = get_active_theme()
    
Ejemplo 6: Genera CSS personalizado
    css = get_css_variables()
"""
