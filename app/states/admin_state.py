import reflex as rx
import logging
from decimal import Decimal, InvalidOperation
from typing import Any

import reflex_enterprise as rxe
from reflex_enterprise.auth import User
from sqlalchemy import select, func

from app.models import (
    UserAccount,
    CurriculumVitae,
    DemoPurchase,
    CVTemplate,
    PremiumPrice,
)
from app.states.role_state import RoleState, is_admin


class AdminState(rx.State):
    allowed: bool = rxe.field(False, auth=True)
    ready: bool = rxe.field(False, auth=True)
    users: list[dict[str, str]] = rxe.field([], auth=is_admin)
    cvs: list[dict[str, str]] = rxe.field([], auth=is_admin)
    purchases: list[dict[str, str]] = rxe.field([], auth=is_admin)
    templates: list[dict[str, str]] = rxe.field([], auth=is_admin)
    counts: dict[str, int] = rxe.field(
        {"users": 0, "cvs": 0, "sales": 0}, auth=is_admin
    )
    price: str = rxe.field("", auth=is_admin)
    error: str = rxe.field("", auth=is_admin)
    message: str = rxe.field("", auth=is_admin)
    _offset: int = 0

    @rxe.event(auth=True)
    async def enter_admin(self):
        self.allowed = False
        self.ready = False
        self.users = []
        self.cvs = []
        self.purchases = []
        self.templates = []
        claims = await User.current() or {}
        sub = str(claims.get("sub", "")).strip()
        try:
            async with rx.asession() as session:
                role = await session.scalar(
                    select(UserAccount.role).where(UserAccount.sub == sub)
                )
            roles = await self.get_state(RoleState)
            roles.role = str(role or "member")
            self.allowed = role == "admin"
            self.ready = True
            self._offset = 0
            if self.allowed:
                yield AdminState.load_data
        except Exception as e:
            logging.exception(f"Error: {e}")
            self.ready = True

    @rxe.event(auth=is_admin)
    async def load_data(self):
        self.error = ""
        try:
            async with rx.asession() as session:
                metrics = (
                    await session.execute(
                        select(
                            select(func.count())
                            .select_from(UserAccount)
                            .scalar_subquery(),
                            select(func.count())
                            .select_from(CurriculumVitae)
                            .where(CurriculumVitae.title != "CV supprimé")
                            .scalar_subquery(),
                            select(func.count())
                            .select_from(DemoPurchase)
                            .where(
                                DemoPurchase.status == "confirmed",
                                DemoPurchase.is_demo.is_(True),
                            )
                            .scalar_subquery(),
                        )
                    )
                ).one()
                self.counts = {
                    "users": int(metrics[0]),
                    "cvs": int(metrics[1]),
                    "sales": int(metrics[2]),
                }
                users = (
                    await session.scalars(
                        select(UserAccount)
                        .order_by(
                            UserAccount.created_at.desc(), UserAccount.sub
                        )
                        .offset(self._offset)
                        .limit(25)
                    )
                ).all()
                cvs = (
                    await session.scalars(
                        select(CurriculumVitae)
                        .order_by(
                            CurriculumVitae.updated_at.desc(),
                            CurriculumVitae.id,
                        )
                        .offset(self._offset)
                        .limit(25)
                    )
                ).all()
                purchases = (
                    await session.scalars(
                        select(DemoPurchase)
                        .order_by(
                            DemoPurchase.created_at.desc(), DemoPurchase.id
                        )
                        .offset(self._offset)
                        .limit(25)
                    )
                ).all()
                templates = (
                    await session.scalars(
                        select(CVTemplate)
                        .order_by(CVTemplate.display_order)
                        .limit(5)
                    )
                ).all()
                amount = await session.scalar(
                    select(PremiumPrice.amount_dzd).where(PremiumPrice.id == 1)
                )
            self.users = [
                {"name": u.name, "email": u.email, "role": u.role, "sub": u.sub}
                for u in users
            ]
            self.cvs = [
                {
                    "title": c.title,
                    "owner": c.owner_sub,
                    "template": c.template_code,
                    "id": str(c.id),
                }
                for c in cvs
            ]
            self.purchases = [
                {
                    "id": str(p.id),
                    "cv": str(p.cv_id),
                    "owner": p.owner_sub,
                    "price": f"{p.price_dzd:.2f} DZD",
                    "status": p.status,
                    "demo": "Oui" if p.is_demo else "Non",
                }
                for p in purchases
            ]
            self.templates = [
                {
                    "code": t.code,
                    "name": t.name,
                    "active": "yes" if t.active else "no",
                }
                for t in templates
            ]
            self.price = f"{amount:.2f}" if amount is not None else ""
        except Exception as e:
            logging.exception(f"Error: {e}")
            self.error = (
                "Impossible de charger les données administratives. Réessayez."
            )

    @rxe.event(auth=is_admin)
    def change_page(self, direction: int):
        self._offset = max(0, self._offset + (25 if direction > 0 else -25))
        return AdminState.load_data

    @rxe.event(auth=is_admin)
    async def save_template(self, form_data: dict[str, Any]):
        code = str(form_data.get("code", ""))
        name = str(form_data.get("name", "")).strip()
        self.error = ""
        if (
            code not in {item[0] for item in CVTemplate.CATALOG}
            or not name
            or len(name) > 100
        ):
            self.error = "Modèle invalide ou nom vide/trop long (100 caractères maximum)."
            return
        try:
            async with rx.asession() as session:
                async with session.begin():
                    template = await session.get(CVTemplate, code)
                    if template is None:
                        self.error = "Modèle introuvable."
                        return
                    template.name = name
                    template.active = form_data.get("active") in (
                        "on",
                        "yes",
                        True,
                    )
            self.message = "Nom et activation enregistrés. Le code du modèle reste inchangé."
            yield AdminState.load_data
        except Exception as e:
            logging.exception(f"Error: {e}")
            self.error = "Impossible de mettre à jour ce modèle."

    @rxe.event(auth=is_admin)
    async def save_price(self, form_data: dict[str, Any]):
        self.error = ""
        try:
            amount = Decimal(
                str(form_data.get("amount", "")).strip().replace(",", ".")
            )
            if (
                not amount.is_finite()
                or amount < 0
                or amount > Decimal("9999999999.99")
                or amount != amount.quantize(Decimal("0.01"))
            ):
                raise ValueError("Montant invalide")
        except (InvalidOperation, ValueError) as e:
            logging.exception(f"Error: {e}")
            self.error = "Saisissez un montant DZD positif ou nul, avec au maximum deux décimales."
            return
        try:
            async with rx.asession() as session:
                async with session.begin():
                    price = await session.get(PremiumPrice, 1)
                    if price is None:
                        session.add(
                            PremiumPrice(
                                id=1, amount_dzd=amount, currency="DZD"
                            )
                        )
                    else:
                        price.amount_dzd = amount
            self.message = "Tarif DZD enregistré. Les achats déjà confirmés conservent leur prix historique."
            yield AdminState.load_data
        except Exception as e:
            logging.exception(f"Error: {e}")
            self.error = "Impossible de mettre à jour le tarif."
