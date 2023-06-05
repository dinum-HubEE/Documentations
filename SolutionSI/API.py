from os import access
import os
import requests
import json
from requests.exceptions import HTTPError
from config import *


def getToken(nbRetry, clientId, clientSecret):
    try:
        payload = 'scope=' + config["acteurType"] + '&grant_type=client_credentials'
        headers = {
            'editorName':config["header"]["editorName"],
            'applicationName':config["header"]["applicationName"],
            'softwareVersion':config["header"]["softwareVersion"],
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        response = requests.request(
            "POST", config["environnement"]["token"], auth=(clientId, clientSecret), headers=headers, data=payload)
        response.raise_for_status()
        
        print(response.request.method, response.status_code, response.request.url,"-", round(response.elapsed.total_seconds() * 1000), "ms")

        jsonResponse = response.json()

        return jsonResponse["access_token"]

    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
        if(nbRetry > 1):
            getToken(nbRetry - 1, clientId, clientSecret)
        else:
            print('Erreur technique, merci de vérifiez vos credentials')
            exit()
    except Exception as err:
        print(f'Other error occurred: {err}')
        if(nbRetry > 1):
            getToken(nbRetry - 1, clientId, clientSecret)
        else:
            print('Erreur technique, merci de vérifiez vos credentials')
            exit()

def getNotification(nbRetry, token):
    try:
        headers = {
            'Authorization': 'Bearer ' + token,
            'editorName':config["header"]["editorName"],
            'applicationName':config["header"]["applicationName"],
            'softwareVersion':config["header"]["softwareVersion"]
        }
        response = requests.request(
            "GET", config["environnement"]["api"] + "teledossiers/v1/notifications?maxResult=" + str(config["nombreDeNotifications"]), headers=headers, data={})
        response.raise_for_status()

        print(response.request.method, response.status_code, response.request.url,"-", round(response.elapsed.total_seconds() * 1000), "ms")
        
        jsonResponse = response.json()
        return jsonResponse

    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
        if(nbRetry > 1):
            getNotification(nbRetry - 1, token)
        else:
            print('il est impossible de récupérer les notifications, merci de vous rapprocher de votre équipe technique')
            exit()
    except Exception as err:
        print(f'Other error occurred: {err}')
        if(nbRetry > 1):
            getNotification(nbRetry - 1, token)
        else:
            print('il est impossible de récupérer les notifications, merci de vous rapprocher de votre équipe technique')
            exit()

def getCasePJ(nbRetry, token, case, attachment, fileName, externalId, repository):
    try:
        headers = {
            'Authorization': 'Bearer ' + token,
            'editorName':config["header"]["editorName"],
            'applicationName':config["header"]["applicationName"],
            'softwareVersion':config["header"]["softwareVersion"]
        }
        response = requests.request(
            "GET", config["environnement"]["api"] + "teledossiers/v1/cases/" + case + "/attachments/" + attachment, headers=headers, data={})
        response.raise_for_status()
        
        print(response.request.method, response.status_code, response.request.url,"-", round(response.elapsed.total_seconds() * 1000), "ms")
        #print("téléchar", fileName)

        isFile = os.path.isdir(repository + externalId)
        if(isFile == False):
            os.makedirs(repository + externalId)

        f = open(repository + externalId + "/" + fileName, "w", encoding='utf-8'))
        f.write(response.text)
        f.close()

    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
        if(nbRetry > 1):
            getCasePJ(nbRetry - 1, token, case, attachment, fileName, externalId, repository)
        else:
            print('impossible de récupérer la pièce jointe :', attachment)
            exit()
    except Exception as err:
        print(f'Other error occurred: {err}')
        if(nbRetry > 1):
            getCasePJ(nbRetry - 1, token, case, attachment, fileName, externalId, repository)
        else:
            print('impossible de récupérer la pièce jointe :', attachment)
            exit()


