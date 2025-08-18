import requests
import json
from pathlib import Path
from typing import Dict, Any
from requests.exceptions import HTTPError
from config import config


def get_access_token(nb_retry: int, client_id: str, client_secret: str) -> str:
    try:
        payload = "scope=" + config["acteurType"] + "&grant_type=client_credentials"
        headers = {
            "editorName": config["header"]["editorName"],
            "applicationName": config["header"]["applicationName"],
            "softwareVersion": config["header"]["softwareVersion"],
            "Content-Type": "application/x-www-form-urlencoded",
        }
        response = requests.request(
            "POST",
            config["environnement"]["token"],
            auth=(client_id, client_secret),
            headers=headers,
            data=payload,
        )
        response.raise_for_status()

        print(
            response.request.method,
            response.status_code,
            response.request.url,
            "-",
            round(response.elapsed.total_seconds() * 1000),
            "ms",
        )

        json_response = response.json()

        return json_response["access_token"]

    except HTTPError as e:
        print(f"HTTP error occurred: {e}")
        if nb_retry > 1:
            get_access_token(nb_retry - 1, client_id, client_secret)
        else:
            print("Erreur technique, merci de vérifiez vos credentials")
            exit()
    except Exception as e:
        print(f"Other error occurred: {e}")
        if nb_retry > 1:
            get_access_token(nb_retry - 1, client_id, client_secret)
        else:
            print("Erreur technique, merci de vérifiez vos credentials")
            exit()


def get_notifications(nb_retry: int, token: str) -> Dict[str, Any]:
    try:
        headers = {
            "Authorization": "Bearer " + token,
            "editorName": config["header"]["editorName"],
            "applicationName": config["header"]["applicationName"],
            "softwareVersion": config["header"]["softwareVersion"],
        }
        response = requests.request(
            "GET",
            config["environnement"]["api"]
            + "teledossiers/v1/notifications?eventDetails=true&maxResult="
            + str(config["notificationMax"]),
            headers=headers,
            data={},
        )
        response.raise_for_status()

        print(
            response.request.method,
            response.status_code,
            response.request.url,
            "-",
            round(response.elapsed.total_seconds() * 1000),
            "ms",
        )

        json_response = response.json()
        return json_response

    except HTTPError as e:
        print(f"HTTP error occurred: {e}")
        if nb_retry > 1:
            get_notifications(nb_retry - 1, token)
        else:
            print(
                "Impossible de récupérer les notifications, merci de vous rapprocher de votre équipe technique"
            )
            exit()
    except Exception as e:
        print(f"Other error occurred: {e}")
        if nb_retry > 1:
            get_notifications(nb_retry - 1, token)
        else:
            print(
                "il est impossible de récupérer les notifications, merci de vous rapprocher de votre équipe technique"
            )
            exit()


def download_case_attachment(
    nb_retry: int,
    token: str,
    case: str,
    attachment: str,
    file_name: str,
    external_id: str,
    download_dir: Path,
) -> None:
    try:
        headers = {
            "Authorization": "Bearer " + token,
            "editorName": config["header"]["editorName"],
            "applicationName": config["header"]["applicationName"],
            "softwareVersion": config["header"]["softwareVersion"],
        }
        response = requests.request(
            "GET",
            config["environnement"]["api"]
            + "teledossiers/v1/cases/"
            + case
            + "/attachments/"
            + attachment,
            headers=headers,
            data={},
        )
        response.raise_for_status()

        print(
            response.request.method,
            response.status_code,
            response.request.url,
            "-",
            round(response.elapsed.total_seconds() * 1000),
            "ms",
        )
        # print("téléchar", file_name)

        download_path = download_dir / external_id / file_name
        download_path.parent.mkdir(parents=True, exist_ok=True)

        with open(download_path, "wb") as f:
            f.write(response.content)

        if not download_path.exists():
            raise ValueError("FILE IS NOT CREATED")

    except HTTPError as e:
        print(f"HTTP error occurred: {e}")
        if nb_retry > 1:
            download_case_attachment(
                nb_retry - 1, token, case, attachment, file_name, external_id, download_dir
            )
        else:
            print("impossible de récupérer la pièce jointe :", attachment)
            exit()
    except Exception as e:
        print(f"Other error occurred: {e}")
        if nb_retry > 1:
            download_case_attachment(
                nb_retry - 1, token, case, attachment, file_name, external_id, download_dir
            )
        else:
            print("impossible de récupérer la pièce jointe :", attachment)
            exit()


