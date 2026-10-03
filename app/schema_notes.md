# Phase schéma uniquement

Aucune session, requête, création de table, migration ou insertion n'est exécutée par ces fichiers. Les modèles sont importés au démarrage pour rendre leur métadonnée disponible au gestionnaire de migrations. Le plan reste inchangé. Le branchement de connexion obligatoire reste isolé du schéma : il n'effectue aucune requête ni attribution de rôle. L'attribution effective des rôles reste hors de cette phase.

## Identité et intégrité

- `UserAccount.sub` est la clé primaire unique et l'identité OIDC stable. Email et nom ne servent jamais de clé d'identité. Le rôle par défaut est `member`, les seules valeurs permises étant `member` et `admin`.
- Chaque CV référence son propriétaire par `sub` et un modèle du catalogue. Un achat référence le couple `(cv_id, owner_sub)` : la base interdit donc un achat associé au CV d'un autre propriétaire.
- Les suppressions de références sont restreintes : aucune suppression en cascade ne détruit silencieusement une commande. La politique de suppression des CV achetés sera définie dans la phase fonctionnelle.
- Dates avec fuseau horaire et valeurs initiales côté serveur. `updated_at` est renouvelé par les écritures SQLAlchemy ; aucune prétention à un déclencheur serveur pour les écritures SQL externes.

## Contenu et catalogue

- `information` est un objet JSONB, `sections` un tableau JSONB ordonné de rubriques répétables, avec numéro de version du schéma. Les valeurs JSON sont récursivement typées ; aucun partage de valeurs mutables par défaut.
- Les futures rubriques pourront contenir un identifiant stable, leur type, titre et liste ordonnée d'entrées. Les formes internes seront validées par l'éditeur ; cette phase contraint uniquement les conteneurs objet/tableau en base.
- Lors d'une modification profonde, remplacer le conteneur JSON complet ou signaler explicitement sa modification à SQLAlchemy. Les mutations imbriquées ne sont pas automatiquement suivies.
- Le catalogue définit exactement Moderne, Classique, Élégant, Minimaliste et Créatif. La clé primaire et la contrainte sur les codes empêchent doublons et sixième modèle. Chaque modèle possède son indicateur d'activation. Les cinq lignes seront insérées après migration, pas dans cette phase.

## Tarif et achats de démonstration

- Le tarif premium est un singleton (`id = 1`), exclusivement en DZD. Montants décimaux exacts à deux décimales, non négatifs. La valeur technique initiale de zéro n'est pas un tarif commercial validé.
- Une commande contient une copie du prix au moment de sa création, sans dépendance au tarif courant, ainsi qu'un statut `pending`, `confirmed` ou `cancelled`, et un indicateur contraint à la démonstration. Aucun champ de carte bancaire.
- Le prix figé ne change pas lorsqu'un administrateur modifie le tarif. L'interdiction de modifier manuellement le prix d'une commande existante sera portée par les futures mutations serveur ; le schéma ne fournit pas un déclencheur d'immutabilité.

## Bootstrap administrateur après migration

Le verrou est un singleton dont la clé primaire vaut obligatoirement 1. Il référence le `sub` du gagnant et ne peut contenir qu'une attribution initiale. Il ne faut pas préinsérer ce verrou.

Le futur raccordement à la connexion devra créer/retrouver le membre et tenter l'insertion du verrou via un insert avec gestion atomique du conflit, dans la même transaction que l'attribution du rôle. Seule la transaction qui insère effectivement le verrou pourra promouvoir son utilisateur à `admin`. Les autres conserveront `member`. Un rollback devra annuler à la fois verrou et promotion ; aucun test de type compter les utilisateurs puis promouvoir.

La contrainte garantit l'unicité du gagnant concurrent, mais n'exécute pas elle-même une promotion. Le raccordement n'est volontairement pas implémenté avant migration. Les futurs événements administratifs devront porter un `auth=` callable serveur fondé sur le rôle persistant, jamais sur une donnée fournie par le client.
