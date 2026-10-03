import logging

import reflex as rx
import reflex_enterprise as rxe
from sqlalchemy import select

from app.models import PremiumPrice, CVTemplate


class PublicSiteState(rx.State):
    price_display: str = rxe.field("Tarif en cours de chargement", auth=False)
    templates: list[dict[str, str]] = rxe.field([], auth=False)

    @rxe.event(auth=False, background=True)
    async def load_public_price(self):
        try:
            async with rx.asession() as session:
                catalog = (
                    await session.scalars(
                        select(CVTemplate)
                        .where(CVTemplate.active.is_(True))
                        .order_by(CVTemplate.display_order)
                        .limit(5)
                    )
                ).all()
                amount = await session.scalar(
                    select(PremiumPrice.amount_dzd).where(PremiumPrice.id == 1)
                )
            templates = [
                {
                    "code": t.code,
                    "name": t.name,
                    "description": "Une composition soignée pour présenter votre parcours.",
                }
                for t in catalog
            ]
            price_display = (
                f"{amount:,.2f} DZD".replace(",", " ").replace(".", ",")
                if amount is not None
                else "Tarif indisponible"
            )
        except Exception as e:
            logging.exception(f"Error: {e}")
            price_display = "Tarif temporairement indisponible"
            templates = []
        async with self:
            self.price_display = price_display
            self.templates = templates
