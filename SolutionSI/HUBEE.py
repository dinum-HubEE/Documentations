from API import *
from config import *

def HUBEE_changementDeStatuts(NombreRetry, token, index):
  patchCase(NombreRetry, token, index["caseId"], config["statusMinimal"])
  postEvent(NombreRetry, token, index["caseId"], "HUBEE_NOTIFIED",config["statusMinimal"])
  patchCase(NombreRetry, token, index["caseId"], config["statusMaximal"])
  postEvent(NombreRetry, token, index["caseId"], config["statusMinimal"],config["statusMaximal"])

def HUBEE_recuperationTeledossier(clientId, clientSecret, repository):
  token = getToken(config["NombreRetry"], clientId, clientSecret)
  notification = getNotification(config["NombreRetry"], token)

  if(len(notification) > 0):

    for index in notification:
      # traitement d'une notification
      if(index["eventId"] == None):
        case = getCase(config["NombreRetry"], token, index["caseId"])

        for PJ in case["attachments"]:
          getCasePJ(config["NombreRetry"], token, index["caseId"], PJ["id"], PJ["fileName"], case["externalId"], repository)

        HUBEE_changementDeStatuts(config["NombreRetry"], token, index)
      else:
        event = getEvent(config["NombreRetry"], token, index["caseId"], index["eventId"])

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
              case = getCase(config["NombreRetry"], token, index["caseId"])

              for PJ in event["attachments"]:
                # téléchargement des Pjs de l'event
                getCaseEventPJ(config["NombreRetry"], token, index["caseId"], index["eventId"], PJ["id"], PJ["fileName"], case["externalId"], repository)

              # changement des status du case et création d'events
              HUBEE_changementDeStatuts(config["NombreRetry"], token, index)
            case _:
              print("erreur lors de la récupération de l'event")

          patchEvent(config["NombreRetry"], token, index["caseId"], index["eventId"], "RECEIVED")

      deleteNotification(config["NombreRetry"], token, index["id"])

    HUBEE_recuperationTeledossier(clientId, clientSecret, repository)
  else:
    print("Il n'y a pas de notification")

for process in config["credentials"]:
  print("Traitement de la démarche: ", process["demarcheName"])
  HUBEE_recuperationTeledossier(process["clientId"], process["clientSecret"], process["dossierDeTelechargement"])