def download_event_attachment(
    nb_retry: int,
    token: str,
    case: str,
    event_id: str,
    attachment: str,
    file_name: str,
    external_id: str,
    download_dir: Path,
) -> None:
    try:
        headers = {
            "Authorization": "Bearer " + token,
            "editorName": config["header"]["editorName"],
            "applicationName": config["header"]["applicationName"],
            "softwareVersion": config["header"]["softwareVersion"],
        }
        response = requests.request(
            "GET",
            config["environnement"]["api"]
            + "teledossiers/v1/cases/"
            + case
            + "/events/"
            + event_id
            + "/attachments/"
            + attachment,
            headers=headers,
            data={},
        )
        response.raise_for_status()

        print(
            response.request.method,
            response.status_code,
            response.request.url,
            "-",
            round(response.elapsed.total_seconds() * 1000),
            "ms",
        )
        print("téléchar", file_name)

        download_path: Path = download_dir / external_id / file_name
        download_path.parent.mkdir(parents=True, exist_ok=True)

        with open(download_path, "wb") as f:
            f.write(response.content)

        if not download_path.exists():
            raise ValueError("FILE IS NOT CREATED")

    except HTTPError as e:
        print(f"HTTP error occurred: {e}")
        if nb_retry > 1:
            download_event_attachment(
                nb_retry - 1,
                token,
                case,
                event_id,
                attachment,
                file_name,
                external_id,
                download_dir,
            )
        else:
            print("impossible de récupérer la pièce jointe :", attachment)
            exit()
    except Exception as err:
        print(f"Other error occurred: {err}")
        if nb_retry > 1:
            download_event_attachment(
                nb_retry - 1,
                token,
                case,
                event_id,
                attachment,
                file_name,
                external_id,
                download_dir,
            )
        else:
            print("impossible de récupérer la pièce jointe :", attachment)
            exit()


def get_case(nb_retry: int, token: str, case: str) -> Dict[str, Any]:
    try:
        headers = {
            "Authorization": "Bearer " + token,
            "editorName": config["header"]["editorName"],
            "applicationName": config["header"]["applicationName"],
            "softwareVersion": config["header"]["softwareVersion"],
        }
        response = requests.request(
            "GET",
            config["environnement"]["api"] + "teledossiers/v1/cases/" + case,
            headers=headers,
            data={},
        )
        response.raise_for_status()

        print(
            response.request.method,
            response.status_code,
            response.request.url,
            "-",
            round(response.elapsed.total_seconds() * 1000),
            "ms",
        )

        json_response = response.json()
        return json_response

    except HTTPError as e:
        print(f"HTTP error occurred: {e}")
        if nb_retry > 1:
            get_case(nb_retry - 1, token, case)
        else:
            print("impossible de récupérer le case:", case)
            exit()
    except Exception as err:
        print(f"Other error occurred: {err}")
        if nb_retry > 1:
            get_case(nb_retry - 1, token, case)
        else:
            print("impossible de récupérer le case:", case)
            exit()


def update_event_status(
    nb_retry: int, token: str, case: str, event: str, status: str
) -> requests.Response:
    try:
        headers = {
            "Authorization": "Bearer " + token,
            "Content-Type": "application/json",
            "editorName": config["header"]["editorName"],
            "applicationName": config["header"]["applicationName"],
            "softwareVersion": config["header"]["softwareVersion"],
        }
        response = requests.request(
            "PATCH",
            config["environnement"]["api"]
            + "teledossiers/v1/cases/"
            + case
            + "/events/"
            + event,
            headers=headers,
            data=json.dumps({"status": status}),
        )
        response.raise_for_status()

        print(
            response.request.method,
            response.status_code,
            response.request.url,
            "-",
            round(response.elapsed.total_seconds() * 1000),
            "ms",
        )

        return response

    except HTTPError as e:
        print(f"HTTP error occurred: {e}")
        if nb_retry > 1:
            update_event_status(nb_retry - 1, token, case, event, status)
        else:
            print("impossible de modifier le status de levent:", case)
            exit()
    except Exception as e:
        print(f"Other error occurred: {e}")
        if nb_retry > 1:
            update_event_status(nb_retry - 1, token, case, event, status)
        else:
            print("impossible de modifier le status de levent:", case)
            exit()


