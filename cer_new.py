
"""
ceramicWEB - Aplicación web para elegir, calcular y cotizar cerámicos/porcelanatos
Estructura de carpetas requerida en tu laptop:
  tu_proyecto/
  ├── app.py                    <- Este archivo
  └── imagenes/
      ├── portada.jpeg          <- Imagen principal del landing
      ├── PROMART_1.png         <- Carrara Li
      ├── PROMART_2.png         <- Nano Gris
      ├── PROMART_3.png         <- Cersaie  (nota: sin guion)
      ├── PROMART_4.png         <- Beige Nano Sur
      ├── PROMART_5.png         <- Valencia 20x120
      ├── PROMART_6.1.png       <- Carrara Blanco 120x60
      ├── SODIMAC_1.webp        <- Café Maderado Golden
      ├── SODIMAC_2.webp        <- Beige Premium Honey
      ├── SODIMAC_3.webp        <- Caramelo Kiara
      ├── SODIMAC_4.webp        <- Marrón Premium Nut
      ├── SODIMAC_5.webp        <- Bosque Beige
      ├── SODIMAC_6.webp        <- Oregon Beige
      ├── CASINELLI_1.webp      <- Alabastrino Blanco
      ├── CASINELLI_2.webp      <- Onyx Azul
      ├── CASINELLI_3.webp      <- Pure Onix Perla
      └── CASINELLI_4.webp      <- Eureka Beige

Instalación: pip install streamlit altair pandas pillow
Ejecución:   streamlit run app.py
"""

import streamlit as st
import pandas as pd
import altair as alt
import math
import os
import base64

# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURACIÓN DE PÁGINA
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ceramicWEB",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────────────────────────────────────
# BASE DE DATOS DE PRODUCTOS  (rutas de imagen EXACTAS según carpeta)
# ─────────────────────────────────────────────────────────────────────────────
PRODUCTOS = [
    # ── PROMART ───────────────────────────────────────────────────────────────
    {
        "id": "p1", "tienda": "PROMART",
        "nombre": "Porcelanato Marmolizado Carrara Li 60x60cm",
        "formato": "60x60 cm", "precio_m2": 58.90, "rendimiento": 1.44,
        "imagen": "OTRO/PROMART_1.png",
        "url": "https://www.promart.pe/porcelanato-marmolizado-60x60-carrara-li-1-44m2/p",
        "tags": ["Ideal para sala", "Fácil de limpiar", "Alta durabilidad"],
        "color_tags": ["#3B82F6", "#10B981", "#8B5CF6"],
    },
    {
        "id": "p2", "tienda": "PROMART",
        "nombre": "Porcelanato Pulido Liso Nano Gris 60x60cm",
        "formato": "60x60 cm", "precio_m2": 52.90, "rendimiento": 1.44,
        "imagen": "OTRO/PROMART_2.png",
        "url": "https://www.promart.pe/piso-porcelanato-liso-unicolor-gris-60x60cm-1-44m2-167830/p",
        "tags": ["Moderno", "Antideslizante", "Resistente"],
        "color_tags": ["#3B82F6", "#F59E0B", "#10B981"],
    },
    {
        "id": "p3", "tienda": "PROMART",
        "nombre": "Porcelanato Mármol Cersaie 60x60cm",
        "formato": "60x60 cm", "precio_m2": 64.90, "rendimiento": 1.44,
        "imagen": "OTRO/PROMART_3.png",
        "url": "https://www.promart.pe/porcelanato-marmol-cersaie-60x60cm-1-44m2/p",
        "tags": ["Premium", "Elegante", "Alta durabilidad"],
        "color_tags": ["#8B5CF6", "#EC4899", "#10B981"],
    },
    {
        "id": "p4", "tienda": "PROMART",
        "nombre": "Porcelanato Beige Nano Sur 60x60cm",
        "formato": "60x60 cm", "precio_m2": 47.90, "rendimiento": 1.44,
        "imagen": "OTRO/PROMART_4.png",
        "url": "https://www.promart.pe/piso-porcelanato-liso-beige-nano-sur-60x60cm/p",
        "tags": ["Económico", "Cálido", "Fácil de limpiar"],
        "color_tags": ["#10B981", "#F59E0B", "#3B82F6"],
    },
    {
        "id": "p5", "tienda": "PROMART",
        "nombre": "Tablón Gress Maderado Valencia 20x120cm",
        "formato": "20x120 cm", "precio_m2": 55.90, "rendimiento": 1.44,
        "imagen": "OTRO/PROMART_5.png",
        "url": "https://www.promart.pe/tablon-gress-maderado-valencia-20x120cm-1-44m2-orange/p",
        "tags": ["Efecto madera", "Largo formato", "Moderno"],
        "color_tags": ["#F59E0B", "#3B82F6", "#EC4899"],
    },
    {
        "id": "p6", "tienda": "PROMART",
        "nombre": "Porcelanato Carrara Blanco 120x60cm",
        "formato": "120x60 cm", "precio_m2": 72.90, "rendimiento": 2.16,
        "imagen": "OTRO/PROMART_6.png",
        "url": "https://www.promart.pe/porcelanato-gress-marmolizado-carrara-blanco-120x60-2-16m2/p",
        "tags": ["Gran formato", "Lujoso", "Luminoso"],
        "color_tags": ["#8B5CF6", "#EC4899", "#10B981"],
    },
    # ── SODIMAC ───────────────────────────────────────────────────────────────
    {
        "id": "s1", "tienda": "SODIMAC",
        "nombre": "Cerámica Café Maderado 20x61cm Golden",
        "formato": "20x61 cm", "precio_m2": 38.90, "rendimiento": 1.86,
        "imagen": "OTRO/SODIMAC_1.webp",
        "url": "https://www.sodimac.com.pe/sodimac-pe/articulo/136358596/ceramica-cafe-maderado-20x61cm-1-86m2-golden/136358597",
        "tags": ["Efecto madera", "Acogedor", "Fácil mantenimiento"],
        "color_tags": ["#F59E0B", "#10B981", "#3B82F6"],
    },
    {
        "id": "s2", "tienda": "SODIMAC",
        "nombre": "Cerámica Beige Maderado 20x61cm Premium Honey",
        "formato": "20x61 cm", "precio_m2": 36.90, "rendimiento": 1.86,
        "imagen": "OTRO/SODIMAC_2.webp",
        "url": "https://www.sodimac.com.pe/sodimac-pe/articulo/136358592/ceramica-beige-maderado-20x61cm-1-86m2-premium-honey/136358593",
        "tags": ["Cálido", "Versátil", "Económico"],
        "color_tags": ["#F59E0B", "#3B82F6", "#10B981"],
    },
    {
        "id": "s3", "tienda": "SODIMAC",
        "nombre": "Cerámica Caramelo Maderado 60x60cm Kiara",
        "formato": "60x60 cm", "precio_m2": 42.90, "rendimiento": 1.48,
        "imagen": "OTRO/SODIMAC_3.webp",
        "url": "https://www.sodimac.com.pe/sodimac-pe/articulo/131495284/ceramica-caramelo-maderado-60x60cm-1-48m2-kiara-caramelo/131495285",
        "tags": ["Ideal para sala", "Gran formato", "Elegante"],
        "color_tags": ["#3B82F6", "#F59E0B", "#8B5CF6"],
    },
    {
        "id": "s4", "tienda": "SODIMAC",
        "nombre": "Cerámica Marrón Maderado 20x61cm Premium Nut",
        "formato": "20x61 cm", "precio_m2": 39.90, "rendimiento": 1.86,
        "imagen": "OTRO/SODIMAC_4.webp",
        "url": "https://www.sodimac.com.pe/sodimac-pe/articulo/136358607/ceramica-marron-maderado-20x61cm-1-86m2-premium-nut/136358611",
        "tags": ["Oscuro", "Resistente", "Moderno"],
        "color_tags": ["#8B5CF6", "#3B82F6", "#10B981"],
    },
    {
        "id": "s5", "tienda": "SODIMAC",
        "nombre": "Cerámica Maderada Bosque Beige 45x45cm",
        "formato": "45x45 cm", "precio_m2": 33.90, "rendimiento": 2.29,
        "imagen": "OTRO/SODIMAC_5.webp",
        "url": "https://www.sodimac.com.pe/sodimac-pe/articulo/151121061/x-maderadas-bosque-beige-2-29-m2/151121063",
        "tags": ["Económico", "Natural", "Fácil mantenimiento"],
        "color_tags": ["#10B981", "#F59E0B", "#3B82F6"],
    },
    {
        "id": "s6", "tienda": "SODIMAC",
        "nombre": "Cerámica Beige Maderado 46x46cm Oregon",
        "formato": "46x46 cm", "precio_m2": 35.90, "rendimiento": 1.90,
        "imagen": "OTRO/SODIMAC_6.webp",
        "url": "https://www.sodimac.com.pe/sodimac-pe/articulo/113778095/ceramica-beige-maderado-46x46cm-1-9m2-oregon/113778097",
        "tags": ["Clásico", "Versátil", "Buen precio"],
        "color_tags": ["#F59E0B", "#10B981", "#3B82F6"],
    },
    # ── CASINELLI ─────────────────────────────────────────────────────────────
    {
        "id": "c1", "tienda": "CASINELLI",
        "nombre": "Porcelanato Geotiles Alabastrino Blanco 60x120",
        "formato": "60x120 cm", "precio_m2": 89.90, "rendimiento": 1.44,
        "imagen": "OTRO/CASINELLI_1.webp",
        "url": "https://www.cassinelli.com/114701-porcelanato-geotiles-alabastrino-blanco-honed-pulido-rect--dest--60x120-caja-1-44-m2/p",
        "tags": ["Premium", "Gran formato", "Luminoso"],
        "color_tags": ["#8B5CF6", "#3B82F6", "#10B981"],
    },
    {
        "id": "c2", "tienda": "CASINELLI",
        "nombre": "Porcelanato Tele Di Marmo Onyx Azul 120x278cm",
        "formato": "120x278 cm", "precio_m2": 145.90, "rendimiento": 3.33,
        "imagen": "OTRO/CASINELLI_2.webp",
        "url": "https://www.cassinelli.com/109755-porcelanato-tele-di-marmo-onyx-azul-brillante---120x278-cm---3-33-m2/p",
        "tags": ["Ultra premium", "Exclusivo", "Espectacular"],
        "color_tags": ["#EC4899", "#8B5CF6", "#3B82F6"],
    },
    {
        "id": "c3", "tienda": "CASINELLI",
        "nombre": "Porcelanato Tele Di Marmo Pure Onix Perla 60x120",
        "formato": "60x120 cm", "precio_m2": 115.90, "rendimiento": 1.44,
        "imagen": "OTRO/CASINELLI_3.webp",
        "url": "https://www.cassinelli.com/113850-porcelanato-tele-di-marmo-pure-onix-perla-pulido---60x120-cm---1-44-m2/p",
        "tags": ["Lujoso", "Pulido", "Elegante"],
        "color_tags": ["#8B5CF6", "#EC4899", "#10B981"],
    },
    {
        "id": "c4", "tienda": "CASINELLI",
        "nombre": "Porcelanato Eureka Beige Mate 60x120cm",
        "formato": "60x120 cm", "precio_m2": 79.90, "rendimiento": 1.44,
        "imagen": "OTRO/CASINELLI_4.webp",
        "url": "https://www.cassinelli.com/103174-porcelanato-eureka-beige-mate---60x120-cm---1-44-m2/p",
        "tags": ["Mate", "Sofisticado", "Versátil"],
        "color_tags": ["#F59E0B", "#3B82F6", "#10B981"],
    },
]

