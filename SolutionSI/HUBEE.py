from API import *
from config import *

def HUBEE_changementDeStatuts(NombreRetry, token, case):
  patchCase(NombreRetry, token, case["caseId"], config["statusMinimal"])
  postEvent(NombreRetry, token, case["caseId"], "HUBEE_NOTIFIED",config["statusMinimal"])
  patchCase(NombreRetry, token, case["caseId"], config["statusMaximal"])
  postEvent(NombreRetry, token, case["caseId"], config["statusMinimal"],config["statusMaximal"])

def HUBEE_recuperationTeledossier(clientId, clientSecret, repository):
  token = getToken(config["NombreRetry"], clientId, clientSecret)
  notifications = getNotification(config["NombreRetry"], token)

  if(len(notifications) > 0):

    for notification in notifications:
      print("Traitement de la notification:",notification["id"])
      # traitement d'une notification
      if(notification["eventId"] == None):
        case = getCase(config["NombreRetry"], token, notification["caseId"])

        for PJ in case["attachments"]:
          getCasePJ(config["NombreRetry"], token, notification["caseId"], PJ["id"], PJ["fileName"], case["externalId"], repository)

        HUBEE_changementDeStatuts(config["NombreRetry"], token, notification)
      else:
        event = getEvent(config["NombreRetry"], token, notification["caseId"], notification["eventId"])

        if(event["status"] == "SENT"):
          
          match event["actionType"]:
            case "STATUS_UPDATE":
              # ceci est un event STATUS_UPDATE
              print("caseNewStatus [", event["caseNewStatus"], "]  message  [", event["message"], "]")
            case "SENDING_MESSAGE":
              # ceci est un event SENDING_MESSAGE
              print("message  [", event["message"], "]")
            case "ATTACH_DEPOSIT":
              # ceci est un event ATTACH_DEPOSIT
              case = getCase(config["NombreRetry"], token, notification["caseId"])

              for PJ in event["attachments"]:
                # téléchargement des Pjs de l'event
                getCaseEventPJ(config["NombreRetry"], token, notification["caseId"], notification["eventId"], PJ["id"], PJ["fileName"], case["externalId"], repository)

              # changement des status du case et création d'events
              HUBEE_changementDeStatuts(config["NombreRetry"], token, notification)
            case _:
              print("erreur lors de la récupération de l'event")

          patchEvent(config["NombreRetry"], token, notification["caseId"], notification["eventId"], "RECEIVED")

      deleteNotification(config["NombreRetry"], token, notification["id"])

    HUBEE_recuperationTeledossier(clientId, clientSecret, repository)
  else:
    print("Il n'y a pas de notification")

for process in config["credentials"]:
  print("Traitement de la démarche: ", process["demarcheName"])
  HUBEE_recuperationTeledossier(process["clientId"], process["clientSecret"], process["dossierDeTelechargement"])
