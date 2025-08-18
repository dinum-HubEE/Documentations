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

- la configuration est disponible dans le fichier `config.toml`

## 🔧 Utilisation d'une ou plusieurs démarches

 - Il est possible d'utiliser une ou plusieurs démarches, vous devez paramétrer dans le fichier de configuration afin d'ajouter dans l'objet credentials les informations liées à une ou plusieurs démarches :
```toml
[[demarches]]
demarche_nom = "nomDeLaDemarche"
client_id = "votreClientId"
client_secret = "votreClientSecret"
dossier_telechargement = "data/file/download/nomDeLaDemarche/"
```

### 🌍 Environnement

```toml
[environnement]
token_url = "url pour le TOKEN"
api_url = "url de l'API"
```
### 🔑 Credentials

- Vos identifiants sont disponibles sur le portail HUBEE
- il y a un couple différent ClientId/ClientSecret par démarche
```toml
client_id = "votreClientId"
client_secret = "votreClientSecret"
```

### 📨 Récupération des notifications

- vous récupérez les notifications par lot de 25 par défaut, merci de ne pas toucher à cette valeur sans raison
```toml
notification_max = 25
```

### 📊 Utilisation des statuts

- suivant la démarche vous devez changer les statuts à mettre sur le télédossier
```toml
status_minimal = "IN_PROGRESS"   # il peut être SENT, SI_RECEIVED ou IN_PROGRESS
status_maximal = "DONE"          # il doit être DONE ou REFUSED
```

### 🔄 Retry

- En cas d'erreur un retry va rejouer la requête par défaut 5 fois. Ne pas toucher à cette valeur sans raison
```toml
nombre_retry = 5
```

### 📂 Dossier de téléchargement

- À la réception d'un télédossier, les PJs iront directement dans le répertoire de sortie, il est possible de paramétrer un répertoire différent pour chaque démarche
```toml
dossier_telechargement = "data/file/download/nomDeLaDemarche/"
```

### 📋 Header

- Pour identifier chaque requête, vous devez renseigner les éléments avec vos informations :
```toml
[header]
editor_name = "SI_XYZ"                    # nom de votre organisation, par exemple COMMUNE X
application_name = "script_HUBEE_DINUM"   # ne pas toucher si vous utilisez ce script
software_version = "1.0.1"               # version de votre logiciel
```

## 🤝 Contribution

Avant de contribuer au dépôt et de faire une PR, il est nécessaire de formater, linter et trier les imports avec [Ruff](https://docs.astral.sh/ruff/) avant de commiter :
```bash
ruff check --fix . && ruff format .
```
