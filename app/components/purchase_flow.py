import reflex as rx
from app.states.purchase_state import PurchaseState


def purchase_actions(cv_id: rx.Var) -> rx.Component:
    return rx.el.div(
        rx.el.button(
            "Achat DÉMO",
            on_click=PurchaseState.open_checkout(cv_id),
            class_name="rounded-full border border-[#D77B67] bg-white px-4 py-2 text-xs font-semibold text-[#17283F] hover:bg-[#F7E8E3]",
        ),
        rx.el.button(
            rx.icon("download", class_name="h-4 w-4"),
            rx.cond(PurchaseState.exporting, "Génération…", "PDF A4"),
            on_click=PurchaseState.download_pdf(cv_id),
            disabled=PurchaseState.exporting,
            class_name="inline-flex items-center gap-2 rounded-full bg-[#17283F] px-4 py-2 text-xs font-semibold text-white hover:bg-[#263D58] disabled:opacity-50",
        ),
        class_name="flex flex-wrap items-center gap-2",
    )


def purchase_feedback() -> rx.Component:
    return rx.el.div(
        rx.el.p(
            PurchaseState.message,
            role="status",
            class_name="text-sm text-green-700",
        ),
        rx.el.p(
            PurchaseState.error, role="alert", class_name="text-sm text-red-700"
        ),
        rx.el.p(
            "Le PDF reprend uniquement la dernière version sauvegardée. Les modifications non enregistrées ne sont pas exportées.",
            class_name="text-xs leading-5 text-[#586374]",
        ),
        class_name="my-4 flex flex-col gap-2",
    )


def checkout_modal() -> rx.Component:
    return rx.cond(
        PurchaseState.checkout_open,
        rx.el.div(
            rx.el.section(
                rx.el.h2(
                    "Confirmation de paiement — DÉMONSTRATION",
                    id="checkout-title",
                    class_name="text-xl font-semibold text-[#17283F]",
                ),
                rx.el.p(
                    PurchaseState.checkout_title,
                    class_name="mt-3 text-sm text-[#586374]",
                ),
                rx.el.p(
                    PurchaseState.price_display,
                    class_name="mt-4 text-3xl font-semibold text-[#17283F]",
                ),
                rx.el.p(
                    "Cet achat est entièrement fictif. Aucun prélèvement, aucune carte collectée et aucun prestataire de paiement. Il débloque le PDF de ce CV uniquement.",
                    class_name="mt-4 text-sm leading-6 text-[#586374]",
                ),
                rx.el.form(
                    rx.el.label(
                        rx.el.input(
                            type="checkbox",
                            name="consent",
                            required=True,
                            class_name="mt-1 h-4 w-4 accent-[#D77B67]",
                        ),
                        rx.el.span(
                            "Je consens explicitement à enregistrer cet achat fictif au montant affiché, sans paiement réel.",
                            class_name="text-sm leading-6 text-[#17283F]",
                        ),
                        class_name="my-5 flex items-start gap-3",
                    ),
                    rx.el.p(
                        PurchaseState.error,
                        role="alert",
                        class_name="mb-3 text-sm text-red-700",
                    ),
                    rx.el.div(
                        rx.el.button(
                            "Confirmer l’achat fictif",
                            type="submit",
                            class_name="rounded-full bg-[#17283F] px-5 py-3 text-sm font-semibold text-white hover:bg-[#263D58]",
                        ),
                        rx.el.button(
                            "Annuler",
                            type="button",
                            on_click=PurchaseState.close_checkout,
                            class_name="rounded-full border border-[#D8D0C4] px-5 py-3 text-sm text-[#17283F] hover:bg-[#F2EEE7]",
                        ),
                        class_name="flex flex-wrap gap-3",
                    ),
                    on_submit=PurchaseState.confirm_demo,
                ),
                role="dialog",
                aria_modal=True,
                aria_labelledby="checkout-title",
                class_name="w-full max-w-lg rounded-2xl border border-[#E7E0D5] bg-[#F8F5EF] p-6 sm:p-8",
            ),
            class_name="fixed inset-0 z-50 flex items-center justify-center overflow-y-auto bg-[#17283F]/60 p-4 font-['Inter']",
        ),
    )
