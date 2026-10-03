import reflex as rx
from app.components.cv_account import account_header
from app.states.admin_state import AdminState


def admin_table(title: str, rows: rx.Var, columns: list[str]) -> rx.Component:
    return rx.el.section(
        rx.el.h2(title, class_name="mb-4 text-xl font-semibold text-[#17283F]"),
        rx.el.div(
            rx.el.div(
                rx.el.table(
                    rx.el.thead(
                        rx.el.tr(
                            rx.foreach(
                                columns,
                                lambda column: rx.el.th(
                                    rx.el.span(
                                        rx.icon("list", class_name="h-3 w-3"),
                                        column,
                                        class_name="flex items-center gap-2",
                                    ),
                                    class_name="bg-[#F2EEE7] px-4 py-3 text-left text-xs font-semibold text-[#17283F]",
                                ),
                            )
                        )
                    ),
                    rx.el.tbody(
                        rx.foreach(
                            rows,
                            lambda row: rx.el.tr(
                                rx.foreach(
                                    columns,
                                    lambda column: rx.el.td(
                                        row[column],
                                        class_name="max-w-xs break-words px-4 py-3 text-xs text-[#586374]",
                                    ),
                                ),
                                class_name="border-t border-[#E7E0D5] bg-white even:bg-[#FCFAF6] hover:bg-[#F2EEE7]",
                            ),
                        )
                    ),
                    class_name="table-auto w-full",
                ),
                class_name="overflow-x-auto",
            ),
            class_name="overflow-hidden rounded-xl border border-[#E7E0D5]",
        ),
        class_name="w-full",
    )


def template_form(item: dict[str, str]) -> rx.Component:
    return rx.el.form(
        rx.el.p(
            item["code"],
            class_name="text-xs font-semibold uppercase tracking-wider text-[#D77B67]",
        ),
        rx.el.input(type="hidden", name="code", value=item["code"]),
        rx.el.label(
            "Nom du modèle",
            rx.el.input(
                name="name",
                default_value=item["name"],
                key=item["name"],
                required=True,
                max_length=100,
                class_name="mt-2 w-full rounded-lg border border-[#DED8CE] bg-white px-3 py-2 text-sm text-[#17283F]",
            ),
            class_name="mt-3 block text-sm text-[#586374]",
        ),
        rx.el.label(
            rx.el.input(
                type="checkbox",
                name="active",
                default_checked=item["active"] == "yes",
                key=item["active"],
                class_name="h-4 w-4 accent-[#D77B67]",
            ),
            "Disponible pour les nouveaux CV",
            class_name="my-4 flex items-center gap-2 text-xs text-[#586374]",
        ),
        rx.el.button(
            "Enregistrer le modèle",
            type="submit",
            class_name="rounded-full bg-[#17283F] px-4 py-2 text-xs font-semibold text-white hover:bg-[#263D58]",
        ),
        on_submit=AdminState.save_template,
        class_name="rounded-xl border border-[#E7E0D5] bg-white p-5",
    )


