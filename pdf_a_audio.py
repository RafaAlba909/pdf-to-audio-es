import sys
import re
import unicodedata
from pathlib import Path

from pypdf import PdfReader
from gtts import gTTS
from pydub import AudioSegment


# ---------- 1) EXTRAER TEXTO DEL PDF ----------

def extraer_texto_pdf(ruta_pdf: Path) -> str:
    reader = PdfReader(str(ruta_pdf))
    paginas = []
    for page in reader.pages:
        contenido = page.extract_text()
        if contenido:
            paginas.append(contenido)
    # Separar páginas con doble salto de línea
    return "\n\n".join(paginas)


# ---------- 2) LIMPIAR EMOJIS Y RAREZAS ----------

def es_caracter_permitido(ch: str) -> bool:
    """
    Dejamos letras, números, espacios y puntuación normal.
    Eliminamos símbolos raros (donde suelen ir emojis, iconos, etc.).
    """
    cat = unicodedata.category(ch)
    if cat.startswith(("L", "N")):  
        return True
    if cat in ("Zs",):             
        return True
    if cat.startswith("P"):       
        return True
    return False


def limpiar_texto(texto: str) -> str:
    lineas_limpias = []
    for linea in texto.splitlines():
        limpia = "".join(ch for ch in linea if es_caracter_permitido(ch))
        limpia = re.sub(r"\s+", " ", limpia).strip()
        lineas_limpias.append(limpia)
    return "\n".join(lineas_limpias)


# ---------- 3) AÑADIR PAUSAS EN TÍTULOS ----------

def marcar_titulos(texto: str) -> str:
    """
    Si una línea es relativamente corta y termina en ':',
    asumimos que es un título y añadimos un punto para forzar pausa.
    """
    nuevas_lineas = []
    for linea in texto.splitlines():
        l = linea.strip()
        if l and len(l) < 80 and l.endswith(":"):
            nuevas_lineas.append(l + ".")  
        else:
            nuevas_lineas.append(linea)
    return "\n".join(nuevas_lineas)


# ---------- 4) DIVIDIR TEXTO EN TROZOS PARA gTTS ----------

def trocear_texto(texto: str, max_caracteres: int = 4000):
    """
    Divide el texto en trozos, intentando cortar por frases.
    """
    texto = texto.strip()
    if len(texto) <= max_caracteres:
        return [texto]

    trozos = []
    actual = []

    frases = re.split(r"(?<=[\.\?\!])\s+", texto)

    longitud_actual = 0
    for frase in frases:
        if longitud_actual + len(frase) + 1 > max_caracteres:
            trozos.append(" ".join(actual).strip())
            actual = [frase]
            longitud_actual = len(frase) + 1
        else:
            actual.append(frase)
            longitud_actual += len(frase) + 1

    if actual:
        trozos.append(" ".join(actual).strip())

    return [t for t in trozos if t]


# ---------- 5) CONVERTIR TEXTO A MP3 (ESPAÑOL CASTELLANO) ----------

def texto_a_mp3(texto: str, ruta_salida: Path):
    ruta_salida = ruta_salida.with_suffix(".mp3")

    trozos = trocear_texto(texto)
    temporales = []

    for i, trozo in enumerate(trozos):
        tts = gTTS(text=trozo, lang="es", tld="es")  
        temp_name = ruta_salida.parent / f"_temp_parte_{i}.mp3"
        tts.save(str(temp_name))
        temporales.append(temp_name)

    if len(temporales) == 1:
        temporales[0].rename(ruta_salida)
        return ruta_salida

    audio_final = AudioSegment.empty()
    for temp in temporales:
        audio_final += AudioSegment.from_mp3(str(temp))

    audio_final.export(str(ruta_salida), format="mp3")
    for temp in temporales:
        try:
            temp.unlink()
        except OSError:
            pass

    return ruta_salida


# ---------- 6) MAIN ----------

def main():
    if len(sys.argv) < 2:
        print("Uso: python pdf_a_audio.py ruta_al_pdf [salida_mp3]")
        sys.exit(1)

    ruta_pdf = Path(sys.argv[1])
    if not ruta_pdf.exists():
        print(f"No encuentro el archivo: {ruta_pdf}")
        sys.exit(1)

    if len(sys.argv) >= 3:
        ruta_mp3 = Path(sys.argv[2])
    else:
        ruta_mp3 = ruta_pdf.with_suffix(".mp3")

    print("Extrayendo texto del PDF...")
    texto = extraer_texto_pdf(ruta_pdf)

    print("Limpiando texto (sin emojis ni símbolos raros)...")
    texto = limpiar_texto(texto)

    print("Marcando títulos con pausas...")
    texto = marcar_titulos(texto)

    print("Convirtiendo a audio (esto puede tardar un poco)...")
    salida = texto_a_mp3(texto, ruta_mp3)

    print(f"Listo. MP3 generado en: {salida}")


if __name__ == "__main__":
    main()
