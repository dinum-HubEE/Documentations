from pathlib import Path

from api import HubeeAPI


def process_hubee_teledossier(
    hubee_api: HubeeAPI, client_id: str, client_secret: str, download_dir: Path
) -> None:
    token: str = hubee_api.get_access_token(client_id, client_secret)
    notifications: dict = hubee_api.get_notifications(token)

    if len(notifications) == 0:
        print("Il n'y a pas de notification.")
        return

    for notif in notifications:
        print("Traitement de la notification:", notif["id"])
        # print(notif)
        # traitement d'une notification
        if notif["eventId"] is None:
            case = hubee_api.get_case(token, notif["caseId"])

            for PJ in case["attachments"]:
                hubee_api.download_case_attachment(
                    token,
                    notif["caseId"],
                    PJ["id"],
                    PJ["fileName"],
                    case["externalId"],
                    download_dir,
                )

            hubee_api.create_status_event(
                token,
                notif["caseId"],
                hubee_api.config["statut_minimal"],
            )
            hubee_api.create_status_event(
                token,
                notif["caseId"],
                hubee_api.config["statut_maximal"],
            )
            hubee_api.delete_notification(token, notif["id"])
        else:
            if notif["eventStatus"] == "RECEIVED":
                hubee_api.delete_notification(token, notif["id"])

            else:
                event = hubee_api.get_event(
                    token,
                    notif["caseId"],
                    notif["eventId"],
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
                        case = hubee_api.get_case(token, notif["caseId"])

                        for PJ in event["attachments"]:
                            # téléchargement des Pjs de l'event
                            hubee_api.download_event_attachment(
                                token,
                                notif["caseId"],
                                notif["eventId"],
                                PJ["id"],
                                PJ["fileName"],
                                case["externalId"],
                                download_dir,
                            )

                        # changement des status du case et création d'events
                        hubee_api.create_status_event(
                            token,
                            notif["caseId"],
                            hubee_api.config["statut_minimal"],
                        )
                        hubee_api.create_status_event(
                            token,
                            notif["caseId"],
                            hubee_api.config["statut_maximal"],
                        )
                    case _:
                        print("erreur lors de la récupération de l'event")

                hubee_api.update_event_status(
                    token,
                    notif["caseId"],
                    notif["eventId"],
                    "RECEIVED",
                )

    process_hubee_teledossier(hubee_api, client_id, client_secret, download_dir)


def main():
    """Fonction principale du script."""
    # Lecture de la configuration depuis HubeeAPI
    hubee_api = HubeeAPI()

    for process in hubee_api.config["demarches"]:
        print("Traitement de la démarche: ", process["demarche_nom"])
        process_hubee_teledossier(
            hubee_api,
            process["client_id"],
            process["client_secret"],
            process["dossier_telechargement"],
        )


if __name__ == "__main__":
    main()
