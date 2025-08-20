# Script de récupération des pièces jointes

Ce script Python est conçu pour les **Services Instructeurs (SI)** afin de permettre la récupération des télédossiers depuis la plateforme HUBEE jusqu'à un répertoire local cible.

## 🚀 Fonctionnalités HUBEE supportées

- Récupération des pièces jointes du télédossier
- Changement de statut
- Acquittement des events
- Récupération des events `SENDING_MESSAGE`
- Récupération des events `ATTACH_DEPOSIT`
- Récupération des events `STATUS_UPDATE`

## 📁 Structure du projet

Le projet est organisé en quatre fichiers principaux :

- **`main.py`** : **À exécuter**. Script principal qui lance le traitement des démarches HUBEE.

- **`config.toml`** : **À modifier**. Fichier de configuration où vous définissez vos URLs, credentials et paramètres.

- **`pyproject.toml`** : **Ne pas toucher**. Fichier de configuration du projet Python qui définit les dépendances et métadonnées.

- **`hubee_client.py`** : **Ne pas toucher**. Module technique qui gère les interactions avec l'API HUBEE via la classe `HubeeClient`.

## 🚀 Usage

### Prérequis

**Python** >= 3.10

### Lancement

**Gestionnaire de paquets** : Le script peut être exécuté de deux façons :
- **Méthode classique** : Avec pip et un environnement virtuel Python
- **Méthode moderne** : Avec [uv](https://docs.astral.sh/uv/) qui gère automatiquement les dépendances

#### Méthode 1 : Python classique

Cette méthode nécessite un environnement virtuel Python pour isoler les dépendances du projet :

```bash
# Installation des dépendances Python
pip install -e .

# Lancement du script Python
python3 main.py
```

#### Méthode 2 : Exécution directe

Cette méthode gère automatiquement l'environnement virtuel et les dépendances :

```bash
# Rendre le script exécutable
chmod +x main.py

# Lancer le script
./main.py
```

## ⚙️ Configuration

Le script utilise un fichier de configuration au format TOML (`config.toml`) pour définir tous les paramètres nécessaires à son fonctionnement. Ce fichier doit être placé dans le même répertoire que le script.

**Étapes de configuration :**

1. **Editer le fichier** `config.toml` dans le répertoire du script
2. **Configurer les URLs de l'environnement** `api_url` et `token_url`
3. **Configurer vos credentials** pour chaque démarche

### 🌍 Configuration de l'environnement

```toml
[environnement]
api_url = "url de l'API"
token_url = "url pour le TOKEN"
```

### 🔧 Utilisation d'une ou plusieurs démarches

Il est possible d'utiliser une ou plusieurs démarches. Chaque démarche peut avoir ses propres paramètres de configuration.

**Structure de configuration pour chaque démarche :**
```toml
[[demarches]]
demarche_nom = "nomDeLaDemarche"
client_id = "votreClientId"
client_secret = "votreClientSecret"
dossier_telechargement = "data/file/download/nomDeLaDemarche/"
statut_minimal = "IN_PROGRESS"   # statut initial : SENT, SI_RECEIVED ou IN_PROGRESS
statut_maximal = "DONE"          # statut final : DONE ou REFUSED
```

**Paramètres expliqués :**
- **`demarche_nom`** : Nom de la démarche HUBEE
- **`client_id`** et **`client_secret`** : Identifiants de connexion (un couple différent par démarche, disponibles sur le portail HUBEE)
- **`dossier_telechargement`** : Répertoire local où seront stockées les pièces jointes (PJs) des télédossiers
- **`statut_minimal`** : Statut intermédiare à appliquer au télédossier avant traitement
- **`statut_maximal`** : Statut final à appliquer au télédossier après traitement

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
statut_minimal = "SI_RECEIVED"   # exemple de statut initial différent
statut_maximal = "DONE"
```

Chaque démarche peut avoir des workflows de statuts différents selon vos besoins métier.

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

## 🤝 Contribution

Avant de contribuer au dépôt et de faire une PR, il est nécessaire de formater, linter et trier les imports avec [Ruff](https://docs.astral.sh/ruff/) avant de commiter :

```bash
ruff check --fix . && ruff format .
```
