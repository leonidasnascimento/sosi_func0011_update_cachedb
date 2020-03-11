import datetime
import logging
import azure.functions as func
import json
import requests
import pathlib
import threading
import time

from configuration_manager.reader import reader

SETTINGS_FILE_PATH = pathlib.Path(__file__).parent.parent.__str__() + "//local.settings.json"

def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()

    try:
        logging.info("Timer job has begun")

        config_obj: reader = reader(SETTINGS_FILE_PATH, 'Values')
        service_lst_updt: str = config_obj.get_value("SERVICE_LIST_UPDATE")
        update_list: [str] = service_lst_updt.split(';') if ((service_lst_updt) and (service_lst_updt != '')) else []     
        headers = {
        'content-type': "application/json",
        'cache-control': "no-cache"
        }

        for svc in update_list:
            requests.request("PUT", svc, headers=headers)
            pass
        
        logging.info("{} services updated their cache database".format(len(update_list)))
        pass
    except Exception as ex:
        error_log = '{} -> {}'
        logging.exception(error_log.format(utc_timestamp, str(ex)))
        pass
    pass