# ─────────────────────────────────────────────────────────────────────────────
# DISTRITOS + TIENDAS CERCANAS
# ─────────────────────────────────────────────────────────────────────────────
DISTRITOS = {
    "Miraflores": (-12.1219, -77.0297), "San Isidro": (-12.1000, -77.0400),
    "Surco": (-12.1500, -76.9978), "La Molina": (-12.0831, -76.9469),
    "San Borja": (-12.1050, -77.0003), "Jesús María": (-12.0700, -77.0481),
    "Pueblo Libre": (-12.0739, -77.0633), "Magdalena": (-12.0897, -77.0729),
    "San Miguel": (-12.0775, -77.0956), "Lince": (-12.0850, -77.0344),
    "Breña": (-12.0600, -77.0481), "Cercado de Lima": (-12.0432, -77.0282),
    "Los Olivos": (-11.9900, -77.0700), "San Martín de Porres": (-12.0200, -77.0900),
    "Independencia": (-11.9900, -77.0550), "Comas": (-11.9356, -77.0553),
    "Ate": (-12.0253, -76.9422), "Santa Anita": (-12.0478, -76.9736),
    "Chorrillos": (-12.1700, -77.0208), "Barranco": (-12.1500, -77.0206),
    "Villa El Salvador": (-12.2133, -76.9428),
    "San Juan de Lurigancho": (-12.0000, -77.0100),
    "Callao": (-12.0565, -77.1181), "Surquillo": (-12.1100, -77.0100),
    "La Victoria": (-12.0653, -77.0178),
}

TIENDAS_CERCANAS = {
    "Miraflores":   [("Promart Miraflores", -12.1050, -77.0250, "PROMART"), ("Sodimac Miraflores", -12.1200, -77.0350, "SODIMAC")],
    "Surco":        [("Promart Surco", -12.1480, -76.9950, "PROMART"), ("Casinelli Surco", -12.1530, -76.9900, "CASINELLI")],
    "San Isidro":   [("Sodimac San Isidro", -12.0980, -77.0380, "SODIMAC"), ("Casinelli San Isidro", -12.1020, -77.0420, "CASINELLI")],
    "La Molina":    [("Promart La Molina", -12.0800, -76.9500, "PROMART"), ("Sodimac La Molina", -12.0860, -76.9470, "SODIMAC")],
    "Los Olivos":   [("Promart Los Olivos", -11.9920, -77.0680, "PROMART"), ("Sodimac Los Olivos", -11.9880, -77.0720, "SODIMAC")],
    "Ate":          [("Promart Ate", -12.0270, -76.9450, "PROMART"), ("Sodimac Ate", -12.0230, -76.9400, "SODIMAC")],
    "Chorrillos":   [("Promart Chorrillos", -12.1680, -77.0200, "PROMART"), ("Sodimac Chorrillos", -12.1720, -77.0220, "SODIMAC")],
}

PRECIOS_TIENDAS = [
    {"Tienda": "Promart - Surco",        "Precio_m2": 47.90, "Precio_caja": 68.98,  "Stock": "Disponible",    "Distancia": "2.1 km", "Tienda_marca": "PROMART"},
    {"Tienda": "Sodimac - Surquillo",    "Precio_m2": 58.00, "Precio_caja": 84.82,  "Stock": "Disponible",    "Distancia": "4.2 km", "Tienda_marca": "SODIMAC"},
    {"Tienda": "Promart - Ate",          "Precio_m2": 60.50, "Precio_caja": 87.12,  "Stock": "Pocas unidades","Distancia": "5.5 km", "Tienda_marca": "PROMART"},
    {"Tienda": "Casinelli - Miraflores", "Precio_m2": 61.30, "Precio_caja": 88.27,  "Stock": "Disponible",    "Distancia": "3.8 km", "Tienda_marca": "CASINELLI"},
    {"Tienda": "Casinelli - San Isidro", "Precio_m2": 63.50, "Precio_caja": 91.44,  "Stock": "Disponible",    "Distancia": "6.1 km", "Tienda_marca": "CASINELLI"},
]

# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────
def img_to_base64(path: str) -> str:
    """Convierte imagen a base64 para embeber en HTML."""
    try:
        with open(path, "rb") as f:
            data = base64.b64encode(f.read()).decode()
        ext = path.split(".")[-1].lower()
        mime = {"jpg": "jpeg", "jpeg": "jpeg", "png": "png", "webp": "webp"}.get(ext, "png")
        return f"data:image/{mime};base64,{data}"
    except:
        return ""

def safe_img_html(path: str, alt: str = "", height: int = 160, fit: str = "cover") -> str:
    """Devuelve HTML con la imagen embebida en base64, o placeholder si no existe."""
    b64 = img_to_base64(path)
    if b64:
        return (
            f'<img src="{b64}" alt="{alt}" '
            f'style="width:100%;height:{height}px;object-fit:{fit};'
            f'border-radius:10px;display:block;background:#0F172A;" />'
        )
    return f"""
    <div style="width:100%;height:{height}px;background:#1E293B;border:1px dashed #334155;
                border-radius:10px;display:flex;align-items:center;justify-content:center;
                color:#475569;font-size:0.85rem;flex-direction:column;gap:0.4rem;">
        <span style="font-size:2rem;">🖼️</span>
        <span>{alt or path}</span>
    </div>"""

def safe_img_st(path: str, alt: str = ""):
    """Muestra imagen con st.image si existe, si no placeholder HTML."""
    if os.path.exists(path):
        st.image(path, use_container_width=True)
    else:
        st.markdown(safe_img_html(path, alt), unsafe_allow_html=True)

