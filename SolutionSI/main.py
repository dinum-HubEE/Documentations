#!/usr/bin/env -S uv run --script
# /// script
# dependencies = [
#     "requests",
# ]
# ///

from pathlib import Path

from api import HubeeAPI


def process_hubee_teledossier(
    hubee_api: HubeeAPI, client_id: str, client_secret: str, download_path: Path
) -> None:
    """Traite les télédossiers pour une démarche donnée.

    Effectue les opérations suivantes: récupération des notifications, téléchargement
    des pièces jointes, mise à jour des statuts et acquittement des events.

    Paramètres:
      - hubee_api: instance configurée de HubeeAPI
      - client_id: identifiant client de la démarche
      - client_secret: secret client de la démarche
      - download_path: répertoire cible pour enregistrer les pièces jointes pour la démarche
    """
    token: str = hubee_api.get_access_token(client_id, client_secret)
    notifications: dict = hubee_api.get_notifications(token)

    if len(notifications) == 0:
        print("Il n'y a pas de notification.")
        return

    for notif in notifications:
        print("Traitement de la notification [", notif["id"], "]")

        if notif["eventId"] is None:
            case = hubee_api.get_case(token, notif["caseId"])

            for PJ in case["attachments"]:
                hubee_api.download_case_attachment(
                    token,
                    notif["caseId"],
                    PJ["id"],
                    PJ["fileName"],
                    case["externalId"],
                    download_path,
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
                                download_path,
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

    process_hubee_teledossier(hubee_api, client_id, client_secret, download_path)


def main():
    """Fonction principale du script."""
    # Lecture de la configuration depuis HubeeAPI
    hubee_api = HubeeAPI()

    for process in hubee_api.config["demarches"]:
        print("Traitement de la démarche: ", process["demarche_nom"])

        # Dossier de téléchargement (avec fallback) + création du répertoire
        configured_dir: str | None = process.get("dossier_telechargement")
        if configured_dir:
            download_path: Path = Path(configured_dir)
        else:
            fallback_dir: str = f"./downloads/{process['demarche_nom']}/"
            print(
                f"  Dossier de téléchargement non configuré, utilisation du fallback: {fallback_dir}"
            )
            download_path = Path(fallback_dir)

        existed_before: bool = download_path.exists()
        if not existed_before:
            download_path.mkdir(parents=True, exist_ok=True)
            print(
                f"  Création du répertoire de téléchargement: {download_path.resolve()}"
            )

        process_hubee_teledossier(
            hubee_api=hubee_api,
            client_id=process["client_id"],
            client_secret=process["client_secret"],
            download_path=download_path,
        )


if __name__ == "__main__":
    main()
