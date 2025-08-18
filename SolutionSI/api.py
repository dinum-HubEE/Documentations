import requests
import json
from pathlib import Path
from typing import Dict, Any
from requests.exceptions import HTTPError
from config import config


class HubeeAPI:
    """Classe pour interagir avec l'API HUBEE."""

    def __init__(self):
        """Initialise l'API avec la configuration."""
        pass

    def _get_headers(
        self, token: str = None, content_type: str = None
    ) -> Dict[str, str]:
        """Génère les headers communs avec options.

        Args:
            token: Token d'authentification (optionnel)
            content_type: Type de contenu (optionnel)

        Returns:
            Dictionnaire des headers
        """
        headers = {
            "editorName": config["header"]["editorName"],
            "applicationName": config["header"]["applicationName"],
            "softwareVersion": config["header"]["softwareVersion"],
        }

        if token:
            headers["Authorization"] = f"Bearer {token}"

        if content_type:
            headers["Content-Type"] = content_type

        return headers

    def get_access_token(
        self, nb_retry: int, client_id: str, client_secret: str
    ) -> str:
        """Récupère un token d'authentification OAuth2 depuis l'API HUBEE."""
        try:
            payload = f"scope={config['acteurType']}&grant_type=client_credentials"
            headers = self._get_headers(content_type="application/x-www-form-urlencoded")
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
                return self.get_access_token(nb_retry - 1, client_id, client_secret)
            else:
                print("Erreur technique, merci de vérifiez vos credentials")
                exit()
        except Exception as e:
            print(f"Other error occurred: {e}")
            if nb_retry > 1:
                return self.get_access_token(nb_retry - 1, client_id, client_secret)
            else:
                print("Erreur technique, merci de vérifiez vos credentials")
                exit()

    def get_notifications(self, nb_retry: int, token: str) -> Dict[str, Any]:
        """Récupère la liste des notifications depuis l'API HUBEE."""
        try:
            headers = self._get_headers(token=token)
            response = requests.request(
                "GET",
                f"{config['environnement']['api']}teledossiers/v1/notifications?eventDetails=true&maxResult={config['notificationMax']}",
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
                return self.get_notifications(nb_retry - 1, token)
            else:
                print(
                    "Impossible de récupérer les notifications, merci de vous rapprocher de votre équipe technique"
                )
                exit()
        except Exception as e:
            print(f"Other error occurred: {e}")
            if nb_retry > 1:
                return self.get_notifications(nb_retry - 1, token)
            else:
                print(
                    "il est impossible de récupérer les notifications, merci de vous rapprocher de votre équipe technique"
                )
                exit()

    def download_case_attachment(
        self,
        nb_retry: int,
        token: str,
        case: str,
        attachment: str,
        file_name: str,
        external_id: str,
        download_dir: Path,
    ) -> None:
        """Télécharge une pièce jointe d'un télédossier et la sauvegarde localement."""
        try:
            headers = self._get_headers(token=token)
            response = requests.request(
                "GET",
                f"{config['environnement']['api']}teledossiers/v1/cases/{case}/attachments/{attachment}",
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
                return self.download_case_attachment(
                    nb_retry - 1,
                    token,
                    case,
                    attachment,
                    file_name,
                    external_id,
                    download_dir,
                )
            else:
                print("impossible de récupérer la pièce jointe :", attachment)
                exit()
        except Exception as e:
            print(f"Other error occurred: {e}")
            if nb_retry > 1:
                return self.download_case_attachment(
                    nb_retry - 1,
                    token,
                    case,
                    attachment,
                    file_name,
                    external_id,
                    download_dir,
                )
            else:
                print("impossible de récupérer la pièce jointe :", attachment)
                exit()

    def download_event_attachment(
        self,
        nb_retry: int,
        token: str,
        case: str,
        event_id: str,
        attachment: str,
        file_name: str,
        external_id: str,
        download_dir: Path,
    ) -> None:
        """Télécharge une pièce jointe d'un événement et la sauvegarde localement."""
        try:
            headers = self._get_headers(token=token)
            response = requests.request(
                "GET",
                f"{config['environnement']['api']}teledossiers/v1/cases/{case}/events/{event_id}/attachments/{attachment}",
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

            with open(download_path, "wb") as e:
                e.write(response.content)

            if not download_path.exists():
                raise ValueError("FILE IS NOT CREATED")

        except HTTPError as e:
            print(f"HTTP error occurred: {e}")
            if nb_retry > 1:
                return self.download_event_attachment(
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
                return self.download_event_attachment(
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

    def get_case(self, nb_retry: int, token: str, case: str) -> Dict[str, Any]:
        """Récupère les informations d'un télédossier depuis l'API HUBEE."""
        try:
            headers = self._get_headers(token=token)
            response = requests.request(
                "GET",
                f"{config['environnement']['api']}teledossiers/v1/cases/{case}",
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
                return self.get_case(nb_retry - 1, token, case)
            else:
                print("impossible de récupérer le case:", case)
                exit()
        except Exception as err:
            print(f"Other error occurred: {err}")
            if nb_retry > 1:
                return self.get_case(nb_retry - 1, token, case)
            else:
                print("impossible de récupérer le case:", case)
                exit()

    def update_event_status(
        self, nb_retry: int, token: str, case: str, event: str, status: str
    ) -> requests.Response:
        """Met à jour le statut d'un événement dans l'API HUBEE."""
        try:
            headers = self._get_headers(token=token, content_type="application/json")
            response = requests.request(
                "PATCH",
                f"{config['environnement']['api']}teledossiers/v1/cases/{case}/events/{event}",
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
                return self.update_event_status(
                    nb_retry - 1, token, case, event, status
                )
            else:
                print("impossible de modifier le status de levent:", case)
                exit()
        except Exception as e:
            print(f"Other error occurred: {e}")
            if nb_retry > 1:
                return self.update_event_status(
                    nb_retry - 1, token, case, event, status
                )
            else:
                print("impossible de modifier le status de levent:", case)
                exit()

    def get_event(
        self, nb_retry: int, token: str, case: str, event: str
    ) -> Dict[str, Any]:
        """Récupère les informations d'un événement depuis l'API HUBEE."""
        try:
            headers = self._get_headers(token=token)
            response = requests.request(
                "GET",
                f"{config['environnement']['api']}teledossiers/v1/cases/{case}/events/{event}",
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
                return self.get_event(nb_retry - 1, token, case, event)
            else:
                print("impossible de récupérer un event:", event)
                exit()
        except Exception:
            if nb_retry > 1:
                return self.get_event(nb_retry - 1, token, case, event)
            else:
                print("impossible de récupérer un event:", event)
                exit()

    def delete_notification(
        self, nb_retry: int, token: str, notification: str
    ) -> requests.Response:
        """Supprime une notification depuis l'API HUBEE."""
        try:
            headers = self._get_headers(token=token)
            response = requests.request(
                "DELETE",
                f"{config['environnement']['api']}teledossiers/v1/notifications/{notification}",
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
                return self.delete_notification(nb_retry - 1, token, notification)
            else:
                print("impossible de supprimer la notification:", notification)
                exit()
        except Exception as err:
            print(f"DELETE NOTIFICATION - Other error occurred: {err}")
            if nb_retry > 1:
                return self.delete_notification(nb_retry - 1, token, notification)
            else:
                print("impossible de supprimer la notification:", notification)
                exit()

    def create_status_event(
        self, nb_retry: int, token: str, case: str, new_status: str
    ) -> Dict[str, Any]:
        """Crée un nouvel événement de changement de statut dans l'API HUBEE."""
        try:
            headers = self._get_headers(token=token, content_type="application/json")
            response = requests.request(
                "POST",
                f"{config['environnement']['api']}teledossiers/v1/cases/{case}/events",
                headers=headers,
                data=json.dumps(
                    {
                        "message": f"passage du télédossier à {new_status}",
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
                return self.create_status_event(nb_retry - 1, token, case, new_status)
            else:
                print("impossible de créer un event:", case)
                exit()
        except Exception as e:
            print(f"Other error occurred: {e}")
            if nb_retry > 1:
                return self.create_status_event(nb_retry - 1, token, case, new_status)
            else:
                print("impossible de créer un event:", case)
                exit()
