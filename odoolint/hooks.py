# -*- coding: utf-8 -*-
# © 2016  Vauxoo (<http://www.vauxoo.com/>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import imp
import logging
import re
from contextlib import contextmanager

from odoo import tools

_logger = logging.getLogger(__name__)


DATA_FILE_NAME = None
DATA_FILE_SECTION = None
DATA_FILE_MODULE = None


@contextmanager
def file_info(filename, filesection, filemodule):
    """Change the file_info temporally
    """
    # pylint: disable=global-statement
    global DATA_FILE_NAME
    global DATA_FILE_SECTION
    global DATA_FILE_MODULE
    DATA_FILE_NAME = filename
    DATA_FILE_SECTION = filesection
    DATA_FILE_MODULE = filemodule
    try:
        yield
    finally:
        DATA_FILE_NAME = None
        DATA_FILE_SECTION = None
        DATA_FILE_MODULE = None


def get_file_info():
    """Return dictionary with file_name, section of file and module real name
    """
    return {
        'file_name': DATA_FILE_NAME,
        'section': DATA_FILE_SECTION,
        'module_real': DATA_FILE_MODULE,
    }


def monkey_patch_convert_file():
    """Monkey patch to odoo.tools.convert.convert_file method to add custom
    information for importation process.
    """
    convert_file_original = tools.convert.convert_file

    def convert_file(*args, **kwargs):
        module = len(args) >= 2 and args[1] or kwargs.get('module')
        filename = len(args) >= 3 and args[2] or kwargs.get('filename')
        section = len(args) >= 7 and args[6] or kwargs.get('kind')
        with file_info(filename, section, module):
            return convert_file_original(*args, **kwargs)
    tools.convert.convert_file = convert_file
    # Reload to propagate patch
    imp.reload(tools)


class WerkzeugFilter(logging.Filter):
    """Add a log error if there is a 404 code in the message"""

    def __init__(self, logger, level=None):
        self.__level = level
        self.__logger = logger
        super(WerkzeugFilter, self).__init__()

    def get_message_status_code(self, msg):
        re_res = re.search(r" (\d+) -$", msg)
        return re_res and int(re_res.group(1))

    def has_error(self, msg):
        status_code = self.get_message_status_code(msg)
        if status_code == 404:
            return True

    def filter(self, record):
        if self.__level is None or record.levelno != self.__level:
            return True
        msg = record.__dict__.get('msg') or ''
        if self.has_error(msg):
            self.__logger.error('werzeurg has error: %s', msg)
        return True


def patch_werkzeug_logger():
    werkzeug_logger = logging.getLogger('werkzeug')
    werkzeug_filter = WerkzeugFilter(_logger, logging.INFO)
    werkzeug_logger.addFilter(werkzeug_filter)


def post_load():
    _logger.info('Patching odoo.tools.convert.convert_file method')
    monkey_patch_convert_file()
    patch_werkzeug_logger()
