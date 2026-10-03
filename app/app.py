import reflex as rx
import reflex_enterprise as rxe

from app.components.admin import admin_page
from app.states.admin_state import AdminState
from app.components.cv_account import my_cvs_page, profile_page
from app.components.cv_editor import cv_editor_page
from app.components.public_site import (
    about_content,
    contact_content,
    faq_content,
    home_content,
    models_content,
    privacy_content,
    pricing_content,
    site_layout,
    terms_content,
)
from app.models import Base
from app.states.public_site_state import PublicSiteState
from app.states.cv_editor_state import CVEditorState
from app.states.cv_library_state import CVLibraryState
from app.states.role_state import RoleState

schema_metadata = Base.metadata


@rxe.page(
    route="/",
    auth=False,
    title="CVPro — Créez un CV professionnel en quelques minutes",
    description="Créez un CV professionnel avec cinq modèles distincts, des conseils simples et une présentation claire de votre parcours.",
)
def index() -> rx.Component:
    return site_layout(home_content())


@rxe.page(
    route="/modeles",
    auth=False,
    title="Modèles de CV — CVPro",
    description="Découvrez les modèles Moderne, Classique, Élégant, Minimaliste et Créatif de CVPro.",
)
def models_page() -> rx.Component:
    return site_layout(models_content())


@rxe.page(
    route="/prix",
    auth=False,
    title="Prix — CVPro",
    description="Comparez l’offre gratuite et le tarif premium de démonstration de CVPro.",
)
def pricing_page() -> rx.Component:
    return site_layout(pricing_content())


@rxe.page(
    route="/a-propos",
    auth=False,
    title="À propos — CVPro",
    description="Découvrez l’approche de CVPro pour présenter un parcours professionnel de façon claire.",
)
def about_page() -> rx.Component:
    return site_layout(about_content())


@rxe.page(
    route="/contact",
    auth=False,
    title="Contact — CVPro",
    description="Informations de contact et d’assistance pour CVPro, actuellement en version de démonstration.",
)
def contact_page() -> rx.Component:
    return site_layout(contact_content())


@rxe.page(
    route="/faq",
    auth=False,
    title="Questions fréquentes — CVPro",
    description="Réponses aux questions sur les modèles, les tarifs et les fonctionnalités disponibles de CVPro.",
)
def faq_page() -> rx.Component:
    return site_layout(faq_content())


@rxe.page(
    route="/confidentialite",
    auth=False,
    title="Confidentialité — CVPro",
    description="Informations provisoires sur la confidentialité et les données personnelles pour CVPro.",
)
def privacy_page() -> rx.Component:
    return site_layout(privacy_content())


@rxe.page(
    route="/conditions",
    auth=False,
    title="Conditions d’utilisation — CVPro",
    description="Conditions provisoires et limites de cette version de démonstration CVPro.",
)
def conditions_page() -> rx.Component:
    return site_layout(terms_content())


@rxe.page(
    route="/creer",
    auth=False,
    title="Créer un CV — CVPro",
    description="Rédigez gratuitement votre CV, choisissez un modèle et prévisualisez-le au format A4.",
)
def create_cv_page() -> rx.Component:
    return cv_editor_page()


@rxe.page(
    route="/mes-cv",
    auth=True,
    title="Mes CV — CVPro",
    description="Reprenez et gérez les CV enregistrés dans votre espace CVPro.",
)
def my_cvs_route() -> rx.Component:
    return my_cvs_page()


@rxe.page(
    route="/profil",
    auth=True,
    title="Mon profil — CVPro",
    description="Consultez votre identité de connexion et gérez votre session CVPro.",
)
def profile_route() -> rx.Component:
    return profile_page()


@rxe.page(
    route="/admin",
    auth=True,
    title="Administration — CVPro",
)
def admin_route() -> rx.Component:
    return admin_page()


app = rxe.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(
            rel="preconnect",
            href="https://fonts.gstatic.com",
            cross_origin="",
        ),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap",
            rel="stylesheet",
        ),
    ],
)
