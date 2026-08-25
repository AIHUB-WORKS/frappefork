# Copyright (c) 2026, Frappe Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE

import logging
import unittest

import frappe
from frappe.utils.logger import get_logger


class TestLogger(unittest.TestCase):
	def test_reuses_handlers_when_frappe_logger_cache_is_reset(self):
		logger_name = "test-logger-cache-reset-all"
		logger = logging.getLogger(logger_name)
		original_handlers = logger.handlers[:]
		original_loggers = frappe.loggers

		try:
			logger.handlers.clear()
			frappe.loggers = {}

			first = get_logger(module="test-logger-cache-reset", allow_site=False, stream_only=True)
			frappe.loggers = {}
			second = get_logger(module="test-logger-cache-reset", allow_site=False, stream_only=True)

			self.assertIs(first, second)
			self.assertEqual(1, len(second.handlers))
		finally:
			for handler in logger.handlers:
				handler.close()
			logger.handlers[:] = original_handlers
			frappe.loggers = original_loggers
