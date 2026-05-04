"""
Convierte un script SQL de PostgreSQL a MySQL.
Uso: python convert_pg_to_mysql.py input.sql output.sql
"""
import re
import sys

def convert(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Eliminar líneas exclusivas de PostgreSQL
    pg_lines = [
        r'SET statement_timeout.*;\n',
        r'SET lock_timeout.*;\n',
        r'SET idle_in_transaction_session_timeout.*;\n',
        r'SET transaction_timeout.*;\n',
        r'SET client_encoding.*;\n',
        r'SET standard_conforming_strings.*;\n',
        r'SELECT pg_catalog\.set_config.*;\n',
        r'SET check_function_bodies.*;\n',
        r'SET xmloption.*;\n',
        r'SET client_min_messages.*;\n',
        r'SET row_security.*;\n',
        r'SELECT pg_catalog\.setval.*;\n',
    ]
    for pattern in pg_lines:
        content = re.sub(pattern, '', content)

    # Eliminar prefijo public.
    content = content.replace('INSERT INTO public.', 'INSERT INTO ')

    # Reemplazar booleanos: true -> 1, false -> 0
    # Solo dentro de VALUES para no afectar comentarios
    def replace_booleans(match):
        s = match.group(0)
        s = re.sub(r'\btrue\b', '1', s)
        s = re.sub(r'\bfalse\b', '0', s)
        return s
    content = re.sub(r'VALUES\s*\(.*?\);', replace_booleans, content, flags=re.DOTALL)

    # Eliminar zona horaria de timestamps: +00, -05, etc.
    content = re.sub(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}(?:\.\d+)?)[+-]\d{2}", r"\1", content)

    # Agregar encabezado MySQL
    header = "SET FOREIGN_KEY_CHECKS=0;\nSET NAMES utf8mb4;\n\n"
    footer = "\nSET FOREIGN_KEY_CHECKS=1;\n"
    content = header + content + footer

    # Eliminar líneas vacías múltiples
    content = re.sub(r'\n{3,}', '\n\n', content)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Conversión completada: {output_path}")

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Uso: python convert_pg_to_mysql.py input.sql output.sql")
        sys.exit(1)
    convert(sys.argv[1], sys.argv[2])
