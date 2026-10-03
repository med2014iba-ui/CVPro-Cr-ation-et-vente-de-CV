import reflex as rx

from app.states.public_site_state import PublicSiteState


_IVORY = "bg-[#F8F5EF]"
_NAVY = "text-[#17283F]"
_CORAL = "text-[#D77B67]"


def site_header() -> rx.Component:
    return rx.el.header(
        rx.el.div(
            rx.el.a(
                rx.icon("file-user", class_name="h-5 w-5 text-[#D77B67]"),
                rx.el.span(
                    "CVPro",
                    class_name="text-xl font-semibold tracking-tight text-[#17283F]",
                ),
                href="/",
                class_name="flex shrink-0 items-center gap-2",
            ),
            rx.el.nav(
                rx.el.a(
                    "Accueil",
                    href="/",
                    class_name="rounded-full px-3 py-2 text-sm font-medium text-[#586374] transition-colors hover:bg-[#EEE8DD] hover:text-[#17283F]",
                ),
                rx.el.a(
                    "Modèles",
                    href="/modeles",
                    class_name="rounded-full px-3 py-2 text-sm font-medium text-[#586374] transition-colors hover:bg-[#EEE8DD] hover:text-[#17283F]",
                ),
                rx.el.a(
                    "Prix",
                    href="/prix",
                    class_name="rounded-full px-3 py-2 text-sm font-medium text-[#586374] transition-colors hover:bg-[#EEE8DD] hover:text-[#17283F]",
                ),
                rx.el.a(
                    "À propos",
                    href="/a-propos",
                    class_name="rounded-full px-3 py-2 text-sm font-medium text-[#586374] transition-colors hover:bg-[#EEE8DD] hover:text-[#17283F]",
                ),
                rx.el.a(
                    "FAQ",
                    href="/faq",
                    class_name="rounded-full px-3 py-2 text-sm font-medium text-[#586374] transition-colors hover:bg-[#EEE8DD] hover:text-[#17283F]",
                ),
                rx.el.a(
                    "Contact",
                    href="/contact",
                    class_name="rounded-full px-3 py-2 text-sm font-medium text-[#586374] transition-colors hover:bg-[#EEE8DD] hover:text-[#17283F]",
                ),
                class_name="flex flex-wrap items-center justify-center gap-1",
            ),
            rx.el.div(
                rx.el.a(
                    "Mes CV",
                    href="/mes-cv",
                    class_name="rounded-full px-3 py-2 text-sm font-semibold text-[#586374] hover:bg-[#EEE8DD]",
                ),
                rx.el.a(
                    "Mon profil",
                    href="/profil",
                    class_name="rounded-full px-3 py-2 text-sm font-semibold text-[#586374] hover:bg-[#EEE8DD]",
                ),
                rx.el.a(
                    "Se connecter",
                    href="/login?redirect_to=/creer",
                    class_name="rounded-full px-3 py-2 text-sm font-semibold text-[#586374] hover:bg-[#EEE8DD]",
                ),
                class_name="hidden items-center sm:flex",
            ),
            rx.el.a(
                "Créer mon CV",
                rx.icon("arrow-up-right", class_name="h-4 w-4"),
                href="/creer?nouveau=1",
                class_name="hidden shrink-0 items-center gap-2 rounded-full bg-[#17283F] px-5 py-3 text-sm font-semibold text-white transition-colors hover:bg-[#263D58] sm:flex",
            ),
            class_name="mx-auto flex w-full max-w-7xl flex-col items-center justify-between gap-3 px-5 py-4 md:flex-row md:px-8",
        ),
        class_name="border-b border-[#E7E0D5] bg-[#F8F5EF]",
    )


