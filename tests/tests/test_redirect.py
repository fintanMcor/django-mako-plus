from django.test import TestCase

from django_mako_plus.router import ViewFunctionRouter
from django_mako_plus.util import log

import logging
import os, os.path


class Tester(TestCase):

    @classmethod
    def setUpTestData(cls):
        # skip debug messages during testing
        cls.loglevel = log.getEffectiveLevel()
        log.setLevel(logging.WARNING)

    @classmethod
    def tearDownTestData(cls):
        # set log level back to normal
        log.setLevel(cls.loglevel)


    def test_redirect_exception(self):
        resp = self.client.get('/tests/redirects.redirect_exception/')
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp['Location'], 'new_location')


    def test_permanent_redirect_exception(self):
        resp = self.client.get('/tests/redirects.permanent_redirect_exception/')
        self.assertEqual(resp.status_code, 301)
        self.assertEqual(resp['Location'], 'permanent_new_location')


    def test_javascript_redirect_exception(self):
        resp = self.client.get('/tests/redirects.javascript_redirect_exception/')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(b'javascript_new_location' in resp.content)


    def test_internal_redirect_exception(self):
        resp = self.client.get('/tests/redirects.internal_redirect_exception/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content, b'new_location2')


    def test_bad_internal_redirect_exception(self):
        resp = self.client.get('/tests/redirects.bad_internal_redirect_exception/')
        self.assertEqual(resp.status_code, 404)
        resp = self.client.get('/tests/redirects.bad_internal_redirect_exception2/')
        self.assertEqual(resp.status_code, 404)


    def test_bad_internal_redirect_exception(self):
        resp = self.client.get('/tests/redirects.bad_internal_redirect_exception/')
        self.assertEqual(resp.status_code, 404)
        resp = self.client.get('/tests/redirects.bad_internal_redirect_exception2/')
        self.assertEqual(resp.status_code, 404)

