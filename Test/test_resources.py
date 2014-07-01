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

import os
import subprocess
import shutil

from unittest import TestCase
from expects import expect

from resources.resources import OrdersDirectoryHandler
from resources.resources import JobsDirectoryHandler
from resources.resources import JDFFilesHandler
from resources.resources import DCMTagParser
from resources.resources import DCMPathHandler


class TestJobsDirectoryHandler(TestCase):

    def setUp(self):
        self.directory_job = os.path.join(os.getcwd(), "temps")
        self.patient_id = "7rAgWJ."
        self.absolute_jobpath = os.path.join(self.directory_job, self.patient_id)
        self.directory_creator = JobsDirectoryHandler(self.directory_job, os.path.join(os.getcwd(), "..", "viewer"),
                                                      self.patient_id, os, shutil)
        self.directory_creator.create_skel_job_directory()

    def tearDown(self):
        if self.directory_creator.check_if_job_directory_exist() == 1:
            shutil.rmtree("temps/7rAgWJ.")

        else:
            pass

    def test_it_must_return_1_if_directory_is_created(self):
        expect(self.directory_creator.check_if_job_directory_exist()).to.equal(1)


class TestOrdersDirectoryHandler(TestCase):

    def setUp(self):
        self.directory = os.path.join(os.getcwd(), "temps", "job")
        self.name = "7rAgWJ"
        self.extension = ".DON"
        self.order_path = self.directory + "\\%s" % self.name + self.extension
        self.orders_handling = OrdersDirectoryHandler(self.directory,
                                                      self.name, self.extension, os)

    def tearDown(self):
        if self.orders_handling.check_if_order_exist() == 1:
            os.remove(os.path.join(self.directory, self.name + self.extension))

        else:
            pass

    def test_it_must_return_1_if_order_exist(self):
        with open(self.order_path, "w") as temp_file:
            temp_file.close()

        expect(self.orders_handling.check_if_order_exist()).to.equal(1)

    def test_it_must_return_0_if_order_not_exist(self):
        expect(self.orders_handling.check_if_order_exist()).to.equal(0)


class TestJDFFilesHandler(TestCase):

    def setUp(self):
        self.job_directory = os.path.join(os.getcwd(), "temps")
        self.file_name = "7rAgWJ.JDF"
        self.jdf_file_path = self.job_directory + "/%s" % self.file_name

        self.jdf_skel = {"JOB_ID=": "%s" % self.file_name.split(".")[0],
                         "PUBLISHER=": "publisher0",
                         "COPIES=": "1",
                         "DISC_TYPE=": "DVD",
                         "CLOSE_DISC=": "YES",
                         "FORMAT=": "JOLIET",
                         "DATA=": "/path/to/dat",
                         "REPLACE_FIELD=": "/path/to/dat",
                         "LABEL=": "/path/to/label"}

        self.jdf_handler = JDFFilesHandler(self.job_directory,
                                           self.jdf_skel.get("JOB_ID="),
                                           self.jdf_skel.get("PUBLISHER="),
                                           self.jdf_skel.get("COPIES="),
                                           self.jdf_skel.get("DISC_TYPE="),
                                           self.jdf_skel.get("DATA="),
                                           self.jdf_skel.get("REPLACE_FIELD="),
                                           self.jdf_skel.get("LABEL="),
                                           os)

        self.jdf_handler.create_jdf_file()

    def tearDown(self):
        os.remove(self.jdf_file_path)

    def test_it_must_retrun_1_if_JDF_exist(self):
        expect(self.jdf_handler.check_if_jdf_exist()).to.equal(1)

    def test_it_must_return_jdf_required_information(self):
        expect(self.jdf_handler.get_jdf_skel()).to.have.keys(self.jdf_skel)


class TestDCMTagParser(TestCase):

    def setUp(self):
        self.current_dir = os.getcwd()
        self.dicom_parser = DCMTagParser(os, subprocess, os.path.join(self.current_dir, "temps",
                                                                      "dicom", "testdicom.dcm"),
                                         os.path.join(self.current_dir, "..", "tools", "bin"))
        os.chdir(os.path.join(self.current_dir, "..", "tools", "bin"))

    def tearDown(self):
        os.chdir(self.current_dir)

    def test_it_must_return_parsed_lines(self):
        expect(self.dicom_parser.get_tag_line(00100020)).to.equal("1462")
        expect(self.dicom_parser.get_tag_line(00100010)).to.equal("1450")

    def test_it_must_return_selected_tags(self):
        expect(self.dicom_parser.get_tag(00100020)).to.equal("7rAgWJ.")
        expect(self.dicom_parser.get_tag(00100010)).to.equal("WRIX")


class TestDCMPathHandler(TestCase):

    def setUp(self):
        dicom_folder_absolute_path = os.path.join(os.getcwd(), "temps", "dicom")
        absolute_out_path = os.path.join(os.getcwd(), "temps", "job", "dicom")
        self.dicom_handler = DCMPathHandler(dicom_folder_absolute_path, absolute_out_path, shutil, os)

    def tearDown(self):
        if os.path.isdir(os.path.join(os.getcwd(), "temps", "job", "dicom")) is True:
            shutil.rmtree(os.path.join(os.getcwd(), "temps", "job", "dicom"))

        else:
            pass

    def test_it_must_move_dicom_folders(self):
        self.dicom_handler.add_dicom_to_viewer()

        expect(os.listdir(os.path.join(os.getcwd(), "temps", "job"))).to.have("dicom")

    def test_it_must_return_number_of_dicom_in_folder(self):
        expect(self.dicom_handler.get_number_of_dicoms_arrived()).to.equal(12)