def site_footer() -> rx.Component:
    return rx.el.footer(
        rx.el.div(
            rx.el.div(
                rx.el.a(
                    rx.icon("file-user", class_name="h-5 w-5 text-[#D77B67]"),
                    rx.el.span(
                        "CVPro", class_name="text-lg font-semibold text-white"
                    ),
                    href="/",
                    class_name="flex items-center gap-2",
                ),
                rx.el.p(
                    "Des outils simples pour présenter votre parcours avec clarté.",
                    class_name="mt-3 max-w-sm text-sm leading-6 text-white/65",
                ),
                class_name="md:col-span-2",
            ),
            rx.el.div(
                rx.el.p(
                    "Explorer",
                    class_name="mb-3 text-xs font-semibold uppercase tracking-[0.16em] text-white/50",
                ),
                rx.el.a(
                    "Les modèles",
                    href="/modeles",
                    class_name="text-sm text-white/80 transition-colors hover:text-white",
                ),
                rx.el.a(
                    "Les tarifs",
                    href="/prix",
                    class_name="text-sm text-white/80 transition-colors hover:text-white",
                ),
                rx.el.a(
                    "Questions fréquentes",
                    href="/faq",
                    class_name="text-sm text-white/80 transition-colors hover:text-white",
                ),
                class_name="flex flex-col items-start gap-3",
            ),
            rx.el.div(
                rx.el.p(
                    "Informations",
                    class_name="mb-3 text-xs font-semibold uppercase tracking-[0.16em] text-white/50",
                ),
                rx.el.a(
                    "À propos",
                    href="/a-propos",
                    class_name="text-sm text-white/80 transition-colors hover:text-white",
                ),
                rx.el.a(
                    "Contact",
                    href="/contact",
                    class_name="text-sm text-white/80 transition-colors hover:text-white",
                ),
                rx.el.a(
                    "Confidentialité",
                    href="/confidentialite",
                    class_name="text-sm text-white/80 transition-colors hover:text-white",
                ),
                rx.el.a(
                    "Conditions",
                    href="/conditions",
                    class_name="text-sm text-white/80 transition-colors hover:text-white",
                ),
                class_name="flex flex-col items-start gap-3",
            ),
            class_name="mx-auto grid w-full max-w-7xl gap-10 px-5 py-12 sm:grid-cols-2 md:grid-cols-4 md:px-8",
        ),
        rx.el.div(
            rx.el.p(
                "© CVPro · Version de démonstration",
                class_name="text-xs text-white/50",
            ),
            rx.el.p(
                "Les informations légales sont à compléter avant toute exploitation commerciale.",
                class_name="text-xs text-white/50",
            ),
            class_name="mx-auto flex w-full max-w-7xl flex-col gap-2 border-t border-white/10 px-5 py-5 md:flex-row md:items-center md:justify-between md:px-8",
        ),
        class_name="bg-[#17283F]",
    )


def site_layout(content: rx.Component) -> rx.Component:
    return rx.el.div(
        site_header(),
        content,
        site_footer(),
        on_mount=PublicSiteState.load_public_price,
        class_name="min-h-screen bg-[#F8F5EF] font-['Inter'] text-[#17283F]",
    )


def section_heading(kicker: str, title: str, description: str) -> rx.Component:
    return rx.el.div(
        rx.el.p(
            kicker.upper(),
            class_name="mb-3 text-xs font-semibold tracking-[0.2em] text-[#D77B67]",
        ),
        rx.el.h2(
            title,
            class_name="text-3xl font-semibold leading-tight tracking-tight text-[#17283F] sm:text-4xl",
        ),
        rx.el.p(
            description,
            class_name="mt-4 max-w-2xl text-base leading-7 text-[#586374]",
        ),
        class_name="mb-10",
    )


