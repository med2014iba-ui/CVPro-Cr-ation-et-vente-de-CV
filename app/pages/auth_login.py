import reflex as rx

import os
from collections.abc import Sequence
from reflex_enterprise.auth import AuthUserState
from app.states.login_redirect_state import LoginRedirectState

_PROVIDER_NAME = os.environ.get("OIDC_PROVIDER_NAME", "")
_LOGIN_LABEL = (
    f"Continue with {_PROVIDER_NAME}" if _PROVIDER_NAME else "Sign in"
)


def _provider_buttons(providers: Sequence) -> list[rx.Component]:
    buttons: list[rx.Component] = []
    for provider in providers:
        buttons.append(
            provider.get_login_button(
                rx.el.button(
                    _LOGIN_LABEL,
                    class_name="w-full rounded-xl bg-[#17283F] px-6 py-4 font-medium text-white hover:bg-[#263D58] focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-[#D77B67]",
                )
            )
        )
    return buttons


def login_page(*, providers: Sequence, **context) -> rx.Component:
    return rx.fragment(
        rx.el.main(
            rx.el.div(
                rx.icon(
                    "file-user",
                    class_name="mx-auto mb-6 h-9 w-9 text-[#D77B67]",
                ),
                rx.el.h1(
                    "CVPro",
                    class_name="mb-3 text-center text-3xl font-semibold text-[#17283F]",
                ),
                rx.el.p(
                    "Connectez-vous pour continuer.",
                    class_name="mb-8 text-center text-sm text-[#586374]",
                ),
                *_provider_buttons(providers),
                class_name="w-full max-w-md rounded-2xl border border-[#E5DFD5] bg-white p-10",
            ),
            class_name="flex min-h-dvh items-center justify-center bg-[#F8F5EF] px-6 font-['Inter'] text-[#17283F]",
        ),
        rx.cond(
            AuthUserState.provider_name != "",
            rx.el.div(on_mount=LoginRedirectState.continue_to_app),
        ),
    )
