import requests
import json
from pathlib import Path
from typing import Any
from requests.exceptions import HTTPError
import tomllib


class HubeeClient:
    """Classe pour interagir avec l'API HUBEE."""

    def __init__(self):
        """Initialise l'API avec la configuration depuis config.toml."""
        try:
            with open("config.toml", "rb") as f:
                self.config: dict[str, Any] = tomllib.load(f)
        except FileNotFoundError:
            raise RuntimeError(
                "Le fichier config.toml est introuvable dans le répertoire courant"
            )
        except tomllib.TOMLDecodeError as e:
            raise RuntimeError(f"Erreur de syntaxe dans config.toml: {e}")
        except Exception as e:
            raise RuntimeError(f"Erreur lors de la lecture de config.toml: {e}")

    def _get_headers(
        self, token: str = None, content_type: str = None
    ) -> dict[str, str]:
        """Génère les headers communs avec options.

        Args:
                token: Token d'authentification (optionnel)
                content_type: Type de contenu (optionnel)

        Returns:
                dictionnaire des headers
        """
        headers = {
            "editorName": self.config["header"]["editor_name"],
            "applicationName": self.config["header"]["application_name"],
            "softwareVersion": self.config["header"]["software_version"],
        }
        if token:
            headers["Authorization"] = f"Bearer {token}"
        if content_type:
            headers["Content-Type"] = content_type
        return headers

    def _log_request(self, response: requests.Response) -> None:
        """Log les informations de la requête HTTP."""
        print(
            response.request.method,
            response.status_code,
            response.request.url,
            "-",
            round(response.elapsed.total_seconds() * 1000),
            "ms",
        )

    def _handle_request_with_retry(
        self,
        method: str,
        url: str,
        headers: dict,
        error_message: str,
        data=None,
        auth=None,
    ) -> requests.Response:
        """Gère les requêtes HTTP avec retry automatique."""
        nb_retry = self.config["nombre_retry"]

        while nb_retry > 0:
            try:
                response = requests.request(
                    method=method,
                    url=url,
                    headers=headers,
                    data=data,
                    auth=auth,
                )
                response.raise_for_status()
                self._log_request(response)
                return response
            except (HTTPError, Exception) as e:
                error_type = "HTTP" if isinstance(e, HTTPError) else "Other"
                print(f"{error_type} error occurred: {e}")

                nb_retry -= 1
                if nb_retry > 0:
                    print(
                        f"Retry attempt {self.config['nombre_retry'] - nb_retry + 1}/{self.config['nombre_retry']}"
                    )
                    continue

                raise RuntimeError(error_message)

    def get_access_token(self, client_id: str, client_secret: str) -> str:
        """Récupère un token d'authentification OAuth2 depuis l'API HUBEE."""
        payload: str = (
            f"scope={self.config['type_acteur']}&grant_type=client_credentials"
        )
        headers: dict[str, str] = self._get_headers(
            content_type="application/x-www-form-urlencoded"
        )
        response: requests.Response = self._handle_request_with_retry(
            method="POST",
            url=self.config["environnement"]["token_url"],
            headers=headers,
            error_message="Erreur technique, merci de vérifiez vos credentials",
            data=payload,
            auth=(client_id, client_secret),
        )
        return response.json()["access_token"]

    def get_notifications(self, token: str) -> dict[str, Any]:
        """Récupère la liste des notifications depuis l'API HUBEE."""
        headers: dict[str, str] = self._get_headers(token=token)
        response: requests.Response = self._handle_request_with_retry(
            method="GET",
            url=f"{self.config['environnement']['api_url']}teledossiers/v1/notifications?eventDetails=true&maxResult={self.config['notification_max']}",
            headers=headers,
            error_message="Impossible de récupérer les notifications, merci de vous rapprocher de votre équipe technique",
        )
        return response.json()

    def download_case_attachment(
        self,
        token: str,
        case: str,
        attachment: str,
        file_name: str,
        external_id: str,
        download_dir: Path,
    ) -> None:
        """Télécharge une pièce jointe d'un télédossier et la sauvegarde localement."""
        headers: dict[str, str] = self._get_headers(token=token)
        response: requests.Response = self._handle_request_with_retry(
            method="GET",
            url=f"{self.config['environnement']['api_url']}teledossiers/v1/cases/{case}/attachments/{attachment}",
            headers=headers,
            error_message=f"impossible de récupérer la pièce jointe : {attachment}",
        )

        # Logique métier de téléchargement (après la réponse)
        # print("téléchar", file_name)
        download_path: Path = download_dir / external_id / file_name
        download_path.parent.mkdir(parents=True, exist_ok=True)

        with open(download_path, "wb") as f:
            f.write(response.content)

        if not download_path.exists():
            raise ValueError("FILE IS NOT CREATED")

    def download_event_attachment(
        self,
        token: str,
        case: str,
        event_id: str,
        attachment: str,
        file_name: str,
        external_id: str,
        download_dir: Path,
    ) -> None:
        """Télécharge une pièce jointe d'un événement et la sauvegarde localement."""
        headers: dict[str, str] = self._get_headers(token=token)
        response: requests.Response = self._handle_request_with_retry(
            method="GET",
            url=f"{self.config['environnement']['api_url']}teledossiers/v1/cases/{case}/events/{event_id}/attachments/{attachment}",
            headers=headers,
            error_message=f"impossible de récupérer la pièce jointe : {attachment}",
        )

        # Logique métier de téléchargement (après la réponse)
        # print("téléchar", file_name)
        download_path: Path = download_dir / external_id / file_name
        download_path.parent.mkdir(parents=True, exist_ok=True)

        with open(download_path, "wb") as e:
            e.write(response.content)

        if not download_path.exists():
            raise ValueError("FILE IS NOT CREATED")

    def get_case(self, token: str, case: str) -> dict[str, Any]:
        """Récupère les informations d'un télédossier depuis l'API HUBEE."""
        headers: dict[str, str] = self._get_headers(token=token)
        response: requests.Response = self._handle_request_with_retry(
            method="GET",
            url=f"{self.config['environnement']['api_url']}teledossiers/v1/cases/{case}",
            headers=headers,
            error_message=f"impossible de récupérer le case: {case}",
        )
        return response.json()

    def update_event_status(
        self, token: str, case: str, event: str, status: str
    ) -> requests.Response:
        """Met à jour le statut d'un événement dans l'API HUBEE."""
        headers: dict[str, str] = self._get_headers(
            token=token, content_type="application/json"
        )
        response: requests.Response = self._handle_request_with_retry(
            method="PATCH",
            url=f"{self.config['environnement']['api_url']}teledossiers/v1/cases/{case}/events/{event}",
            headers=headers,
            error_message=f"impossible de modifier le status de levent: {case}",
            data=json.dumps({"status": status}),
        )
        return response

    def get_event(self, token: str, case: str, event: str) -> dict[str, Any]:
        """Récupère les informations d'un événement depuis l'API HUBEE."""
        headers: dict[str, str] = self._get_headers(token=token)
        response: requests.Response = self._handle_request_with_retry(
            method="GET",
            url=f"{self.config['environnement']['api_url']}teledossiers/v1/cases/{case}/events/{event}",
            headers=headers,
            error_message=f"impossible de récupérer un event: {event}",
        )
        return response.json()

    def delete_notification(self, token: str, notification: str) -> requests.Response:
        """Supprime une notification depuis l'API HUBEE."""
        headers: dict[str, str] = self._get_headers(token=token)
        response: requests.Response = self._handle_request_with_retry(
            method="DELETE",
            url=f"{self.config['environnement']['api_url']}teledossiers/v1/notifications/{notification}",
            headers=headers,
            error_message=f"impossible de supprimer la notification: {notification}",
        )
        return response

    def create_status_event(
        self, token: str, case: str, new_status: str
    ) -> dict[str, Any]:
        """Crée un nouvel événement de changement de statut dans l'API HUBEE."""
        headers: dict[str, str] = self._get_headers(
            token=token, content_type="application/json"
        )
        response: requests.Response = self._handle_request_with_retry(
            method="POST",
            url=f"{self.config['environnement']['api_url']}teledossiers/v1/cases/{case}/events",
            headers=headers,
            error_message=f"impossible de créer un event: {case}",
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
        return response.json()