def admin_content() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.foreach(
                ["users", "cvs", "sales"],
                lambda key: rx.el.article(
                    rx.el.p(
                        rx.match(
                            key,
                            ("users", "Utilisateurs inscrits"),
                            ("cvs", "CV non supprimés"),
                            "Achats démo confirmés",
                        ),
                        class_name="text-sm text-[#586374]",
                    ),
                    rx.el.p(
                        AdminState.counts[key],
                        class_name="mt-3 text-3xl font-semibold text-[#17283F]",
                    ),
                    class_name="w-full rounded-xl border border-[#E7E0D5] bg-white p-6",
                ),
            ),
            class_name="grid grid-cols-1 gap-4 sm:grid-cols-3",
        ),
        rx.el.p(
            "Aucune vente réelle : tous les achats sont fictifs. Les tableaux affichent 25 lignes par page, du plus récent au plus ancien.",
            class_name="text-sm text-[#586374]",
        ),
        rx.el.p(
            AdminState.error, role="alert", class_name="text-sm text-red-700"
        ),
        rx.el.p(
            AdminState.message,
            role="status",
            class_name="text-sm text-green-700",
        ),
        admin_table(
            "Utilisateurs", AdminState.users, ["name", "email", "role", "sub"]
        ),
        admin_table(
            "CV enregistrés",
            AdminState.cvs,
            ["title", "template", "owner", "id"],
        ),
        admin_table(
            "Achats fictifs et confirmations",
            AdminState.purchases,
            ["id", "cv", "owner", "price", "status", "demo"],
        ),
        rx.el.div(
            rx.el.button(
                "Page précédente",
                on_click=AdminState.change_page(-1),
                class_name="rounded-full border border-[#D8D0C4] bg-white px-4 py-2 text-sm text-[#17283F]",
            ),
            rx.el.button(
                "Page suivante",
                on_click=AdminState.change_page(1),
                class_name="rounded-full border border-[#D8D0C4] bg-white px-4 py-2 text-sm text-[#17283F]",
            ),
            rx.el.button(
                "Actualiser",
                on_click=AdminState.load_data,
                class_name="rounded-full bg-[#17283F] px-4 py-2 text-sm text-white",
            ),
            class_name="flex flex-wrap gap-3",
        ),
        rx.el.h2(
            "Catalogue des cinq modèles",
            class_name="text-xl font-semibold text-[#17283F]",
        ),
        rx.el.p(
            "Les codes sont immuables. Désactiver un modèle empêche sa sélection pour un nouveau CV, sans bloquer les CV existants ni leur export.",
            class_name="text-sm text-[#586374]",
        ),
        rx.el.div(
            rx.foreach(AdminState.templates, template_form),
            class_name="grid gap-4 sm:grid-cols-2 lg:grid-cols-3",
        ),
        rx.el.form(
            rx.el.h2(
                "Tarif premium de démonstration · DZD",
                class_name="text-xl font-semibold text-[#17283F]",
            ),
            rx.el.label(
                "Montant (deux décimales maximum)",
                rx.el.input(
                    name="amount",
                    default_value=AdminState.price,
                    key=AdminState.price,
                    required=True,
                    placeholder="0.00",
                    class_name="mt-2 block w-full rounded-lg border border-[#DED8CE] bg-white px-4 py-3 text-sm text-[#17283F]",
                ),
                class_name="mt-4 block text-sm text-[#586374]",
            ),
            rx.el.button(
                "Enregistrer le tarif DZD",
                type="submit",
                class_name="mt-4 rounded-full bg-[#17283F] px-5 py-3 text-sm font-semibold text-white",
            ),
            on_submit=AdminState.save_price,
            class_name="rounded-xl border border-[#E7E0D5] bg-white p-6",
        ),
        class_name="flex w-full flex-col gap-6",
    )


def admin_page() -> rx.Component:
    return rx.el.div(
        rx.el.div(on_mount=AdminState.enter_admin),
        account_header(),
        rx.el.main(
            rx.el.h1(
                "Administration CVPro",
                class_name="mb-7 text-3xl font-semibold text-[#17283F]",
            ),
            rx.cond(
                AdminState.ready,
                rx.cond(
                    AdminState.allowed,
                    admin_content(),
                    rx.el.p(
                        "Accès réservé aux administrateurs. Aucune donnée administrative n’est accessible depuis ce compte.",
                        class_name="rounded-xl border border-[#E7E0D5] bg-white p-6 text-sm text-[#586374]",
                    ),
                ),
                rx.el.p(
                    "Vérification de vos droits…",
                    class_name="animate-pulse text-sm text-[#586374]",
                ),
            ),
            class_name="mx-auto w-full max-w-7xl px-5 py-10 md:px-8",
        ),
        class_name="min-h-dvh bg-[#F8F5EF] font-['Inter'] text-[#17283F]",
    )
