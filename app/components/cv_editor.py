import reflex as rx
from app.components.purchase_flow import (
    purchase_actions,
    purchase_feedback,
    checkout_modal,
)
from app.states.public_site_state import PublicSiteState

from app.components.cv_preview import cv_preview_a4
from app.states.cv_editor_state import CVEditorState
from app.states.role_state import RoleState


_STEPS = [
    "Informations personnelles",
    "Poste recherché",
    "Résumé professionnel",
    "Expériences",
    "Formations",
    "Compétences",
    "Langues",
    "Certifications",
    "Projets",
    "Centres d’intérêt",
    "Modèle",
    "Vérification",
]


def editor_input(
    label: str, field: str, value: rx.Var, placeholder: str = ""
) -> rx.Component:
    return rx.el.label(
        rx.el.span(
            label, class_name="mb-2 block text-sm font-semibold text-[#17283F]"
        ),
        rx.el.input(
            placeholder=placeholder,
            on_change=lambda text: CVEditorState.set_text(field, text).debounce(
                500
            ),
            class_name="w-full rounded-lg border border-[#DED8CE] bg-white px-4 py-3 text-sm text-[#17283F] outline-none transition focus:border-[#D77B67] focus:ring-2 focus:ring-[#D77B67]/20",
            default_value=value,
        ),
        class_name="block",
    )


def step_navigation_item(label: str, index: int) -> rx.Component:
    return rx.el.button(
        rx.el.span(
            index + 1, class_name="text-[10px] font-semibold tracking-wider"
        ),
        rx.el.span(label, class_name="hidden text-left text-xs md:inline"),
        on_click=CVEditorState.set_active_step(index),
        class_name=rx.cond(
            CVEditorState.active_step == index,
            "flex w-full items-center gap-3 rounded-lg bg-[#17283F] px-3 py-2.5 text-white transition-colors",
            "flex w-full items-center gap-3 rounded-lg px-3 py-2.5 text-[#586374] transition-colors hover:bg-[#EEE8DD] hover:text-[#17283F]",
        ),
    )


def step_sidebar() -> rx.Component:
    return rx.el.nav(
        rx.foreach(
            _STEPS, lambda label, index: step_navigation_item(label, index)
        ),
        class_name="flex gap-1 overflow-x-auto border-b border-[#E7E0D5] bg-white p-3 md:w-56 md:shrink-0 md:flex-col md:overflow-visible md:border-b-0 md:border-r md:p-4",
    )


def personal_step() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h2(
                "Vos coordonnées",
                class_name="text-xl font-semibold text-[#17283F]",
            ),
            rx.el.p(
                "Ajoutez les informations utiles pour être contacté. La photo reste facultative.",
                class_name="mt-2 text-sm leading-6 text-[#586374]",
            ),
        ),
        editor_input(
            "Titre de ce CV",
            "cv_title",
            CVEditorState.cv_title,
            "Ex. Candidature chef de projet",
        ),
        rx.el.div(
            editor_input(
                "Prénom *",
                "first_name",
                CVEditorState.first_name,
                "Votre prénom",
            ),
            editor_input(
                "Nom *", "last_name", CVEditorState.last_name, "Votre nom"
            ),
            class_name="grid gap-4 sm:grid-cols-2",
        ),
        rx.el.div(
            editor_input(
                "Adresse e-mail",
                "email",
                CVEditorState.email,
                "nom@exemple.com",
            ),
            editor_input("Téléphone", "phone", CVEditorState.phone, "+213 …"),
            class_name="grid gap-4 sm:grid-cols-2",
        ),
        rx.el.div(
            editor_input("Ville", "city", CVEditorState.city, "Alger"),
            editor_input(
                "Site ou profil professionnel",
                "website",
                CVEditorState.website,
                "https://…",
            ),
            class_name="grid gap-4 sm:grid-cols-2",
        ),
        rx.el.div(
            rx.el.div(
                rx.icon("image-plus", class_name="h-5 w-5 text-[#D77B67]"),
                rx.el.div(
                    rx.el.p(
                        "Photo de profil",
                        class_name="text-sm font-semibold text-[#17283F]",
                    ),
                    rx.el.p(
                        "JPG, PNG ou WebP · 5 Mo maximum",
                        class_name="mt-1 text-xs text-[#7B8187]",
                    ),
                ),
                class_name="flex items-start gap-3",
            ),
            rx.upload.root(
                rx.el.div(
                    "Déposer une photo ou cliquer pour choisir",
                    class_name="rounded-lg border border-dashed border-[#D8D0C4] px-4 py-5 text-center text-xs font-medium text-[#586374] transition hover:border-[#D77B67] hover:bg-[#FCFAF6]",
                ),
                id="photo_upload",
                accept={
                    "image/jpeg": [".jpg", ".jpeg"],
                    "image/png": [".png"],
                    "image/webp": [".webp"],
                },
                max_files=1,
                class_name="mt-4 block cursor-pointer",
            ),
            rx.el.button(
                "Importer la photo sélectionnée",
                on_click=CVEditorState.handle_photo_upload(
                    rx.upload_files(upload_id="photo_upload")
                ),
                class_name="mt-3 rounded-full border border-[#D8D0C4] px-4 py-2 text-xs font-semibold text-[#17283F] transition hover:bg-[#F2EEE7]",
            ),
            rx.cond(
                CVEditorState.photo_filename,
                rx.el.p(
                    "Photo prête pour l’aperçu.",
                    class_name="mt-2 text-xs text-green-600",
                ),
            ),
            class_name="rounded-xl border border-[#E7E0D5] bg-[#FCFAF6] p-4",
        ),
        class_name="flex flex-col gap-5",
    )


