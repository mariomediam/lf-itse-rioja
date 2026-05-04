"""
Corrige incompatibilidades PostgreSQL → MySQL en archivos Python con SQL raw.
Conversiones:
  - STRING_AGG(expr, 'sep' ORDER BY expr) → GROUP_CONCAT(expr ORDER BY expr SEPARATOR 'sep')
  - expr || 'x' || expr  → CONCAT(expr, 'x', expr)
  - %s::INTEGER / %s::int → CAST(%s AS UNSIGNED)
"""
import re
import sys
from pathlib import Path


def fix_string_agg(text):
    """
    STRING_AGG(
        expr,
        ', '
        ORDER BY expr2
    )
    →
    GROUP_CONCAT(expr ORDER BY expr2 SEPARATOR ', ')
    """
    def replacer(m):
        inner = m.group(1)
        # Separar expr, separador y ORDER BY
        order_match = re.search(r'ORDER BY\s+(.*)', inner, re.DOTALL | re.IGNORECASE)
        if not order_match:
            return m.group(0)
        order_expr = order_match.group(1).strip()
        before_order = inner[:order_match.start()].strip().rstrip(',').strip()
        # Extraer expresión y separador: último string entre comillas es el separador
        sep_match = re.search(r",\s*('[^']*')\s*$", before_order)
        if not sep_match:
            return m.group(0)
        separator = sep_match.group(1)
        expr = before_order[:sep_match.start()].strip()
        return f"GROUP_CONCAT({expr} ORDER BY {order_expr} SEPARATOR {separator})"

    pattern = re.compile(r'STRING_AGG\s*\((.*?)\)', re.DOTALL | re.IGNORECASE)
    return pattern.sub(replacer, text)


def fix_concat_pipes(text):
    """
    Convierte cadenas de || en CONCAT().
    Detecta líneas/expresiones con || y las envuelve en CONCAT().
    """
    # Reemplaza patrones de concatenación con ||
    # Patrón: uno o más "término || término"
    def replace_chain(m):
        full = m.group(0)
        # Dividir por ||
        parts = re.split(r'\s*\|\|\s*', full)
        parts = [p.strip() for p in parts if p.strip()]
        return 'CONCAT(' + ', '.join(parts) + ')'

    # Busca cadenas de concatenación con ||
    # Término: cualquier cosa que no sea || ni fin de línea lógica
    term = r"(?:COALESCE\([^)]+\)|TRIM\([^)]*\)|'[^']*'|[\w.]+)"
    chain = rf'{term}(?:\s*\|\|\s*{term})+'
    return re.sub(chain, replace_chain, text)


def fix_casts(text):
    """
    %s::INTEGER / %s::int → CAST(%s AS UNSIGNED)
    expr::INTEGER → CAST(expr AS UNSIGNED)
    """
    text = re.sub(r'(%s)::(?:INTEGER|INT|int|integer)', r'CAST(\1 AS UNSIGNED)', text)
    text = re.sub(r'(\w+)::(?:INTEGER|INT|int|integer)', r'CAST(\1 AS UNSIGNED)', text)
    return text


def fix_file(path):
    original = Path(path).read_text(encoding='utf-8')
    result = fix_string_agg(original)
    result = fix_concat_pipes(result)
    result = fix_casts(result)
    if result != original:
        Path(path).write_text(result, encoding='utf-8')
        print(f"[OK] {path}")
    else:
        print(f"[--] Sin cambios: {path}")


if __name__ == '__main__':
    files = sys.argv[1:] if len(sys.argv) > 1 else []
    if not files:
        base = Path(__file__).parent.parent / 'backend' / 'app_lf_itse' / 'services'
        files = list(base.glob('*.py'))
    for f in files:
        fix_file(str(f))
