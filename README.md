![Hubee logo](https://global-uploads.webflow.com/62987c69557994988d440d3c/629e2185dc21ae5084313260_logo_hubee%20(002)-p-1080.png)





# Projet HUBEE

## Nous contacter
- Contact : contact@hubee.numerique.gouv.fr

## Documentations
- [Documentations Fonctionnelles](https://github.com/dinum-HubEE/Documentations/releases/latest/download/DocumentationsFonctionnelles.zip)
- [Documentations Techniques](https://github.com/dinum-HubEE/Documentations/releases/latest/download/DocumentationsTechniques.zip)

## Contrat d'interface
  
### Swagger
Pour les opérateurs de services en ligne :
- [Folder](https://github.com/dinum-HubEE/Documentations/releases/latest/download/swagger.zip)
- [Subscriptions](https://github.com/dinum-HubEE/Documentations/releases/latest/download/swagger.zip)

Pour les services instructeurs :
- [Folder](https://github.com/dinum-HubEE/Documentations/releases/latest/download/swagger.zip)

Outil de prévisualisation du swagger - [Swagger Editor](https://editor.swagger.io/)

## Valise Générique

- [Valise Générique](https://github.com/dinum-HubEE/Documentations/releases/latest/download/valiseGenerique.zip)
- [Postman](https://www.postman.com/downloads/)
	- [Collection postman](https://github.com/dinum-HubEE/Documentations/tree/main/Documentations%20Techniques/valise_g%C3%A9n%C3%A9rique/COLLECTION)
	- [Environnement postman](https://github.com/dinum-HubEE/Documentations/tree/main/Documentations%20Techniques/valise_g%C3%A9n%C3%A9rique/ENVIRONNEMENT)


### Les environnements
|Environnement|API|TOKEN|PORTAIL|
|-|-|-|-|
|Production|||https://hubee.numerique.gouv.fr|
|recette|https://apibacasablehubee.imfr.cgi.com|https://apibacasablehubee.imfr.cgi.com/token|https://portailbacasablehubee.imfr.cgi.com/|
|preproduction|https://api.bas.hubee.numerique.gouv.fr|https://auth.bas.hubee.numerique.gouv.fr/oauth2/token|https://portail.bas.hubee.numerique.gouv.fr/|

### Démarches disponibles
|Démarche|ProcessCode|Opérateur de service en ligne|Destinataires|PJs autorisées|Type des PJs|
|-|-|-|-|-|-|
|Flux Bénéficiaires quotidiens RSA|RSABEI-RSABAI|CNAF|Conseils départementaux|application/xml|RSABEI<br>RSABAI|
|Flux Bénéficiaires exceptionnels RSA|RSABEX-RSABAX|CNAF|Conseils départementaux|application/xml|RSABEX<br>RSABAX|
|Flux Financiers mensuels RSA|RSAFIM|CNAF|Conseils départementaux|A venir||
|Flux Financiers annuels RSA|RSAFIX|CNAF|Conseils départementaux|A venir||
|Flux Créances Transférées RSA|RSACTM|CNAF|Conseils départementaux|A venir||
|Flux Instructions RSA|IRSACG-IRSDCG|CNAF|Conseils départementaux|A venir||
|Flux grossesses Cristal GRO|GRO|CNAF|Conseils départementaux|A venir||
|Flux grossesses image GED/SGR|SGR|CNAF|Conseils départementaux|A venir||
|Flux Bénéficiaires quotidiens RSA|MSABEI|CNAF|Conseils départementaux|A venir||
|Flux Bénéficiaires mensuels RSA|MSABEM|CNAF|Conseils départementaux|A venir||
|Flux Bénéficiaires exceptionnels RSA|MSABEX|CNAF|Conseils départementaux|A venir||
|Flux Financiers mensuels RSA|MSAFIM|CNAF|Conseils départementaux|A venir||
|Flux Bénéficiaires mensuels RSA|RSABEM-RSABAM|CNAF|Conseils départementaux|A venir||
|Flux simplification grossesses DSG|DSG|CNAF|Conseils départementaux|A venir||
|Récupération des coordonnees de contacts allocataires du RSA|ContactsAllocataires-BRSA|CNAF|Conseils départementaux|A venir||
|Certificat de décès électronique|CERTDC|DGS|Communes|A venir||
|Service National d’Accueil Téléphonique pour l’Enfance en Danger|SNATED|SNATED|Conseils départementaux|A venir||
|depotDossierPACS|depotDossierPACS|DILA|Communes|A venir||
|Demande d'acte d'Etat civil|EtatCivil|DILA|Communes|A venir||
|Recensement Citoyen Obligatoire|recensementCitoyen|DILA|Communes|A venir||
|Déclaration de Changement de Coordonnées|JeChangeDeCoordonnees|DILA|Communes|A venir||