def role_step() -> rx.Component:
    return rx.el.div(
        rx.el.h2(
            "Le poste visé", class_name="text-xl font-semibold text-[#17283F]"
        ),
        rx.el.p(
            "Un intitulé précis aide les recruteurs à comprendre rapidement votre objectif.",
            class_name="mt-2 text-sm leading-6 text-[#586374]",
        ),
        editor_input(
            "Intitulé professionnel *",
            "job_title",
            CVEditorState.job_title,
            "Ex. Responsable marketing digital",
        ),
        class_name="flex flex-col gap-5",
    )


def summary_step() -> rx.Component:
    return rx.el.div(
        rx.el.h2(
            "Votre résumé", class_name="text-xl font-semibold text-[#17283F]"
        ),
        rx.el.p(
            "Présentez en quelques phrases votre expertise, vos points forts et votre objectif. 2 000 caractères maximum.",
            class_name="mt-2 text-sm leading-6 text-[#586374]",
        ),
        editor_input(
            "Résumé professionnel",
            "summary",
            CVEditorState.summary,
            "Professionnel·le avec une expérience en…",
        ),
        rx.el.p(
            "Conseil : privilégiez des faits et des compétences que vous pouvez illustrer.",
            class_name="text-xs text-[#7B8187]",
        ),
        class_name="flex flex-col gap-5",
    )


def section_item_card(item: dict[str, str]) -> rx.Component:
    return rx.el.article(
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    item["title"],
                    class_name="text-sm font-semibold text-[#17283F]",
                ),
                rx.el.p(
                    f"{item['organization']} · {item['period']}",
                    class_name="mt-1 text-xs text-[#737B82]",
                ),
                class_name="min-w-0",
            ),
            rx.el.div(
                rx.el.button(
                    "Modifier",
                    on_click=CVEditorState.edit_section_item(item["id"]),
                    class_name="rounded-full px-3 py-1.5 text-xs font-semibold text-[#17283F] hover:bg-[#EEE8DD]",
                ),
                rx.el.button(
                    "Supprimer",
                    on_click=CVEditorState.delete_section_item(item["id"]),
                    class_name="rounded-full px-3 py-1.5 text-xs font-semibold text-[#B86251] hover:bg-[#F7E8E3]",
                ),
                class_name="flex shrink-0 items-center gap-1",
            ),
            class_name="flex flex-wrap items-start justify-between gap-3",
        ),
        rx.cond(
            item["details"],
            rx.el.p(
                item["details"],
                class_name="mt-3 text-xs leading-5 text-[#586374]",
            ),
        ),
        class_name="rounded-lg border border-[#E7E0D5] bg-white p-4",
    )


