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

- **`api.py`** : **Ne pas toucher**. Module technique qui gère les interactions avec l'API HUBEE.

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

Il est possible d'utiliser une ou plusieurs démarches. Vous devez paramétrer dans le fichier de configuration afin d'ajouter les informations liées à une ou plusieurs démarches, de la manière suivante :

```toml
[[demarches]]
demarche_nom = "nomDeLaDemarche"
client_id = "votreClientId"
client_secret = "votreClientSecret"
dossier_telechargement = "data/file/download/nomDeLaDemarche/"
```

Pour chaque démarche, il y a un couple différent `client_id` / `client_secret` à compléter.
Vos identifiants sont disponibles sur le portail HUBEE.

À la réception d'un télédossier, les pièces jointes (PJs) iront directement dans un répertore local de votre choix, défini par `dossier_telechargement`.
Il est possible de paramétrer un répertoire différent pour chaque démarche.

**Exemple de configuration :**
```toml
[[demarches]]
demarche_nom = "CERTDC"
client_id = "votreClientId"
client_secret = "votreClientSecret"
dossier_telechargement = "./downloads/CERTDC/"

[[demarches]]
demarche_nom = "EtatCivil"
client_id = "votreClientId"
client_secret = "votreClientSecret"
dossier_telechargement = "./downloads/EtatCivil/"
```

### 📊 Configuration de l'utilisation des statuts

Suivant la démarche, vous devez changer les statuts à mettre sur le télédossier :
```toml
statut_minimal = "IN_PROGRESS"   # il peut être SENT, SI_RECEIVED ou IN_PROGRESS
statut_maximal = "DONE"          # il doit être DONE ou REFUSED
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

Le script récupère les notifications par lot de 25 par défaut. Ne pas toucher à cette valeur sans raison :
```toml
notification_max = 25
```

En cas d'erreur de communication avec l'API Hubee, le script va retenter de communiquer avec l'API un nombre de fois défini par `nombre_retry` dans la configuration. Par défaut, cette valeur est de 5, il est déconseillé de le modifier.
```toml
nombre_retry = 5
```

## 🤝 Contribution

Avant de contribuer au dépôt et de faire une PR, il est nécessaire de formater, linter et trier les imports avec [Ruff](https://docs.astral.sh/ruff/) avant de commiter :

```bash
ruff check --fix . && ruff format .
```
