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

    def __init__(self, jobs_folder, viewer_absolute_path, patient_id,  os_stat, shutil):
        self.__os = os_stat
        self.__jobs_directory = jobs_folder
        self.__patient_id = patient_id
        self.viewer = viewer_absolute_path
        self.__shutil = shutil
        self.__absolute_job_data_folder = self.__os.path.join(self.__jobs_directory, self.__patient_id, "DATA")

    def check_if_job_directory_exist(self):
        if self.__os.path.exists(self.__absolute_job_data_folder)is True:

            return 1

        else:

            return 0

    def create_skel_job_directory(self):
        #Create Job Folder, with Patient ID
        self.__shutil.copytree(self.viewer, self.__absolute_job_data_folder)


class OrdersDirectoryHandler(object):

    def __init__(self, orders_directory, job_id, order_extension, os_stat):
        self.__orders_directory = orders_directory
        self.__os = os_stat
        self.__extension = order_extension
        self.__order_name = job_id

    def check_if_order_exist(self):
        if self.__os.path.exists(self.__os.path.join(self.__orders_directory, (self.__order_name + self.__extension))):

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

            return 1

        else:

            return 0

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

                for jdf_content in self.get_jdf_skel():

                    jdf_file.write((jdf_content + skel_of_jdffile.get(jdf_content) + "\n"))


class DCMTagParser(object):

    def __init__(self, os, subprocess, path_of_dicom_to_parse, path_to_dcm2txt_tool_folder):
        self.__os = os
        self.__subprocess = subprocess
        self.dicom_to_parse = path_of_dicom_to_parse
        self.parser_tool_folder = path_to_dcm2txt_tool_folder

    def get_tag(self, dicom_tag_to_extract):
        self.__os.chdir(self.parser_tool_folder)

        dicom_tag_line = self.get_tag_line(dicom_tag_to_extract)

        parser = self.__subprocess.Popen(["powershell", ".\dcm2txt.bat -c %s | Select-String %s" %
                                          (self.dicom_to_parse, dicom_tag_line)],
                                         stdout=self.__subprocess.PIPE, shell=True)
        parser_out = parser.stdout.read()

        #Data is closed between brackets, its reformat the string.
        brackets_positions = [parser_out.find("["), parser_out.find("]")]
        dicom_tag_containt = parser_out[brackets_positions[0]+1:brackets_positions[1]]

        return dicom_tag_containt

    def get_tag_line(self, tag):

        dicom_tags = {00100020: "1462",
                      00100010: "1450"}

        return dicom_tags.get(tag)


class DCMPathHandler(object):

    def __init__(self, dicom_folder_absolute_path, absolute_out_path, shutil, os):
        self.__os = os
        self.__shutil = shutil
        self._dicom_path = dicom_folder_absolute_path
        self._viewer_path = absolute_out_path

    def add_dicom_to_viewer(self):
        self.__shutil.copytree(self._dicom_path, self._viewer_path)

    def get_number_of_dicoms_arrived(self):
        number = len(range(len(self.__os.listdir(self._dicom_path))))

        return number