def resume_thumbnail(code: str) -> rx.Component:
    return rx.match(
        code,
        (
            "moderne",
            rx.el.div(
                rx.el.div(
                    rx.el.div(class_name="h-2 w-16 rounded bg-[#17283F]"),
                    rx.el.div(class_name="mt-2 h-1 w-24 rounded bg-[#B8C8D5]"),
                    class_name="bg-[#EAF0F3] px-4 py-4",
                ),
                rx.el.div(
                    rx.el.div(class_name="h-1.5 w-14 rounded bg-[#17283F]"),
                    rx.el.div(
                        class_name="mt-2 h-1 w-full rounded bg-[#D9DFE2]"
                    ),
                    rx.el.div(
                        class_name="mt-1.5 h-1 w-4/5 rounded bg-[#D9DFE2]"
                    ),
                    rx.el.div(
                        class_name="mt-4 h-1.5 w-12 rounded bg-[#17283F]"
                    ),
                    rx.el.div(
                        class_name="mt-2 h-1 w-full rounded bg-[#D9DFE2]"
                    ),
                    class_name="p-4",
                ),
                class_name="min-h-52 overflow-hidden rounded-t-lg bg-white",
            ),
        ),
        (
            "classique",
            rx.el.div(
                rx.el.div(
                    rx.el.p(
                        "NOM PRÉNOM",
                        class_name="font-serif text-[10px] font-bold tracking-[0.12em] text-[#17283F]",
                    ),
                    rx.el.p(
                        "Fonction souhaitée",
                        class_name="mt-1 font-serif text-[7px] italic text-[#586374]",
                    ),
                    class_name="border-b-2 border-[#17283F] px-4 py-5 text-center",
                ),
                rx.el.div(
                    rx.el.p(
                        "EXPÉRIENCE",
                        class_name="font-serif text-[7px] font-bold tracking-widest text-[#17283F]",
                    ),
                    rx.el.div(class_name="mt-2 h-1 w-full bg-[#D9DFE2]"),
                    rx.el.div(class_name="mt-1 h-1 w-4/5 bg-[#D9DFE2]"),
                    rx.el.p(
                        "FORMATION",
                        class_name="mt-4 font-serif text-[7px] font-bold tracking-widest text-[#17283F]",
                    ),
                    rx.el.div(class_name="mt-2 h-1 w-full bg-[#D9DFE2]"),
                    class_name="px-4 py-3",
                ),
                class_name="min-h-52 overflow-hidden rounded-t-lg bg-white",
            ),
        ),
        (
            "elegant",
            rx.el.div(
                rx.el.div(
                    rx.el.div(class_name="h-9 w-9 rounded-full bg-[#E9D8D0]"),
                    rx.el.div(
                        rx.el.div(class_name="h-2 w-16 rounded bg-[#17283F]"),
                        rx.el.div(
                            class_name="mt-2 h-1 w-20 rounded bg-[#C4B4AA]"
                        ),
                    ),
                    class_name="flex items-center gap-3 border-b border-[#E8DED6] px-4 py-5",
                ),
                rx.el.div(
                    rx.el.div(class_name="h-1.5 w-12 rounded bg-[#D77B67]"),
                    rx.el.div(
                        class_name="mt-2 h-1 w-full rounded bg-[#DED9D4]"
                    ),
                    rx.el.div(
                        class_name="mt-1.5 h-1 w-4/5 rounded bg-[#DED9D4]"
                    ),
                    rx.el.div(
                        class_name="mt-4 h-1.5 w-10 rounded bg-[#D77B67]"
                    ),
                    rx.el.div(
                        class_name="mt-2 h-1 w-full rounded bg-[#DED9D4]"
                    ),
                    class_name="px-4 py-3",
                ),
                class_name="min-h-52 overflow-hidden rounded-t-lg bg-[#FFFEFC]",
            ),
        ),
        (
            "minimaliste",
            rx.el.div(
                rx.el.div(
                    rx.el.p(
                        "prénom nom",
                        class_name="text-[10px] font-light lowercase tracking-wide text-[#17283F]",
                    ),
                    rx.el.p(
                        "Intitulé professionnel",
                        class_name="mt-1 text-[7px] font-light text-[#586374]",
                    ),
                    class_name="px-5 py-5",
                ),
                rx.el.div(
                    rx.el.div(class_name="h-px w-full bg-[#E5E5E2]"),
                    rx.el.p(
                        "Expérience",
                        class_name="mt-4 text-[7px] font-medium text-[#17283F]",
                    ),
                    rx.el.div(class_name="mt-2 h-1 w-full bg-[#E6E6E3]"),
                    rx.el.div(class_name="mt-1 h-1 w-3/4 bg-[#E6E6E3]"),
                    rx.el.p(
                        "Compétences",
                        class_name="mt-4 text-[7px] font-medium text-[#17283F]",
                    ),
                    rx.el.div(class_name="mt-2 h-1 w-2/3 bg-[#E6E6E3]"),
                    class_name="px-5",
                ),
                class_name="min-h-52 overflow-hidden rounded-t-lg bg-white",
            ),
        ),
        (
            "creatif",
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        class_name="absolute left-0 top-0 h-full w-2 bg-[#D77B67]"
                    ),
                    rx.el.p(
                        "NOM",
                        class_name="text-[10px] font-black uppercase tracking-[0.15em] text-[#17283F]",
                    ),
                    rx.el.p(
                        "Création & idées",
                        class_name="mt-1 text-[7px] font-semibold text-[#D77B67]",
                    ),
                    class_name="relative bg-[#F6E8E1] px-5 py-5",
                ),
                rx.el.div(
                    rx.el.div(
                        class_name="h-1.5 w-14 rounded-full bg-[#17283F]"
                    ),
                    rx.el.div(
                        class_name="mt-2 h-1 w-full rounded-full bg-[#D9DFE2]"
                    ),
                    rx.el.div(
                        class_name="mt-1.5 h-1 w-3/4 rounded-full bg-[#D9DFE2]"
                    ),
                    rx.el.div(
                        class_name="mt-4 h-1.5 w-10 rounded-full bg-[#D77B67]"
                    ),
                    rx.el.div(
                        class_name="mt-2 h-1 w-4/5 rounded-full bg-[#D9DFE2]"
                    ),
                    class_name="p-4",
                ),
                class_name="min-h-52 overflow-hidden rounded-t-lg bg-white",
            ),
        ),
        rx.el.div(
            "Aperçu du modèle",
            class_name="min-h-52 rounded-t-lg bg-white p-8 text-center text-sm text-[#586374]",
        ),
    )


def template_card(code: str, name: str, description: str) -> rx.Component:
    return rx.el.article(
        rx.el.div(
            resume_thumbnail(code),
            class_name="overflow-hidden rounded-t-xl bg-white p-5 pb-0",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.h3(
                    name, class_name="text-lg font-semibold text-[#17283F]"
                ),
                rx.el.span(
                    "CV",
                    class_name="rounded-full bg-[#F1ECE4] px-2.5 py-1 text-[10px] font-semibold uppercase tracking-wider text-[#586374]",
                ),
                class_name="flex items-center justify-between gap-3",
            ),
            rx.el.p(
                description,
                class_name="mt-2 min-h-12 text-sm leading-6 text-[#586374]",
            ),
            rx.el.a(
                "Choisir ce modèle",
                rx.icon("arrow-right", class_name="h-4 w-4"),
                href=f"/creer?modele={code}",
                class_name="mt-5 inline-flex items-center gap-2 text-sm font-semibold text-[#17283F] transition-colors hover:text-[#D77B67]",
            ),
            class_name="p-5",
        ),
        class_name="overflow-hidden rounded-xl border border-[#E7E0D5] bg-white transition-transform duration-200 hover:-translate-y-1",
    )


