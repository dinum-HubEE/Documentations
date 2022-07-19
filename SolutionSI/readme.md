
# script de récupération des Pjs

## Description
Il s'agit d'un script qui permet d'automatiser la récupération des télédossiers depuis HUBEE jusqu'a un répertoire cible

## Fonctionnalitées HUBEE supportées
- Récupération des PJs du télédossier
- Changement de statut
- Acquittement des events
- Récupération des events SENDING_MESSAGE
- Récupération des events ATTACH_DEPOSIT
- Récupération des events STATUS_UPDATE

## Installation
 - Python >= v3.10
 - installer pip
 
## dependences
 - pip install requests
 
## lancement
 - python3 HUBEE.py

## fichiers
 - API.py contient toutes les requêtes API
 - HUBEE.py contient la logique d'utilisation de l'API
 - config.py contient la configuration à modifier

## configuration
- la configuration est disponible dans le fichier config.py

### environnement
- token: url pour le TOKEN
- api: url de l'API

### credentials
- vos identifiants sont disponibles sur le portail HUBEE
- il y a un couple différent ClientId/ClientSecret par démarche
- clientId: votre clientId de l'abonnement en question
- clientSecret: votre clientSecret de l'abonnement en question

### récupération des notifications
- par défaut vous récupérez les notifications par 25, merci de ne pas toucher à cette valeur sans raison
- nombreDeNotifications: nombre de notification à récupérer à chaque cycle

### utilisation des statuts
- suivant la démarche vous devez changer les statuts à mettre sur le télédossier
- statusMinimal: l'utilisation du premier statut, il peut être SENT, SI_RECEIVED ou IN_PROGRESS
- statusMaximal: l'utilisation du statut inal, il doit être DONE ou REFUSED

### retry
- En cas d'erreur un retry est en place pour rejouer la requête
- NombreRetry: par défaut à 5, ne pas toucher à cette valeur sans raison

### dossier de téléchargement
- à la réception d'un télédossier les Pjs iront directement dans le répertoire de sorti
- dossierDeTelechargement: vous devez renseigner le répertoire de sorti
