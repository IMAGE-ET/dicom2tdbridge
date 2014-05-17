# _*_ coding: utf-8 _*_

__author__ = 'izamarro'
__version__ = '0.0.1a'

import os

from unittest import TestCase
from expects import expect

from jobs_worker import OrdersDirectoryHandler
from jobs_worker import JobsDirectoryHandler
from jobs_worker import JDFFilesHandler


class TestJobsDirectoryHandler(TestCase):

    def setUp(self):

        self.directory_job = "/home/izamarro/workdev/burner2/Test/temp/jobstest"
        self.patient_id = "9991"
        self.absolute_jobpath = self.directory_job + "/%s" % self.patient_id

        self.directory_creator = JobsDirectoryHandler(self.directory_job, self.patient_id, os)
        self.directory_creator.create_skel_job_directory()

    def tearDown(self):

        self.directory_creator.delete_job_directory()

    def test_when_directory_is_created_and_check_it_return_true(self):

        expect(self.directory_creator.check_if_job_directory_exist()).to.equal(True)

    def test_if_directory_already_exists_not_try_to_create(self):

        expect(self.directory_creator.create_skel_job_directory()).to.equal(False)

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

        self.jdf_handler = JDFFilesHandler(self.job_directory, self.file_name.split(".")[0], os)
        self.jdf_handler.create_jdf_file()

    def tearDown(self):

        os.remove(self.jdf_file_path)

    def test_when_check_for_jdf_file_and_exist_return_true(self):

        expect(self.jdf_handler.check_if_jdf_exist()).to.equal(True)

    def test_jdf_skel_must_have_required_information(self):

        jdf_fields = {"JOB_ID=": "=%s" % self.file_name.split(".")[0],
                      "PUBLISHER=": "publisher0",
                      "COPIES=": "1",
                      "DISC_TYPE=": "DVD",
                      "CLOSE_DISC=": "YES",
                      "FORMAT=": "JOLIET",
                      "DATA=": "/path/to/dat",
                      "REPLACE_FIELD=": "/path/to/dat",
                      "LABEL=": "/path/to/label"}

        expect(self.jdf_handler.get_jdf_skel(jdf_fields.get("PUBLISHER="),
                                             jdf_fields.get("COPIES="),
                                             jdf_fields.get("DISC_TYPE="),
                                             jdf_fields.get("DATA="),
                                             jdf_fields.get("REPLACE_FIELD="),
                                             jdf_fields.get("LABEL="))).to.have.keys(jdf_fields)

