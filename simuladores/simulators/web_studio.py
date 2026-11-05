"""
WEB_STUDIO.PY - Motor en Python para el Simulador de Web Studio
Compilación en vivo, ensamblaje de documentos HTML5/CSS3/JS y depuración.
"""

import re
import html

class WebStudioSimulator:
    def __init__(self):
        pass

    def build_preview_document(self, html_code: str, css_code: str, js_code: str) -> dict:
        """
        Ensambla un documento HTML completo inyectando CSS y JS con intercepción
        segura de la consola del navegador para depuración en vivo.
        """
        # Inyector de captura de logs de consola
        console_interceptor = """
        <script>
          (function() {
            var oldLog = console.log;
            var oldErr = console.error;
            var oldWarn = console.warn;
            function postMsg(type, args) {
              try {
                var txt = Array.from(args).map(function(a) {
                  return (typeof a === 'object') ? JSON.stringify(a) : String(a);
                }).join(' ');
                window.parent.postMessage({ type: 'CONSOLE_LOG', level: type, text: txt }, '*');
              } catch(e) {}
            }
            console.log = function() { postMsg('log', arguments); oldLog.apply(console, arguments); };
            console.error = function() { postMsg('error', arguments); oldErr.apply(console, arguments); };
            console.warn = function() { postMsg('warn', arguments); oldWarn.apply(console, arguments); };
            window.onerror = function(msg, url, line) {
              postMsg('error', ['Error línea ' + line + ': ' + msg]);
            };
          })();
        </script>
        """

        full_doc = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>
    /* Reset base */
    * {{ box-sizing: border-box; }}
    body {{ font-family: system-ui, -apple-system, sans-serif; margin: 0; padding: 16px; }}
    {css_code}
  </style>
  {console_interceptor}
</head>
<body>
  {html_code}
  <script>
    try {{
      {js_code}
    }} catch(err) {{
      console.error(err.message);
    }}
  </script>
</body>
</html>"""

        # Validación sintáctica básica en Python
        warnings = []
        if "<script" in html_code and "</script>" not in html_code:
            warnings.append("Advertencia: Etiqueta <script> no cerrada en el HTML.")
        if html_code.count("<div") != html_code.count("</div"):
            warnings.append("Advertencia: El número de etiquetas <div> y </div> no coincide.")

        return {
            'document': full_doc,
            'warnings': warnings,
            'size_bytes': len(full_doc.encode('utf-8'))
        }


if __name__ == '__main__':
    studio = WebStudioSimulator()
    res = studio.build_preview_document("<h1>Hola Mundo</h1>", "h1 { color: red; }", "console.log('Test');")
    print("Previsualización generada:", res['size_bytes'], "bytes")
