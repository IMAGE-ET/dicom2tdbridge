# _*_ coding: utf-8 _*_

__author__ = 'izamarro'
__version__ = '0.0.1a'


class JobsDirectoryHandler(object):

    def __init__(self, jobs_directory, patientid, os_stat):

        self.__jobs_directory = jobs_directory
        self.__patient_id = patientid
        self.__absolute_job_path = self.__jobs_directory + ("/%s" % self.__patient_id)
        self.__os = os_stat

    def get_job_skel(self):

        skel = {"absolute_job_path": self.__absolute_job_path,
                "data_job_path": self.__absolute_job_path + "/DATA"}

        return skel

    def create_skel_job_directory(self):

        if self.check_if_job_directory_exist() is False:

            try:
                self.__os.mkdir(self.get_job_skel()["absolute_job_path"])
                self.__os.mkdir(self.get_job_skel()["data_job_path"])
                return True

            except:
                raise

        else:
            return False

    def check_if_job_directory_exist(self):

        if self.__os.path.exists(self.get_job_skel()["absolute_job_path"]) is True:

            return True

        else:

            return False

    def delete_job_directory(self):

        if self.check_if_job_directory_exist() is True:

            try:
                self.__os.rmdir(self.get_job_skel()["data_job_path"])
                self.__os.rmdir(self.get_job_skel()["absolute_job_path"])

                return True

            except:
                raise

        else:
            return False

class OrdersDirectoryHandler(object):

    def __init__(self, orders_directory, job_name, order_extension, os_stat):

        self.__orders_directory = orders_directory
        self.__os = os_stat
        self.__extension = order_extension
        self.__order_name = job_name

    def check_if_order_exist(self):

        if self.__os.path.exists(self.__orders_directory + "/%s" % (self.__order_name + self.__extension)):
            return True

        else:
            return False
