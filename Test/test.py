# _*_ coding: utf-8 _*_

__author__ = 'izamarro'
__version__ = '0.0.1a'

import os
from mock import Mock
from unittest import TestCase
from expects import expect

from workerclass import OrdersFileHandler
from workerclass import JobsDirectoryHandler


class TestJobsDirectoryHandler(TestCase):

    def setUp(self):

        self.date_for_job = Mock()
        self.date_for_job.directory_job = "/home/izamarro/workdev/burner2/Test/temp"
        self.date_for_job.patient_id = "9991"
        self.date_for_job.absolute_jobpath = self.date_for_job.directory_job + "/%s" % self.date_for_job.patient_id

        self.directory_creator = JobsDirectoryHandler(self.date_for_job.directory_job, self.date_for_job.patient_id, os)
        self.directory_creator.create_absolute_job_path_directory()

    def tearDown(self):

        os.rmdir(self.date_for_job.absolute_jobpath)

    def test_if_directory_is_created_in_job_directory(self):

        expect([self.directory_creator.get_job_directory_path()]).to.have(self.date_for_job.absolute_jobpath)

    def test_if_directory_already_exists_not_try_to_create(self):

        expect([self.directory_creator.create_absolute_job_path_directory()]).to.equal([False])


class TestOrdersDirectoryHandler(TestCase):

    def setUp(self):

        self.file_needs = Mock()
        self.file_needs.directory = "/home/izamarro/workdev/burner2/Test/temp/orderstest"
        self.file_needs.name = "9991"
        self.file_needs.extension = ".DON"
        self.file_needs.order_path = self.file_needs.directory + "/%s" % self.file_needs.name + \
                                     self.file_needs.extension

        self.orders_handling = OrdersFileHandler(self.file_needs.directory, self.file_needs.extension, os)

        with open(self.file_needs.order_path, "w") as tempfile:
            tempfile.close()

    def tearDown(self):

        os.remove(os.path.join(self.file_needs.directory, self.file_needs.name + self.file_needs.extension))

    def test_if_return_the_filename_without_file_extension(self):

        expect([self.orders_handling.get_order_file_name_askey_and_extension_asvalue()]).to.equal([{self.file_needs.name: self.file_needs.extension}])