def get_tienda_color(tienda: str) -> str:
    return {"PROMART": "#F97316", "SODIMAC": "#3B82F6", "CASINELLI": "#10B981"}.get(tienda, "#8B5CF6")

def calcular_materiales(area_m2: float, precio_m2: float, rendimiento: float) -> dict:
    cajas              = math.ceil(area_m2 / rendimiento)
    costo_ceramica     = cajas * rendimiento * precio_m2
    bolsas_pegamento   = math.ceil(area_m2 / 3.5)
    costo_pegamento    = bolsas_pegamento * 28.50
    bolsas_fragua      = math.ceil(area_m2 / 12)
    costo_fragua       = bolsas_fragua * 21.90
    paq_crucetas       = math.ceil(area_m2 / 4)
    costo_crucetas     = paq_crucetas * 11.90
    paq_niveladores    = math.ceil(area_m2 / 4)
    costo_niveladores  = paq_niveladores * 17.90
    costo_complementos = costo_pegamento + costo_fragua + costo_crucetas + costo_niveladores
    costo_total        = costo_ceramica + costo_complementos
    return {
        "cajas": cajas, "costo_ceramica": costo_ceramica,
        "bolsas_pegamento": bolsas_pegamento, "costo_pegamento": costo_pegamento,
        "bolsas_fragua": bolsas_fragua, "costo_fragua": costo_fragua,
        "paq_crucetas": paq_crucetas, "costo_crucetas": costo_crucetas,
        "paq_niveladores": paq_niveladores, "costo_niveladores": costo_niveladores,
        "costo_complementos": costo_complementos, "costo_total": costo_total,
    }