def collection_step() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h2(
                CVEditorState.selected_kind_label,
                class_name="text-xl font-semibold text-[#17283F]",
            ),
            rx.el.p(
                "Ajoutez les éléments les plus pertinents. Vous pourrez les modifier ou les supprimer à tout moment.",
                class_name="mt-2 text-sm leading-6 text-[#586374]",
            ),
        ),
        rx.foreach(CVEditorState.visible_sections, section_item_card),
        rx.el.div(
            rx.el.h3(
                rx.cond(
                    CVEditorState.editing_item_id,
                    "Modifier l’élément",
                    "Ajouter un élément",
                ),
                class_name="text-sm font-semibold text-[#17283F]",
            ),
            editor_input(
                "Intitulé *",
                "item_title",
                CVEditorState.item_title,
                "Ex. Développeur logiciel",
            ),
            rx.el.div(
                editor_input(
                    "Organisation / établissement",
                    "item_organization",
                    CVEditorState.item_organization,
                    "Entreprise, école…",
                ),
                editor_input(
                    "Période",
                    "item_period",
                    CVEditorState.item_period,
                    "2022 – 2024",
                ),
                class_name="grid gap-4 sm:grid-cols-2",
            ),
            editor_input(
                "Description",
                "item_details",
                CVEditorState.item_details,
                "Responsabilités, résultats ou détails utiles",
            ),
            rx.el.div(
                rx.el.button(
                    rx.cond(
                        CVEditorState.editing_item_id,
                        "Enregistrer les modifications",
                        "Ajouter à mon CV",
                    ),
                    on_click=CVEditorState.save_section_item,
                    class_name="rounded-full bg-[#17283F] px-5 py-3 text-sm font-semibold text-white transition hover:bg-[#263D58]",
                ),
                rx.cond(
                    CVEditorState.editing_item_id,
                    rx.el.button(
                        "Annuler",
                        on_click=CVEditorState.clear_item_form,
                        class_name="rounded-full px-4 py-3 text-sm font-semibold text-[#586374] hover:bg-[#EEE8DD]",
                    ),
                ),
                class_name="flex flex-wrap items-center gap-2",
            ),
            class_name="flex flex-col gap-4 rounded-xl border border-[#E7E0D5] bg-[#FCFAF6] p-5",
        ),
        class_name="flex flex-col gap-4",
    )


def template_card(item: dict[str, str]) -> rx.Component:
    return rx.el.button(
        rx.el.div(
            rx.el.div(
                class_name=rx.match(
                    item["code"],
                    ("moderne", "h-14 rounded-t-md bg-[#17283F]"),
                    (
                        "classique",
                        "h-14 rounded-t-md border-b-2 border-[#17283F] bg-white",
                    ),
                    ("elegant", "h-14 rounded-t-md bg-[#FCF8F4]"),
                    ("minimaliste", "h-14 rounded-t-md bg-white"),
                    "h-14 rounded-t-md border-l-4 border-[#D77B67] bg-[#F6E8E1]",
                )
            ),
            rx.el.div(
                rx.el.p(
                    item["name"],
                    class_name="text-sm font-semibold text-[#17283F]",
                ),
                rx.el.p(
                    item["description"],
                    class_name="mt-1 text-xs leading-5 text-[#586374]",
                ),
                class_name="p-3 text-left",
            ),
            class_name=rx.cond(
                CVEditorState.template_code == item["code"],
                "overflow-hidden rounded-xl border-2 border-[#D77B67] bg-white text-left",
                "overflow-hidden rounded-xl border border-[#E7E0D5] bg-white text-left transition hover:border-[#B8AFA2]",
            ),
        ),
        on_click=CVEditorState.choose_template(item["code"]),
        class_name="w-full",
    )


def template_step() -> rx.Component:
    return rx.el.div(
        rx.el.h2(
            "Choisissez votre mise en page",
            class_name="text-xl font-semibold text-[#17283F]",
        ),
        rx.el.p(
            "Votre contenu reste intact lorsque vous changez de modèle.",
            class_name="mt-2 text-sm leading-6 text-[#586374]",
        ),
        rx.el.div(
            rx.foreach(PublicSiteState.templates, template_card),
            class_name="grid gap-3 sm:grid-cols-2 xl:grid-cols-3",
        ),
        class_name="flex flex-col gap-5",
    )


def review_step() -> rx.Component:
    return rx.el.div(
        rx.icon("circle-check", class_name="h-8 w-8 text-[#D77B67]"),
        rx.el.h2(
            "Votre aperçu est prêt",
            class_name="mt-3 text-xl font-semibold text-[#17283F]",
        ),
        rx.el.p(
            "Relisez l’aperçu A4 à droite. Vous pouvez revenir à chaque étape pour corriger votre contenu. La rédaction et l’aperçu sont gratuits.",
            class_name="mt-2 max-w-xl text-sm leading-6 text-[#586374]",
        ),
        rx.el.div(
            rx.el.p(
                "À vérifier avant de partager",
                class_name="font-semibold text-[#17283F]",
            ),
            rx.el.p(
                "Exactitude des dates et coordonnées · orthographe · pertinence des éléments · lisibilité du modèle",
                class_name="mt-2 text-sm leading-6 text-[#586374]",
            ),
            class_name="mt-5 rounded-xl border border-[#E7E0D5] bg-white p-5",
        ),
    )


