from pathlib import Path

from api import (
    get_access_token,
    get_notifications,
    get_case,
    download_case_attachment,
    create_status_event,
    delete_notification,
    get_event,
    download_event_attachment,
    update_event_status,
)
from config import config


def process_hubee_telefolders(client_id: str, client_secret: str, download_dir: Path) -> None:
    token = get_access_token(config["NombreRetry"], client_id, client_secret)
    notifications = get_notifications(config["NombreRetry"], token)

    if len(notifications) > 0:
        for notification in notifications:
            print("Traitement de la notification:", notification["id"])
            # print(notification)
            # traitement d'une notification
            if notification["eventId"] is None:
                case = get_case(config["NombreRetry"], token, notification["caseId"])

                for PJ in case["attachments"]:
                    download_case_attachment(
                        config["NombreRetry"],
                        token,
                        notification["caseId"],
                        PJ["id"],
                        PJ["fileName"],
                        case["externalId"],
                        download_dir,
                    )

                create_status_event(
                    config["NombreRetry"],
                    token,
                    notification["caseId"],
                    config["statusMinimal"],
                )
                create_status_event(
                    config["NombreRetry"],
                    token,
                    notification["caseId"],
                    config["statusMaximal"],
                )
                delete_notification(config["NombreRetry"], token, notification["id"])
            else:
                if notification["eventStatus"] == "RECEIVED":
                    delete_notification(config["NombreRetry"], token, notification["id"])

                else:
                    event = get_event(
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
                            case = get_case(
                                config["NombreRetry"], token, notification["caseId"]
                            )

                            for PJ in event["attachments"]:
                                # téléchargement des Pjs de l'event
                                download_event_attachment(
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
                            create_status_event(
                                config["NombreRetry"],
                                token,
                                notification["caseId"],
                                config["statusMinimal"],
                            )
                            create_status_event(
                                config["NombreRetry"],
                                token,
                                notification["caseId"],
                                config["statusMaximal"],
                            )
                        case _:
                            print("erreur lors de la récupération de l'event")

                    update_event_status(
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
