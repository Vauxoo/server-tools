# -*- coding: utf-8 -*-

import logging

from openerp.tests import HttpCase


class TestFilter(logging.Filter):
    """Class to add the record logging filtered in `self.buffer`
    and don't show it
    """

    def __init__(self, level=None):
        super(TestFilter, self).__init__()
        self.buffer = []
        self.__level = level

    def filter(self, record):
        if self.__level is None or record.levelno != self.__level:
            return True
        self.buffer.append(record.__dict__)


class TestWerkzeug404(HttpCase):
    def setUp(self):
        super(TestWerkzeug404, self).setUp()
        self.__logger_filter = TestFilter(logging.ERROR)
        for logger in ['openerp.addons.odoolint.hooks', 'openerp.netsvc']:
            self.__logger = logging.getLogger(logger)
            self.__logger.addFilter(self.__logger_filter)

    def tearDown(self):
        super(TestWerkzeug404, self).tearDown()
        self.__logger.removeFilter(self.__logger_filter)

    def test_werkzeug_404(self):
        self.phantom_js('/no_exists', "console.log('ok')", "console")
        self.assertEqual(len(self.__logger_filter.buffer), 2)
