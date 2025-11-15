import csv
import time
from urllib.parse import urljoin, urlparse, parse_qs

import requests
from bs4 import BeautifulSoup, Tag

BASE_URL = "https://apli.bizkaia.net/apps/danok/at/castellano/"
LIST_URL = urljoin(BASE_URL, "ca_lista.asp")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64) IreneScraper/1.0",
    "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
}


def get_list_page(session):
    """Descarga la página de lista de artesanos."""
    resp = session.get(LIST_URL, headers=HEADERS, timeout=20)
    resp.raise_for_status()
    resp.encoding = "iso-8859-1"
    return resp.text


def parse_list(html):
    """
    Parsea la lista principal y devuelve una lista de dicts con:
    - ID
    - nombre
    - actividad (descripción general)
    - subactividad (tipo de oficio)
    - detalle_url
    """
    soup = BeautifulSoup(html, "html.parser")

    form = soup.find("form", id="frmBuscar")
    td = form.find_next("td")  # el <td> donde está todo el listado

    current_activity = None
    current_subactivity = None
    entries = []

    for elem in td.descendants:
        # Bloques de actividad / subactividad
        if getattr(elem, "name", None) == "p":
            img = elem.find("img")
            if not img:
                continue
            alt = img.get("alt", "")
            text = elem.get_text(" ", strip=True)
            name = text
            if "Actividad" in alt:
                current_activity = name
            elif "Subactividad" in alt:
                current_subactivity = name

        # Enlaces a cada artesano
        elif getattr(elem, "name", None) == "a" and "azulitop" in (elem.get("class") or []):
            nombre = elem.get_text(strip=True)
            detalle_url = urljoin(BASE_URL, elem["href"])

            qs = parse_qs(urlparse(detalle_url).query)
            id_ = qs.get("Codigo", [""])[0]

            entries.append(
                {
                    "ID": id_,
                    "nombre": nombre,
                    "actividad": current_activity or "",
                    "subactividad": current_subactivity or "",
                    "detalle_url": detalle_url,
                }
            )

    return entries


def extract_field_from_info_p(info_p, label_substring):
    """
    En el <p class='texto_normal'> final de la ficha,
    extrae el texto que sigue a <b>Label...</b> hasta el siguiente <br>.
    """
    if not info_p:
        return ""

    b = info_p.find("b", string=lambda s: s and label_substring in s)
    if not b:
        return ""

    parts = []
    for sib in b.next_siblings:
        if isinstance(sib, Tag) and sib.name == "br":
            break
        parts.append(str(sib))

    return BeautifulSoup("".join(parts), "html.parser").get_text(" ", strip=True)


def get_detail_info(session, url):
    """
    Descarga la ficha de detalle y devuelve:
    - pueblo (Municipio)
    - telefono
    - email
    - descripcion (2º p.texto_normal)
    - imagenes (lista de urls absolutas)
    """
    try:
        resp = session.get(url, headers=HEADERS, timeout=20)
        resp.raise_for_status()
        resp.encoding = "iso-8859-1"
    except Exception as e:
        print(f"[WARN] No se pudo descargar {url}: {e}")
        return {
            "pueblo": "",
            "telefono": "",
            "email": "",
            "descripcion": "",
            "imagenes": [],
        }

    soup = BeautifulSoup(resp.text, "html.parser")

    # Todos los p.texto_normal
    p_blocks = soup.find_all("p", class_="texto_normal")

    # Descripción: el segundo p.texto_normal (en tu ejemplo: "Asociación de Artesanía")
    descripcion = ""
    if len(p_blocks) >= 2:
        descripcion = p_blocks[1].get_text(" ", strip=True)

    # Info de Dirección/Municipio/Teléfono/E-mail está en el p que contiene "Dirección"
    info_p = None
    for p in p_blocks:
        if p.find("b", string=lambda s: s and "Dirección" in s):
            info_p = p
            break

    pueblo = extract_field_from_info_p(info_p, "Municipio")
    telefono = extract_field_from_info_p(info_p, "Teléfono")

    # Email: primero probamos un mailto dentro de ese p
    email = ""
    if info_p:
        mail_link = info_p.find("a", href=lambda h: h and "mailto:" in h)
        if mail_link:
            href = mail_link["href"]
            email = href.split(":", 1)[-1].strip()

    # Si no, buscamos cualquier cosa con @
    if not email:
        text = soup.get_text(" ", strip=True)
        for token in text.split():
            if "@" in token and "." in token:
                email = token.strip(",.;")
                break

    # Enlaces a imágenes: a href="../imagenes/...."
    imagenes = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        # Filtramos a las imágenes de la sección, evitando logos (../irudiak)
        if "imagenes" in href.lower():
            # Solo formatos típicos de imagen
            if href.lower().endswith((".jpg", ".jpeg", ".png", ".gif", ".webp")):
                imagenes.append(urljoin(url, href))

    return {
        "pueblo": pueblo,
        "telefono": telefono,
        "email": email,
        "descripcion": descripcion,
        "imagenes": imagenes,
    }


def main():
    session = requests.Session()

    print("Descargando lista...")
    html = get_list_page(session)

    print("Parseando lista...")
    entries = parse_list(html)
    print(f"Encontradas {len(entries)} entidades")

    with open("artesanos_bizkaia.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "ID",
                "Pueblo exacto",
                "Latitud",
                "Longitud",
                "Tipo de oficio",
                "Descripción",
                "Email",
                "Teléfono",
                "Enlace",
                "Enlace imágenes",
            ]
        )

        for i, e in enumerate(entries, start=1):
            print(f"[{i}/{len(entries)}] {e['nombre']} -> {e['detalle_url']}")

            detail = get_detail_info(session, e["detalle_url"])
            time.sleep(0.5)  # pequeña pausa por cortesía

            # Script 1: latitud / longitud vacías (las rellenaremos en el script 2)
            lat = ""
            lon = ""

            # Descripción: priorizamos la de detalle;
            # si viniera vacía, usamos la Actividad de la lista.
            descripcion_final = detail["descripcion"] or e["actividad"]

            # Enlace imágenes: concatenamos todas las URLs encontradas
            imagenes_str = "; ".join(detail["imagenes"]) if detail["imagenes"] else ""

            writer.writerow(
                [
                    e["ID"],
                    detail["pueblo"],          # Pueblo exacto (Municipio)
                    lat,                       # Latitud (vacía por ahora)
                    lon,                       # Longitud (vacía por ahora)
                    e["subactividad"],         # Tipo de oficio
                    descripcion_final,         # Descripción
                    detail["email"],
                    detail["telefono"],
                    e["detalle_url"],
                    imagenes_str,
                ]
            )


if __name__ == "__main__":
    main()