def getCaseEventPJ(nbRetry, token, case, eventId, attachment, fileName, externalId, repository):
    try:
        headers = {
            'Authorization': 'Bearer ' + token,
            'editorName':config["header"]["editorName"],
            'applicationName':config["header"]["applicationName"],
            'softwareVersion':config["header"]["softwareVersion"]
        }
        response = requests.request(
            "GET", config["environnement"]["api"]  + "teledossiers/v1/cases/" + case + "/events/" + eventId + "/attachments/" + attachment, headers=headers, data={})
        response.raise_for_status()
        
        print(response.request.method, response.status_code, response.request.url,"-", round(response.elapsed.total_seconds() * 1000), "ms")
        print("téléchar", fileName)

        isFile = os.path.isdir(repository + externalId)
        if(isFile == False):
            os.makedirs(repository + externalId)

        f = open(repository + externalId + "/" + fileName, "w", encoding='utf-8'))
        f.write(response.text)
        f.close()

    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
        if(nbRetry > 1):
            getCaseEventPJ(nbRetry - 1, token, case, eventId, attachment, fileName, externalId, repository)
        else:
            print('impossible de récupérer la pièce jointe :', attachment)
            exit()
    except Exception as err:
        print(f'Other error occurred: {err}')
        if(nbRetry > 1):
            getCaseEventPJ(nbRetry - 1, token, case, eventId, attachment, fileName, externalId, repository)
        else:
            print('impossible de récupérer la pièce jointe :', attachment)
            exit()

def getCase(nbRetry, token, case):
    try:
        headers = {
            'Authorization': 'Bearer ' + token,
            'editorName':config["header"]["editorName"],
            'applicationName':config["header"]["applicationName"],
            'softwareVersion':config["header"]["softwareVersion"]
        }
        response = requests.request(
            "GET", config["environnement"]["api"] + "teledossiers/v1/cases/" + case, headers=headers, data={})
        response.raise_for_status()

        print(response.request.method, response.status_code, response.request.url,"-", round(response.elapsed.total_seconds() * 1000), "ms")

        jsonResponse = response.json()
        return jsonResponse

    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
        if(nbRetry > 1):
            getCase(nbRetry - 1, token, case)
        else:
            print('impossible de récupérer le case:', case)
            exit()
    except Exception as err:
        print(f'Other error occurred: {err}')
        if(nbRetry > 1):
            getCase(nbRetry - 1, token, case)
        else:
            print('impossible de récupérer le case:', case)
            exit()


def patchEvent(nbRetry, token, case, event, status):
    try:
        headers = {
            'Authorization': 'Bearer ' + token,
            'Content-Type': 'application/json',
            'editorName':config["header"]["editorName"],
            'applicationName':config["header"]["applicationName"],
            'softwareVersion':config["header"]["softwareVersion"]
        }
        response = requests.request(
            "PATCH", config["environnement"]["api"]  + "teledossiers/v1/cases/" + case + "/events/" + event, headers=headers, data=json.dumps({"status": status}))
        response.raise_for_status()
        
        print(response.request.method, response.status_code, response.request.url,"-", round(response.elapsed.total_seconds() * 1000), "ms")

        return response

    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
        if(nbRetry > 1):
            patchEvent(nbRetry - 1, token, case, event, status)
        else:
            print('impossible de modifier le status de levent:', case)
            exit()
    except Exception as err:
        print(f'Other error occurred: {err}')
        if(nbRetry > 1):
            patchEvent(nbRetry - 1, token, case, event, status)
        else:
            print('impossible de modifier le status de levent:', case)
            exit()


