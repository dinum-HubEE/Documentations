# Script de récupération des pièces jointes

Ce script Python est conçu pour les **Services Instructeurs (SI)** afin de simplifier et optimiser la récupération des télédossiers depuis la plateforme HUBEE jusqu'à un répertoire cible.

## Fonctionnalités HUBEE supportées
- Récupération des PJs du télédossier
- Changement de statut
- Acquittement des events
- Récupération des events `SENDING_MESSAGE`
- Récupération des events `ATTACH_DEPOSIT`
- Récupération des events ``STATUS_UPDATE`

## Structure du projet
 - `api.py` contient toutes les requêtes API
 - `hubee.py` contient la logique d'utilisation de l'API
 - `config.py` contient la configuration à modifier

## Prérequis
**Python** >= 3.10

## Installation
```bash
# Installation avec pip depuis le répertoire du projet
pip install -e .

# Ou installation directe des dépendances
pip install requests
```

## Lancement
Dans votre environnement virtuel, faire:
```bash
python3 hubee.py
```

## Configuration
- la configuration est disponible dans le fichier `config.py`

## Utilisation d'une ou plusieurs démarches
 - Il est possible d'utiliser une ou plusieurs démarches, vous devez paramétrer dans le fichier de configuration afin d'ajouter dans l'objet credentials les informations liées à une ou plusieurs démarches :
```python
{
    'demarcheName':'nomDeLaDemarche',
    'clientId':'votreClientId',
    'clientSecret':'votreClientSecret',
    'dossierDeTelechargement':'data/file/download/nomDeLaDemarche/',
}
```

### Environnement
```python
'environnement' :{
    'token':'url pour le TOKEN',
    'api':'url de l'API'
}
```
### Credentials
- Vos identifiants sont disponibles sur le portail HUBEE
- il y a un couple différent ClientId/ClientSecret par démarche
```python
{
    'clientId':'votreClientId',
    'clientSecret':'votreClientSecret',
}
```

### Récupération des notifications
- vous récupérez les notifications par lot de 25 par défaut, merci de ne pas toucher à cette valeur sans raison
```python
{
    'nombreDeNotifications':'25'
}
```

### Utilisation des statuts
- suivant la démarche vous devez changer les statuts à mettre sur le télédossier
```python
{
    'statusMinimal':'IN_PROGRESS',   -> il peut être SENT, SI_RECEIVED ou IN_PROGRESS
    'statusMaximal':'DONE'           -> il doit être DONE ou REFUSED
}
```

### Retry
- En cas d'erreur un retry va rejouer la requête par défaut 5 fois. Ne pas toucher à cette valeur sans raison
```python
{
    'NombreRetry': 5
}
```

### Dossier de téléchargement
- À la réception d'un télédossier, les PJs iront directement dans le répertoire de sortie, il est possible de paramétrer un répertoire différent pour chaque démarche
```python
{
    'dossierDeTelechargement':'data/file/download/nomDeLaDemarche/'
}
```

### Header
- Pour identifier chaque requête, vous devez renseigner les éléments avec vos informations :
```python
    'header':{
        'editorName':'SI_XYZ',            -> nom de votre organisation, par exemple COMMUNE X
        'applicationName':'script_HUBEE_DINUM',   -> ne pas toucher si vous utilisez ce script
        'softwareVersion':'1.0.1'         -> version de votre logiciel
    },
```
