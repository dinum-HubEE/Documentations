
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

## utilisation de une ou plusieurs démarches
 - Il est possible d'utiliser une ou plusieurs démarches, vous devez paramétrer dans le fichier de configuration afin de rajouter dans l'objet credentials les informations liées à une ou plusieurs démarches :
```
{
    'demarcheName':'nomDeLaDemarche',
    'clientId':'votreClientId',
    'clientSecret':'votreClientSecret',
    'dossierDeTelechargement':'data/file/download/nomDeLaDemarche/',
}
```

### environnement
```
'environnement' :{
    'token':'url pour le TOKEN',
    'api':'url de l'API'
}
```
### credentials
- vos identifiants sont disponibles sur le portail HUBEE
- il y a un couple différent ClientId/ClientSecret par démarche
```
{
    'clientId':'votreClientId',
    'clientSecret':'votreClientSecret',
}
```

### récupération des notifications
- vous récupérez les notifications par lot de 25 par défaut, merci de ne pas toucher à cette valeur sans raison
```
{
    'nombreDeNotifications':'25'
}
```

### utilisation des statuts
- suivant la démarche vous devez changer les statuts à mettre sur le télédossier
```
{
    'statusMinimal':'IN_PROGRESS',   -> il peut être SENT, SI_RECEIVED ou IN_PROGRESS
    'statusMaximal':'DONE'           -> il doit être DONE ou REFUSED
}
```

### retry
- En cas d'erreur un retry va rejouer la requête par défaut 5 fois, ne pas toucher à cette valeur sans raison
```
{
    'NombreRetry': 5
}
```

### dossier de téléchargement
- à la réception d'un télédossier les Pjs iront directements dans le répertoire de sorti, il est possible de paramétrer un répertoire différent pour chaque démarche
```
{
    'dossierDeTelechargement':'data/file/download/nomDeLaDemarche/'
}
```

### header
- Pour identifier chaque requête, vous devez renseigner les éléments avec vos informations
```
    'header':{
        'editorName':'SI_XYZ',            -> nom de votre orgnaisation, par exemple COMMUNE X
        'applicationName':'serveur_SI',   -> nom de votre logiciel / serveur
        'softwareVersion':'1.0.1'         -> version de votre logiciel
    },
```
