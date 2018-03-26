#!/usr/bin/env python
# -*- coding: utf8 -*-

import os, sys
import argparse
import glob

from atomshields import *


class AtomshieldsCli(object):

	NAME = "AtomShields CLI"

	ACTION_INSTALL = "install"
	ACTION_UNINSTALL = "uninstall"
	ACTION_SHOW = "show"
	ACTION_RUN = "run"
	ACTION_HELP = "help"
	ACTIONS = [ACTION_INSTALL, ACTION_UNINSTALL, ACTION_SHOW, ACTION_RUN, ACTION_HELP]


	CONTEXT_CHECKERS = "checkers"
	CONTEXTS_REPORTS = "reports"
	CONTEXTS = [CONTEXT_CHECKERS, CONTEXTS_REPORTS]

	def __init__(self, verbose = False):
		"""
		Class constructor
		"""
		self._context = None
		self._action = None
		self._path = None
		self._verbose = False
		self.verbose = verbose

	@property
	def context(self):
		return self._context

	@context.setter
	def context(self, value):
		if value is not None:
			self._context = value.lower()
		else:
			self._context = value

	@property
	def verbose(self):
		return self._verbose

	@verbose.setter
	def verbose(self, value):
		if value is not None and value:
			self._verbose = True
		else:
			self._verbose = False

	@property
	def action(self):
		return self._action

	@action.setter
	def action(self, value):
		if value is not None:
			self._action = value.lower()
		else:
			self._action = value	

	@property
	def path(self):
		return self._path

	@path.setter
	def path(self, value):
		if value is not None and os.path.exists(value):
			self._path = os.path.abspath(value)
		else:
			self._path = value

	@property
	def name(self):
		return self._name

	@name.setter
	def name(self, value):
		self._name = value




	def getFiles(self, path, extension="*.py", exclude=[]):
		_p = os.path.join(path, extension)
		return [fn for fn in glob.glob(_p) if not os.path.basename(fn) in exclude]

	def getPlugins(self, path, classArgs = None):
		
		if classArgs is None:
			classArgs = {}

		data = {}
		exclude = ["__init__.py", "base.py"]
		for f in AtomShieldsScanner._getFiles(path, "*.py", exclude=exclude):
			try:
				instance = AtomShieldsScanner._getClassInstance(path = f, args = classArgs)
				if instance is not None:
					data[instance.__class__.NAME] = instance.__class__.DESCRIPTION
			except Exception as e:
				AtomShieldsScanner._debug("[!] %s" % e)
		return data

	def _show(self, path, classArgs = None):
		if classArgs is None:
			classArgs = {}

		items = self.getPlugins(path, classArgs)
		for k in items.keys():
			print "%-20s\t%-60s" % (k, items[k])

	def showCheckers(self):
		print ""
		print "%-20s\t%-60s" % ("Name", "Description")
		print "-"*90
		self._show(path = AtomShieldsScanner.CHECKERS_DIR, classArgs = {})
		print ""

	def showReports(self):
		self._show(path = AtomShieldsScanner.REPORTS_DIR, classArgs = {})


	@staticmethod
	def help():
		return ""

	def execute(self):
		"""
		To perform the needed tasks
		"""
		if self.context == self.__class__.CONTEXT_CHECKERS:
			# Operate with checkers
			if self.action == self.__class__.ACTION_SHOW:
				self.showCheckers()
			elif self.action == self.__class__.ACTION_INSTALL:
				AtomShieldsScanner.installChecker(self.path)
			elif self.action == self.__class__.ACTION_UNINSTALL:
				if self.path.endswith(".py"):
					AtomShieldsScanner.uninstallPlugin(path = self.path)
				else:
					# Path must be NAME
					AtomShieldsScanner.uninstallChecker(self.path)
		elif self.context == self.__class__.CONTEXTS_REPORTS:
			# Operate with reports
			if self.action == self.__class__.ACTION_SHOW:
				self.showReports()
			elif self.action == self.__class__.ACTION_INSTALL:
				AtomShieldsScanner.installReport(self.path)
			elif self.action == self.__class__.ACTION_UNINSTALL:
				if self.path.endswith(".py"):
					AtomShieldsScanner.uninstallPlugin(path = self.path)
				else:
					# Path must be NAME
					AtomShieldsScanner.uninstallReport(self.path)
		else:

			# Check if context is not needed
			if self.action.lower() == self.__class__.ACTION_RUN:
				# Run the scan
				if self.path is None:
					raise Exception("You must set a target path.")
				instance = AtomShieldsScanner(self.path, verbose=self.verbose)
				instance.project = self.name
				instance.run()
			else:
				raise Exception("Invalid context. Allowed values: {values}".format(values=str(AtomshieldsCli.CONTEXTS)))

if __name__ == "__main__":

	# Get Args
	parser = argparse.ArgumentParser(prog=AtomshieldsCli.NAME)
	parser.add_argument("action", action="store", default="show", help="Set the action to do")
	parser.add_argument("context", nargs='?', action="store", default=None, help="Set the context to operate with checkers")
	parser.add_argument("--target", action="store", metavar="path_to_scan", help="Set the target folder to scan")
	parser.add_argument("--name", action="store", required=False, metavar="project_name", help="Set the project (repo) name")
	parser.add_argument("-v","--verbose", action="store_true", help="Run verboselly")
	args = parser.parse_args()


	# Check if action is allowed
	if args.action.lower() not in AtomshieldsCli.ACTIONS:
		raise Exception("Invalid action. Allowed values: {actions}".format(actions=str(AtomshieldsCli.ACTIONS)))


	# Print Help
	if args.action.lower() == AtomshieldsCli.ACTION_HELP:
		print AtomshieldsCli.help()


	cli = AtomshieldsCli(verbose = args.verbose)
	cli.context = args.context
	cli.action = args.action
	cli.path = args.target
	cli.name = args.name
	cli.execute()