def step_content() -> rx.Component:
    return rx.match(
        CVEditorState.active_step,
        (0, personal_step()),
        (1, role_step()),
        (2, summary_step()),
        (3, collection_step()),
        (4, collection_step()),
        (5, collection_step()),
        (6, collection_step()),
        (7, collection_step()),
        (8, collection_step()),
        (9, collection_step()),
        (10, template_step()),
        review_step(),
    )


def editor_workflow() -> rx.Component:
    return rx.el.div(
        step_sidebar(),
        rx.el.section(
            rx.el.div(
                rx.el.p(
                    f"ÉTAPE {CVEditorState.active_step + 1} / 12",
                    class_name="text-[10px] font-semibold tracking-[0.18em] text-[#D77B67]",
                ),
                rx.el.h1(
                    rx.match(
                        CVEditorState.active_step,
                        (0, "Informations personnelles"),
                        (1, "Poste recherché"),
                        (2, "Résumé professionnel"),
                        (3, "Expériences"),
                        (4, "Formations"),
                        (5, "Compétences"),
                        (6, "Langues"),
                        (7, "Certifications"),
                        (8, "Projets"),
                        (9, "Centres d’intérêt"),
                        (10, "Choix du modèle"),
                        "Vérification",
                    ),
                    class_name="mt-2 text-2xl font-semibold tracking-tight text-[#17283F]",
                ),
                class_name="mb-6",
            ),
            rx.cond(
                CVEditorState.error_message,
                rx.el.div(
                    rx.icon("circle-alert", class_name="h-4 w-4"),
                    CVEditorState.error_message,
                    class_name="mb-4 flex gap-2 rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700",
                ),
            ),
            rx.cond(
                CVEditorState.notice_message,
                rx.el.p(
                    CVEditorState.notice_message,
                    class_name="mb-4 text-xs font-medium text-green-600",
                ),
            ),
            step_content(),
            rx.el.div(
                rx.el.button(
                    rx.icon("arrow-left", class_name="h-4 w-4"),
                    "Précédent",
                    on_click=CVEditorState.set_active_step(
                        CVEditorState.active_step - 1
                    ),
                    disabled=CVEditorState.active_step == 0,
                    class_name="inline-flex items-center gap-2 rounded-full border border-[#D8D0C4] px-4 py-2.5 text-sm font-semibold text-[#17283F] transition hover:bg-[#F2EEE7] disabled:opacity-40",
                ),
                rx.el.div(
                    rx.el.button(
                        rx.icon("save", class_name="h-4 w-4"),
                        "Enregistrer",
                        on_click=CVEditorState.save_cv,
                        class_name="inline-flex items-center gap-2 rounded-full bg-[#17283F] px-5 py-2.5 text-sm font-semibold text-white transition hover:bg-[#263D58]",
                    ),
                    rx.el.a(
                        rx.icon("log-in", class_name="h-4 w-4"),
                        "Se connecter",
                        href="/login?redirect_to=/creer",
                        class_name="inline-flex items-center gap-2 rounded-full bg-[#17283F] px-5 py-2.5 text-sm font-semibold text-white transition hover:bg-[#263D58]",
                    ),
                    rx.cond(
                        CVEditorState.active_step < 11,
                        rx.el.button(
                            "Continuer",
                            rx.icon("arrow-right", class_name="h-4 w-4"),
                            on_click=CVEditorState.set_active_step(
                                CVEditorState.active_step + 1
                            ),
                            class_name="inline-flex items-center gap-2 rounded-full border border-[#D8D0C4] px-4 py-2.5 text-sm font-semibold text-[#17283F] transition hover:bg-[#F2EEE7]",
                        ),
                    ),
                    class_name="flex flex-wrap items-center justify-end gap-2",
                ),
                class_name="mt-8 flex flex-wrap items-center justify-between gap-3 border-t border-[#E7E0D5] pt-5",
            ),
            class_name="min-w-0 flex-1 p-5 sm:p-7 lg:p-9",
        ),
        class_name="flex min-h-[700px] flex-col rounded-2xl border border-[#E7E0D5] bg-white md:flex-row",
    )


