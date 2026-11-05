# -*- coding: utf-8 -*-
"""
Catálogo de Cursos, Plantillas de Código y Apuntes Oficiales para CodeLingo
Organizado en los 4 Grupos:
1. Lenguajes de Programación
2. Desarrollo Web
3. Terminal
4. Hardware de Computadora
"""

COURSE_CATALOG = {
    "languages": {
        "name": "Lenguajes",
        "icon": "🐍",
        "courses": [
            {"id": "Python", "name": "Python", "icon": "🐍"},
            {"id": "C++", "name": "C++", "icon": "⚡"},
            {"id": "C", "name": "C", "icon": "⚙️"},
            {"id": "Javascript", "name": "Javascript", "icon": "🟨"},
            {"id": "Java", "name": "Java", "icon": "☕"}
        ]
    },
    "web": {
        "name": "Desarrollo Web",
        "icon": "🌐",
        "courses": [
            {"id": "HTML", "name": "HTML", "icon": "📄"},
            {"id": "CSS", "name": "CSS", "icon": "🎨"},
            {"id": "Javascript Web", "name": "Javascript Web", "icon": "🌐"}
        ]
    },
    "terminals": {
        "name": "Terminal",
        "icon": "💻",
        "courses": [
            {"id": "Terminal de Windows", "name": "Terminal de Windows", "icon": "🪟"},
            {"id": "Terminal de Linux", "name": "Terminal de Linux", "icon": "🐧"}
        ]
    },
    "hardware": {
        "name": "Hardware de Computadora",
        "icon": "⚙️",
        "courses": [
            {"id": "Conceptos Generales", "name": "Conceptos Generales", "icon": "💡"},
            {"id": "PC de Escritorio", "name": "PC de Escritorio", "icon": "🖥️"},
            {"id": "Notebook", "name": "Notebook", "icon": "💻"}
        ]
    }
}

CODE_TEMPLATES = {
    "Python": """# Python 3.12 - Ejercicio guiado con Byte
radio = 5
PI = 3.1416

# Calcula el área e imprime el resultado
area = PI * (radio ** 2)
print("Radio del círculo:", radio)
print("Área calculada:", area)
""",
    "C++": """// C++ 14 - Salida con streams
#include <iostream>
using namespace std;

int main() {
    double radio = 5.0;
    const double PI = 3.1416;
    double area = PI * radio * radio;
    
    cout << "Radio: " << radio << endl;
    cout << "Área calculada: " << area << endl;
    return 0;
}
""",
    "C": """/* C (Clang) - Tipos primitivos */
#include <stdio.h>

int main() {
    float radio = 5.0f;
    float PI = 3.1416f;
    float area = PI * radio * radio;
    
    printf("Radio: %.2f\\n", radio);
    printf("Área calculada: %.2f\\n", area);
    return 0;
}
""",
    "Javascript": """// JavaScript ES6
const radio = 5;
const PI = 3.1416;

const area = PI * Math.pow(radio, 2);
console.log("Radio:", radio);
console.log("Área calculada:", area.toFixed(2));
""",
    "Java": """// Java 21 - Sintaxis pura
public class Main {
    public static void main(String[] args) {
        double radio = 5.0;
        double PI = 3.1416;
        double area = PI * Math.pow(radio, 2);
        
        System.out.println("Radio: " + radio);
        System.out.println("Área calculada: " + area);
    }
}
""",
    "HTML": """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>Mi Primera Web</title>
</head>
<body>
  <h1>¡Hola Mundo con HTML5! 🚀</h1>
  <p>Párrafo semántico de prueba en CodeLingo.</p>
  <button onclick="alert('¡HTML y JS vinculados!')">Presióname</button>
</body>
</html>
""",
    "CSS": """<!DOCTYPE html>
<html>
<head>
  <style>
    body { font-family: sans-serif; background: #e0f2fe; text-align: center; padding: 20px; }
    .caja { background: white; padding: 20px; border-radius: 16px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); display: inline-block; }
    button { background: #58cc02; color: white; border: none; padding: 10px 16px; border-radius: 8px; font-weight: bold; }
  </style>
</head>
<body>
  <div class="caja">
    <h2>Estilos con CSS3 🎨</h2>
    <p>Probando colores, bordes redondeados y sombras.</p>
    <button>Botón Estilizado</button>
  </div>
</body>
</html>
""",
    "Javascript Web": """<!DOCTYPE html>
<html>
<body>
  <h2 id="titulo">Texto Original</h2>
  <button onclick="cambiar()">Cambiar Contenido con JS</button>
  <script>
    function cambiar() {
      document.getElementById('titulo').innerText = '¡DOM Modificado con JavaScript!';
    }
  </script>
</body>
</html>
"""
}