def model_gallery() -> rx.Component:
    return rx.el.div(
        rx.foreach(
            PublicSiteState.templates,
            lambda item: template_card(
                item["code"], item["name"], item["description"]
            ),
        ),
        rx.cond(
            PublicSiteState.templates.length() == 0,
            rx.el.p(
                "Catalogue indisponible ou aucun modèle actuellement actif.",
                class_name="text-sm text-[#586374]",
            ),
        ),
        class_name="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3",
    )


def primary_cta(label: str = "Créer mon CV") -> rx.Component:
    return rx.el.a(
        label,
        rx.icon("arrow-right", class_name="h-4 w-4"),
        href="/creer?nouveau=1",
        class_name="inline-flex items-center justify-center gap-2 rounded-full bg-[#17283F] px-6 py-3.5 text-sm font-semibold text-white transition-colors hover:bg-[#263D58] focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-[#D77B67]",
    )


def home_content() -> rx.Component:
    return rx.el.main(
        rx.el.section(
            rx.el.div(
                rx.el.div(
                    rx.el.p(
                        "Votre parcours, clairement présenté",
                        class_name="mb-5 text-xs font-semibold uppercase tracking-[0.2em] text-[#D77B67]",
                    ),
                    rx.el.h1(
                        "Créez un CV professionnel en quelques minutes",
                        class_name="max-w-2xl text-4xl font-semibold leading-[1.08] tracking-tight text-[#17283F] sm:text-5xl lg:text-6xl",
                    ),
                    rx.el.p(
                        "Structurez vos expériences et vos compétences dans une mise en page soignée. Choisissez un modèle, puis préparez votre CV à votre rythme.",
                        class_name="mt-6 max-w-xl text-base leading-7 text-[#586374] sm:text-lg",
                    ),
                    rx.el.div(
                        primary_cta(),
                        rx.el.a(
                            "Découvrir les modèles",
                            href="/modeles",
                            class_name="inline-flex items-center gap-2 px-2 py-3 text-sm font-semibold text-[#17283F] transition-colors hover:text-[#D77B67]",
                        ),
                        class_name="mt-8 flex flex-col items-start gap-3 sm:flex-row sm:items-center",
                    ),
                    rx.el.p(
                        "Aucun résultat ni emploi garanti : votre CV reste le reflet de votre expérience.",
                        class_name="mt-5 text-xs leading-5 text-[#7B8187]",
                    ),
                    class_name="py-10 lg:py-16",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.div(
                            rx.el.span(
                                "APERÇU DE MODÈLE",
                                class_name="text-[9px] font-semibold tracking-[0.18em] text-[#586374]",
                            ),
                            rx.el.span(
                                "01 / 05",
                                class_name="text-[9px] font-medium text-[#8B8B86]",
                            ),
                            class_name="mb-4 flex items-center justify-between",
                        ),
                        rx.el.div(
                            resume_thumbnail("moderne"),
                            class_name="overflow-hidden rounded-lg border border-[#E7E0D5] bg-white p-2",
                        ),
                        rx.el.div(
                            rx.icon(
                                "sparkles", class_name="h-4 w-4 text-[#D77B67]"
                            ),
                            rx.el.p(
                                "Une présentation claire, à votre image.",
                                class_name="text-xs font-medium text-[#586374]",
                            ),
                            class_name="mt-4 flex items-center gap-2",
                        ),
                        class_name="rotate-1 rounded-2xl border border-[#E7E0D5] bg-white p-6",
                    ),
                    rx.el.div(
                        "SOIGNEZ CHAQUE DÉTAIL",
                        class_name="absolute -bottom-5 -left-3 rounded-full border border-[#E7E0D5] bg-[#F8F5EF] px-4 py-2 text-[9px] font-semibold tracking-[0.14em] text-[#586374] sm:-left-8",
                    ),
                    class_name="relative mx-auto w-full max-w-sm py-8 lg:my-8",
                ),
                class_name="mx-auto grid w-full max-w-7xl items-center gap-10 px-5 py-8 md:px-8 lg:grid-cols-[1.1fr_0.9fr] lg:gap-16 lg:py-16",
            ),
            class_name="overflow-hidden border-b border-[#E7E0D5]",
        ),
        rx.el.section(
            rx.el.div(
                section_heading(
                    "Une mise en page pour chaque parcours",
                    "Choisissez votre style",
                    "Cinq compositions distinctes pour présenter votre profil avec une structure lisible et un ton qui vous ressemble.",
                ),
                model_gallery(),
                rx.el.div(
                    rx.el.a(
                        "Voir les cinq modèles",
                        rx.icon("arrow-right", class_name="h-4 w-4"),
                        href="/modeles",
                        class_name="inline-flex items-center gap-2 text-sm font-semibold text-[#17283F] hover:text-[#D77B67]",
                    ),
                    class_name="mt-8 text-center",
                ),
                class_name="mx-auto w-full max-w-7xl px-5 py-16 md:px-8 lg:py-24",
            ),
        ),
        how_it_works_section(),
        rx.el.section(
            rx.el.div(
                rx.el.div(
                    section_heading(
                        "Commencez simplement",
                        "Une option gratuite, un choix premium",
                        "Rédaction et aperçu gratuits. Après sauvegarde, confirmez un achat fictif pour télécharger votre PDF A4. Aucun prélèvement.",
                    )
                ),
                pricing_cards(),
                class_name="mx-auto w-full max-w-7xl px-5 py-16 md:px-8 lg:py-24",
            ),
            class_name="border-y border-[#E7E0D5] bg-[#F2EEE7]",
        ),
        rx.el.section(
            rx.el.div(
                section_heading(
                    "À vos questions",
                    "Quelques repères utiles",
                    "Les réponses essentielles sur la rédaction, les achats fictifs et le téléchargement PDF.",
                ),
                faq_list(),
                rx.el.div(
                    rx.el.a(
                        "Toutes les réponses",
                        href="/faq",
                        class_name="inline-flex items-center gap-2 text-sm font-semibold text-[#17283F] hover:text-[#D77B67]",
                    ),
                    class_name="mt-7",
                ),
                class_name="mx-auto w-full max-w-4xl px-5 py-16 md:px-8 lg:py-24",
            ),
        ),
    )


