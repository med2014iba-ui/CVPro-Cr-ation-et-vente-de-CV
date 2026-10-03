import reflex as rx
from reflex_enterprise.auth import User

from app.components.purchase_flow import (
    purchase_actions,
    purchase_feedback,
    checkout_modal,
)
from app.states.cv_library_state import CVLibraryState
from app.states.role_state import RoleState


def cv_list_card(item: dict[str, str]) -> rx.Component:
    return rx.el.article(
        rx.el.div(
            rx.el.div(
                rx.icon("file-user", class_name="h-5 w-5 text-[#D77B67]"),
                rx.el.div(
                    rx.el.h2(
                        item["title"],
                        class_name="text-lg font-semibold text-[#17283F]",
                    ),
                    rx.el.p(
                        f"Modèle {item['template']} · Modifié le {item['updated']}",
                        class_name="mt-1 text-xs text-[#737B82]",
                    ),
                ),
                class_name="flex min-w-0 items-start gap-3",
            ),
            rx.el.div(
                rx.el.a(
                    "Ouvrir",
                    href=f"/creer?cv_id={item['id']}",
                    class_name="rounded-full bg-[#17283F] px-4 py-2 text-xs font-semibold text-white hover:bg-[#263D58]",
                ),
                purchase_actions(item["id"]),
                rx.el.button(
                    "Dupliquer",
                    on_click=CVLibraryState.duplicate_cv(item["id"]),
                    class_name="rounded-full border border-[#D8D0C4] px-4 py-2 text-xs font-semibold text-[#17283F] hover:bg-[#F2EEE7]",
                ),
                rx.el.button(
                    "Supprimer",
                    on_click=CVLibraryState.delete_cv(item["id"]),
                    class_name="rounded-full px-3 py-2 text-xs font-semibold text-[#B86251] hover:bg-[#F7E8E3]",
                ),
                class_name="flex flex-wrap items-center gap-2",
            ),
            class_name="flex flex-col justify-between gap-4 sm:flex-row sm:items-center",
        ),
        class_name="rounded-xl border border-[#E7E0D5] bg-white p-5 sm:p-6",
    )


def account_header() -> rx.Component:
    return rx.el.header(
        rx.el.div(
            rx.el.a(
                rx.icon("file-user", class_name="h-5 w-5 text-[#D77B67]"),
                rx.el.span(
                    "CVPro", class_name="text-lg font-semibold text-[#17283F]"
                ),
                href="/",
                class_name="flex items-center gap-2",
            ),
            rx.el.nav(
                rx.el.a(
                    "Créer un CV",
                    href="/creer?nouveau=1",
                    class_name="rounded-full px-4 py-2 text-sm font-semibold text-[#17283F] hover:bg-[#EEE8DD]",
                ),
                rx.cond(
                    RoleState.role == "admin",
                    rx.el.a(
                        "Administration",
                        href="/admin",
                        class_name="rounded-full px-4 py-2 text-sm font-semibold text-[#17283F] hover:bg-[#EEE8DD]",
                    ),
                ),
                rx.el.a(
                    "Mon profil",
                    href="/profil",
                    class_name="rounded-full px-4 py-2 text-sm font-semibold text-[#17283F] hover:bg-[#EEE8DD]",
                ),
                class_name="flex items-center gap-1",
            ),
            class_name="mx-auto flex w-full max-w-7xl items-center justify-between px-5 py-4 md:px-8",
        ),
        class_name="border-b border-[#E7E0D5] bg-[#F8F5EF]",
    )


