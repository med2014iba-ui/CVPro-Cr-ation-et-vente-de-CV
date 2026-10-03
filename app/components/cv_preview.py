import reflex as rx

from app.states.cv_editor_state import CVEditorState


def preview_identity() -> rx.Component:
    return rx.el.div(
        rx.cond(
            CVEditorState.photo_filename,
            rx.image(
                src=rx.get_upload_url(CVEditorState.photo_filename),
                class_name="h-20 w-20 rounded-full object-cover",
            ),
            rx.el.div(
                rx.icon("user-round", class_name="h-8 w-8 text-[#9A9B99]"),
                class_name="flex h-20 w-20 items-center justify-center rounded-full bg-[#EEEAE3]",
            ),
        ),
        rx.el.div(
            rx.el.h1(
                rx.cond(
                    (CVEditorState.first_name != "")
                    | (CVEditorState.last_name != ""),
                    f"{CVEditorState.first_name} {CVEditorState.last_name}",
                    "Prénom Nom",
                ),
                class_name="text-2xl font-semibold leading-tight",
            ),
            rx.el.p(
                rx.cond(
                    CVEditorState.job_title,
                    CVEditorState.job_title,
                    "Intitulé professionnel",
                ),
                class_name="mt-2 text-sm",
            ),
            class_name="min-w-0 flex-1",
        ),
        class_name="flex items-center gap-4",
    )


def preview_name(class_name: str) -> rx.Component:
    return rx.el.h1(
        rx.cond(
            (CVEditorState.first_name != "") | (CVEditorState.last_name != ""),
            f"{CVEditorState.first_name} {CVEditorState.last_name}",
            "Prénom Nom",
        ),
        class_name=class_name,
    )


def preview_contact() -> rx.Component:
    return rx.el.div(
        rx.cond(
            CVEditorState.email,
            rx.el.p(CVEditorState.email, class_name="break-all"),
        ),
        rx.cond(CVEditorState.phone, rx.el.p(CVEditorState.phone)),
        rx.cond(CVEditorState.city, rx.el.p(CVEditorState.city)),
        rx.cond(
            CVEditorState.website,
            rx.el.p(CVEditorState.website, class_name="break-all"),
        ),
        class_name="mt-5 flex flex-col gap-1 text-xs leading-5",
    )


def preview_summary() -> rx.Component:
    return rx.cond(
        CVEditorState.summary,
        rx.el.section(
            rx.el.h2(
                "Profil",
                class_name="mb-2 text-xs font-bold uppercase tracking-[0.14em]",
            ),
            rx.el.p(
                CVEditorState.summary,
                class_name="text-xs leading-5 text-[#586374]",
            ),
            class_name="mt-6",
        ),
    )


def preview_entry(item: dict[str, str]) -> rx.Component:
    return rx.el.article(
        rx.el.div(
            rx.el.h3(
                item["title"], class_name="text-xs font-semibold text-[#17283F]"
            ),
            rx.cond(
                item["period"],
                rx.el.span(
                    item["period"],
                    class_name="shrink-0 text-[9px] text-[#737B82]",
                ),
            ),
            class_name="flex flex-wrap items-start justify-between gap-x-3 gap-y-1",
        ),
        rx.cond(
            item["organization"],
            rx.el.p(
                item["organization"],
                class_name="mt-1 text-[10px] font-medium text-[#586374]",
            ),
        ),
        rx.cond(
            item["details"],
            rx.el.p(
                item["details"],
                class_name="mt-1 text-[10px] leading-4 text-[#626A72]",
            ),
        ),
        class_name="mb-3",
    )


def preview_sections() -> rx.Component:
    return rx.el.div(
        rx.foreach(
            CVEditorState.sections,
            lambda item: rx.el.section(
                rx.el.h2(
                    item["label"],
                    class_name="mb-3 border-b border-[#E7E0D5] pb-1.5 text-[10px] font-bold uppercase tracking-[0.13em] text-[#17283F]",
                ),
                preview_entry(item),
                class_name="mt-5",
            ),
        ),
    )


