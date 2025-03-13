config = {
    'environnement' :{
        'token':'',
        'api':''
    },
    'notificationMax': 25,
    'acteurType':'SI',
    'statusMinimal':'IN_PROGRESS',
    'statusMaximal':'DONE',
    'NombreRetry': 5,
    'header':{
        'editorName':'SI_XYZ',
        'applicationName':'serveur_SI',
        'softwareVersion':'1.0.1'
    },
    'demarches' :[{
        'demarcheNom':'CERTDC',
        'clientId':'',
        'clientSecret':'',
        'dossierDeTelechargement':'data/file/download/CERTDC/',
    },
    {
        'demarcheNom':'EtatCivil',
        'clientId':'',
        'clientSecret':'',
        'dossierDeTelechargement':'data/file/download/EtatCivil/',
    }],
}