def how_it_works_section() -> rx.Component:
    return rx.el.section(
        rx.el.div(
            section_heading(
                "De l’idée au document",
                "Comment ça marche",
                "Un parcours simple en trois étapes, conçu pour vous aider à organiser les informations que vous souhaitez partager.",
            ),
            rx.el.div(
                step_card(
                    "01",
                    "Choisissez un modèle",
                    "Parcourez les compositions et sélectionnez celle qui convient à votre secteur et à votre style.",
                ),
                step_card(
                    "02",
                    "Présentez votre parcours",
                    "Rassemblez vos coordonnées, expériences, formations et compétences dans un ordre clair.",
                ),
                step_card(
                    "03",
                    "Relisez et finalisez",
                    "Vérifiez chaque information et la lisibilité de votre document avant de l’utiliser.",
                ),
                class_name="grid grid-cols-1 gap-5 md:grid-cols-3",
            ),
            class_name="mx-auto w-full max-w-7xl px-5 py-16 md:px-8 lg:py-24",
        ),
    )


def step_card(number: str, title: str, description: str) -> rx.Component:
    return rx.el.article(
        rx.el.p(
            number,
            class_name="mb-8 text-sm font-semibold tracking-[0.14em] text-[#D77B67]",
        ),
        rx.el.h3(title, class_name="text-xl font-semibold text-[#17283F]"),
        rx.el.p(
            description, class_name="mt-3 text-sm leading-6 text-[#586374]"
        ),
        class_name="rounded-xl border border-[#E7E0D5] bg-white p-6 sm:p-8",
    )


def pricing_cards() -> rx.Component:
    return rx.el.div(
        rx.el.article(
            rx.el.p(
                "Pour démarrer",
                class_name="text-sm font-semibold text-[#586374]",
            ),
            rx.el.h3(
                "Gratuit",
                class_name="mt-3 text-3xl font-semibold tracking-tight text-[#17283F]",
            ),
            rx.el.p(
                "Explorez les modèles et préparez le contenu de votre CV.",
                class_name="mt-3 min-h-14 text-sm leading-6 text-[#586374]",
            ),
            rx.el.ul(
                rx.el.li(
                    rx.icon("check", class_name="h-4 w-4 text-[#D77B67]"),
                    "Rédaction et aperçu A4 gratuits",
                    class_name="flex items-start gap-2 text-sm text-[#586374]",
                ),
                rx.el.li(
                    rx.icon("check", class_name="h-4 w-4 text-[#D77B67]"),
                    "Sauvegarde de plusieurs CV après connexion",
                    class_name="flex items-start gap-2 text-sm text-[#586374]",
                ),
                class_name="mt-6 flex flex-col gap-3",
            ),
            rx.el.a(
                "Découvrir les modèles",
                href="/modeles",
                class_name="mt-8 inline-flex text-sm font-semibold text-[#17283F] hover:text-[#D77B67]",
            ),
            class_name="rounded-xl border border-[#E7E0D5] bg-white p-7 sm:p-9",
        ),
        rx.el.article(
            rx.el.div(
                rx.el.p(
                    "Pour aller plus loin",
                    class_name="text-sm font-semibold text-[#586374]",
                ),
                rx.el.span(
                    "DÉMONSTRATION",
                    class_name="rounded-full bg-[#F7E8E3] px-3 py-1 text-[9px] font-bold tracking-[0.14em] text-[#B86251]",
                ),
                class_name="flex flex-wrap items-center justify-between gap-3",
            ),
            rx.el.p(
                PublicSiteState.price_display,
                class_name="mt-3 text-3xl font-semibold tracking-tight text-[#17283F]",
            ),
            rx.el.p(
                "Tarif courant de démonstration. Après sauvegarde et consentement explicite à un achat fictif, téléchargez le PDF A4 de votre CV. Aucun paiement réel.",
                class_name="mt-3 min-h-14 text-sm leading-6 text-[#586374]",
            ),
            rx.el.ul(
                rx.el.li(
                    rx.icon("check", class_name="h-4 w-4 text-[#D77B67]"),
                    "PDF A4 dans le style choisi, depuis le CV sauvegardé",
                    class_name="flex items-start gap-2 text-sm text-[#586374]",
                ),
                rx.el.li(
                    rx.icon("info", class_name="h-4 w-4 text-[#D77B67]"),
                    "Aucun achat réel dans cette version",
                    class_name="flex items-start gap-2 text-sm text-[#586374]",
                ),
                class_name="mt-6 flex flex-col gap-3",
            ),
            rx.el.a(
                "En savoir plus",
                href="/prix",
                class_name="mt-8 inline-flex text-sm font-semibold text-[#17283F] hover:text-[#D77B67]",
            ),
            class_name="rounded-xl border border-[#D9CFC2] bg-[#FCFAF6] p-7 sm:p-9",
        ),
        class_name="grid grid-cols-1 gap-5 md:grid-cols-2",
    )


