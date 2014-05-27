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

import subprocess
from unittest import TestCase

import os
from expects import expect
from resources.dcm4tdbridge import OrdersDirectoryHandler
from resources.dcm4tdbridge import JobsDirectoryHandler
from resources.dcm4tdbridge import JDFFilesHandler
from resources.dcm4tdbridge import DicomTagFile


class TestJobsDirectoryHandler(TestCase):

    def setUp(self):

        self.directory_job = "/home/izamarro/workdev/burner2/Test/temp/jobstest"
        self.patient_id = "9991"
        self.absolute_jobpath = self.directory_job + "/%s" % self.patient_id

        self.directory_creator = JobsDirectoryHandler(self.directory_job, self.patient_id, os)
        self.directory_creator.create_skel_job_directory()

    def tearDown(self):

        if self.directory_creator.check_if_job_directory_exist() is True:
            self.directory_creator.delete_job_directory()

    def test_when_directory_is_created_and_check_it_return_true(self):

        expect(self.directory_creator.check_if_job_directory_exist()).to.equal(True)

    def test_if_skel_job_directory_is_deleted(self):

        self.directory_creator.delete_job_directory()
        expect([self.directory_creator.check_if_job_directory_exist()]).to.equal([False])

    def test_if_dictionary_contain_job_directory_skel(self):

        expect(self.directory_creator.get_job_skel()).to.have.keys(
            {"absolute_job_path": self.absolute_jobpath,
             "data_job_path": (self.absolute_jobpath + "/DATA")})


class TestOrdersDirectoryHandler(TestCase):

    def setUp(self):

        self.directory = "/home/izamarro/workdev/burner2/Test/temp/orderstest"
        self.name = "9991"
        self.extension = ".DON"
        self.order_path = self.directory + "/%s" % self.name + self.extension
        self.orders_handling = OrdersDirectoryHandler(self.directory,
                                                      self.name, self.extension, os)

        with open(self.order_path, "w") as tempfile:
            tempfile.close()

    def tearDown(self):

        os.remove(os.path.join(self.directory, self.name + self.extension))

    def test_when_i_check_for_extension_and_exist_return_true(self):

        expect(self.orders_handling.check_if_order_exist()).to.equal(True)


class TestJDFFilesHandler(TestCase):

    def setUp(self):

        self.job_directory = "/home/izamarro/workdev/burner2/Test/temp/jdftest"
        self.file_name = "9991.JDF"
        self.jdf_file_path = self.job_directory + "/%s" % self.file_name.split(".")[0] + "/%s" % self.file_name

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

        pass
        os.remove(self.jdf_file_path)

    def test_when_check_for_jdf_file_and_exist_return_true(self):

        expect(self.jdf_handler.check_if_jdf_exist()).to.equal(True)

    def test_jdf_skel_must_have_required_information(self):

        expect(self.jdf_handler.get_jdf_skel()).to.have.keys(self.jdf_skel)


class TestDicomTagFile(TestCase):

    def setUp(self):
        self.dicomtag = DicomTagFile("/home/izamarro/workdev/burner2/Test/temp/dicomtest/941CDA9B/DICOM/6B3C060E",
                                     "/home/izamarro/workdev/burner2/Test/temp/dicomtest/941CDA9B/dicomtag.txt",
                                     subprocess,
                                     "/home/izamarro/workdev/burner2/DATA/tools/bin",
                                     "dcm2txt",
                                     os)

    def tearDown(self):
        #os.remove("/home/izamarro/workdev/burner2/Test/temp/dicomtest/941CDA9B/dicomtag.txt")
        pass

    def test_if_have_dicom_txt_info_file(self):

        self.dicomtag.create_dicom_tag_file()
        dicom_test_directory = "/home/izamarro/workdev/burner2/Test/temp/dicomtest/941CDA9B"
        expect(os.listdir(dicom_test_directory)).to.have("dicomtag.txt")
