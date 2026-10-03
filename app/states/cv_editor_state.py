import logging
import uuid
from pathlib import Path

import reflex as rx
import reflex_enterprise as rxe
from reflex_enterprise.auth import User
from sqlalchemy import select

from app.models import CurriculumVitae, CVTemplate
from app.states.role_state import ensure_account


_SECTION_LABELS: dict[str, str] = {
    "experiences": "Expériences professionnelles",
    "formations": "Formations",
    "competences": "Compétences",
    "langues": "Langues",
    "certifications": "Certifications",
    "projets": "Projets",
    "interets": "Centres d’intérêt",
}


class CVEditorState(rx.State):
    active_step: int = rxe.field(0, auth=False)
    cv_id: str = rxe.field("", auth=False)
    cv_title: str = rxe.field("Mon CV", auth=False)
    template_code: str = rxe.field("moderne", auth=False)
    first_name: str = rxe.field("", auth=False)
    last_name: str = rxe.field("", auth=False)
    email: str = rxe.field("", auth=False)
    phone: str = rxe.field("", auth=False)
    city: str = rxe.field("", auth=False)
    website: str = rxe.field("", auth=False)
    job_title: str = rxe.field("", auth=False)
    summary: str = rxe.field("", auth=False)
    photo_filename: str = rxe.field("", auth=False)
    sections: list[dict[str, str]] = rxe.field([], auth=False)
    selected_kind: str = rxe.field("experiences", auth=False)
    item_title: str = rxe.field("", auth=False)
    item_organization: str = rxe.field("", auth=False)
    item_period: str = rxe.field("", auth=False)
    item_details: str = rxe.field("", auth=False)
    editing_item_id: str = rxe.field("", auth=False)
    error_message: str = rxe.field("", auth=False)
    notice_message: str = rxe.field("", auth=False)
    show_mobile_preview: bool = rxe.field(False, auth=False)

    @rxe.var(auth=False)
    def visible_sections(self) -> list[dict[str, str]]:
        return [
            item for item in self.sections if item["kind"] == self.selected_kind
        ]

    @rxe.var(auth=False)
    def selected_kind_label(self) -> str:
        return _SECTION_LABELS.get(self.selected_kind, "Rubrique")

    @rxe.event(auth=False)
    def set_active_step(self, step: int):
        self.active_step = max(0, min(step, 11))
        self.error_message = ""
        if 3 <= self.active_step <= 9:
            kinds = list(_SECTION_LABELS)
            self.selected_kind = kinds[self.active_step - 3]

    @rxe.event(auth=False)
    def set_text(self, field: str, value: str):
        allowed = {
            "cv_title": "cv_title",
            "first_name": "first_name",
            "last_name": "last_name",
            "email": "email",
            "phone": "phone",
            "city": "city",
            "website": "website",
            "job_title": "job_title",
            "summary": "summary",
            "item_title": "item_title",
            "item_organization": "item_organization",
            "item_period": "item_period",
            "item_details": "item_details",
        }
        target = allowed.get(field)
        if target:
            setattr(self, target, value[:4000])
            self.error_message = ""

    @rxe.event(auth=False)
    async def choose_template(self, code: str):
        if code in {
            "moderne",
            "classique",
            "elegant",
            "minimaliste",
            "creatif",
        }:
            try:
                async with rx.asession() as session:
                    active = await session.scalar(
                        select(CVTemplate.active).where(CVTemplate.code == code)
                    )
                if active:
                    self.template_code = code
                else:
                    self.error_message = "Ce modèle n’est pas disponible pour une nouvelle sélection."
            except Exception as e:
                logging.exception(f"Error: {e}")
                self.error_message = "Impossible de vérifier ce modèle."

    @rxe.event(auth=False)
    def toggle_mobile_preview(self):
        self.show_mobile_preview = not self.show_mobile_preview

    def _clear_item_form(self):
        self.item_title = ""
        self.item_organization = ""
        self.item_period = ""
        self.item_details = ""
        self.editing_item_id = ""
        self.error_message = ""

    @rxe.event(auth=False)
    def clear_item_form(self):
        self._clear_item_form()

    @rxe.event(auth=False)
    def save_section_item(self):
        title = self.item_title.strip()
        if not title:
            self.error_message = "Ajoutez un intitulé pour cet élément."
            return
        if len(title) > 180 or len(self.item_details) > 2000:
            self.error_message = "Vérifiez la longueur des champs (180 caractères pour le titre, 2 000 pour le détail)."
            return
        item_id = self.editing_item_id or str(uuid.uuid4())
        record = {
            "id": item_id,
            "kind": self.selected_kind,
            "label": _SECTION_LABELS[self.selected_kind],
            "title": title,
            "organization": self.item_organization.strip()[:180],
            "period": self.item_period.strip()[:100],
            "details": self.item_details.strip()[:2000],
        }
        if self.editing_item_id:
            self.sections = [
                record if row["id"] == item_id else row for row in self.sections
            ]
            self.notice_message = "Élément mis à jour."
        else:
            self.sections = [*self.sections, record]
            self.notice_message = "Élément ajouté."
        self._clear_item_form()

    @rxe.event(auth=False)
    def edit_section_item(self, item_id: str):
        for item in self.sections:
            if item["id"] == item_id:
                self.selected_kind = item["kind"]
                self.item_title = item["title"]
                self.item_organization = item["organization"]
                self.item_period = item["period"]
                self.item_details = item["details"]
                self.editing_item_id = item_id
                break

    @rxe.event(auth=False)
    def delete_section_item(self, item_id: str):
        self.sections = [
            item for item in self.sections if item["id"] != item_id
        ]
        self.notice_message = "Élément supprimé."
        if self.editing_item_id == item_id:
            self.clear_item_form()

    @rxe.event(auth=False)
    async def handle_photo_upload(self, files: list[rx.UploadFile]):
        if not files:
            return
        file = files[0]
        suffix = Path(file.name).suffix.lower()
        if suffix not in {".jpg", ".jpeg", ".png", ".webp"}:
            self.error_message = (
                "Format non accepté. Utilisez JPG, PNG ou WebP."
            )
            return
        try:
            data = await file.read()
            valid_signature = (
                data.startswith(b"\xff\xd8\xff")
                or data.startswith(b"\x89PNG\r\n\x1a\n")
                or (
                    len(data) >= 12
                    and data[:4] == b"RIFF"
                    and data[8:12] == b"WEBP"
                )
            )
            if not data or len(data) > 5 * 1024 * 1024 or not valid_signature:
                self.error_message = (
                    "La photo doit être une image valide de 5 Mo maximum."
                )
                return
            upload_dir = rx.get_upload_dir()
            upload_dir.mkdir(parents=True, exist_ok=True)
            filename = f"cv_photo_{uuid.uuid4().hex}{suffix}"
            (upload_dir / filename).write_bytes(data)
            self.photo_filename = filename
            self.error_message = ""
            self.notice_message = "Photo ajoutée."
        except Exception as e:
            logging.exception(f"Error: {e}")
            self.error_message = (
                "Impossible d’enregistrer cette photo pour le moment."
            )

    def _reset_draft(self):
        self.active_step = 0
        self.cv_id = ""
        self.cv_title = "Mon CV"
        self.template_code = "moderne"
        self.first_name = ""
        self.last_name = ""
        self.email = ""
        self.phone = ""
        self.city = ""
        self.website = ""
        self.job_title = ""
        self.summary = ""
        self.photo_filename = ""
        self.sections = []
        self.selected_kind = "experiences"
        self.clear_item_form()
        self.error_message = ""
        self.notice_message = ""

    @rxe.event(auth=False)
    async def load_editor(self):
        query = self.router.url.query_parameters
        cv_id = str(query.get("cv_id", "")).strip()
        if not cv_id:
            template = str(query.get("modele", "")).strip()
            if str(query.get("nouveau", "")) == "1" or template:
                self._reset_draft()
            if template in {
                "moderne",
                "classique",
                "elegant",
                "minimaliste",
                "creatif",
            }:
                await self.choose_template(template)
            return
        claims = await User.current() or {}
        sub = str(claims.get("sub", "")).strip()
        if not sub:
            return
        try:
            record_id = uuid.UUID(cv_id)
            async with rx.asession() as session:
                cv = await session.scalar(
                    select(CurriculumVitae).where(
                        CurriculumVitae.id == record_id,
                        CurriculumVitae.owner_sub == sub,
                        CurriculumVitae.title != "CV supprimé",
                    )
                )
            if cv is None:
                self.error_message = "Ce CV est introuvable ou n’est pas accessible depuis ce compte."
                return
            information = cv.information or {}
            self.cv_id = str(cv.id)
            self.cv_title = cv.title
            self.template_code = cv.template_code
            self.first_name = str(information.get("first_name", ""))
            self.last_name = str(information.get("last_name", ""))
            self.email = str(information.get("email", ""))
            self.phone = str(information.get("phone", ""))
            self.city = str(information.get("city", ""))
            self.website = str(information.get("website", ""))
            self.job_title = str(information.get("job_title", ""))
            self.summary = str(information.get("summary", ""))
            self.photo_filename = str(information.get("photo_filename", ""))
            self.sections = [
                {
                    key: str(item.get(key, ""))
                    for key in (
                        "id",
                        "kind",
                        "label",
                        "title",
                        "organization",
                        "period",
                        "details",
                    )
                }
                for item in cv.sections
                if isinstance(item, dict)
            ]
            self.notice_message = "Votre CV a été chargé."
        except Exception as e:
            logging.exception(f"Error: {e}")
            self.error_message = "Impossible de charger ce CV pour le moment."

    @rxe.event(auth=True)
    async def save_cv(self):
        claims = await User.current() or {}
        sub = str(claims.get("sub", "")).strip()
        if not sub:
            self.error_message = "Connectez-vous pour enregistrer votre CV."
            return
        if not self.first_name.strip() or not self.last_name.strip():
            self.error_message = (
                "Renseignez votre prénom et votre nom avant l’enregistrement."
            )
            self.active_step = 0
            return
        if not self.job_title.strip():
            self.error_message = (
                "Indiquez le poste recherché avant d’enregistrer."
            )
            self.active_step = 1
            return
        if self.email and "@" not in self.email:
            self.error_message = "Vérifiez le format de votre adresse e-mail."
            self.active_step = 0
            return
        information = {
            "first_name": self.first_name.strip()[:120],
            "last_name": self.last_name.strip()[:120],
            "email": self.email.strip()[:320],
            "phone": self.phone.strip()[:80],
            "city": self.city.strip()[:120],
            "website": self.website.strip()[:255],
            "job_title": self.job_title.strip()[:180],
            "summary": self.summary.strip()[:2000],
            "photo_filename": self.photo_filename[:255],
        }
        try:
            await ensure_account(
                sub,
                str(claims.get("email", "")),
                str(claims.get("name", "")),
            )
            async with rx.asession() as session:
                async with session.begin():
                    cv = None
                    if self.cv_id:
                        record_id = uuid.UUID(self.cv_id)
                        cv = await session.scalar(
                            select(CurriculumVitae)
                            .where(
                                CurriculumVitae.id == record_id,
                                CurriculumVitae.owner_sub == sub,
                                CurriculumVitae.title != "CV supprimé",
                            )
                            .with_for_update()
                        )
                        if cv is None:
                            self.error_message = "Ce CV n’est plus accessible. Rechargez la page et réessayez."
                            return
                    else:
                        cv = CurriculumVitae(owner_sub=sub)
                    active = await session.scalar(
                        select(CVTemplate.active).where(
                            CVTemplate.code == self.template_code
                        )
                    )
                    if not active and (
                        not self.cv_id or cv.template_code != self.template_code
                    ):
                        self.error_message = "Ce modèle est désactivé. Sélectionnez un modèle disponible."
                        return
                    if not self.cv_id:
                        session.add(cv)
                    cv.title = self.cv_title.strip()[:255] or "Mon CV"
                    cv.template_code = self.template_code
                    cv.information = information
                    cv.sections = [dict(item) for item in self.sections]
                    await session.flush()
                    saved_id = str(cv.id)
            self.cv_id = saved_id
            self.error_message = ""
            self.notice_message = "CV enregistré dans votre espace personnel."
        except Exception as e:
            logging.exception(f"Error: {e}")
            self.error_message = "L’enregistrement a échoué. Vos informations restent dans l’éditeur."