def page_intro(kicker: str, title: str, description: str) -> rx.Component:
    return rx.el.div(
        rx.el.p(
            kicker.upper(),
            class_name="mb-4 text-xs font-semibold tracking-[0.2em] text-[#D77B67]",
        ),
        rx.el.h1(
            title,
            class_name="max-w-4xl text-4xl font-semibold leading-tight tracking-tight text-[#17283F] sm:text-5xl",
        ),
        rx.el.p(
            description,
            class_name="mt-5 max-w-3xl text-base leading-7 text-[#586374] sm:text-lg",
        ),
        class_name="mb-12",
    )


def models_content() -> rx.Component:
    return rx.el.main(
        rx.el.div(
            page_intro(
                "Galerie des modèles",
                "Cinq façons de présenter votre parcours",
                "Chaque aperçu illustre une composition différente. Les contenus sont des éléments de maquette, pas des exemples de CV réels.",
            ),
            model_gallery(),
            rx.el.p(
                "Choisissez un modèle pour ouvrir l’éditeur gratuit. Vous pourrez encore changer de style sans perdre votre contenu.",
                class_name="mt-8 text-sm leading-6 text-[#7B8187]",
            ),
            class_name="mx-auto w-full max-w-7xl px-5 py-14 md:px-8 lg:py-20",
        ),
    )


def pricing_content() -> rx.Component:
    return rx.el.main(
        rx.el.div(
            page_intro(
                "Tarifs transparents",
                "Commencez gratuitement, choisissez ensuite",
                "Le montant ci-dessous est le tarif courant en DZD. L’achat est strictement fictif, sans prélèvement ni collecte de carte, et débloque le PDF d’un CV sauvegardé.",
            ),
            pricing_cards(),
            rx.el.div(
                rx.icon(
                    "info", class_name="mt-0.5 h-5 w-5 shrink-0 text-[#D77B67]"
                ),
                rx.el.p(
                    "La confirmation d’achat fictif se déroule dans l’éditeur ou dans Mes CV, après connexion et sauvegarde. Aucun prestataire de paiement n’intervient. Aucun achat réel ni contrat de vente commerciale.",
                    class_name="text-sm leading-6 text-[#586374]",
                ),
                class_name="mt-8 flex gap-3 rounded-xl border border-[#E7E0D5] bg-white p-5",
            ),
            class_name="mx-auto w-full max-w-5xl px-5 py-14 md:px-8 lg:py-20",
        ),
    )


def about_content() -> rx.Component:
    return rx.el.main(
        rx.el.div(
            page_intro(
                "À propos de CVPro",
                "Un CV lisible commence par une bonne structure",
                "CVPro est conçu autour d’une idée simple : aider chacun à organiser son parcours et à le présenter avec clarté, sans promettre de résultat professionnel.",
            ),
            rx.el.div(
                rx.el.article(
                    rx.icon(
                        "layout-template", class_name="h-6 w-6 text-[#D77B67]"
                    ),
                    rx.el.h2(
                        "Des modèles réfléchis",
                        class_name="mt-5 text-xl font-semibold text-[#17283F]",
                    ),
                    rx.el.p(
                        "Des compositions distinctes pour différents styles de candidature, avec la lisibilité comme point de départ.",
                        class_name="mt-3 text-sm leading-6 text-[#586374]",
                    ),
                    class_name="rounded-xl border border-[#E7E0D5] bg-white p-7",
                ),
                rx.el.article(
                    rx.icon("list-checks", class_name="h-6 w-6 text-[#D77B67]"),
                    rx.el.h2(
                        "Vos informations, votre choix",
                        class_name="mt-5 text-xl font-semibold text-[#17283F]",
                    ),
                    rx.el.p(
                        "Vous décidez des expériences et compétences pertinentes à faire apparaître. Relisez toujours les informations avant de partager votre CV.",
                        class_name="mt-3 text-sm leading-6 text-[#586374]",
                    ),
                    class_name="rounded-xl border border-[#E7E0D5] bg-white p-7",
                ),
                rx.el.article(
                    rx.icon(
                        "heart-handshake", class_name="h-6 w-6 text-[#D77B67]"
                    ),
                    rx.el.h2(
                        "Un parcours clair",
                        class_name="mt-5 text-xl font-semibold text-[#17283F]",
                    ),
                    rx.el.p(
                        "Rédigez et prévisualisez gratuitement. Connectez-vous pour sauvegarder, puis confirmez un achat fictif pour télécharger votre PDF A4. Aucun prélèvement.",
                        class_name="mt-3 text-sm leading-6 text-[#586374]",
                    ),
                    class_name="rounded-xl border border-[#E7E0D5] bg-white p-7",
                ),
                class_name="grid grid-cols-1 gap-5 md:grid-cols-3",
            ),
            class_name="mx-auto w-full max-w-7xl px-5 py-14 md:px-8 lg:py-20",
        ),
    )


