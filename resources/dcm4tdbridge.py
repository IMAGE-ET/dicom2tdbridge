"""
    resources_class
    Copyright (C) {2014}  {Ivan Zamarro Sanchez}

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along
    with this program; if not, write to the Free Software Foundation, Inc.,
    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA
"""

# _*_ coding: utf-8 _*_

__author__ = 'izamarro'
__version__ = '0.0.1a'


class JobsDirectoryHandler(object):

    def __init__(self, jobs_folder, patient_id, os_stat):
        self.__os = os_stat
        self.__jobs_directory = jobs_folder
        self.__patient_id = patient_id
        self.__absolute_job_data_folder = self.__os.path.join(self.__jobs_directory, self.__patient_id, "DATA")

    def check_if_job_directory_exist(self):

        if self.__os.path.exists(self.__absolute_job_data_folder)is True:

            return 1

        else:

            return 0

    def create_skel_job_directory(self):
        self.__os.mkdir(self.__os.path.join(self.__jobs_directory, self.__patient_id))
        self.__os.mkdir(self.__os.path.join(self.__absolute_job_data_folder))

    def delete_job_directory(self):
        self.__os.rmdir(self.__os.path.join(self.__absolute_job_data_folder))
        self.__os.rmdir(self.__os.path.join(self.__jobs_directory, self.__patient_id))


class OrdersDirectoryHandler(object):

    def __init__(self, orders_directory, job_id, order_extension, os_stat):

        self.__orders_directory = orders_directory
        self.__os = os_stat
        self.__extension = order_extension
        self.__order_name = job_id

    def check_if_order_exist(self):

        if self.__os.path.exists(self.__orders_directory + "/%s" % (self.__order_name + self.__extension)):
            return 1

        else:
            return 0


class JDFFilesHandler(object):

    def __init__(self, job_folder, job_id, name_of_publisher, number_of_copies, disc_type, absolute_data_path,
                 path_of_replace_field_file, path_of_label_file, os):

        self.job_folder = job_folder
        self.job_id = job_id
        self.__os = os
        self.__name_of_publisher = name_of_publisher
        self.__number_of_copies = number_of_copies
        self.__disc_type = disc_type
        self.__absolute_data_path = absolute_data_path
        self.__path_of_replace_field_file = path_of_replace_field_file
        self.__path_of_label_file = path_of_label_file

    def check_if_jdf_exist(self):
        if self.__os.path.exists(self.__os.path.join(self.job_folder, "%s.JDF" % self.job_id)) is True:

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

            with open(self.__os.path.join(self.job_folder, "%s.JDF" % self.job_id), "w") as jdf_file:

                for i in self.get_jdf_skel():

                    jdf_file.write((i + skel_of_jdffile.get(i) + "\n"))
