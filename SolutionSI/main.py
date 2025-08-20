#!/usr/bin/env python3

from pathlib import Path

from hubee_client import HubeeClient, HubeeStatus


def process_hubee_teledossier(
    hubee_client: HubeeClient,
    client_id: str,
    client_secret: str,
    download_path: Path,
    min_status: str,
    max_status: str,
) -> None:
    """Traite les télédossiers pour une démarche donnée.

    Effectue les opérations suivantes: récupération des notifications, téléchargement
    des pièces jointes, mise à jour des statuts et acquittement des events.

    Paramètres:
      - hubee_client: instance configurée de HubeeClient
      - client_id: identifiant client de la démarche
      - client_secret: secret client de la démarche
      - download_path: répertoire cible pour enregistrer les pièces jointes pour la démarche
      - min_status: statut minimal à appliquer au télédossier
      - max_status: statut maximal à appliquer au télédossier
    """
    token: str = hubee_client.get_access_token(client_id, client_secret)
    notifications: dict = hubee_client.get_notifications(token)

    if len(notifications) == 0:
        print("Il n'y a pas de notification.")
        return

    for notif in notifications:
        print("Traitement de la notification [", notif["id"], "]")

        if notif["eventId"] is None:
            case = hubee_client.get_case(token, notif["caseId"])

            for PJ in case["attachments"]:
                hubee_client.download_case_attachment(
                    token,
                    notif["caseId"],
                    PJ["id"],
                    PJ["fileName"],
                    case["externalId"],
                    download_path,
                )

            hubee_client.create_event(
                token,
                notif["caseId"],
                min_status,
            )
            hubee_client.create_event(
                token,
                notif["caseId"],
                max_status,
            )
            hubee_client.delete_notification(token, notif["id"])
        else:
            if notif["eventStatus"] == "RECEIVED":
                hubee_client.delete_notification(token, notif["id"])

            else:
                event = hubee_client.get_event(
                    token,
                    notif["caseId"],
                    notif["eventId"],
                )

                match event["actionType"]:
                    case "STATUS_UPDATE":
                        # ceci est un event STATUS_UPDATE
                        status_desc = HubeeStatus.get_description(event["caseNewStatus"])
                        print(
                            f"  → Changement de statut: {event['caseNewStatus']} ({status_desc}) - Message: {event['message']}"
                        )
                    case "SENDING_MESSAGE":
                        # ceci est un event SENDING_MESSAGE
                        print("message  [", event["message"], "]")
                    case "ATTACH_DEPOSIT":
                        # ceci est un event ATTACH_DEPOSIT
                        case = hubee_client.get_case(token, notif["caseId"])

                        for PJ in event["attachments"]:
                            # téléchargement des Pjs de l'event
                            hubee_client.download_event_attachment(
                                token,
                                notif["caseId"],
                                notif["eventId"],
                                PJ["id"],
                                PJ["fileName"],
                                case["externalId"],
                                download_path,
                            )

                        # changement des status du case et création d'events
                        print(
                            f"  → Passage au statut: {min_status} ({HubeeStatus.get_description(min_status)})"
                        )
                        hubee_client.create_event(
                            token,
                            notif["caseId"],
                            min_status,
                        )
                        print(
                            f"  → Passage au statut: {max_status} ({HubeeStatus.get_description(max_status)})"
                        )
                        hubee_client.create_event(
                            token,
                            notif["caseId"],
                            max_status,
                        )
                    case _:
                        print("erreur lors de la récupération de l'event")

                hubee_client.update_event_status(
                    token,
                    notif["caseId"],
                    notif["eventId"],
                    "RECEIVED",
                )

    process_hubee_teledossier(
        hubee_client,
        client_id,
        client_secret,
        download_path,
        min_status,
        max_status,
    )


def main():
    """Fonction principale du script."""
    # Lecture de la configuration depuis HubeeClient
    hubee_client = HubeeClient()

    for process in hubee_client.config["demarches"]:
        print("Traitement de la démarche: ", process["name"])

        # Dossier de téléchargement (avec fallback) + création du répertoire
        configured_dir: str | None = process.get("download_path")
        if configured_dir:
            download_path: Path = Path(configured_dir)
        else:
            fallback_dir: str = f"./downloads/{process['name']}/"
            print(
                f"  Dossier de téléchargement non configuré, utilisation du fallback: {fallback_dir}"
            )
            download_path = Path(fallback_dir)

        existed_before: bool = download_path.exists()
        if not existed_before:
            download_path.mkdir(parents=True, exist_ok=True)
            print(f"  Création du répertoire de téléchargement: {download_path.resolve()}")

        process_hubee_teledossier(
            hubee_client=hubee_client,
            client_id=process["client_id"],
            client_secret=process["client_secret"],
            download_path=download_path,
            min_status=process["min_status"],
            max_status=process["max_status"],
        )


if __name__ == "__main__":
    main()
