import logging
from uuid import UUID

import reflex as rx
import reflex_enterprise as rxe
from reflex_enterprise.auth import User
from sqlalchemy import select

from app.models import CurriculumVitae, DemoPurchase
from typing import TypedDict


class CVListItem(TypedDict):
    id: str
    title: str
    template: str
    updated: str


class CVLibraryState(rx.State):
    cvs: list[CVListItem] = rxe.field([], auth=True)
    message: str = rxe.field("", auth=True)
    error_message: str = rxe.field("", auth=True)

    @rxe.event(auth=True, background=True)
    async def load_cvs(self):
        claims = await User.current() or {}
        sub = str(claims.get("sub", "")).strip()
        if not sub:
            return
        try:
            async with rx.asession() as session:
                rows = (
                    await session.scalars(
                        select(CurriculumVitae)
                        .where(
                            CurriculumVitae.owner_sub == sub,
                            CurriculumVitae.title != "CV supprimé",
                        )
                        .order_by(CurriculumVitae.updated_at.desc())
                        .limit(100)
                    )
                ).all()
            result: list[CVListItem] = [
                {
                    "id": str(cv.id),
                    "title": cv.title,
                    "template": cv.template_code,
                    "updated": cv.updated_at.strftime("%d/%m/%Y à %H:%M")
                    if cv.updated_at
                    else "Date indisponible",
                }
                for cv in rows
            ]
            async with self:
                self.cvs = result
                self.error_message = ""
        except Exception as e:
            logging.exception(f"Error: {e}")
            async with self:
                self.error_message = (
                    "Impossible de charger vos CV pour le moment."
                )

    @rxe.event(auth=True)
    async def duplicate_cv(self, cv_id: str):
        claims = await User.current() or {}
        sub = str(claims.get("sub", "")).strip()
        if not sub:
            return
        try:
            async with rx.asession() as session:
                async with session.begin():
                    original = await session.scalar(
                        select(CurriculumVitae).where(
                            CurriculumVitae.id == UUID(cv_id),
                            CurriculumVitae.owner_sub == sub,
                            CurriculumVitae.title != "CV supprimé",
                        )
                    )
                    if original is None:
                        self.error_message = "Ce CV est introuvable."
                        return
                    clone = CurriculumVitae(
                        owner_sub=sub,
                        title=f"{original.title[:245]} — copie",
                        template_code=original.template_code,
                        schema_version=original.schema_version,
                        information=dict(original.information),
                        sections=[dict(item) for item in original.sections],
                    )
                    session.add(clone)
            self.message = "Une copie de votre CV a été créée."
            return CVLibraryState.load_cvs
        except Exception as e:
            logging.exception(f"Error: {e}")
            self.error_message = "Impossible de dupliquer ce CV pour le moment."

    @rxe.event(auth=True)
    async def delete_cv(self, cv_id: str):
        claims = await User.current() or {}
        sub = str(claims.get("sub", "")).strip()
        if not sub:
            return
        try:
            async with rx.asession() as session:
                async with session.begin():
                    cv = await session.scalar(
                        select(CurriculumVitae).where(
                            CurriculumVitae.id == UUID(cv_id),
                            CurriculumVitae.owner_sub == sub,
                            CurriculumVitae.title != "CV supprimé",
                        )
                    )
                    if cv is None:
                        self.error_message = "Ce CV est introuvable."
                        return
                    purchases = await session.scalar(
                        select(DemoPurchase.id)
                        .where(
                            DemoPurchase.cv_id == cv.id,
                            DemoPurchase.owner_sub == sub,
                        )
                        .limit(1)
                    )
                    if purchases:
                        cv.title = "CV supprimé"
                        cv.information = {}
                        cv.sections = []
                    else:
                        await session.delete(cv)
            self.message = (
                "CV supprimé. Les données du document ont été effacées."
            )
            return CVLibraryState.load_cvs
        except Exception as e:
            logging.exception(f"Error: {e}")
            self.error_message = "Impossible de supprimer ce CV pour le moment."
