# _*_ coding: utf-8 _*_

__author__ = 'izamarro'
__version__ = '0.0.1a'


class JobsDirectoryHandler(object):

    def __init__(self, jobs_directory, patient_id, os_stat):

        self.__jobs_directory = jobs_directory
        self.__patient_id = patient_id
        self.__absolute_job_path = self.__jobs_directory + ("/%s" % self.__patient_id)
        self.__os = os_stat

    def get_job_skel(self):

        skel = {"absolute_job_path": self.__absolute_job_path,
                "data_job_path": self.__absolute_job_path + "/DATA"}

        return skel

    def create_skel_job_directory(self):

        try:
            self.__os.mkdir(self.get_job_skel()["absolute_job_path"])
            self.__os.mkdir(self.get_job_skel()["data_job_path"])
            return True

        except:
            raise

    def check_if_job_directory_exist(self):

        if self.__os.path.exists(self.get_job_skel()["absolute_job_path"]) is True:

            return True

        else:

            return False

    def delete_job_directory(self):

        try:
            self.__os.rmdir(self.get_job_skel()["data_job_path"])
            self.__os.rmdir(self.get_job_skel()["absolute_job_path"])

            return True

        except:
            raise

class OrdersDirectoryHandler(object):

    def __init__(self, orders_directory, job_id, order_extension, os_stat):

        self.__orders_directory = orders_directory
        self.__os = os_stat
        self.__extension = order_extension
        self.__order_name = job_id

    def check_if_order_exist(self):

        if self.__os.path.exists(self.__orders_directory + "/%s" % (self.__order_name + self.__extension)):
            return True

        else:
            return False


class JDFFilesHandler(object):

    def __init__(self, job_directory, job_id, os):

        self.jdf_path = job_directory + "/%s" % job_id + "/%s" % (job_id + ".JDF")
        self.job_id = job_id
        self.__os = os

    def check_if_jdf_exist(self):

        if self.__os.path.exists(self.jdf_path) is True:

            return True

        else:
            return False

    def create_jdf_file(self):

        try:

            with open(self.jdf_path, "w") as jdf_file:
                jdf_file.close()
        except:
            raise

    def get_jdf_skel(self, name_of_publisher, number_of_copies, disc_type, absolute_data_path, path_of_replace_field_file,
                     path_of_label_file):

        jdf_skel = {"JOB_ID=": "=%s" % self.job_id,
                    "PUBLISHER=": name_of_publisher,
                    "COPIES=": number_of_copies,
                    "DISC_TYPE=": disc_type,
                    "CLOSE_DISC=": "YES",
                    "FORMAT=": "JOLIET",
                    "DATA=": absolute_data_path,
                    "REPLACE_FIELD=": path_of_replace_field_file,
                    "LABEL=": path_of_label_file}

        return jdf_skel