def my_cvs_page() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            on_mount=[CVLibraryState.load_cvs, RoleState.refresh_current_role]
        ),
        account_header(),
        rx.el.main(
            rx.el.div(
                rx.el.p(
                    "VOTRE ESPACE",
                    class_name="text-xs font-semibold tracking-[0.2em] text-[#D77B67]",
                ),
                rx.el.h1(
                    "Mes CV",
                    class_name="mt-2 text-4xl font-semibold tracking-tight text-[#17283F]",
                ),
                rx.el.p(
                    "Retrouvez vos documents, reprenez leur rédaction ou créez une copie.",
                    class_name="mt-3 text-sm leading-6 text-[#586374]",
                ),
                rx.el.div(
                    rx.el.p(
                        CVLibraryState.message,
                        class_name="text-sm font-medium text-green-700",
                    ),
                    rx.el.p(
                        CVLibraryState.error_message,
                        class_name="text-sm font-medium text-red-700",
                    ),
                    class_name="mt-5 flex flex-col gap-2",
                ),
                purchase_feedback(),
                rx.cond(
                    CVLibraryState.cvs.length() > 0,
                    rx.el.div(
                        rx.foreach(CVLibraryState.cvs, cv_list_card),
                        class_name="mt-7 flex flex-col gap-3",
                    ),
                    rx.el.div(
                        rx.icon("files", class_name="h-8 w-8 text-[#D77B67]"),
                        rx.el.h2(
                            "Votre espace est prêt",
                            class_name="mt-3 text-lg font-semibold text-[#17283F]",
                        ),
                        rx.el.p(
                            "Les CV que vous enregistrez apparaîtront ici. La rédaction et l’aperçu sont gratuits.",
                            class_name="mt-2 max-w-lg text-sm leading-6 text-[#586374]",
                        ),
                        rx.el.a(
                            "Créer mon premier CV",
                            rx.icon("arrow-right", class_name="h-4 w-4"),
                            href="/creer?nouveau=1",
                            class_name="mt-5 inline-flex w-fit items-center gap-2 rounded-full bg-[#17283F] px-5 py-3 text-sm font-semibold text-white hover:bg-[#263D58]",
                        ),
                        class_name="mt-8 rounded-2xl border border-dashed border-[#D8D0C4] bg-white p-8 text-center sm:p-12",
                    ),
                ),
                class_name="mx-auto w-full max-w-5xl px-5 py-12 md:px-8 lg:py-16",
            ),
            class_name="min-w-0 flex-1",
        ),
        checkout_modal(),
        class_name="min-h-dvh bg-[#F8F5EF] font-['Inter'] text-[#17283F]",
    )


def profile_page() -> rx.Component:
    return rx.el.div(
        rx.el.div(on_mount=RoleState.refresh_current_role),
        account_header(),
        rx.el.main(
            rx.el.div(
                rx.el.p(
                    "VOTRE COMPTE",
                    class_name="text-xs font-semibold tracking-[0.2em] text-[#D77B67]",
                ),
                rx.el.h1(
                    "Mon profil",
                    class_name="mt-2 text-4xl font-semibold tracking-tight text-[#17283F]",
                ),
                rx.el.p(
                    "Votre identité de connexion et les options de votre espace CVPro.",
                    class_name="mt-3 text-sm leading-6 text-[#586374]",
                ),
                rx.el.section(
                    rx.cond(
                        User.picture,
                        rx.image(
                            src=User.picture,
                            class_name="h-16 w-16 rounded-full object-cover",
                        ),
                        rx.el.div(
                            rx.icon(
                                "user-round",
                                class_name="h-7 w-7 text-[#8B8B86]",
                            ),
                            class_name="flex h-16 w-16 items-center justify-center rounded-full bg-[#EEEAE3]",
                        ),
                    ),
                    rx.el.div(
                        rx.el.p(
                            User.name,
                            class_name="text-lg font-semibold text-[#17283F]",
                        ),
                        rx.el.p(
                            User.email, class_name="mt-1 text-sm text-[#586374]"
                        ),
                        rx.el.p(
                            rx.cond(
                                RoleState.role == "admin",
                                "Administrateur CVPro",
                                "Compte membre",
                            ),
                            class_name="mt-3 w-fit rounded-full bg-[#F2EEE7] px-3 py-1 text-xs font-semibold text-[#586374]",
                        ),
                    ),
                    class_name="mt-8 flex flex-col items-start gap-5 rounded-2xl border border-[#E7E0D5] bg-white p-6 sm:flex-row sm:items-center sm:p-8",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.icon(
                            "shield-check", class_name="h-5 w-5 text-[#D77B67]"
                        ),
                        rx.el.p(
                            "Connexion sécurisée par votre compte Reflex.",
                            class_name="text-sm text-[#586374]",
                        ),
                        class_name="flex items-center gap-3",
                    ),
                    rx.el.button(
                        rx.icon("log-out", class_name="h-4 w-4"),
                        "Se déconnecter",
                        on_click=User.logout,
                        class_name="mt-6 inline-flex items-center gap-2 rounded-full border border-[#D8D0C4] px-5 py-3 text-sm font-semibold text-[#17283F] transition hover:bg-[#F2EEE7]",
                    ),
                    class_name="mt-5 rounded-xl bg-[#FCFAF6] p-5",
                ),
                class_name="mx-auto w-full max-w-3xl px-5 py-12 md:px-8 lg:py-16",
            ),
            class_name="min-w-0 flex-1",
        ),
        class_name="min-h-dvh bg-[#F8F5EF] font-['Inter'] text-[#17283F]",
    )
