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
from unittest import TestCase
from expects import expect

from resources.resources import OrdersDirectoryHandler
from resources.resources import JobsDirectoryHandler
from resources.resources import JDFFilesHandler
from resources.resources import DCMTagParser


class TestJobsDirectoryHandler(TestCase):

    def setUp(self):
        self.directory_job = os.path.join(os.getcwd(), "temps")
        self.patient_id = "9991"
        self.absolute_jobpath = os.path.join(self.directory_job, self.patient_id)
        self.directory_creator = JobsDirectoryHandler(self.directory_job, self.patient_id, os)
        self.directory_creator.create_skel_job_directory()

    def tearDown(self):
        if self.directory_creator.check_if_job_directory_exist() == 1:
            self.directory_creator.delete_job_directory()

        else:
            pass

    def test_when_directory_is_created_and_check_it_return_1(self):
        expect(self.directory_creator.check_if_job_directory_exist()).to.equal(1)

    def test_if_skel_job_directory_is_deleted(self):
        self.directory_creator.delete_job_directory()
        expect(self.directory_creator.check_if_job_directory_exist()).to.equal(0)


class TestOrdersDirectoryHandler(TestCase):

    def setUp(self):
        self.directory = os.path.join(os.getcwd(), "temps", "orders")
        self.name = "9991"
        self.extension = ".DON"
        self.order_path = self.directory + "/%s" % self.name + self.extension
        self.orders_handling = OrdersDirectoryHandler(self.directory,
                                                      self.name, self.extension, os)

    def tearDown(self):
        if self.orders_handling.check_if_order_exist() == 1:
            os.remove(os.path.join(self.directory, self.name + self.extension))

        else:
            pass

    def test_when_i_check_for_extension_and_exist_return_1(self):
        with open(self.order_path, "w") as temp_file:
            temp_file.close()

        expect(self.orders_handling.check_if_order_exist()).to.equal(1)

    def test_when_check_for_extension_and_not_exist_return_0(self):
        expect(self.orders_handling.check_if_order_exist()).to.equal(0)


class TestJDFFilesHandler(TestCase):

    def setUp(self):

        self.job_directory = os.path.join(os.getcwd(), "temps", "orders")
        self.file_name = "9991.JDF"
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

    def test_when_check_for_jdf_file_and_exist_return_1(self):
        expect(self.jdf_handler.check_if_jdf_exist()).to.equal(1)

    def test_jdf_skel_must_have_required_information(self):
        expect(self.jdf_handler.get_jdf_skel()).to.have.keys(self.jdf_skel)


class TestDCMTagParser(TestCase):

    def setUp(self):
        current_dir = os.getcwd()
        self.dicomtag = DCMTagParser(os.path.join(os.getcwd(), "temps", "testdicom.dcm"),
                                     os.path.join(os.getcwd(), "temps", "tags.txt"),
                                     os.path.join(os.getcwd(), "..", "tools", "bin"), "dcm2txt.bat", subprocess, os)

        self.dicomtag.extract_tags_from_dicomfile()
        os.chdir(current_dir)

    def tearDown(self):
        os.remove(os.path.join(os.getcwd(), "temps", "tags.txt"))

    def test_when_passed_an_dicom_path_must_write_pipeline_in_a_file(self):
        expect(os.listdir(os.path.join(os.getcwd(), "temps"))).to.have("tags.txt")

    def test_when_call_a_method_for_parser_tagfile_return_dictionary(self):
        expect(self.dicomtag.extract_tags_from_tagfile()).to.have.keys("patient_id", "patient_name")