NOTES_LIBRARY = [
    {
        "course": "Python", "group": "Lenguajes",
        "title": "Fundamentos de Python 3.12 y Tipos", "icon": "🐍",
        "pages": "4 Páginas", "status": "Desbloqueado ✅",
        "content": """CODELINGO - APUNTES OFICIALES DE PYTHON 3.12
======================================================
1. VARIABLES Y TIPOS PRIMITIVOS:
   - int: Enteros (ej: edad = 25)
   - float: Decimales (ej: pi = 3.1416)
   - str: Cadenas de texto ("Hola Mundo")
   - bool: True o False

2. OPERADORES ARITMÉTICOS:
   + (suma), - (resta), * (multiplicación), / (división flotante)
   // (división entera), % (módulo), ** (potencia)

3. ENTRADA Y SALIDA:
   print("Texto", variable)
   valor = input("Ingrese dato: ")

4. CONSEJO DE LA IA BYTE:
   "Usa nombres en minúsculas con guiones bajos (snake_case)
   para mantener tu código limpio y profesional."
"""
    },
    {
        "course": "C++", "group": "Lenguajes",
        "title": "Sintaxis de C++ y Streams de Salida", "icon": "⚡",
        "pages": "5 Páginas", "status": "Desbloqueado ✅",
        "content": """CODELINGO - APUNTES OFICIALES DE C++ 14
======================================================
1. TIPADO ESTRICTO:
   int, double, float, char, bool
2. CABECERAS ESENCIALES:
   #include <iostream>
   using namespace std;
3. ENTRADA Y SALIDA ESTÁNDAR:
   cout << "Salida" << endl;
   cin >> variable;
"""
    },
    {
        "course": "C", "group": "Lenguajes",
        "title": "Tipos Primitivos y Memoria en C", "icon": "⚙️",
        "pages": "3 Páginas", "status": "Desbloqueado ✅",
        "content": """CODELINGO - APUNTES OFICIALES DE C (CLANG)
======================================================
1. ESTRUCTURA BÁSICA:
   #include <stdio.h>
   int main() { return 0; }
2. FORMATOS EN PRINTF:
   %d (entero), %f (flotante), %s (cadena), %c (carácter)
3. MEMORIA: Punteros (*) y direcciones (&).
"""
    },
    {
        "course": "Javascript", "group": "Lenguajes",
        "title": "Variables, Funciones Flecha y ES6", "icon": "🟨",
        "pages": "6 Páginas", "status": "Desbloqueado ✅",
        "content": """CODELINGO - APUNTES OFICIALES DE JAVASCRIPT ES6
======================================================
1. DECLARACIONES: const (constantes) y let (variables reasignables)
2. ARROW FUNCTIONS: const suma = (a, b) => a + b;
3. MÉTODOS MATEMÁTICOS: Math.PI, Math.pow(), toFixed()
"""
    },
    {
        "course": "Java", "group": "Lenguajes",
        "title": "Programación Orientada a Objetos en Java 21", "icon": "☕",
        "pages": "5 Páginas", "status": "Desbloqueado ✅",
        "content": """CODELINGO - APUNTES OFICIALES DE JAVA 21
======================================================
1. ESTRUCTURA DE CLASES:
   public class Main {
       public static void main(String[] args) {
           System.out.println("Hola Java");
       }
   }
2. COMPILACIÓN: javac Main.java && java Main
"""
    },
    {
        "course": "HTML", "group": "Desarrollo Web",
        "title": "Estructura Semántica y Etiquetas HTML5", "icon": "📄",
        "pages": "4 Páginas", "status": "Desbloqueado ✅",
        "content": """CODELINGO - APUNTES OFICIALES DE HTML5
======================================================
1. ETIQUETAS ESTRUCTURALES: <header>, <nav>, <main>, <section>, <footer>
2. TEXTO: <h1> a <h6>, <p>, <span>, <a>
3. FORMULARIOS: <form>, <input>, <button>
"""
    },
    {
        "course": "CSS", "group": "Desarrollo Web",
        "title": "Box Model, Flexbox y Sombras en CSS3", "icon": "🎨",
        "pages": "5 Páginas", "status": "Desbloqueado ✅",
        "content": """CODELINGO - APUNTES OFICIALES DE CSS3
======================================================
1. MODELO DE CAJA: Content -> Padding -> Border -> Margin
2. FLEXBOX: display: flex; justify-content: center; align-items: center;
3. SOMBRAS: box-shadow: 0 4px 0 #46A302 (Estilo Duolingo)
"""
    },
    {
        "course": "Javascript Web", "group": "Desarrollo Web",
        "title": "Manipulación del DOM y Eventos Web", "icon": "🌐",
        "pages": "4 Páginas", "status": "Desbloqueado ✅",
        "content": """CODELINGO - APUNTES OFICIALES DE JAVASCRIPT WEB
======================================================
1. SELECCIÓN DOM: document.getElementById('id'), querySelector('.clase')
2. EVENTOS: elemento.addEventListener('click', callback)
3. PROPIEDADES: innerText, innerHTML, style.backgroundColor
"""
    },
    {
        "course": "Terminal de Windows", "group": "Terminal",
        "title": "Comandos PowerShell y Consola Windows", "icon": "🪟",
        "pages": "3 Páginas", "status": "Desbloqueado ✅",
        "content": """CODELINGO - APUNTES DE WINDOWS POWERSHELL / CMD
======================================================
1. LISTAR ARCHIVOS: dir / Get-ChildItem
2. CREAR CARPETA: mkdir nombre
3. NAVEGACIÓN: cd ruta, cd .. (retroceder)
4. LIMPIAR PANTALLA: cls
5. RED: ipconfig
"""
    },
    {
        "course": "Terminal de Linux", "group": "Terminal",
        "title": "Comandos Bash, Permisos y Rutas Ubuntu", "icon": "🐧",
        "pages": "4 Páginas", "status": "Desbloqueado ✅",
        "content": """CODELINGO - APUNTES DE LINUX UBUNTU (BASH)
======================================================
1. LISTAR ARCHIVOS: ls, ls -la (muestra ocultos y permisos)
2. DIRECTORIO ACTUAL: pwd
3. CREAR CARPETA: mkdir nombre
4. VER ARCHIVO: cat archivo.txt
5. PERMISOS: chmod +x script.sh
6. LIMPIAR: clear
"""
    },
    {
        "course": "Hardware de Computadora", "group": "Hardware",
        "title": "Arquitectura y Comparativa PC vs Notebook", "icon": "⚙️",
        "pages": "6 Páginas", "status": "Desbloqueado ✅",
        "content": """CODELINGO - APUNTES OFICIALES DE HARDWARE
======================================================
1. CPU: Cerebro informático. Socket en PC vs BGA soldado en laptops.
2. RAM: Memoria volátil de alta velocidad (DIMM en PC vs SO-DIMM en laptop).
3. GPU: Acelera gráficos 3D y machine learning (PCIe en PC vs iGPU/Móvil).
4. ALMACENAMIENTO: SSD NVMe M.2 (hasta 7000 MB/s) vs HDD (150 MB/s).
5. PSU: Fuente 80 Plus en PC vs Adaptador externo en laptops.
"""
    }
]
