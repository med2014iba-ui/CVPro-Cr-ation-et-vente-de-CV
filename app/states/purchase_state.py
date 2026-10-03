import reflex as rx
import asyncio
import logging
from decimal import Decimal
from typing import Any
from uuid import UUID

import reflex_enterprise as rxe
from reflex_enterprise.auth import User
from sqlalchemy import select

from app.models import CurriculumVitae, DemoPurchase, PremiumPrice
from app.components.pdf_document import render_cv_pdf


class PurchaseState(rx.State):
    checkout_open: bool = rxe.field(False, auth=True)
    checkout_title: str = rxe.field("", auth=True)
    price_display: str = rxe.field("", auth=True)
    message: str = rxe.field("", auth=True)
    error: str = rxe.field("", auth=True)
    exporting: bool = rxe.field(False, auth=True)
    _quote_cv: str = ""
    _quote_sub: str = ""
    _quote_amount: str = ""

    @rxe.event(auth=True)
    def close_checkout(self):
        self.checkout_open = False
        self._quote_cv = ""
        self._quote_sub = ""
        self._quote_amount = ""

    @rxe.event(auth=True)
    async def open_checkout(self, cv_id: str):
        self.error = ""
        self.message = ""
        self.checkout_open = False
        self._quote_cv = ""
        if not cv_id:
            self.error = "Enregistrez d’abord votre CV, puis ouvrez la confirmation de démonstration."
            return
        claims = await User.current() or {}
        sub = str(claims.get("sub", "")).strip()
        if not sub:
            return
        try:
            async with rx.asession() as session:
                cv = await session.scalar(
                    select(CurriculumVitae).where(
                        CurriculumVitae.id == UUID(cv_id),
                        CurriculumVitae.owner_sub == sub,
                        CurriculumVitae.title != "CV supprimé",
                    )
                )
                if cv is None:
                    self.error = (
                        "Ce CV sauvegardé est introuvable ou inaccessible."
                    )
                    return
                purchased = await session.scalar(
                    select(DemoPurchase.id)
                    .where(
                        DemoPurchase.cv_id == cv.id,
                        DemoPurchase.owner_sub == sub,
                        DemoPurchase.status == "confirmed",
                        DemoPurchase.is_demo.is_(True),
                    )
                    .limit(1)
                )
                if purchased:
                    self.message = "Achat fictif déjà confirmé pour ce CV. Vous pouvez télécharger son PDF sans nouvel achat."
                    return
                amount = await session.scalar(
                    select(PremiumPrice.amount_dzd).where(PremiumPrice.id == 1)
                )
                if amount is None:
                    self.error = "Le tarif est indisponible. Aucune confirmation n’a été enregistrée."
                    return
                self.checkout_title = cv.title
                self._quote_cv = str(cv.id)
            self._quote_sub = sub
            self._quote_amount = str(amount)
            self.price_display = f"{amount:,.2f} DZD".replace(",", " ").replace(
                ".", ","
            )
            self.checkout_open = True
        except Exception as e:
            logging.exception(f"Error: {e}")
            self.error = "Impossible d’ouvrir la confirmation de démonstration. Réessayez."

    @rxe.event(auth=True)
    async def confirm_demo(self, form_data: dict[str, Any]):
        self.error = ""
        claims = await User.current() or {}
        sub = str(claims.get("sub", "")).strip()
        if not sub or sub != self._quote_sub or not self._quote_cv:
            self.error = (
                "Cette confirmation a expiré. Ouvrez de nouveau le parcours."
            )
            return
        if form_data.get("consent") not in ("on", "yes", True):
            self.error = (
                "Votre consentement explicite à cet achat fictif est requis."
            )
            return
        try:
            async with rx.asession() as session:
                async with session.begin():
                    cv = await session.scalar(
                        select(CurriculumVitae)
                        .where(
                            CurriculumVitae.id == UUID(self._quote_cv),
                            CurriculumVitae.owner_sub == sub,
                            CurriculumVitae.title != "CV supprimé",
                        )
                        .with_for_update()
                    )
                    if cv is None:
                        self.error = "Ce CV n’est plus accessible. Aucun achat enregistré."
                        return
                    existing = await session.scalar(
                        select(DemoPurchase.id)
                        .where(
                            DemoPurchase.cv_id == cv.id,
                            DemoPurchase.owner_sub == sub,
                            DemoPurchase.status == "confirmed",
                            DemoPurchase.is_demo.is_(True),
                        )
                        .limit(1)
                    )
                    if existing is None:
                        price = await session.scalar(
                            select(PremiumPrice)
                            .where(PremiumPrice.id == 1)
                            .with_for_update()
                        )
                        if price is None or price.amount_dzd != Decimal(
                            self._quote_amount
                        ):
                            self.error = "Le tarif a changé ou est indisponible. Fermez cette fenêtre et vérifiez le nouveau prix avant de consentir."
                            return
                        session.add(
                            DemoPurchase(
                                cv_id=cv.id,
                                owner_sub=sub,
                                price_dzd=price.amount_dzd,
                                currency="DZD",
                                status="confirmed",
                                is_demo=True,
                            )
                        )
            self.checkout_open = False
            self._quote_cv = ""
            self._quote_sub = ""
            self._quote_amount = ""
            self.message = "Achat de DÉMONSTRATION confirmé. Aucun prélèvement. Le PDF de ce CV est désormais téléchargeable."
            from app.states.cv_library_state import CVLibraryState

            yield CVLibraryState.load_cvs
        except Exception as e:
            logging.exception(f"Error: {e}")
            self.error = "La confirmation a échoué. Aucun paiement réel n’est effectué ; vous pouvez réessayer sans double achat."

    @rxe.event(auth=True, background=True)
    async def download_pdf(self, cv_id: str):
        async with self:
            if self.exporting:
                return
            self.exporting = True
            self.error = ""
            self.message = ""
        try:
            claims = await User.current() or {}
            sub = str(claims.get("sub", "")).strip()
            if not sub or not cv_id:
                raise ValueError(
                    "Enregistrez votre CV et connectez-vous avant de télécharger."
                )
            async with rx.asession() as session:
                cv = await session.scalar(
                    select(CurriculumVitae).where(
                        CurriculumVitae.id == UUID(cv_id),
                        CurriculumVitae.owner_sub == sub,
                        CurriculumVitae.title != "CV supprimé",
                        select(DemoPurchase.id)
                        .where(
                            DemoPurchase.cv_id == CurriculumVitae.id,
                            DemoPurchase.owner_sub == sub,
                            DemoPurchase.status == "confirmed",
                            DemoPurchase.is_demo.is_(True),
                        )
                        .exists(),
                    )
                )
                if cv is None:
                    raise ValueError(
                        "Export refusé : CV inaccessible ou achat fictif confirmé absent pour ce compte."
                    )
                information = dict(cv.information)
                sections = [dict(item) for item in cv.sections]
                code = cv.template_code
                filename = f"CVPro-{cv.id.hex[:12]}.pdf"
            pdf = await asyncio.to_thread(
                render_cv_pdf, information, sections, code
            )
            async with self:
                self.message = "PDF A4 généré depuis la dernière version sauvegardée de votre CV."
            yield rx.download(data=pdf, filename=filename)
        except ValueError as e:
            logging.exception(f"Error: {e}")
            async with self:
                self.error = str(e)
        except Exception as e:
            logging.exception(f"Error: {e}")
            async with self:
                self.error = "La génération PDF a échoué. Votre achat fictif reste confirmé ; réessayez plus tard."
        finally:
            async with self:
                self.exporting = False
