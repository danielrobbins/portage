# Copyright 2017 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2

import functools
import random

from portage import os
from portage.tests import TestCase
from portage.util._eventloop.global_event_loop import global_event_loop
from portage.util.futures.futures import Future

class CallSoonFifoTestCase(TestCase):

	def testCallSoonFifo(self):

		inputs = [random.random() for index in range(10)]
		outputs = []
		finished = Future()

		def add_output(value):
			outputs.append(value)
			if len(outputs) == len(inputs):
				finished.set_result(True)

		event_loop = global_event_loop()
		for value in inputs:
			event_loop.call_soon(functools.partial(add_output, value))

		event_loop.run_until_complete(finished)
		self.assertEqual(inputs, outputs)