def contact_content() -> rx.Component:
    return rx.el.main(
        rx.el.div(
            page_intro(
                "Contact",
                "Une question sur CVPro ?",
                "Nous souhaitons rendre les informations utiles et faciles à trouver. Cette version de démonstration ne publie pas encore de canal de support dédié.",
            ),
            rx.el.div(
                rx.icon("message-circle", class_name="h-6 w-6 text-[#D77B67]"),
                rx.el.h2(
                    "Le support sera annoncé ici",
                    class_name="mt-4 text-xl font-semibold text-[#17283F]",
                ),
                rx.el.p(
                    "Aucune adresse de contact ou formulaire n’est actuellement configuré. Nous préférons ne pas afficher de coordonnées non vérifiées. Les informations de contact du responsable du service devront être publiées avant son ouverture commerciale.",
                    class_name="mt-3 max-w-2xl text-sm leading-7 text-[#586374]",
                ),
                rx.el.a(
                    "Consulter les questions fréquentes",
                    rx.icon("arrow-right", class_name="h-4 w-4"),
                    href="/faq",
                    class_name="mt-6 inline-flex items-center gap-2 text-sm font-semibold text-[#17283F] hover:text-[#D77B67]",
                ),
                class_name="rounded-2xl border border-[#E7E0D5] bg-white p-7 sm:p-10",
            ),
            class_name="mx-auto w-full max-w-5xl px-5 py-14 md:px-8 lg:py-20",
        ),
    )


def faq_item(question: str, answer: str) -> rx.Component:
    return rx.el.details(
        rx.el.summary(
            question,
            class_name="flex cursor-pointer list-none items-center justify-between gap-4 py-5 text-base font-semibold text-[#17283F] marker:hidden",
        ),
        rx.el.p(
            answer, class_name="pb-5 pr-8 text-sm leading-7 text-[#586374]"
        ),
        class_name="border-b border-[#E7E0D5] [&_summary::-webkit-details-marker]:hidden",
    )


def faq_list() -> rx.Component:
    return rx.el.div(
        faq_item(
            "Puis-je créer un CV dès maintenant ?",
            "Oui. La rédaction et l’aperçu A4 sont gratuits et accessibles sans compte. Connectez-vous uniquement pour enregistrer votre CV dans votre espace personnel.",
        ),
        faq_item(
            "Les aperçus montrent-ils de vrais CV ?",
            "Non. Ce sont des maquettes visuelles génériques, sans données personnelles ni témoignages.",
        ),
        faq_item(
            "Que comprend l’offre gratuite ?",
            "La rédaction, le choix parmi les cinq modèles et l’aperçu A4 sont gratuits. L’enregistrement de plusieurs CV est disponible après connexion.",
        ),
        faq_item(
            "Le prix premium affiché est-il payable ?",
            "Aucun paiement réel. Le tarif courant sert uniquement à une confirmation fictive avec consentement explicite. Une fois cet achat démo confirmé, vous pouvez télécharger le PDF du même CV, sans nouvel achat. Aucune carte n’est collectée.",
        ),
        faq_item(
            "Le tarif est affiché dans quelle devise ?",
            "Le tarif courant et chaque achat fictif sont exprimés en dinars algériens (DZD). Les confirmations conservent le montant affiché au moment de leur enregistrement.",
        ),
        faq_item(
            "CVPro garantit-il un entretien ou un emploi ?",
            "Non. Un CV clair peut aider à présenter un parcours, mais CVPro ne garantit ni entretien, ni embauche, ni réponse d’un recruteur.",
        ),
        class_name="divide-y-0",
    )


