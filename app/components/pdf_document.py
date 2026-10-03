import reflex as rx
import base64
import logging
import re
from html import escape

from app.models import JSONValue


_PDF_CSS = """
@page { size: A4; margin: 14mm; }
* { box-sizing: border-box; }
body { margin: 0; color: #17283F; font-family: Inter, sans-serif; font-size: 10pt; line-height: 1.55; }
header { padding: 9mm; } h1 { margin: 0; font-size: 24pt; line-height: 1.15; overflow-wrap: anywhere; }
.job { margin-top: 3mm; } .contact { font-size: 9pt; margin-top: 5mm; }
p { margin: 1mm 0; white-space: pre-wrap; overflow-wrap: anywhere; }
main { padding: 6mm 9mm; } section { margin-top: 6mm; }
h2 { font-size: 10pt; text-transform: uppercase; letter-spacing: 1pt; border-bottom: 1px solid #E7E0D5; padding-bottom: 2mm; margin: 0 0 3mm; break-after: avoid; }
h3 { margin: 0; font-size: 10pt; } .period { font-size: 8pt; color: #737B82; }
.organization, .details { font-size: 9pt; color: #586374; }
article { break-inside: avoid; } .photo { width: 24mm; height: 24mm; border-radius: 50%; object-fit: cover; margin-bottom: 4mm; }
.moderne header { float: left; width: 34%; background: #17283F; color: white; padding: 8mm 6mm; }
.moderne h1 { font-size: 20pt; } .moderne .job { color: #D8B1A5; }
.moderne main { margin-left: 34%; padding: 6mm; }
.classique { font-family: serif; } .classique header { text-align: center; border-bottom: 2px solid #17283F; }
.classique .job { font-style: italic; }
.elegant { background: #FFFEFC; } .elegant header { background: #FCF8F4; border-bottom: 1px solid #E8DED6; }
.elegant main:before { content: ''; display: block; height: 1mm; width: 20mm; background: #D77B67; }
.minimaliste h1 { font-weight: 300; text-transform: lowercase; letter-spacing: 1pt; }
.minimaliste main { border-top: 1px solid #E5E5E2; }
.creatif header { background: #F6E8E1; border-left: 3mm solid #D77B67; }
.creatif h1 { text-transform: uppercase; font-weight: 900; } .creatif .job { color: #B86251; }
.creatif main:before { content: ''; display: block; height: 1.5mm; width: 18mm; background: #17283F; }
"""


def _photo_data(filename: str) -> str:
    if not filename:
        return ""
    if not re.fullmatch(
        r"cv_photo_[0-9a-f]{32}\.(jpg|jpeg|png|webp)", filename
    ):
        raise ValueError(
            "Photo non valide dans le CV sauvegardé. Réimportez-la puis enregistrez."
        )
    path = rx.get_upload_dir() / filename
    try:
        if not path.exists():
            raise ValueError(
                "La photo sauvegardée n’est plus disponible. Réimportez-la puis enregistrez votre CV."
            )
        if path.stat().st_size > 5 * 1024 * 1024:
            raise ValueError("Photo trop volumineuse.")
        data = path.read_bytes()
        mime = ""
        if data.startswith(b"\xff\xd8\xff"):
            mime = "image/jpeg"
        elif data.startswith(b"\x89PNG\r\n\x1a\n"):
            mime = "image/png"
        elif data[:4] == b"RIFF" and data[8:12] == b"WEBP":
            mime = "image/webp"
        if not mime:
            raise ValueError("Photo invalide. Réimportez-la puis enregistrez.")
        return f"data:{mime};base64,{base64.b64encode(data).decode('ascii')}"
    except Exception as e:
        logging.exception(f"Error: {e}")
        raise


def build_cv_html(
    information: dict[str, JSONValue],
    sections: list[dict[str, JSONValue]],
    code: str,
) -> str:
    code = (
        code
        if code in {"moderne", "classique", "elegant", "minimaliste", "creatif"}
        else "moderne"
    )
    name = escape(
        f"{information.get('first_name', '')} {information.get('last_name', '')}"
    )
    job = escape(information.get("job_title", ""))
    photo_uri = _photo_data(information.get("photo_filename", ""))
    photo = (
        f'<img class="photo" src="{photo_uri}" alt="Photo">'
        if photo_uri
        else ""
    )
    contacts = "".join(
        f"<p>{escape(information.get(key, ''))}</p>"
        for key in ("email", "phone", "city", "website")
        if information.get(key)
    )
    summary = escape(information.get("summary", ""))
    profile = (
        f"<section><h2>Profil</h2><p>{summary}</p></section>" if summary else ""
    )
    entries = []
    for item in sections:
        label = escape(item.get("label", ""))
        title = escape(item.get("title", ""))
        period = escape(item.get("period", ""))
        organization = escape(item.get("organization", ""))
        details = escape(item.get("details", ""))
        entries.append(
            f'<section><h2>{label}</h2><article><h3>{title}</h3><p class="period">{period}</p><p class="organization">{organization}</p><p class="details">{details}</p></article></section>'
        )
    content = "".join(entries)
    return f'<!doctype html><html lang="fr"><head><meta charset="utf-8"><style>{_PDF_CSS}</style></head><body class="{code}"><header>{photo}<h1>{name}</h1><p class="job">{job}</p><div class="contact">{contacts}</div></header><main>{profile}{content}</main></body></html>'


def _restricted_fetcher(url: str, *args, **kwargs) -> dict[str, bytes | str]:
    match = re.fullmatch(
        r"data:(image/[A-Za-z0-9][A-Za-z0-9!#$&^_.+-]*);base64,"
        r"((?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?)",
        url,
    )
    if not match or not match.group(2):
        raise ValueError("Ressource interdite ou URI invalide dans le PDF.")
    mime, payload = match.groups()
    data = base64.b64decode(payload, validate=True)
    if base64.b64encode(data).decode("ascii") != payload:
        raise ValueError("Encodage base64 invalide dans le PDF.")
    return {"string": data, "mime_type": mime}


def render_cv_pdf(
    information: dict[str, JSONValue],
    sections: list[dict[str, JSONValue]],
    code: str,
) -> bytes:
    from weasyprint import HTML

    pdf = HTML(
        string=build_cv_html(information, sections, code),
        url_fetcher=_restricted_fetcher,
    ).write_pdf()
    if not pdf.startswith(b"%PDF-"):
        raise ValueError("Le document PDF n’a pas pu être généré.")
    return pdf