def get_event(nb_retry: int, token: str, case: str, event: str) -> Dict[str, Any]:
    try:
        headers = {
            "Authorization": "Bearer " + token,
            "editorName": config["header"]["editorName"],
            "applicationName": config["header"]["applicationName"],
            "softwareVersion": config["header"]["softwareVersion"],
        }
        response = requests.request(
            "GET",
            config["environnement"]["api"]
            + "teledossiers/v1/cases/"
            + case
            + "/events/"
            + event,
            headers=headers,
            data={},
        )
        response.raise_for_status()

        print(
            response.request.method,
            response.status_code,
            response.request.url,
            "-",
            round(response.elapsed.total_seconds() * 1000),
            "ms",
        )

        json_response = response.json()
        return json_response

    except HTTPError:
        if nb_retry > 1:
            get_event(nb_retry - 1, token, case, event)
        else:
            print("impossible de récupérer un event:", event)
            exit()
    except Exception:
        if nb_retry > 1:
            get_event(nb_retry - 1, token, case, event)
        else:
            print("impossible de récupérer un event:", event)
            exit()


def delete_notification(
    nb_retry: int, token: str, notification: str
) -> requests.Response:
    try:
        headers = {
            "Authorization": "Bearer " + token,
            "editorName": config["header"]["editorName"],
            "applicationName": config["header"]["applicationName"],
            "softwareVersion": config["header"]["softwareVersion"],
        }
        response = requests.request(
            "DELETE",
            config["environnement"]["api"]
            + "teledossiers/v1/notifications/"
            + notification,
            headers=headers,
        )
        response.raise_for_status()

        print(
            response.request.method,
            response.status_code,
            response.request.url,
            "-",
            round(response.elapsed.total_seconds() * 1000),
            "ms",
        )

        # json_response = response.json()
        return response

    except HTTPError as e:
        print(f"HTTP error occurred: {e}")
        if nb_retry > 1:
            delete_notification(nb_retry - 1, token, notification)
        else:
            print("impossible de supprimer la notification:", notification)
            exit()
    except Exception as err:
        print(f"DELETE NOTIFICATION - Other error occurred: {err}")
        if nb_retry > 1:
            delete_notification(nb_retry - 1, token, notification)
        else:
            print("impossible de supprimer la notification:", notification)
            exit()


def create_status_event(nb_retry: int, token: str, case: str, new_status: str) -> Dict[str, Any]:
    try:
        headers = {
            "Authorization": "Bearer " + token,
            "Content-Type": "application/json",
            "editorName": config["header"]["editorName"],
            "applicationName": config["header"]["applicationName"],
            "softwareVersion": config["header"]["softwareVersion"],
        }
        response = requests.request(
            "POST",
            config["environnement"]["api"]
            + "teledossiers/v1/cases/"
            + case
            + "/events",
            headers=headers,
            data=json.dumps(
                {
                    "message": "passage du teledossier a" + new_status,
                    "actionType": "STATUS_UPDATE",
                    "author": "me",
                    "notification": True,
                    "caseNewStatus": new_status,
                }
            ),
        )

        response.raise_for_status()

        print(
            response.request.method,
            response.status_code,
            response.request.url,
            "-",
            round(response.elapsed.total_seconds() * 1000),
            "ms",
        )

        json_response = response.json()
        return json_response

    except HTTPError as e:
        print(f"HTTP error occurred: {e}")
        if nb_retry > 1:
            create_status_event(nb_retry - 1, token, case, new_status)
        else:
            print("impossible de créer un event:", case)
            exit()
    except Exception as e:
        print(f"Other error occurred: {e}")
        if nb_retry > 1:
            create_status_event(nb_retry - 1, token, case, new_status)
        else:
            print("impossible de créer un event:", case)
            exit()