def editor_header() -> rx.Component:
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
            rx.el.div(
                rx.el.a(
                    "Mes CV",
                    href="/mes-cv",
                    class_name="rounded-full px-3 py-2 text-sm font-semibold text-[#586374] hover:bg-[#EEE8DD]",
                ),
                rx.el.a(
                    "Se connecter",
                    href="/login?redirect_to=/creer",
                    class_name="rounded-full px-3 py-2 text-sm font-semibold text-[#586374] hover:bg-[#EEE8DD]",
                ),
                class_name="flex items-center gap-1",
            ),
            class_name="mx-auto flex w-full max-w-[1600px] items-center justify-between px-5 py-4 md:px-8",
        ),
        class_name="border-b border-[#E7E0D5] bg-[#F8F5EF]",
    )


def cv_editor_page() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            on_mount=[
                CVEditorState.load_editor,
                PublicSiteState.load_public_price,
                RoleState.refresh_current_role,
            ]
        ),
        editor_header(),
        rx.el.main(
            rx.el.div(
                rx.el.div(
                    rx.el.p(
                        "ÉDITEUR DE CV",
                        class_name="text-xs font-semibold tracking-[0.2em] text-[#D77B67]",
                    ),
                    rx.el.h1(
                        "Donnez forme à votre parcours",
                        class_name="mt-2 text-3xl font-semibold tracking-tight text-[#17283F] sm:text-4xl",
                    ),
                    rx.el.p(
                        "Rédigez gratuitement, choisissez un style et visualisez votre CV en temps réel.",
                        class_name="mt-3 max-w-3xl text-sm leading-6 text-[#586374]",
                    ),
                    class_name="mb-7",
                ),
                rx.el.div(
                    rx.el.button(
                        rx.icon("pen-line", class_name="h-4 w-4"),
                        "Rédaction",
                        on_click=CVEditorState.toggle_mobile_preview,
                        class_name=rx.cond(
                            CVEditorState.show_mobile_preview,
                            "flex-1 rounded-full px-4 py-2 text-sm text-[#586374]",
                            "flex-1 rounded-full bg-white px-4 py-2 text-sm font-semibold text-[#17283F]",
                        ),
                    ),
                    rx.el.button(
                        rx.icon("eye", class_name="h-4 w-4"),
                        "Aperçu A4",
                        on_click=CVEditorState.toggle_mobile_preview,
                        class_name=rx.cond(
                            CVEditorState.show_mobile_preview,
                            "flex-1 rounded-full bg-white px-4 py-2 text-sm font-semibold text-[#17283F]",
                            "flex-1 rounded-full px-4 py-2 text-sm text-[#586374]",
                        ),
                    ),
                    class_name="mb-4 flex rounded-full bg-[#EEEAE3] p-1 md:hidden",
                ),
                rx.el.div(
                    rx.el.div(
                        editor_workflow(),
                        class_name=rx.cond(
                            CVEditorState.show_mobile_preview,
                            "hidden md:block",
                            "block",
                        ),
                    ),
                    rx.el.aside(
                        rx.el.div(
                            rx.el.div(
                                rx.el.div(
                                    rx.icon(
                                        "file-text",
                                        class_name="h-4 w-4 text-[#D77B67]",
                                    ),
                                    rx.el.p(
                                        "APERÇU A4",
                                        class_name="text-[10px] font-semibold tracking-[0.18em] text-[#586374]",
                                    ),
                                    class_name="flex items-center gap-2",
                                ),
                                rx.el.p(
                                    CVEditorState.template_code,
                                    class_name="text-xs font-medium capitalize text-[#7B8187]",
                                ),
                                class_name="mb-4 flex items-center justify-between",
                            ),
                            cv_preview_a4(),
                            rx.el.div(
                                purchase_actions(CVEditorState.cv_id),
                                purchase_feedback(),
                                class_name="mt-4",
                            ),
                            rx.el.p(
                                "PDF A4 après sauvegarde et confirmation d’un achat fictif. Aucun prélèvement.",
                                class_name="mt-3 text-center text-[11px] text-[#7B8187]",
                            ),
                        ),
                        class_name=rx.cond(
                            CVEditorState.show_mobile_preview,
                            "block min-w-0",
                            "hidden min-w-0 md:block",
                        ),
                    ),
                    class_name="grid w-full min-w-0 gap-6 xl:grid-cols-[minmax(0,1fr)_minmax(390px,0.9fr)]",
                ),
                class_name="mx-auto w-full max-w-[1600px] px-4 py-8 sm:px-6 lg:px-8",
            ),
            class_name="min-w-0 flex-1",
        ),
        checkout_modal(),
        class_name="min-h-dvh bg-[#F8F5EF] font-['Inter'] text-[#17283F]",
    )
