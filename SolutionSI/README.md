# Script de récupération des pièces jointes

Ce script Python est conçu pour les **Services Instructeurs (SI)** afin de permettre la récupération des télédossiers depuis la plateforme HUBEE jusqu'à un répertoire local.

## 📁 Structure du projet

Le projet est organisé en quatre fichiers principaux :

- **`main.py`** : **À exécuter**. Script principal qui lance le téléchargement des pièces jointes pour vos démarches HUBEE configurées.

- **`config.toml`** : **À modifier**. Fichier de configuration où vous définissez vos démarches, credentials et paramètres.

- **`pyproject.toml`** : **Ne pas toucher**. Fichier de configuration du projet Python qui définit les dépendances et métadonnées.

- **`hubee_client.py`** : **Ne pas toucher**. Module technique qui gère les interactions avec l'API HUBEE via la classe `HubeeClient`.

## 🚀 Usage

### Prérequis

**Python** >= 3.10

### Installation et exécution

```bash
# Créer et activer un environnement virtuel
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# Installer les dépendances
pip install -e .

# Lancer le script
python3 main.py
```

**Note :** Vous pouvez aussi utiliser [uv](https://docs.astral.sh/uv/) ou [Poetry](https://python-poetry.org/) pour gérer automatiquement l'environnement virtuel et les dépendances.

## ⚙️ Configuration

Le script utilise un fichier de configuration au format TOML (`config.toml`) pour définir tous les paramètres nécessaires à son fonctionnement. Ce fichier doit être placé dans le même répertoire que le script.

**Étapes de configuration :**

1. **Editer le fichier** `config.toml` dans le répertoire du script
2. **Configurer les URLs de l'environnement** `api_url` et `token_url`
3. **Configurer vos credentials** pour chaque démarche

### 🌍 Configuration de l'environnement

**Documentation complète des environnements :** [Documentations HUBEE](https://github.com/dinum-HubEE/Documentations)

Le fichier `config.toml` est configuré par défaut pour l'environnement de **préproduction**.
Pour utiliser un autre environnement, modifiez les URLs suivantes :

```toml
[environnement]
api_url = "https://api.bas.hubee.numerique.gouv.fr"        # URL de l'API (préproduction par défaut)
token_url = "https://auth.bas.hubee.numerique.gouv.fr/oauth2/token"  # URL pour l'authentification (préproduction par défaut)
```

### 🔧 Utilisation d'une ou plusieurs démarches

Il est possible d'utiliser une ou plusieurs démarches. Chaque démarche peut avoir ses propres paramètres de configuration et des workflows de statuts personnalisés selon vos besoins métier. **Les statuts sont automatiquement validés** grâce à l'enum `HubeeStatus` qui garantit la conformité avec l'API HUBEE.

**Structure de configuration pour chaque démarche :**
```toml
[[demarches]]
demarche_nom = "nomDeLaDemarche"
client_id = "votreClientId"
client_secret = "votreClientSecret"
dossier_telechargement = "./downloads/MaDemarche/"
statut_minimal = "IN_PROGRESS"   # statut initial : SENT, SI_RECEIVED ou IN_PROGRESS
statut_maximal = "DONE"          # statut final : DONE ou REFUSED
```

**Paramètres expliqués :**
- **`demarche_nom`** : Nom de la démarche HUBEE (consultez la [documentation HUBEE](https://github.com/dinum-HubEE/Documentations) pour la liste complète des démarches disponibles)
- **`client_id`** et **`client_secret`** : Identifiants de connexion (un couple différent par démarche)
- **`dossier_telechargement`** : Répertoire local où seront stockées les pièces jointes (PJs) des télédossiers
- **`statut_minimal`** : Statut intermédiaire à appliquer au télédossier avant traitement
- **`statut_maximal`** : Statut final à appliquer au télédossier après traitement

Pour obtenir vos `client_id` et `client_secret` :

1. **Consultez** la [documentation HUBEE](https://github.com/dinum-HubEE/Documentations) pour identifier le bon portail selon votre environnement (recette, préproduction, production)
2. **Connectez-vous** au portail approprié
3. **Accédez** au menu « Gestion des abonnements »
4. **Sélectionnez** la démarche concernée
5. **Récupérez** les credentials depuis la fiche de la démarche, modalité d'accès "API" 

**Exemple de configuration complète :**
```toml
[[demarches]]
demarche_nom = "CERTDC"
client_id = "votreClientId"
client_secret = "votreClientSecret"
dossier_telechargement = "./downloads/CERTDC/"
statut_minimal = "IN_PROGRESS"
statut_maximal = "DONE"

[[demarches]]
demarche_nom = "EtatCivil"
client_id = "votreClientId"
client_secret = "votreClientSecret"
dossier_telechargement = "./downloads/EtatCivil/"
statut_minimal = "SI_RECEIVED"   # exemple de statut intermédiaire différent
statut_maximal = "DONE"
```

### 📋 Header

Pour identifier chaque requête, vous devez renseigner le nom de votre organisation :
```toml
[header]
editor_name = "SI_XYZ"                    # nom de votre organisation, par exemple COMMUNE X
application_name = "script_HUBEE_DINUM"   # ne pas toucher si vous utilisez ce script
software_version = "2.0.0"                # ne pas toucher si vous utilisez ce script
```

### ⚙️ Autres configurations

D'autres paramètres peuvent être configurés, mais il est déconseillé de changer ces valeurs.

Le script récupère les notifications par lot de 25 par défaut :
```toml
notification_max = 25
```

En cas d'erreur de communication avec l'API Hubee, le script va retenter de communiquer avec l'API un nombre de fois défini par `nombre_retry` dans la configuration. Par défaut, cette valeur est de 5 :
```toml
nombre_retry = 5
```

## 🤝 Contribuer à ce script

Avant de contribuer au dépôt et de faire une PR, il est nécessaire de formater, linter et trier les imports avec [Ruff](https://docs.astral.sh/ruff/) avant de commiter :

```bash
ruff check --fix . && ruff format .
```

## 📞 Support et Contact

Pour toute question ou problème avec ce script, vous pouvez contacter l'équipe HUBEE :

**Email :** contact@hubee.numerique.gouv.fr
