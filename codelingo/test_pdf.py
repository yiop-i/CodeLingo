import sys
import os
sys.path.append(os.path.dirname(__file__))
from pdf_generator import export_section_pdf

out = os.path.join(os.path.dirname(__file__), "test_output.pdf")
export_section_pdf("Python", "Fundamentos y Sintaxis", {
    "overview": "Variables, tipos de datos y operadores en Python 3.12.",
    "key_points": ["Uso de tipado dinamico", "f-strings para formateo"],
    "code_example": "x = 10\nprint(f'Valor: {x}')",
    "tips": ["Recuerda usar nombres en snake_case"]
}, out)
print("PDF CREATED:", os.path.exists(out), "SIZE:", os.path.getsize(out))
