from api import (
    getToken,
    getNotification,
    getCase,
    getCasePJ,
    postEvent,
    deleteNotification,
    getEvent,
    getCaseEventPJ,
    patchEvent,
)
from config import config


def process_hubee_telefolders(client_id: str, client_secret: str, download_dir: str) -> None:
    token = getToken(config["NombreRetry"], client_id, client_secret)
    notifications = getNotification(config["NombreRetry"], token)

    if len(notifications) > 0:
        for notification in notifications:
            print("Traitement de la notification:", notification["id"])
            # print(notification)
            # traitement d'une notification
            if notification["eventId"] is None:
                case = getCase(config["NombreRetry"], token, notification["caseId"])

                for PJ in case["attachments"]:
                    getCasePJ(
                        config["NombreRetry"],
                        token,
                        notification["caseId"],
                        PJ["id"],
                        PJ["fileName"],
                        case["externalId"],
                        download_dir,
                    )

                postEvent(
                    config["NombreRetry"],
                    token,
                    notification["caseId"],
                    config["statusMinimal"],
                )
                postEvent(
                    config["NombreRetry"],
                    token,
                    notification["caseId"],
                    config["statusMaximal"],
                )
                deleteNotification(config["NombreRetry"], token, notification["id"])
            else:
                if notification["eventStatus"] == "RECEIVED":
                    deleteNotification(config["NombreRetry"], token, notification["id"])

                else:
                    event = getEvent(
                        config["NombreRetry"],
                        token,
                        notification["caseId"],
                        notification["eventId"],
                    )

                    match event["actionType"]:
                        case "STATUS_UPDATE":
                            # ceci est un event STATUS_UPDATE
                            print(
                                "caseNewStatus [",
                                event["caseNewStatus"],
                                "]  message  [",
                                event["message"],
                                "]",
                            )
                        case "SENDING_MESSAGE":
                            # ceci est un event SENDING_MESSAGE
                            print("message  [", event["message"], "]")
                        case "ATTACH_DEPOSIT":
                            # ceci est un event ATTACH_DEPOSIT
                            case = getCase(
                                config["NombreRetry"], token, notification["caseId"]
                            )

                            for PJ in event["attachments"]:
                                # téléchargement des Pjs de l'event
                                getCaseEventPJ(
                                    config["NombreRetry"],
                                    token,
                                    notification["caseId"],
                                    notification["eventId"],
                                    PJ["id"],
                                    PJ["fileName"],
                                    case["externalId"],
                                    download_dir,
                                )

                            # changement des status du case et création d'events
                            postEvent(
                                config["NombreRetry"],
                                token,
                                notification["caseId"],
                                config["statusMinimal"],
                            )
                            postEvent(
                                config["NombreRetry"],
                                token,
                                notification["caseId"],
                                config["statusMaximal"],
                            )
                        case _:
                            print("erreur lors de la récupération de l'event")

                    patchEvent(
                        config["NombreRetry"],
                        token,
                        notification["caseId"],
                        notification["eventId"],
                        "RECEIVED",
                    )

        process_hubee_telefolders(client_id, client_secret, download_dir)
    else:
        print("Il n'y a pas de notification")


for process in config["demarches"]:
    print("Traitement de la démarche: ", process["demarcheNom"])
    process_hubee_telefolders(
        process["clientId"], process["clientSecret"], process["dossierDeTelechargement"]
    )