def patchCase(nbRetry, token, case, status):
    try:
        headers = {
            'Authorization': 'Bearer ' + token,
            'Content-Type': 'application/json',
            'editorName':config["header"]["editorName"],
            'applicationName':config["header"]["applicationName"],
            'softwareVersion':config["header"]["softwareVersion"]
        }
        response = requests.request(
            "PATCH", config["environnement"]["api"] + "teledossiers/v1/cases/" + case, headers=headers, data=json.dumps({"status": status}))
        response.raise_for_status()
        
        print(response.request.method, response.status_code, response.request.url,"-", round(response.elapsed.total_seconds() * 1000), "ms")

        return response

    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
        if(nbRetry > 1):
            patchCase(nbRetry - 1, token, case, status)
        else:
            print('impossible de modifier le status du case:', case)
            exit()
    except Exception as err:
        print(f'Other error occurred: {err}')
        if(nbRetry > 1):
            patchCase(nbRetry - 1, token, case, status)
        else:
            print('impossible de modifier le status du case:', case)
            exit()


def getEvent(nbRetry, token, case, event):
    try:
        headers = {
            'Authorization': 'Bearer ' + token,
            'editorName':config["header"]["editorName"],
            'applicationName':config["header"]["applicationName"],
            'softwareVersion':config["header"]["softwareVersion"]
        }
        response = requests.request(
            "GET", config["environnement"]["api"] + "teledossiers/v1/cases/" + case + "/events/" + event, headers=headers, data={})
        response.raise_for_status()
        
        print(response.request.method, response.status_code, response.request.url,"-", round(response.elapsed.total_seconds() * 1000), "ms")

        jsonResponse = response.json()
        return jsonResponse

    except HTTPError as http_err:
        if(nbRetry > 1):
            getEvent(nbRetry - 1, token, case, event)
        else:
            print('impossible de récupérer un event:', event)
            exit()
    except Exception as err:
        if(nbRetry > 1):
            getEvent(nbRetry - 1, token, case, event)
        else:
            print('impossible de récupérer un event:', event)
            exit()


def deleteNotification(nbRetry, token, notification):
    try:
        headers = {
            'Authorization': 'Bearer ' + token,
            'editorName':config["header"]["editorName"],
            'applicationName':config["header"]["applicationName"],
            'softwareVersion':config["header"]["softwareVersion"]
        }
        response = requests.request(
            "DELETE", config["environnement"]["api"] + "teledossiers/v1/notifications/" + notification, headers=headers)
        response.raise_for_status()
        
        print(response.request.method, response.status_code, response.request.url,"-", round(response.elapsed.total_seconds() * 1000), "ms")

        #jsonResponse = response.json()
        return response

    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
        if(nbRetry > 1):
            deleteNotification(nbRetry - 1, token, notification)
        else:
            print('impossible de supprimer la notification:', notification)
            exit()
    except Exception as err:
        print(f'DELETE NOTIFICATION - Other error occurred: {err}')
        if(nbRetry > 1):
            deleteNotification(nbRetry - 1, token, notification)
        else:
            print('impossible de supprimer la notification:', notification)
            exit()


def postEvent(nbRetry, token, case, currentStatus, newStatus):
    try:
        headers = {
            'Authorization': 'Bearer ' + token,
            'Content-Type': 'application/json',
            'editorName':config["header"]["editorName"],
            'applicationName':config["header"]["applicationName"],
            'softwareVersion':config["header"]["softwareVersion"]
        }
        response = requests.request(
            "POST", config["environnement"]["api"] + "teledossiers/v1/cases/" + case + "/events", headers=headers, data=json.dumps({
                "message": "passage du teledossier a" + newStatus,
                "actionType": "STATUS_UPDATE",
                "author": "me",
                "notification": True,
                "caseCurrentStatus": currentStatus,
                "caseNewStatus": newStatus
            }))

        response.raise_for_status()
        
        print(response.request.method, response.status_code, response.request.url,"-", round(response.elapsed.total_seconds() * 1000), "ms")

        jsonResponse = response.json()
        return jsonResponse

    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
        if(nbRetry > 1):
            postEvent(nbRetry - 1, token, case, currentStatus, newStatus)
        else:
            print('impossible de créer un event:', case)
            exit()
    except Exception as err:
        print(f'Other error occurred: {err}')
        if(nbRetry > 1):
            postEvent(nbRetry - 1, token, case, currentStatus, newStatus)
        else:
            print('impossible de créer un event:', case)
            exit()
