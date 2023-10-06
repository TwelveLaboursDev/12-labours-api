"""
Functionality for using external service
- get
- check_service_status
"""

from services.gen3.gen3_service import Gen3Service
from services.gen3.sgqlc import SimpleGraphQLClient
from services.irods.irods_service import iRODSService
from services.orthanc.orthanc_service import OrthancService


class ExternalService:
    """
    External services functionality
    """

    def __init__(self):
        self.__services = {
            "gen3": {
                "object": Gen3Service(SimpleGraphQLClient()),
                "connection": None,
                "status": False,
            },
            "irods": {
                "object": iRODSService("irods"),
                "connection": None,
                "status": False,
            },
            "irods_ep": {
                "object": iRODSService("irods_ep"),
                "connection": None,
                "status": False,
            },
            "orthanc": {
                "object": OrthancService(),
                "connection": None,
                "status": False,
            },
        }

    def use(self, service):
        """
        Handler for getting service object
        """
        # Make sure service connection exist and is valid
        #
        if (
            self.__services[service]["connection"]
            and self.__services[service]["status"]
        ):
            return self.__services[service]["object"]
        return None

    def check_service_status(self, startup=False):
        """
        Handler for checking external service status
        """
        connection = {}
        for name, service in self.__services.items():
            if not service["status"]:
                service["object"].connection()
            else:
                service["object"].status()
            service["connection"] = service["object"].get_connection()
            service["status"] = service["object"].get_status()
            if startup:
                connection[name] = service["status"]
            else:
                connection[name] = service["connection"]
        return connection
