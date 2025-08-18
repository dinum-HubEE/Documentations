# Script de récupération des pièces jointes

Ce script Python est conçu pour les **Services Instructeurs (SI)** afin de simplifier et optimiser la récupération des télédossiers depuis la plateforme HUBEE jusqu'à un répertoire cible.

## 🚀 Fonctionnalités HUBEE supportées

- Récupération des pièces jointes du télédossier
- Changement de statut
- Acquittement des events
- Récupération des events `SENDING_MESSAGE`
- Récupération des events `ATTACH_DEPOSIT`
- Récupération des events `STATUS_UPDATE`

## 📁 Structure du projet

- `main.py`: script principal, contient la logique d'utilisation de l'API
- `config.toml`: fichier de configuration TOML à modifier
- `api.py`: contient toutes les requêtes API

## ⚙️ Prérequis

**Python** >= 3.10

## 📦 Installation

```bash
# Installation avec pip depuis le répertoire du projet
pip install -e .

# Ou installation directe des dépendances
pip install requests
```

## 🚀 Lancement

Dans votre environnement virtuel, faire:
```bash
python3 main.py
```

## ⚙️ Configuration

Le script utilise un fichier de configuration au format TOML (`config.toml`) pour définir tous les paramètres nécessaires à son fonctionnement. Ce fichier doit être placé dans le même répertoire que le script.

**Étapes de configuration :**

1. **Editer le fichier** `config.toml` dans le répertoire du script
2. **Configurer les URLs de l'environnement** `api_url` et `token_url`
3. **Configurer vos credentials** pour chaque démarche
4. **Ajuster les paramètres** selon vos besoins (statuts, dossiers, etc.)

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

### 📨 Configuration de la récupération des notifications

Le script récupère les notifications par lot de 25 par défaut. Ne pas toucher à cette valeur sans raison :
```toml
notification_max = 25
```

### 🔄  Configuration du retry

En cas d'erreur de communication avec l'API Hubee, le script va retenter de communiquer avec l'API un nombre de fois défini par `nombre_retry` dans la configuration. Par défaut, cette valeur est de 5, il est déconseillé de le modifier.
```toml
nombre_retry = 5
```

### 📋 Header

Pour identifier chaque requête, vous devez renseigner les éléments avec vos informations :

```toml
[header]
editor_name = "SI_XYZ"                    # nom de votre organisation, par exemple COMMUNE X
application_name = "script_HUBEE_DINUM"   # ne pas toucher si vous utilisez ce script
software_version = "1.0.1"                # version de votre logiciel
```

## 🤝 Contribution

Avant de contribuer au dépôt et de faire une PR, il est nécessaire de formater, linter et trier les imports avec [Ruff](https://docs.astral.sh/ruff/) avant de commiter :

```bash
ruff check --fix . && ruff format .
```
