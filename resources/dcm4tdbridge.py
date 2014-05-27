# _*_ coding: utf-8 _*_

__author__ = 'izamarro'
__version__ = '0.0.1a'


class JobsDirectoryHandler(object):

    def __init__(self, jobs_directory, patient_id, os_stat):

        self.__jobs_directory = jobs_directory
        self.__patient_id = patient_id
        self.__absolute_job_path = self.__jobs_directory + ("/%s" % self.__patient_id)
        self.__os = os_stat

    def check_if_job_directory_exist(self):

        if self.__os.path.exists(self.get_job_skel()["absolute_job_path"]) is True:

            return True

        else:

            return False

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

    def __init__(self, job_directory, job_id, name_of_publisher, number_of_copies, disc_type, absolute_data_path,
                 path_of_replace_field_file, path_of_label_file, os):

        self.job_id = job_id
        self.jdf_path = job_directory + "/%s" % job_id + "/%s" % (job_id + ".JDF")
        self.__os = os
        self.__name_of_publisher = name_of_publisher
        self.__number_of_copies = number_of_copies
        self.__disc_type = disc_type
        self.__absolute_data_path = absolute_data_path
        self.__path_of_replace_field_file = path_of_replace_field_file
        self.__path_of_label_file = path_of_label_file

    def check_if_jdf_exist(self):

        if self.__os.path.exists(self.jdf_path) is True:

            return True

        else:
            return False

    def get_jdf_skel(self):

        jdf_skel = {"JOB_ID=": "%s" % self.job_id,
                    "PUBLISHER=": self.__name_of_publisher,
                    "COPIES=": self.__number_of_copies,
                    "DISC_TYPE=": self.__disc_type,
                    "CLOSE_DISC=": "YES",
                    "FORMAT=": "JOLIET",
                    "DATA=": self.__absolute_data_path,
                    "REPLACE_FIELD=": self.__path_of_replace_field_file,
                    "LABEL=": self.__path_of_label_file}

        return jdf_skel

    def create_jdf_file(self):

            skel_of_jdffile = self.get_jdf_skel()

            with open(self.jdf_path, "w") as jdf_file:

                for i in self.get_jdf_skel():

                    jdf_file.write((i + skel_of_jdffile.get(i) + "\n"))


class DicomTagFile(object):

    def __init__(self, dicom_file_path, out_file_path, subprocess_control, dcm_tool_directory, tool_name, os):

        self.dicom_to_parse = dicom_file_path
        self.out_directory = out_file_path
        self.subprocess = subprocess_control
        self.tools_directory = dcm_tool_directory
        self.tool = tool_name
        self.os = os

    def create_dicom_tag_file(self):
            self.os.chdir(self.tools_directory)
            self.subprocess.call([".//%s -c %s > %s" % (self.tool, self.dicom_to_parse, self.out_directory)], shell=True)