def faq_content() -> rx.Component:
    return rx.el.main(
        rx.el.div(
            page_intro(
                "Centre d’aide",
                "Questions fréquentes",
                "Des réponses concrètes sur les modèles, les tarifs affichés et l’état actuel du service.",
            ),
            faq_list(),
            rx.el.div(
                rx.el.p(
                    "Vous ne trouvez pas votre réponse ?",
                    class_name="font-semibold text-[#17283F]",
                ),
                rx.el.a(
                    "Consulter la page contact",
                    href="/contact",
                    class_name="mt-2 inline-flex text-sm font-semibold text-[#D77B67] hover:text-[#17283F]",
                ),
                class_name="mt-10 rounded-xl bg-[#F2EEE7] p-6",
            ),
            class_name="mx-auto w-full max-w-4xl px-5 py-14 md:px-8 lg:py-20",
        ),
    )


def legal_notice(title: str, message: str) -> rx.Component:
    return rx.el.div(
        rx.icon(
            "triangle-alert",
            class_name="mt-0.5 h-5 w-5 shrink-0 text-[#D77B67]",
        ),
        rx.el.p(message, class_name="text-sm leading-6 text-[#586374]"),
        class_name="mb-10 flex gap-3 rounded-xl border border-[#E7E0D5] bg-white p-5",
    )


def privacy_content() -> rx.Component:
    return rx.el.main(
        rx.el.div(
            page_intro(
                "Informations légales",
                "Confidentialité",
                "Informations de préparation sur les données personnelles et les éléments à préciser avant la mise en service de CVPro.",
            ),
            legal_notice(
                "Confidentialité",
                "Document provisoire : l’identité du responsable de traitement, ses coordonnées, les durées de conservation, les destinataires et les modalités d’exercice des droits ne sont pas encore renseignés. Ce texte ne remplace pas une politique juridique validée.",
            ),
            rx.el.div(
                rx.el.h2(
                    "À préciser avant l’ouverture",
                    class_name="text-xl font-semibold text-[#17283F]",
                ),
                rx.el.p(
                    "La rédaction et l’aperçu peuvent être utilisés sans compte ; l’enregistrement en base des CV nécessite une connexion. Avant toute exploitation commerciale, la politique devra décrire précisément les informations traitées, leurs finalités et leur base juridique.",
                    class_name="mt-4 text-sm leading-7 text-[#586374]",
                ),
                rx.el.p(
                    "Elle devra également indiquer les éventuels prestataires et transferts, les durées de conservation, les mesures de sécurité, ainsi que les moyens de demander l’accès, la rectification ou l’effacement des données, selon la réglementation applicable.",
                    class_name="mt-4 text-sm leading-7 text-[#586374]",
                ),
                rx.el.p(
                    "La connexion peut faire intervenir le service d’identité de la plateforme. Les informations exactes transmises et les responsabilités respectives devront être exposées dans une notice complète avant toute collecte opérationnelle.",
                    class_name="mt-4 text-sm leading-7 text-[#586374]",
                ),
                class_name="max-w-3xl",
            ),
            class_name="mx-auto w-full max-w-5xl px-5 py-14 md:px-8 lg:py-20",
        ),
    )


def terms_content() -> rx.Component:
    return rx.el.main(
        rx.el.div(
            page_intro(
                "Informations légales",
                "Conditions d’utilisation",
                "Les conditions ci-dessous signalent les limites de cette vitrine. Les conditions contractuelles finales restent à établir par l’exploitant du service.",
            ),
            legal_notice(
                "Conditions provisoires",
                "CVPro est présenté ici en version de démonstration. Cette page n’est pas un contrat de vente et ne définit pas encore les conditions d’un service commercial.",
            ),
            rx.el.div(
                rx.el.h2(
                    "État actuel du service",
                    class_name="text-xl font-semibold text-[#17283F]",
                ),
                rx.el.p(
                    "Les pages publiques, les aperçus graphiques et le tarif de démonstration sont fournis à titre informatif. Les aperçus de CV sont des maquettes et ne représentent ni des utilisateurs ni des résultats réels.",
                    class_name="mt-4 text-sm leading-7 text-[#586374]",
                ),
                rx.el.p(
                    "L’éditeur gratuit, l’enregistrement après connexion et le PDF A4 sont disponibles. Le téléchargement nécessite un achat fictif confirmé pour votre propre CV sauvegardé. Cet achat est strictement démonstratif : aucun prélèvement, aucune carte, aucun prestataire de paiement. Le montant DZD affiché n’est pas une offre payable.",
                    class_name="mt-4 text-sm leading-7 text-[#586374]",
                ),
                rx.el.h2(
                    "Éléments à publier avant commercialisation",
                    class_name="mt-9 text-xl font-semibold text-[#17283F]",
                ),
                rx.el.p(
                    "Les conditions finales devront notamment identifier l’exploitant, préciser les fonctionnalités et les prérequis, le prix et les modalités de paiement, les règles de résiliation et de remboursement, la propriété intellectuelle, les responsabilités, le droit applicable et les voies de réclamation.",
                    class_name="mt-4 text-sm leading-7 text-[#586374]",
                ),
                class_name="max-w-3xl",
            ),
            class_name="mx-auto w-full max-w-5xl px-5 py-14 md:px-8 lg:py-20",
        ),
    )
