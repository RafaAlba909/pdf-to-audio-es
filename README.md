# 📌 PDF-to-Audio ES — Convertidor de PDF a audiolibro en español

Este proyecto convierte documentos PDF (como resúmenes, apuntes o capítulos de libros) en un único archivo **MP3 narrado en español castellano**.

Está pensado para:

- Estudiar mientras caminas o entrenas  
- Escuchar resúmenes en el móvil  
- Repasar apuntes sin mirar pantalla  
- Transformar notas en audiolibros personales 🎧  

El programa limpia el texto, elimina emojis y símbolos innecesarios, y añade pequeñas pausas en títulos y secciones para que la narración suene más natural.

---

## 🚀 Funcionalidades

- 📄 Extrae texto de PDFs digitales (no escaneados)
- 🧹 Elimina emojis y símbolos decorativos automáticamente
- 🎙️ Convierte el texto a voz en español de España
- ⏸️ Añade pausas cortas en títulos y encabezados
- 🎧 Genera **un único archivo MP3**
- 🧩 Divide el texto en fragmentos largos sin perder fluidez

---

## 🛠️ Requisitos

Python 3.9+ recomendado.

Instalar dependencias:

```bash
pip install pypdf gTTS pydub
