# _*_ coding: utf-8 _*_

__author__ = 'izamarro'
__version__ = '0.0.1a'

"""

El objetivo del modulo es implementar la lógica de colaboración con el software TDBRIDGE propietario de EPSON, que
a traves de un sistema de escritura de ficheros, en formato (.JDF) permite implementar, en este caso, la grabación de
estudios radiológicos con un visor DICOM incororado, a través de su hardware propietario EPSON PP100II.

El modulo se encarga de la logica en la preparación de un trabajo de grabación, que incluya imágenes radiológicas,
visor DICOM, y gestione la orden con TDBRIDGE.
"""


class JobsDirectoryHandler(object):
    
    def __init__(self, jobs_directory, patientid, os_stat):

        self.__jobs_directory = jobs_directory
        self.__patient_id = patientid
        self.__absolute_job_path = self.__jobs_directory + ("/%s" % self.__patient_id)
        self.__os = os_stat

    def create_absolute_job_path_directory(self):

        absolute_job_path = self.__jobs_directory + ("/%s" % self.__patient_id)

        if self.get_job_directory_path() is "":
            try:
                self.__os.mkdir(absolute_job_path)
                return True

            except OSError:
                raise
        else:
            return False

    def get_job_directory_path(self):

        if self.__os.path.exists(self.__absolute_job_path) is True:
            return str(self.__absolute_job_path)

        else:
            return ""


class OrdersFileHandler(object):

    def __init__(self, orders_directory, order_extension, os_stat):

        self.__orders_directory = orders_directory
        self.__os = os_stat
        self.__extension = order_extension

    def get_order_file_name_askey_and_extension_asvalue(self):

        for orders_files_names in self.__os.listdir(self.__orders_directory):

            if orders_files_names[-4:] == self.__extension:

                return {orders_files_names[:-4]: self.__extension}

            else:
                return False