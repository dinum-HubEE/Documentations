from pathlib import Path

from api import HubeeAPI


def process_hubee_telefolders(
    client_id: str, client_secret: str, download_dir: Path
) -> None:
    hubee_api = HubeeAPI()
    token: str = hubee_api.get_access_token(client_id, client_secret)
    notifications: dict = hubee_api.get_notifications(token)

    if len(notifications) == 0:
        print("Il n'y a pas de notification")
        return

    for notification in notifications:
        print("Traitement de la notification:", notification["id"])
        # print(notification)
        # traitement d'une notification
        if notification["eventId"] is None:
            case = hubee_api.get_case(token, notification["caseId"])

            for PJ in case["attachments"]:
                hubee_api.download_case_attachment(
                    token,
                    notification["caseId"],
                    PJ["id"],
                    PJ["fileName"],
                    case["externalId"],
                    download_dir,
                )

            hubee_api.create_status_event(
                token,
                notification["caseId"],
                hubee_api.config["status_minimal"],
            )
            hubee_api.create_status_event(
                token,
                notification["caseId"],
                hubee_api.config["status_maximal"],
            )
            hubee_api.delete_notification(token, notification["id"])
        else:
            if notification["eventStatus"] == "RECEIVED":
                hubee_api.delete_notification(token, notification["id"])

            else:
                event = hubee_api.get_event(
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
                        case = hubee_api.get_case(token, notification["caseId"])

                        for PJ in event["attachments"]:
                            # téléchargement des Pjs de l'event
                            hubee_api.download_event_attachment(
                                token,
                                notification["caseId"],
                                notification["eventId"],
                                PJ["id"],
                                PJ["fileName"],
                                case["externalId"],
                                download_dir,
                            )

                        # changement des status du case et création d'events
                        hubee_api.create_status_event(
                            token,
                            notification["caseId"],
                            hubee_api.config["status_minimal"],
                        )
                        hubee_api.create_status_event(
                            token,
                            notification["caseId"],
                            hubee_api.config["status_maximal"],
                        )
                    case _:
                        print("erreur lors de la récupération de l'event")

                hubee_api.update_event_status(
                    token,
                    notification["caseId"],
                    notification["eventId"],
                    "RECEIVED",
                )

    process_hubee_telefolders(client_id, client_secret, download_dir)


# Lecture de la configuration depuis HubeeAPI
hubee_api = HubeeAPI()

for process in hubee_api.config["demarches"]:
    print("Traitement de la démarche: ", process["demarche_nom"])
    process_hubee_telefolders(
        process["client_id"],
        process["client_secret"],
        process["dossier_telechargement"],
    )
