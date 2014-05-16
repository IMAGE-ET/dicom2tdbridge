# _*_ coding: utf-8 _*_

__author__ = 'izamarro'
__version__ = '0.0.1a'

import os
from mock import Mock
from unittest import TestCase
from expects import expect

from jobs_worker import OrdersDirectoryHandler
from jobs_worker import JobsDirectoryHandler
from jobs_worker import JDFFilesHandler


class TestJobsDirectoryHandler(TestCase):

    def setUp(self):

        self.date_for_job = Mock()
        self.date_for_job.directory_job = "/home/izamarro/workdev/burner2/Test/temp/jobstest"
        self.date_for_job.patient_id = "9991"
        self.date_for_job.absolute_jobpath = self.date_for_job.directory_job + "/%s" % self.date_for_job.patient_id

        self.directory_creator = JobsDirectoryHandler(self.date_for_job.directory_job, self.date_for_job.patient_id, os)
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
            {"absolute_job_path": self.date_for_job.absolute_jobpath,
             "data_job_path": (self.date_for_job.absolute_jobpath + "/DATA")})


class TestOrdersDirectoryHandler(TestCase):

    def setUp(self):

        self.file_needs = Mock()
        self.file_needs.directory = "/home/izamarro/workdev/burner2/Test/temp/orderstest"
        self.file_needs.name = "9991"
        self.file_needs.extension = ".DON"
        self.file_needs.order_path = self.file_needs.directory + "/%s" \
                                                                 % self.file_needs.name + self.file_needs.extension
        self.orders_handling = OrdersDirectoryHandler(self.file_needs.directory,
                                                      self.file_needs.name, self.file_needs.extension, os)

        with open(self.file_needs.order_path, "w") as tempfile:
            tempfile.close()

    def tearDown(self):

        os.remove(os.path.join(self.file_needs.directory, self.file_needs.name + self.file_needs.extension))

    def test_when_i_check_for_extension_and_exist_return_true(self):

        expect(self.orders_handling.check_if_order_exist()).to.equal(True)


class TestJDFFilesHandler(TestCase):

    def setUp(self):

        self.jdf_needs = Mock()
        self.jdf_needs.job_directory = "/home/izamarro/workdev/burner2/Test/temp/jobstest"
        self.jdf_needs.file_name = "9991.JDF"
        self.jdf_file_path = self.jdf_needs.job_directory + "/%s" % self.jdf_needs.file_name.split(".")[0] + "/%s" % self.jdf_needs.file_name

        self.jdf_handler = JDFFilesHandler(self.jdf_needs.job_directory, self.jdf_needs.file_name.split(".")[0], os)

        self.directory_handler = JobsDirectoryHandler(self.jdf_needs.job_directory,
                                                      self.jdf_needs.file_name.split(".")[0], os)

        self.directory_handler.create_skel_job_directory()

    def tearDown(self):

        os.remove(self.jdf_file_path)
        self.directory_handler.delete_job_directory()

    def test_when_check_for_jdf_file_and_exist_return_true(self):

        self.jdf_handler.create_jdf_file()
        expect(self.jdf_handler.check_if_jdf_exist()).to.equal(True)