# ─────────────────────────────────────────────────────────────────────────────
# CSS GLOBAL
# ─────────────────────────────────────────────────────────────────────────────
def inject_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

    html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
        background-color: #0F172A !important;
        font-family: 'Inter', sans-serif !important;
        color: #F1F5F9 !important;
    }
    #MainMenu, footer, header { visibility: hidden; }
    [data-testid="stToolbar"] { display: none; }
    [data-testid="collapsedControl"] { display: none; }

    .main .block-container {
        max-width: 1280px;
        padding: 1.5rem 2rem 4rem 2rem;
        margin: 0 auto;
    }

    /* ── Botones ── */
    .stButton > button {
        background: linear-gradient(135deg, #3B82F6, #2563EB);
        color: white !important;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 1.5rem;
        font-weight: 700;
        font-size: 1rem !important;
        cursor: pointer;
        transition: all 0.2s ease;
        width: 100%;
        letter-spacing: 0.01em;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #60A5FA, #3B82F6);
        transform: translateY(-2px);
        box-shadow: 0 6px 24px rgba(59,130,246,0.45);
    }

    /* ── Selectbox ── */
    .stSelectbox > div > div {
        background-color: #1E293B !important;
        border: 1.5px solid #334155 !important;
        border-radius: 10px !important;
        color: #F1F5F9 !important;
        font-size: 1rem !important;
    }
    div[data-baseweb="select"] * { background-color: #1E293B !important; color: #F1F5F9 !important; }
    div[data-baseweb="popover"] * { background-color: #1E293B !important; color: #F1F5F9 !important; }
    div[data-baseweb="menu"] { background-color: #1E293B !important; border: 1px solid #334155 !important; border-radius: 10px !important; }
    div[data-baseweb="option"] { background-color: #1E293B !important; color: #F1F5F9 !important; font-size: 1rem !important; }
    div[data-baseweb="option"]:hover { background-color: #334155 !important; color: #60A5FA !important; }
    li[aria-selected="true"] { background-color: #1D4ED8 !important; color: white !important; }

    /* ── Inputs ── */
    .stNumberInput > div > div > input {
        background-color: #1E293B !important;
        border: 1.5px solid #334155 !important;
        border-radius: 10px !important;
        color: #F1F5F9 !important;
        font-size: 1.05rem !important;
        font-weight: 500;
    }
    .stNumberInput > div > div > input:focus {
        border-color: #3B82F6 !important;
        box-shadow: 0 0 0 3px rgba(59,130,246,0.2) !important;
    }
    .stSelectbox label, .stNumberInput label { color: #94A3B8 !important; font-weight: 600; font-size: 0.95rem !important; }

    /* ── Multiselect ── */
    .stMultiSelect > div > div {
        background-color: #1E293B !important;
        border: 1.5px solid #334155 !important;
        border-radius: 10px !important;
        color: #F1F5F9 !important;
    }
    .stMultiSelect label { color: #94A3B8 !important; font-weight: 600; font-size: 0.95rem !important; }
    [data-baseweb="tag"] { background-color: #1D4ED8 !important; color: white !important; }

    /* ── Scrollbar ── */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: #0F172A; }
    ::-webkit-scrollbar-thumb { background: #334155; border-radius: 3px; }

    /* ── Nav pills ── */
    .nav-pills-wrap {
        display: flex; gap: 0.4rem; margin-bottom: 2rem;
        background: #1E293B; border-radius: 14px; padding: 0.4rem;
    }
    .nav-pill { flex:1; text-align:center; padding: 0.5rem 0.6rem; border-radius:10px;
                font-size: 0.9rem; font-weight: 600; color: #64748B; }
    .nav-pill.active { background: #3B82F6; color: white; }

    /* ── Step header ── */
    .step-header {
        background: #1E293B; border-left: 4px solid #3B82F6;
        border-radius: 0 14px 14px 0; padding: 1rem 1.5rem; margin-bottom: 1.5rem;
    }
    .step-badge {
        background: #3B82F6; color: white; font-size: 0.8rem; font-weight: 700;
        padding: 3px 12px; border-radius: 20px; display: inline-block; margin-bottom: 0.4rem;
    }
    .step-title { font-size: 2rem; font-weight: 800; color: #F1F5F9; margin: 0; }

    /* ── Info / warn boxes ── */
    .info-box {
        background: #0F2231; border: 1px solid #1E4976; border-radius: 12px;
        padding: 1rem 1.4rem; margin: 0.8rem 0; font-size: 1rem; color: #93C5FD;
    }
    .warn-box {
        background: #2D1B00; border: 1px solid #92400E; border-radius: 12px;
        padding: 1rem 1.4rem; margin: 0.8rem 0; color: #FCD34D; font-size: 0.95rem;
    }

    /* ── Big metrics ── */
    .big-metric {
        background: linear-gradient(135deg, #1E3A5F, #1E293B);
        border: 1.5px solid #3B82F6; border-radius: 16px;
        padding: 1.8rem; text-align: center; margin: 0.6rem 0;
    }
    .big-metric .val { font-size: 3.2rem; font-weight: 900; color: #60A5FA; line-height: 1.1; }
    .big-metric .lbl { font-size: 1rem; color: #94A3B8; margin-top: 0.4rem; font-weight: 500; }
    .big-metric-green { background: linear-gradient(135deg, #052e16, #1E293B); border-color: #10B981; }
    .big-metric-green .val { color: #34D399; }

    /* ── Small info tiles ── */
    .info-tile {
        background: #1E293B; border: 1px solid #334155; border-radius: 12px;
        padding: 1rem; text-align: center;
    }
    .info-tile .tl { color: #64748B; font-size: 0.85rem; font-weight: 500; }
    .info-tile .tv { color: #F1F5F9; font-size: 1.2rem; font-weight: 700; margin-top: 0.2rem; }

    /* ── Material rows ── */
    .mat-row { display:flex; justify-content:space-between; align-items:center;
               padding: 0.9rem 0; border-bottom: 1px solid #1E293B; }
    .mat-row:last-child { border-bottom: none; }
    .mat-name { color: #CBD5E1; font-size: 1rem; font-weight: 500; }
    .mat-sub { color: #64748B; font-size: 0.82rem; margin-top: 2px; }
    .mat-price { color: #F1F5F9; font-weight: 700; font-size: 1.05rem; }

    /* ── Total box ── */
    .total-box {
        background: linear-gradient(135deg, #0F172A, #1E293B);
        border: 2px solid #3B82F6; border-radius: 14px; padding: 1.4rem 1.8rem; margin-top: 1rem;
    }
    .total-lbl { color: #94A3B8; font-size: 0.95rem; font-weight: 500; }
    .total-val { color: #60A5FA; font-size: 2rem; font-weight: 900; margin-top: 0.2rem; }

    /* ── Store cards ── */
    .store-card {
        background: #1E293B; border: 1.5px solid #334155; border-radius: 14px;
        padding: 1.1rem 1.4rem; margin-bottom: 0.7rem; cursor: pointer; transition: all 0.2s;
    }
    .store-card:hover { border-color: #3B82F6; box-shadow: 0 0 18px rgba(59,130,246,0.2); }
    .store-card.selected { border-color: #10B981 !important; box-shadow: 0 0 22px rgba(16,185,129,0.25); }
    .store-name { color: #F1F5F9; font-weight: 700; font-size: 1.05rem; }
    .store-sub { color: #64748B; font-size: 0.85rem; margin-top: 2px; }
    .store-price { color: #60A5FA; font-size: 1.15rem; font-weight: 800; }
    .store-price-sub { color: #64748B; font-size: 0.8rem; }

    /* ── Badges ── */
    .badge-green { background:#10B981;color:white;padding:3px 12px;border-radius:20px;font-size:0.78rem;font-weight:700; }
    .badge-yellow { background:#F59E0B;color:#0F172A;padding:3px 12px;border-radius:20px;font-size:0.78rem;font-weight:700; }
    .badge-red { background:#EF4444;color:white;padding:3px 12px;border-radius:20px;font-size:0.78rem;font-weight:700; }
    .badge-blue { background:#3B82F6;color:white;padding:3px 12px;border-radius:20px;font-size:0.78rem;font-weight:700; }

    /* ── Tags en producto ── */
    .tag { display:inline-block; border:1px solid; border-radius:20px;
           font-size:0.78rem; font-weight:600; padding:3px 10px; margin:2px 2px; }

    /* ── WhatsApp / product link ── */
    .wa-btn {
        background: linear-gradient(135deg,#25D366,#128C7E); color:white;
        text-decoration:none; border-radius:14px; padding:1.1rem 2rem; font-size:1.05rem;
        font-weight:800; display:block; text-align:center; margin:0.5rem 0; transition:all 0.2s;
    }
    .wa-btn:hover { opacity:0.9; transform:translateY(-1px); color:white; text-decoration:none; }
    .prod-link-btn {
        background:transparent; color:#60A5FA; text-decoration:none;
        border:2px solid #3B82F6; border-radius:14px; padding:0.95rem 2rem; font-size:1rem;
        font-weight:700; display:block; text-align:center; margin:0.5rem 0; transition:all 0.2s;
    }
    .prod-link-btn:hover { background:#1e3a5f; color:#93C5FD; text-decoration:none; }

    /* ── Hero landing ── */
    .hero-title { font-size:3.4rem; font-weight:900; line-height:1.12; color:#F1F5F9; margin-bottom:1.2rem; }
    .hero-title span { color:#60A5FA; }
    .hero-sub { color:#94A3B8; font-size:1.15rem; line-height:1.7; margin-bottom:1.5rem; }
    .feature-item {
        display:flex; align-items:center; gap:0.9rem; padding:1rem 1.2rem;
        background:#1E293B; border:1px solid #334155; border-radius:12px; margin-bottom:0.6rem;
        color:#CBD5E1; font-size:1rem; font-weight:500;
    }
    .feature-num {
        background:#3B82F6; color:white; width:32px; height:32px; border-radius:50%;
        display:flex; align-items:center; justify-content:center; font-size:0.9rem;
        font-weight:800; flex-shrink:0;
    }

    /* ── Cotización lista compra ── */
    .cot-row { display:flex; justify-content:space-between; align-items:center;
               padding: 0.95rem 0; border-bottom:1px solid #334155; }
    .cot-row:last-child { border-bottom:none; }
    .cot-name { color:#CBD5E1; font-size:1rem; font-weight:500; }
    .cot-sub { color:#64748B; font-size:0.82rem; margin-top:2px; }
    .cot-price { color:#F1F5F9; font-weight:700; font-size:1.05rem; }
    </style>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# NAV PILLS
# ─────────────────────────────────────────────────────────────────────────────
def nav_pills(current: int):
    labels = ["Inicio", "Proyecto", "Productos", "Calculadora", "Tiendas", "Cotización"]
    pills = "".join(
        f'<div class="nav-pill {"active" if i == current else ""}">{l}</div>'
        for i, l in enumerate(labels)
    )
    st.markdown(f'<div class="nav-pills-wrap">{pills}</div>', unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════════════════════
# PASO 0 – LANDING
# ═════════════════════════════════════════════════════════════════════════════
def pantalla_landing():
    nav_pills(0)

    col_txt, col_img = st.columns([1.1, 0.9], gap="large")

    with col_txt:
        # Nombre de la web
        st.markdown("""
        <div style="text-align:center;margin-bottom:1.2rem;">
            <div style="font-size:3rem;font-weight:900;color:#F1F5F9;letter-spacing:-0.03em;">
                🏠 <span style="color:#60A5FA;">ceramic</span>WEB
            </div>
            <span style="background:#1E3A5F;color:#60A5FA;padding:4px 16px;
                        border-radius:20px;font-size:0.9rem;font-weight:600;">
                Asistente de cotización
            </span>
        </div>
        <h1 class="hero-title">
            Te ayudamos a<br>
            <span>elegir, calcular</span><br>
            y cotizar cerámicos o<br>porcelanatos para tu hogar
        </h1>
        <p class="hero-sub">
            Sin tecnicismos. Sin complicaciones. En pocos pasos podrás comparar opciones,
            estimar materiales y solicitar una cotización con mayor confianza.
        </p>
        """, unsafe_allow_html=True)

        st.markdown('<p style="color:#CBD5E1;font-size:1.05rem;font-weight:700;margin-bottom:0.6rem;">¿Cómo funciona?</p>', unsafe_allow_html=True)
        features = [
            ("🏠", "Elige el ambiente a remodelar"),
            ("🗂️", "Explora productos recomendados"),
            ("📐", "Calcula materiales y costos"),
            ("🏪", "Compara tiendas y cotiza"),
        ]
        for i, (icon, text) in enumerate(features, 1):
            st.markdown(f"""
            <div class="feature-item">
                <div class="feature-num">{i}</div>
                <span>{icon} {text}</span>
            </div>""", unsafe_allow_html=True)

        st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)
        col_btn, col_info = st.columns([1, 1])
        with col_btn:
            if st.button("🚀 Empezar ahora", use_container_width=True):
                st.session_state.step = 1
                st.rerun()
        with col_info:
            st.markdown("""
            <div style="padding:0.8rem;text-align:center;color:#64748B;font-size:0.9rem;">
                ✅ Gratis · Sin registro · En minutos<br>
                <span style="font-size:0.82rem;">Compara precios, revisa stock y cotiza en tiendas de Lima</span>
            </div>""", unsafe_allow_html=True)

    with col_img:
        # Imagen portada
        portada_path = "OTRO/portada.jpeg"
        b64_portada = img_to_base64(portada_path)
        if b64_portada:
            st.markdown(f"""
            <div style="border-radius:20px;overflow:hidden;border:1px solid #334155;box-shadow:0 20px 60px rgba(0,0,0,0.5);">
                <img src="{b64_portada}" style="width:100%;display:block;"/>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background:linear-gradient(135deg,#1E3A5F,#1E293B);border:1px solid #334155;
                        border-radius:20px;padding:4rem 2rem;text-align:center;color:#475569;
                        box-shadow:0 20px 60px rgba(0,0,0,0.5);">
                <div style="font-size:4rem;margin-bottom:1rem;">🏠</div>
                <div style="font-size:1rem;color:#64748B;">Coloca "portada.jpeg" en la carpeta imagenes/</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("""
        <div style="display:flex;gap:0.6rem;margin-top:1rem;flex-wrap:wrap;">
            <span style="background:#F9731622;border:1px solid #F97316;color:#FB923C;
                          padding:6px 14px;border-radius:20px;font-size:0.88rem;font-weight:600;">🏢 Promart</span>
            <span style="background:#3B82F622;border:1px solid #3B82F6;color:#60A5FA;
                          padding:6px 14px;border-radius:20px;font-size:0.88rem;font-weight:600;">🏢 Sodimac</span>
            <span style="background:#10B98122;border:1px solid #10B981;color:#34D399;
                          padding:6px 14px;border-radius:20px;font-size:0.88rem;font-weight:600;">🏢 Casinelli</span>
        </div>""", unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════════════════════
# PASO 1 – PROYECTO
# ═════════════════════════════════════════════════════════════════════════════
def pantalla_proyecto():
    nav_pills(1)
    st.markdown("""
    <div class="step-header">
        <span class="step-badge">Paso 1 de 5</span>
        <h2 class="step-title">Tu proyecto</h2>
    </div>
    <div class="info-box">
        📍 Esta información se usará para calcular materiales y mostrar tiendas cercanas a tu distrito.
    </div>
    """, unsafe_allow_html=True)

    col_left, col_right = st.columns([1, 1], gap="large")

    with col_left:
        st.markdown('<p style="color:#F1F5F9;font-size:1.15rem;font-weight:700;margin-bottom:0.8rem;">🏠 ¿Dónde vas a remodelar?</p>', unsafe_allow_html=True)
        
        ambientes = [
            ("OTRO/Baño.webp",   "Baño"),
            ("OTRO/Cocina.jpg",  "Cocina"),
            ("OTRO/Sala.webp",   "Sala"),
        ]
        cols_amb = st.columns(3)
        for i, (img_file, amb) in enumerate(ambientes):
            with cols_amb[i]:
                is_active = st.session_state.get("ambiente") == amb
                border = "#3B82F6" if is_active else "#334155"
                bg = "#1E3A5F" if is_active else "#1E293B"
                img_html = safe_img_html(img_file, amb, height=120)
                st.markdown(f"""
                <div style="background:{bg};border:2px solid {border};border-radius:14px;
                            padding:0.6rem 0.6rem 0.4rem 0.6rem;margin-bottom:0.5rem;">
                    {img_html}
                    <div style="color:#F1F5F9;font-size:0.95rem;font-weight:700;
                                text-align:center;margin-top:0.5rem;">{amb}</div>
                </div>""", unsafe_allow_html=True)
                btn_lbl = f"✓ {amb}" if is_active else f"Elegir {amb}"
                if st.button(btn_lbl, key=f"amb_{amb}", use_container_width=True):
                    st.session_state.ambiente = amb
                    st.rerun()

        st.markdown('<p style="color:#F1F5F9;font-size:1.15rem;font-weight:700;margin:1.2rem 0 0.5rem 0;">📍 ¿En qué distrito te encuentras?</p>', unsafe_allow_html=True)
        distrito_opts = ["Selecciona tu distrito"] + list(DISTRITOS.keys())
        sel = st.session_state.get("distrito", "Selecciona tu distrito")
        idx = distrito_opts.index(sel) if sel in distrito_opts else 0
        distrito = st.selectbox("Distrito", distrito_opts, index=idx, label_visibility="collapsed")
        if distrito != "Selecciona tu distrito":
            st.session_state.distrito = distrito

    with col_right:
        st.markdown('<p style="color:#F1F5F9;font-size:1.15rem;font-weight:700;margin-bottom:0.8rem;">📐 Medidas del ambiente</p>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            largo = st.number_input("Largo (m)", min_value=0.1, max_value=200.0,
                                     value=float(st.session_state.get("largo", 4.5)),
                                     step=0.1, format="%.1f")
        with c2:
            ancho = st.number_input("Ancho (hombre)", min_value=0.1, max_value=200.0,
                                     value=float(st.session_state.get("ancho", 3.2)),
                                     step=0.1, format="%.1f")
        area = largo * ancho
        st.markdown(f"""
        <div style="background:#1E293B;border:1.5px solid #334155;border-radius:12px;
                    padding:1rem 1.4rem;margin:0.4rem 0 1.2rem 0;
                    display:flex;justify-content:space-between;align-items:center;">
            <span style="color:#94A3B8;font-size:1rem;font-weight:500;">Área calculada</span>
            <span style="color:#60A5FA;font-weight:900;font-size:1.4rem;">{area:.2f} m²</span>
        </div>""", unsafe_allow_html=True)

        st.markdown('<p style="color:#F1F5F9;font-size:1.15rem;font-weight:700;margin-bottom:0.5rem;">💰 Presupuesto aproximado</p>', unsafe_allow_html=True)
        presupuesto = st.number_input("Presupuesto (S/)", min_value=0.0,
                                       value=float(st.session_state.get("presupuesto", 2000.0)),
                                       step=100.0, format="%.0f",
                                       help="No es necesario que sea exacto")
        st.session_state.largo = largo
        st.session_state.ancho = ancho
        st.session_state.area = area
        st.session_state.presupuesto = presupuesto

    st.markdown("<div style='height:2rem'></div>", unsafe_allow_html=True)
    col_b, _, col_n = st.columns([1, 2, 1])
    with col_b:
        if st.button("← Volver", use_container_width=True):
            st.session_state.step = 0; st.rerun()
    with col_n:
        can = st.session_state.get("ambiente") and st.session_state.get("distrito","") not in ["", "Selecciona tu distrito"]
        if can:
            if st.button("Continuar →", use_container_width=True):
                st.session_state.step = 2; st.rerun()
        else:
            st.markdown('<div style="text-align:center;color:#64748B;font-size:0.95rem;padding:0.7rem;">⚠️ Elige un ambiente y distrito para continuar</div>', unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════════════════════
# PASO 2 – PRODUCTOS  (imágenes embebidas en base64 + fix del HTML doble div)
# ═════════════════════════════════════════════════════════════════════════════
def pantalla_productos():
    nav_pills(2)
    ambiente = st.session_state.get("ambiente", "Piso interior")
    st.markdown(f"""
    <div class="step-header">
        <span class="step-badge">Paso 2 de 5</span>
        <h2 class="step-title">Productos recomendados</h2>
    </div>
    <p style="color:#94A3B8;font-size:1rem;margin-bottom:1.2rem;">
        Opciones para tu <strong style="color:#60A5FA;">{ambiente}</strong> ·
        <strong style="color:#F1F5F9;">{len(PRODUCTOS)}</strong> resultados disponibles
    </p>
    """, unsafe_allow_html=True)

    selected_id = st.session_state.get("producto_id")
    tiendas_filter = st.multiselect(
        "Filtrar por tienda",
        ["PROMART", "SODIMAC", "CASINELLI"],
        default=["PROMART", "SODIMAC", "CASINELLI"],
    )
    prods = [p for p in PRODUCTOS if p["tienda"] in tiendas_filter]

    # Grid 3 columnas
    for i in range(0, len(prods), 3):
        row = prods[i:i+3]
        cols = st.columns(3, gap="medium")
        for j, prod in enumerate(row):
            with cols[j]:
                is_sel = selected_id == prod["id"]
                border_col = "#10B981" if is_sel else "#334155"
                tienda_col = get_tienda_color(prod["tienda"])

                # Badge de tienda + badge seleccionado
                sel_html = '<span style="background:#10B981;color:white;font-size:0.75rem;padding:2px 10px;border-radius:20px;">✓ Seleccionado</span>' if is_sel else ""
                tags_html = " ".join(
                    f'<span class="tag" style="border-color:{prod["color_tags"][k]};color:{prod["color_tags"][k]};">{t}</span>'
                    for k, t in enumerate(prod["tags"])
                )
                img_html = safe_img_html(prod["imagen"], prod["nombre"], height=190, fit="contain")

                card_html = f"""
<div style="background:#1E293B;border:2px solid {border_col};border-radius:16px;padding:1rem;margin-bottom:0.3rem;transition:all 0.2s;">
<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.6rem;">
<span style="background:{tienda_col}22;color:{tienda_col};font-size:0.78rem;font-weight:700;padding:3px 10px;border-radius:20px;">{prod["tienda"]}</span>
{sel_html}
</div>
{img_html}
<div style="margin-top:0.8rem;">
<div style="font-size:0.95rem;font-weight:700;color:#F1F5F9;line-height:1.35;margin-bottom:0.3rem;">{prod["nombre"]}</div>
<div style="color:#94A3B8;font-size:0.85rem;margin-bottom:0.3rem;">Formato: {prod["formato"]} &nbsp;·&nbsp; Rend: {prod["rendimiento"]} m²/caja</div>
<div style="color:#60A5FA;font-size:1.2rem;font-weight:900;margin-bottom:0.5rem;">S/ {prod["precio_m2"]:.2f}<span style="font-size:0.8rem;color:#94A3B8;font-weight:400;"> / m²</span></div>
<div style="margin-bottom:0.5rem;">{tags_html}</div>
</div>
</div>"""
                st.markdown(card_html, unsafe_allow_html=True)

                btn_lbl = "✓ Seleccionado" if is_sel else "Seleccionar y calcular →"
                if st.button(btn_lbl, key=f"sel_{prod['id']}", use_container_width=True):
                    st.session_state.producto_id = prod["id"]
                    st.rerun()

    st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)
    col_b, _, col_n = st.columns([1, 2, 1])
    with col_b:
        if st.button("← Volver", key="back2", use_container_width=True):
            st.session_state.step = 1; st.rerun()
    with col_n:
        if st.session_state.get("producto_id"):
            if st.button("Ver calculadora →", key="next2", use_container_width=True):
                st.session_state.step = 3; st.rerun()
        else:
            st.markdown('<div style="text-align:center;color:#64748B;font-size:0.95rem;padding:0.7rem;">Selecciona un producto para continuar</div>', unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════════════════════
# PASO 3 – CALCULADORA
# ═════════════════════════════════════════════════════════════════════════════
def pantalla_calculadora():
    nav_pills(3)
    prod = next((p for p in PRODUCTOS if p["id"] == st.session_state.get("producto_id")), None)
    if not prod:
        st.warning("Vuelve y selecciona un producto."); return

    area = float(st.session_state.get("area", 0))
    calc = calcular_materiales(area, prod["precio_m2"], prod["rendimiento"])
    st.session_state.calc = calc

    st.markdown("""
    <div class="step-header">
        <span class="step-badge">Paso 3 de 5</span>
        <h2 class="step-title">Calculadora de materiales</h2>
    </div>""", unsafe_allow_html=True)

    tc = get_tienda_color(prod["tienda"])
    st.markdown(f"""
    <div style="background:#1E293B;border:1px solid #334155;border-radius:14px;
                padding:1.1rem 1.4rem;margin-bottom:1.5rem;display:flex;align-items:center;gap:1rem;">
        <span style="background:{tc}22;border:1.5px solid {tc};border-radius:10px;
                     padding:5px 14px;color:{tc};font-size:0.9rem;font-weight:800;">{prod["tienda"]}</span>
        <div>
            <div style="color:#F1F5F9;font-weight:700;font-size:1.05rem;">{prod["nombre"]}</div>
            <div style="color:#94A3B8;font-size:0.9rem;">S/ {prod["precio_m2"]:.2f} / m² · Rendimiento: {prod["rendimiento"]} m²/caja</div>
        </div>
    </div>""", unsafe_allow_html=True)

    col_main, col_side = st.columns([1.2, 0.8], gap="large")

    with col_main:
        st.markdown('<p style="color:#F1F5F9;font-size:1.15rem;font-weight:700;margin-bottom:0.8rem;">📐 Cálculo de cerámica</p>', unsafe_allow_html=True)
        st.markdown(f"""
        <div style="background:#1E293B;border:1px solid #334155;border-radius:12px;
                    padding:1rem 1.4rem;margin-bottom:0.6rem;
                    display:flex;justify-content:space-between;align-items:center;">
            <span style="color:#CBD5E1;font-size:1rem;">Área del ambiente</span>
            <span style="color:#F1F5F9;font-weight:700;font-size:1.1rem;">{area:.2f} m²</span>
        </div>""", unsafe_allow_html=True)

        st.markdown(f"""
        <div class="big-metric">
            <div class="lbl">📏 Área total a cubrir</div>
            <div class="val">{area:.2f} <span style="font-size:1.6rem;">m²</span></div>
        </div>""", unsafe_allow_html=True)

        tc1, tc2 = st.columns(2)
        with tc1:
            st.markdown(f'<div class="info-tile"><div class="tl">Formato del producto</div><div class="tv">{prod["formato"]}</div></div>', unsafe_allow_html=True)
        with tc2:
            st.markdown(f'<div class="info-tile"><div class="tl">Rendimiento por caja</div><div class="tv">{prod["rendimiento"]} m²</div></div>', unsafe_allow_html=True)

        st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class="big-metric big-metric-green">
            <div class="lbl">📦 Cajas necesarias</div>
            <div class="val">{calc["cajas"]} <span style="font-size:1.6rem;">cajas</span></div>
        </div>""", unsafe_allow_html=True)

        st.markdown('<p style="color:#F1F5F9;font-size:1.1rem;font-weight:700;margin:1.2rem 0 0.6rem 0;">🧱 Materiales complementarios</p>', unsafe_allow_html=True)
        mats = [
            ("Pegamento para porcelanato (bolsa 25 kg)", f"{calc['bolsas_pegamento']} bolsas",  f"S/ {calc['costo_pegamento']:,.2f}"),
            ("Fragua (bolsa)",                            f"{calc['bolsas_fragua']} bolsas",      f"S/ {calc['costo_fragua']:,.2f}"),
            ("Crucetas / separadores",                   f"{calc['paq_crucetas']} paquetes",     f"S/ {calc['costo_crucetas']:,.2f}"),
            ("Niveladores",                              f"{calc['paq_niveladores']} paquetes",  f"S/ {calc['costo_niveladores']:,.2f}"),
        ]
        mat_html = '<div style="background:#1E293B;border:1px solid #334155;border-radius:14px;padding:0.5rem 1.4rem;">'
        for n, c, p in mats:
            mat_html += f'<div class="mat-row"><div><div class="mat-name">{n}</div><div class="mat-sub">{c}</div></div><div class="mat-price">{p}</div></div>'
        mat_html += "</div>"
        st.markdown(mat_html, unsafe_allow_html=True)

    with col_side:
        st.markdown('<p style="color:#F1F5F9;font-size:1.1rem;font-weight:700;margin-bottom:0.8rem;">💰 Resumen de costos</p>', unsafe_allow_html=True)
        for lbl, val, col in [
            ("Cerámico / porcelanato",      f"S/ {calc['costo_ceramica']:,.2f}",    "#60A5FA"),
            ("Materiales complementarios",  f"S/ {calc['costo_complementos']:,.2f}", "#94A3B8"),
        ]:
            st.markdown(f"""
            <div style="display:flex;justify-content:space-between;align-items:center;
                        padding:0.9rem 1.1rem;background:#1E293B;border-radius:10px;margin-bottom:0.5rem;">
                <span style="color:#CBD5E1;font-size:0.95rem;font-weight:500;">{lbl}</span>
                <span style="color:{col};font-weight:800;font-size:1rem;">{val}</span>
            </div>""", unsafe_allow_html=True)

        st.markdown(f"""
        <div class="total-box">
            <div class="total-lbl">💳 Costo estimado total</div>
            <div class="total-val">S/ {calc["costo_total"]:,.2f}</div>
        </div>""", unsafe_allow_html=True)

        pres = float(st.session_state.get("presupuesto", 0))
        if pres > 0:
            dif = pres - calc["costo_total"]
            if dif >= 0:
                st.markdown(f"""
                <div style="background:#052e16;border:1.5px solid #10B981;border-radius:12px;padding:0.9rem 1.1rem;margin-top:0.8rem;">
                    <div style="color:#34D399;font-size:1rem;font-weight:700;">✅ Dentro de tu presupuesto</div>
                    <div style="color:#6EE7B7;font-size:0.9rem;margin-top:0.2rem;">Te sobran S/ {dif:,.2f}</div>
                </div>""", unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="background:#2D0000;border:1.5px solid #EF4444;border-radius:12px;padding:0.9rem 1.1rem;margin-top:0.8rem;">
                    <div style="color:#FCA5A5;font-size:1rem;font-weight:700;">⚠️ Supera tu presupuesto</div>
                    <div style="color:#F87171;font-size:0.9rem;margin-top:0.2rem;">Diferencia: S/ {abs(dif):,.2f}</div>
                </div>""", unsafe_allow_html=True)

        st.markdown("""
        <div class="warn-box" style="margin-top:1rem;">
            ⚠️ Cálculo referencial. Los precios y cantidades pueden variar según la tienda y el tipo de instalación.
        </div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:2rem'></div>", unsafe_allow_html=True)
    col_b, _, col_n = st.columns([1, 2, 1])
    with col_b:
        if st.button("← Volver", key="back3", use_container_width=True):
            st.session_state.step = 2; st.rerun()
    with col_n:
        if st.button("Ver dónde comprar →", key="next3", use_container_width=True):
            st.session_state.step = 4; st.rerun()


# ═════════════════════════════════════════════════════════════════════════════
# PASO 4 – TIENDAS  (interactivo + gráfica BAJO el mapa + sin Maestro)
# ═════════════════════════════════════════════════════════════════════════════
def pantalla_tiendas():
    nav_pills(4)
    prod = next((p for p in PRODUCTOS if p["id"] == st.session_state.get("producto_id")), PRODUCTOS[0])
    distrito = st.session_state.get("distrito", "Miraflores")

    st.markdown("""
    <div class="step-header">
        <span class="step-badge">Paso 4 de 5</span>
        <h2 class="step-title">Comparar tiendas</h2>
    </div>""", unsafe_allow_html=True)

    # Inicializar tienda seleccionada
    if "tienda_seleccionada" not in st.session_state:
        st.session_state.tienda_seleccionada = None

    col_lista, col_mapa = st.columns([1, 1], gap="large")

    with col_lista:
        # Filtros
        fil_cols = st.columns(3)
        filtros = ["Menor precio", "Más cercano", "Mayor stock"]
        for i, f in enumerate(filtros):
            with fil_cols[i]:
                activo = st.session_state.get("tienda_filtro") == f
                style = "background:linear-gradient(135deg,#3B82F6,#2563EB);color:white;" if activo else ""
                if st.button(f, key=f"ff_{i}", use_container_width=True):
                    st.session_state.tienda_filtro = f; st.rerun()

        st.markdown(f"""
        <div style="color:#94A3B8;font-size:0.95rem;margin:0.8rem 0;">
            🔍 Buscando: <strong style="color:#CBD5E1;">{prod["nombre"]}</strong>
        </div>""", unsafe_allow_html=True)

        # Lista de tiendas interactiva
        for t in PRECIOS_TIENDAS:
            tid = t["Tienda"]
            is_sel = st.session_state.tienda_seleccionada == tid
            border = "#10B981" if is_sel else "#334155"
            bg = "linear-gradient(135deg,#05291722,#1E293B)" if is_sel else "#1E293B"
            sel_mark = '<span class="badge-green" style="float:right;">✓ Seleccionada</span>' if is_sel else ""

            if t["Stock"] == "Disponible":
                badge = '<span class="badge-green">Disponible</span>'
            elif t["Stock"] == "Pocas unidades":
                badge = '<span class="badge-yellow">Pocas unidades</span>'
            else:
                badge = '<span class="badge-red">Sin stock</span>'

            tc = get_tienda_color(t["Tienda_marca"])

            store_html = f"""
<div style="background:{bg};border:2px solid {border};border-radius:14px;padding:1.1rem 1.4rem;margin-bottom:0.6rem;">
{sel_mark}
<div style="display:flex;justify-content:space-between;align-items:flex-start;gap:1rem;">
<div>
<span style="background:{tc}22;color:{tc};font-size:0.75rem;font-weight:700;padding:2px 8px;border-radius:20px;">{t["Tienda_marca"]}</span>
<div class="store-name" style="margin-top:0.3rem;">{tid}</div>
<div class="store-sub">{t["Distancia"]} · Retiro en tienda</div>
<div style="margin-top:0.4rem;">{badge}</div>
</div>
<div style="text-align:right;">
<div class="store-price">S/ {t["Precio_m2"]:.2f}/m²</div>
<div class="store-price-sub">S/ {t["Precio_caja"]:.2f}/caja</div>
</div>
</div>
</div>"""
            st.markdown(store_html, unsafe_allow_html=True)

            btn_lbl = "✓ Seleccionada" if is_sel else f"Seleccionar {tid.split(' - ')[0]} →"
            if st.button(btn_lbl, key=f"tsel_{tid}", use_container_width=True):
                st.session_state.tienda_seleccionada = tid; st.rerun()

    with col_mapa:
        lat, lon = DISTRITOS.get(distrito, (-12.0464, -77.0428))
        zoom = 13
        iframe_src = f"https://maps.google.com/maps?q=tiendas+ceramicos+porcelanatos+{distrito}+Lima&output=embed&z={zoom}&ll={lat},{lon}"
        maps_url   = f"https://www.google.com/maps/search/tiendas+ceramicos+porcelanatos/@{lat},{lon},{zoom}z"

        st.markdown(f"""
        <div style="margin-bottom:0.8rem;">
            <div style="color:#F1F5F9;font-weight:700;font-size:1.05rem;margin-bottom:0.2rem;">
                📍 Tiendas cercanas a: <span style="color:#60A5FA;">{distrito}</span>
            </div>
            <div style="color:#64748B;font-size:0.88rem;">Mostrando distribuidores de cerámicos y porcelanatos</div>
        </div>
        <div style="border-radius:16px;overflow:hidden;border:1px solid #334155;">
            <iframe src="{iframe_src}" width="100%" height="340"
                    style="border:0;display:block;" allowfullscreen="" loading="lazy"
                    referrerpolicy="no-referrer-when-downgrade"></iframe>
        </div>
        <a href="{maps_url}" target="_blank"
           style="display:block;text-align:center;color:#60A5FA;font-size:0.88rem;
                  margin-top:0.5rem;text-decoration:none;">
            🔗 Abrir en Google Maps →
        </a>""", unsafe_allow_html=True)

        # Tiendas cercanas
        tiendas_dist = TIENDAS_CERCANAS.get(distrito, [])
        if tiendas_dist:
            st.markdown('<p style="color:#F1F5F9;font-size:0.95rem;font-weight:700;margin:1rem 0 0.5rem 0;">Tiendas en tu área:</p>', unsafe_allow_html=True)
            for nombre, _, _, marca in tiendas_dist:
                tc2 = get_tienda_color(marca)
                nearby_html = f"""
<div style="background:#1E293B;border:1px solid #334155;border-radius:10px;padding:0.7rem 1rem;margin-bottom:0.4rem;display:flex;align-items:center;gap:0.8rem;">
<span style="background:{tc2}22;color:{tc2};font-size:0.75rem;font-weight:700;padding:2px 8px;border-radius:20px;">{marca}</span>
<span style="color:#CBD5E1;font-size:0.92rem;font-weight:500;">{nombre}</span>
<span class="badge-green" style="margin-left:auto;">Disponible</span>
</div>"""
                st.markdown(nearby_html, unsafe_allow_html=True)

        # ── GRÁFICA BAJO EL MAPA ──────────────────────────────────────────
        st.markdown('<p style="color:#F1F5F9;font-size:1.05rem;font-weight:700;margin:1.2rem 0 0.6rem 0;">📊 Comparativa de precios (S/m²)</p>', unsafe_allow_html=True)

        df_chart = pd.DataFrame({
            "Tienda": [t["Tienda"] for t in PRECIOS_TIENDAS],
            "Precio": [t["Precio_m2"] for t in PRECIOS_TIENDAS],
            "Marca":  [t["Tienda_marca"] for t in PRECIOS_TIENDAS],
        }).sort_values("Precio")

        color_scale = alt.Scale(
            domain=["PROMART", "SODIMAC", "CASINELLI"],
            range=["#F97316", "#3B82F6", "#10B981"]
        )
        chart = (
            alt.Chart(df_chart)
            .mark_bar(cornerRadiusTopLeft=8, cornerRadiusTopRight=8)
            .encode(
                x=alt.X("Tienda:N", sort=None,
                         axis=alt.Axis(labelColor="#CBD5E1", titleColor="#94A3B8",
                                       labelFontSize=13, labelAngle=-25, title=None)),
                y=alt.Y("Precio:Q",
                         axis=alt.Axis(labelColor="#CBD5E1", titleColor="#94A3B8",
                                       labelFontSize=13, gridColor="#1E293B", title="S/ por m²")),
                color=alt.Color("Marca:N", scale=color_scale,
                                legend=alt.Legend(title="Tienda", labelColor="#CBD5E1",
                                                  titleColor="#94A3B8", labelFontSize=12)),
                tooltip=[
                    alt.Tooltip("Tienda:N", title="Tienda"),
                    alt.Tooltip("Precio:Q", title="S/ por m²", format=".2f"),
                ],
            )
            .properties(height=230, background="#1E293B")
            .configure_view(strokeWidth=0)
            .configure_axis(domainColor="#334155", tickColor="#334155")
        )
        st.altair_chart(chart, use_container_width=True)

    st.markdown("<div style='height:2rem'></div>", unsafe_allow_html=True)
    col_b, _, col_n = st.columns([1, 2, 1])
    with col_b:
        if st.button("← Volver", key="back4", use_container_width=True):
            st.session_state.step = 3; st.rerun()
    with col_n:
        if st.button("Ver cotización final →", key="next4", use_container_width=True):
            st.session_state.step = 5; st.rerun()


# ═════════════════════════════════════════════════════════════════════════════
# PASO 5 – COTIZACIÓN FINAL
# ═════════════════════════════════════════════════════════════════════════════
def pantalla_cotizacion():
    nav_pills(5)
    prod     = next((p for p in PRODUCTOS if p["id"] == st.session_state.get("producto_id")), PRODUCTOS[0])
    area     = float(st.session_state.get("area", 0))
    calc     = st.session_state.get("calc") or calcular_materiales(area, prod["precio_m2"], prod["rendimiento"])
    ambiente = st.session_state.get("ambiente", "Sala")
    distrito = st.session_state.get("distrito", "Lima")

    # Tienda seleccionada en paso 4
    tienda_sel_nombre = st.session_state.get("tienda_seleccionada") or "Promart - Surco"
    tienda_sel_data   = next((t for t in PRECIOS_TIENDAS if t["Tienda"] == tienda_sel_nombre), PRECIOS_TIENDAS[0])

    st.markdown("""
    <div class="step-header">
        <span class="step-badge">Paso 5 de 5</span>
        <h2 class="step-title">Cotización final</h2>
    </div>""", unsafe_allow_html=True)

    col_main, col_act = st.columns([1.2, 0.8], gap="large")

    with col_main:
        tc = get_tienda_color(prod["tienda"])
        st.markdown(f"""
        <div style="background:#1E293B;border:1px solid #334155;border-radius:16px;
                    padding:1.4rem 1.6rem;margin-bottom:1.4rem;">
            <div style="color:#94A3B8;font-size:0.82rem;font-weight:700;letter-spacing:0.05em;margin-bottom:0.8rem;">
                RESUMEN DEL PROYECTO
            </div>
            <div style="display:flex;gap:2rem;flex-wrap:wrap;margin-bottom:0.8rem;">
                <div><div style="color:#64748B;font-size:0.8rem;">Ambiente</div>
                     <div style="color:#F1F5F9;font-weight:700;font-size:1rem;">{ambiente}</div></div>
                <div><div style="color:#64748B;font-size:0.8rem;">Área</div>
                     <div style="color:#60A5FA;font-weight:800;font-size:1rem;">{area:.2f} m²</div></div>
                <div><div style="color:#64748B;font-size:0.8rem;">Distrito</div>
                     <div style="color:#F1F5F9;font-weight:700;font-size:1rem;">{distrito}</div></div>
            </div>
            <div style="padding-top:0.8rem;border-top:1px solid #334155;">
                <div style="color:#64748B;font-size:0.8rem;">Producto elegido</div>
                <div style="color:#F1F5F9;font-size:1rem;font-weight:700;margin-top:0.2rem;">{prod["nombre"]}</div>
                <div style="color:{tc};font-size:0.88rem;margin-top:0.1rem;">{prod["tienda"]} · S/ {prod["precio_m2"]:.2f}/m²</div>
            </div>
        </div>""", unsafe_allow_html=True)

        st.markdown('<p style="color:#F1F5F9;font-size:1.1rem;font-weight:700;margin-bottom:0.6rem;">🛒 Lista de compra</p>', unsafe_allow_html=True)

        items = [
            (prod["nombre"],              f"{calc['cajas']} cajas",              calc["costo_ceramica"],    "#60A5FA"),
            ("Pegamento para porcelanato", f"{calc['bolsas_pegamento']} bolsas",  calc["costo_pegamento"],   "#CBD5E1"),
            ("Fragua",                     f"{calc['bolsas_fragua']} bolsas",     calc["costo_fragua"],      "#CBD5E1"),
            ("Crucetas / separadores",     f"{calc['paq_crucetas']} paquetes",    calc["costo_crucetas"],    "#CBD5E1"),
            ("Niveladores",                f"{calc['paq_niveladores']} paquetes", calc["costo_niveladores"], "#CBD5E1"),
        ]
        lista_html = f"""
        <div style="background:#1E293B;border:1px solid #334155;border-radius:14px;padding:0.5rem 1.4rem;">
            <div style="display:flex;justify-content:flex-end;padding:0.5rem 0;color:#64748B;font-size:0.85rem;">
                {len(items)} elementos
            </div>"""
        for nombre, cant, precio, col in items:
            lista_html += f"""
            <div class="cot-row">
                <div><div class="cot-name">{nombre}</div><div class="cot-sub">{cant}</div></div>
                <div style="color:{col};font-weight:800;font-size:1.05rem;">S/ {precio:,.2f}</div>
            </div>"""
        lista_html += f"""
            <div style="display:flex;justify-content:space-between;align-items:center;
                        padding:1.1rem 0 0.5rem 0;border-top:2px solid #334155;margin-top:0.5rem;">
                <div style="color:#F1F5F9;font-weight:800;font-size:1.1rem;">Total estimado</div>
                <div style="color:#60A5FA;font-size:1.6rem;font-weight:900;">S/ {calc["costo_total"]:,.2f}</div>
            </div>
        </div>"""
        st.markdown(lista_html, unsafe_allow_html=True)

    with col_act:
        tsel_color = get_tienda_color(tienda_sel_data["Tienda_marca"])
        st.markdown(f"""
        <div style="background:#1E293B;border:1.5px solid {tsel_color};border-radius:16px;
                    padding:1.4rem;margin-bottom:1rem;">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.8rem;">
                <div style="color:#94A3B8;font-size:0.82rem;font-weight:700;letter-spacing:0.05em;">TIENDA SELECCIONADA</div>
                <span class="badge-green">Material disponible</span>
            </div>
            <div style="color:#F1F5F9;font-weight:800;font-size:1.1rem;">{tienda_sel_data["Tienda"]}</div>
            <div style="color:#64748B;font-size:0.88rem;margin-top:0.3rem;">📍 Lima, Perú</div>
            <div style="color:#64748B;font-size:0.88rem;margin-top:0.1rem;">🕐 Lun-Dom 7:00 a.m. - 10:00 p.m.</div>
            <div style="color:{tsel_color};font-size:1.1rem;font-weight:800;margin-top:0.6rem;">
                S/ {tienda_sel_data["Precio_m2"]:.2f} / m²
            </div>
        </div>""", unsafe_allow_html=True)

        st.markdown("""
        <div class="warn-box">
            ⚠️ Los precios son referenciales y pueden variar. Verifica la información final directamente con la tienda antes de concretar la compra.
        </div>""", unsafe_allow_html=True)

        # WhatsApp
        wa_msg = (
            f"Hola! Quisiera cotizar materiales para mi proyecto de {ambiente} en {distrito}:%0A%0A"
            f"*Producto:* {prod['nombre']} ({prod['tienda']})%0A"
            f"*Cajas necesarias:* {calc['cajas']} cajas%0A"
            f"*Área total:* {area:.2f} m²%0A%0A"
            f"*Lista de materiales:*%0A"
            f"- Cerámico/porcelanato: {calc['cajas']} cajas — S/ {calc['costo_ceramica']:,.2f}%0A"
            f"- Pegamento: {calc['bolsas_pegamento']} bolsas — S/ {calc['costo_pegamento']:,.2f}%0A"
            f"- Fragua: {calc['bolsas_fragua']} bolsas — S/ {calc['costo_fragua']:,.2f}%0A"
            f"- Crucetas: {calc['paq_crucetas']} paquetes — S/ {calc['costo_crucetas']:,.2f}%0A"
            f"- Niveladores: {calc['paq_niveladores']} paquetes — S/ {calc['costo_niveladores']:,.2f}%0A%0A"
            f"*Total estimado: S/ {calc['costo_total']:,.2f}*%0A%0A"
            f"Tienda de referencia: {tienda_sel_data['Tienda']} (S/ {tienda_sel_data['Precio_m2']:.2f}/m²)%0A%0A"
            f"¿Pueden confirmar disponibilidad y precio final? Gracias!"
        )
        wa_url = f"https://wa.me/51971517830?text={wa_msg}"

        st.markdown(f'<a href="{wa_url}" target="_blank" class="wa-btn">📲 Solicitar cotización por WhatsApp</a>', unsafe_allow_html=True)
        st.markdown(f'<a href="{prod["url"]}" target="_blank" class="prod-link-btn">🔗 Ir a la página del producto</a>', unsafe_allow_html=True)

        st.markdown("<div style='height:0.8rem'></div>", unsafe_allow_html=True)
        col_s, col_n2 = st.columns(2)
        with col_s:
            if st.button("💾 Guardar cotización", use_container_width=True):
                st.success("¡Cotización registrada!")
        with col_n2:
            if st.button("🔄 Nueva búsqueda", use_container_width=True):
                for k in ["step","ambiente","distrito","largo","ancho","area",
                           "presupuesto","producto_id","calc","tienda_filtro","tienda_seleccionada"]:
                    st.session_state.pop(k, None)
                st.rerun()


# ═════════════════════════════════════════════════════════════════════════════
# MAIN
# ═════════════════════════════════════════════════════════════════════════════
def main():
    inject_css()
    if "step" not in st.session_state:
        st.session_state.step = 0
    step = st.session_state.step
    if   step == 0: pantalla_landing()
    elif step == 1: pantalla_proyecto()
    elif step == 2: pantalla_productos()
    elif step == 3: pantalla_calculadora()
    elif step == 4: pantalla_tiendas()
    elif step == 5: pantalla_cotizacion()

if __name__ == "__main__":
    main()