def modern_preview() -> rx.Component:
    return rx.el.div(
        rx.el.aside(
            rx.el.div(
                rx.cond(
                    CVEditorState.photo_filename,
                    rx.image(
                        src=rx.get_upload_url(CVEditorState.photo_filename),
                        class_name="h-20 w-20 rounded-full object-cover",
                    ),
                    rx.el.div(
                        rx.icon(
                            "user-round", class_name="h-8 w-8 text-white/60"
                        ),
                        class_name="flex h-20 w-20 items-center justify-center rounded-full bg-white/10",
                    ),
                ),
                preview_name(
                    "mt-5 text-xl font-semibold leading-tight text-white"
                ),
                rx.el.p(
                    CVEditorState.job_title,
                    class_name="mt-2 text-xs font-medium text-[#D8B1A5]",
                ),
                preview_contact(),
                class_name="p-6",
            ),
            class_name="w-[34%] shrink-0 bg-[#17283F] px-1 py-2 text-white",
        ),
        rx.el.div(
            preview_summary(),
            preview_sections(),
            class_name="flex-1 p-7",
        ),
        class_name="flex min-h-[680px] bg-white text-[#17283F]",
    )


def classic_preview() -> rx.Component:
    return rx.el.div(
        rx.el.header(
            preview_name(
                "font-serif text-2xl font-bold tracking-wide text-[#17283F]"
            ),
            rx.el.p(
                CVEditorState.job_title,
                class_name="mt-2 font-serif text-sm italic text-[#586374]",
            ),
            preview_contact(),
            class_name="border-b-2 border-[#17283F] px-7 py-8 text-center",
        ),
        rx.el.div(
            preview_summary(),
            preview_sections(),
            class_name="px-8 py-6 font-serif",
        ),
        class_name="min-h-[680px] bg-white text-[#17283F]",
    )


def elegant_preview() -> rx.Component:
    return rx.el.div(
        rx.el.header(
            preview_identity(),
            preview_contact(),
            class_name="border-b border-[#E8DED6] bg-[#FCF8F4] px-7 py-7",
        ),
        rx.el.div(
            rx.el.div(class_name="mb-5 h-1 w-16 bg-[#D77B67]"),
            preview_summary(),
            preview_sections(),
            class_name="px-7 py-6",
        ),
        class_name="min-h-[680px] bg-[#FFFEFC] text-[#17283F]",
    )


def minimal_preview() -> rx.Component:
    return rx.el.div(
        rx.el.header(
            preview_name(
                "text-2xl font-light lowercase tracking-wide text-[#17283F]"
            ),
            rx.el.p(
                CVEditorState.job_title,
                class_name="mt-2 text-xs font-light text-[#586374]",
            ),
            preview_contact(),
            class_name="px-8 py-9",
        ),
        rx.el.div(
            rx.el.div(class_name="h-px bg-[#E5E5E2]"),
            preview_summary(),
            preview_sections(),
            class_name="px-8 py-5",
        ),
        class_name="min-h-[680px] bg-white text-[#17283F]",
    )


def creative_preview() -> rx.Component:
    return rx.el.div(
        rx.el.header(
            rx.el.div(
                preview_name(
                    "text-2xl font-black uppercase tracking-tight text-[#17283F]"
                ),
                rx.el.p(
                    CVEditorState.job_title,
                    class_name="mt-2 text-xs font-semibold text-[#B86251]",
                ),
                preview_contact(),
                class_name="relative z-10 px-7 py-7",
            ),
            rx.el.div(
                class_name="absolute left-0 top-0 h-full w-2 bg-[#D77B67]"
            ),
            class_name="relative overflow-hidden bg-[#F6E8E1]",
        ),
        rx.el.div(
            rx.el.div(class_name="mb-5 h-1.5 w-14 rounded-full bg-[#17283F]"),
            preview_summary(),
            preview_sections(),
            class_name="px-7 py-6",
        ),
        class_name="min-h-[680px] bg-white text-[#17283F]",
    )


def cv_preview_a4() -> rx.Component:
    return rx.el.div(
        rx.match(
            CVEditorState.template_code,
            ("moderne", modern_preview()),
            ("classique", classic_preview()),
            ("elegant", elegant_preview()),
            ("minimaliste", minimal_preview()),
            ("creatif", creative_preview()),
            modern_preview(),
        ),
        class_name="mx-auto aspect-[210/297] w-full max-w-[560px] overflow-hidden border border-[#DDD8D0] bg-white text-left",
    )
