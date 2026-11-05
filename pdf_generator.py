# -*- coding: utf-8 -*-
"""
PDF_GENERATOR.PY - Generador de Documentos PDF Oficiales en Python Puro
Produce archivos PDF 1.4 auténticos y válidos sin dependencias externas (ReportLab, etc.).
Genera apuntes y resúmenes educativos descargables al completar cada sección.
"""

import os
import re

class SimplePDFWriter:
    """Motor minimalista y robusto para escribir PDFs 1.4 estándar con texto, títulos, recuadros y formato."""
    def __init__(self, title="Apuntes Oficiales CodeLingo", author="CodeLingo AI Tutor"):
        self.title = title
        self.author = author
        self.pages = []
        self.current_page_commands = []
        self.page_width = 595.28   # A4 ancho en puntos
        self.page_height = 841.89  # A4 alto en puntos
        self.margin_x = 50.0
        self.margin_top = 50.0
        self.margin_bottom = 50.0
        self.cursor_y = self.page_height - self.margin_top

    def new_page(self):
        if self.current_page_commands:
            self.pages.append(self.current_page_commands)
            self.current_page_commands = []
        self.cursor_y = self.page_height - self.margin_top
        # Dibujar encabezado decorativo en cada página
        self._draw_page_header()

    def _draw_page_header(self):
        # Barra superior decorativa verde estilo Duolingo
        self.current_page_commands.append("0.345 0.800 0.008 rg") # #58CC02
        self.current_page_commands.append(f"50 {self.page_height - 35} 495 4 re f")
        # Texto del header
        self.current_page_commands.append("0.4 0.4 0.4 rg")
        self.current_page_commands.append("BT /F1 8 Tf")
        self.current_page_commands.append(f"50 {self.page_height - 46} Td (CODELINGO ACADEMY - GUIA OFICIAL DE ESTUDIO) Tj ET")

    def _check_page_break(self, required_space=30.0):
        if self.cursor_y - required_space < self.margin_bottom:
            self.new_page()

    def add_title(self, text):
        self._check_page_break(50.0)
        self.cursor_y -= 25.0
        clean_text = self._escape_text(text)
        # Sombra suave / banner
        self.current_page_commands.append("0.96 0.98 0.95 rg")
        self.current_page_commands.append(f"45 {self.cursor_y - 8} 505 32 re f")
        self.current_page_commands.append("0.22 0.52 0.01 rg")
        self.current_page_commands.append(f"45 {self.cursor_y - 8} 5 32 re f")
        self.current_page_commands.append("0.1 0.1 0.1 rg")
        self.current_page_commands.append("BT /F2 16 Tf")
        self.current_page_commands.append(f"60 {self.cursor_y} Td ({clean_text}) Tj ET")
        self.cursor_y -= 20.0

    def add_subtitle(self, text):
        self._check_page_break(35.0)
        self.cursor_y -= 18.0
        clean_text = self._escape_text(text)
        self.current_page_commands.append("0.1 0.4 0.8 rg") # Azul suave
        self.current_page_commands.append("BT /F2 12 Tf")
        self.current_page_commands.append(f"50 {self.cursor_y} Td ({clean_text}) Tj ET")
        self.cursor_y -= 14.0

    def add_paragraph(self, text, indent=50.0):
        lines = self._wrap_text(text, max_chars=82)
        for line in lines:
            self._check_page_break(18.0)
            self.cursor_y -= 14.0
            clean_line = self._escape_text(line)
            self.current_page_commands.append("0.15 0.15 0.15 rg")
            self.current_page_commands.append("BT /F1 10 Tf")
            self.current_page_commands.append(f"{indent} {self.cursor_y} Td ({clean_line}) Tj ET")
        self.cursor_y -= 6.0

    def add_bullet(self, title, desc=""):
        full_text = f"- {title}: {desc}" if desc else f"- {title}"
        self.add_paragraph(full_text, indent=60.0)

    def add_code_block(self, code_str):
        raw_lines = code_str.strip().split("\n")
        block_height = len(raw_lines) * 13.0 + 16.0
        self._check_page_break(min(block_height, 150.0))
        box_y = self.cursor_y - block_height + 4
        # Fondo oscuro para el bloque de código
        self.current_page_commands.append("0.08 0.11 0.16 rg") # Dark slate
        self.current_page_commands.append(f"50 {box_y} 495 {block_height} re f")
        self.current_page_commands.append("0.2 0.3 0.4 rg")
        self.current_page_commands.append(f"50 {box_y} 495 {block_height} re s")
        
        inner_y = self.cursor_y - 12.0
        for line in raw_lines:
            clean_line = self._escape_text(line[:85])
            self.current_page_commands.append("0.43 0.90 0.72 rg") # Verde menta código
            self.current_page_commands.append("BT /F3 9 Tf")
            self.current_page_commands.append(f"60 {inner_y} Td ({clean_line}) Tj ET")
            inner_y -= 13.0
        self.cursor_y = box_y - 12.0

    def _wrap_text(self, text, max_chars=80):
        words = text.split()
        if not words:
            return [""]
        lines = []
        current = words[0]
        for w in words[1:]:
            if len(current) + len(w) + 1 <= max_chars:
                current += " " + w
            else:
                lines.append(current)
                current = w
        lines.append(current)
        return lines

    def _escape_text(self, s):
        # Convertir caracteres acentuados o especiales a ASCII estándar para Type1 fonts
        replacements = {
            'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u',
            'Á': 'A', 'É': 'E', 'Í': 'I', 'Ó': 'O', 'Ú': 'U',
            'ñ': 'n', 'Ñ': 'N', '¿': '', '¡': '', '“': '"', '”': '"',
            '’': "'", '‘': "'", '—': '-', '–': '-', '•': '*'
        }
        for k, v in replacements.items():
            s = s.replace(k, v)
        # Escapar paréntesis y contrabarras de formato PDF
        s = s.replace('\\', '\\\\').replace('(', '\\(').replace(')', '\\)')
        # Filtrar caracteres no imprimibles
        return "".join([c if 32 <= ord(c) <= 126 else '?' for c in s])

    def generate(self, output_path):
        """Compila las páginas a un archivo PDF 1.4 estándar."""
        if self.current_page_commands or not self.pages:
            self.pages.append(self.current_page_commands)

        total_pages = len(self.pages)
        objects = []

        def add_obj(content):
            objects.append(content)
            return len(objects)

        # 1. Catálogo
        cat_id = add_obj("<< /Type /Catalog /Pages 2 0 R >>")
        # 2. Pages root (se actualiza luego)
        pages_root_idx = len(objects)
        objects.append(None)

        # 3. Fuentes
        f1_id = add_obj("<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")
        f2_id = add_obj("<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>")
        f3_id = add_obj("<< /Type /Font /Subtype /Type1 /BaseFont /Courier >>")

        page_ids = []
        for p_idx, page_cmds in enumerate(self.pages):
            # Agregar pie de página con número
            footer_text = self._escape_text(f"Pagina {p_idx + 1} de {total_pages} - Generado por CodeLingo AI")
            page_cmds.append("0.5 0.5 0.5 rg")
            page_cmds.append("BT /F1 8 Tf")
            page_cmds.append(f"230 30 Td ({footer_text}) Tj ET")

            stream_data = "\n".join(page_cmds)
            stream_len = len(stream_data.encode('latin1', errors='replace'))
            content_id = add_obj(f"<< /Length {stream_len} >>\nstream\n{stream_data}\nendstream")

            p_id = add_obj(
                f"<< /Type /Page /Parent 2 0 R\n"
                f"   /MediaBox [0 0 {self.page_width:.2f} {self.page_height:.2f}]\n"
                f"   /Resources << /Font << /F1 {f1_id} 0 R /F2 {f2_id} 0 R /F3 {f3_id} 0 R >> >>\n"
                f"   /Contents {content_id} 0 R >>"
            )
            page_ids.append(p_id)

        # Completar Pages Root
        kids_str = " ".join([f"{pid} 0 R" for pid in page_ids])
        objects[pages_root_idx] = f"<< /Type /Pages /Kids [{kids_str}] /Count {total_pages} >>"

        # Escribir estructura PDF
        xref_offsets = []
        pdf_bytes = bytearray()
        pdf_bytes.extend(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")

        for idx, obj in enumerate(objects):
            xref_offsets.append(len(pdf_bytes))
            pdf_bytes.extend(f"{idx + 1} 0 obj\n{obj}\nendobj\n".encode('latin1', errors='replace'))

        xref_pos = len(pdf_bytes)
        pdf_bytes.extend(f"xref\n0 {len(objects) + 1}\n0000000000 65535 f \n".encode('latin1'))
        for offset in xref_offsets:
            pdf_bytes.extend(f"{offset:010d} 00000 n \n".encode('latin1'))

        trailer = (
            f"trailer\n"
            f"<< /Size {len(objects) + 1}\n"
            f"   /Root 1 0 R\n"
            f"   /Info << /Title ({self._escape_text(self.title)}) /Author ({self._escape_text(self.author)}) >>\n"
            f">>\n"
            f"startxref\n"
            f"{xref_pos}\n"
            f"%%EOF\n"
        )
        pdf_bytes.extend(trailer.encode('latin1'))

        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        with open(output_path, "wb") as f:
            f.write(pdf_bytes)
        return output_path


def export_section_pdf(course_name, section_title, summary_dict, target_path):
    """
    Función de alto nivel para generar el PDF de apuntes oficiales desbloqueados al finalizar una sección.
    """
    writer = SimplePDFWriter(title=f"Apuntes: {course_name} - {section_title}")
    writer.new_page()

    writer.add_title(f"CODELINGO: {course_name.upper()}")
    writer.add_subtitle(f"Apuntes Oficiales - {section_title}")
    writer.add_paragraph(
        "Felicitaciones por completar con exito esta seccion. "
        "A continuacion tienes la sintesis teorica, reglas clave de sintaxis, buenas practicas y resumen del temario."
    )

    if "overview" in summary_dict:
        writer.add_subtitle("1. Resumen Conceptual")
        writer.add_paragraph(summary_dict["overview"])

    if "key_points" in summary_dict:
        writer.add_subtitle("2. Puntos Clave y Buenas Practicas")
        for pt in summary_dict["key_points"]:
            writer.add_bullet(pt)

    if "code_example" in summary_dict:
        writer.add_subtitle("3. Chuleta de Sintaxis y Ejemplo")
        writer.add_code_block(summary_dict["code_example"])

    if "tips" in summary_dict:
        writer.add_subtitle("4. Consejos del Asistente Byte")
        for tip in summary_dict["tips"]:
            writer.add_bullet("Tip", tip)

    return writer.generate(target_path)
