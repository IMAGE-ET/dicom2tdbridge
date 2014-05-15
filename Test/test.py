# _*_ coding: utf-8 _*_

__author__ = 'hlecter'
__version__ = '0.0.1a'

import os
from mock import Mock
from workerclass import JobsDirectoryHandler
from unittest import TestCase
from expects import expect


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