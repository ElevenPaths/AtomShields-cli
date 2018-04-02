#!/usr/bin/env python
# -*- coding: utf8 -*-

#
# This file is part of AtomShields
# Copyright (C) ElevenPaths
#
# DESCRIPTION
# This file creates a CLI to interact with Atomshields
#

import os, sys
import argparse
import glob

from atomshields import *


class AtomshieldsCli(object):

	NAME = "AtomShields CLI"
	COMMAND = "ascli"

	ACTION_INSTALL = "install"
	ACTION_UNINSTALL = "uninstall"
	ACTION_SHOW = "show"
	ACTION_RUN = "run"
	ACTIONS = [ACTION_INSTALL, ACTION_UNINSTALL, ACTION_SHOW, ACTION_RUN]


	CONTEXT_CHECKERS = "checkers"
	CONTEXTS_REPORTS = "reports"
	CONTEXTS = [CONTEXT_CHECKERS, CONTEXTS_REPORTS]

	def __init__(self, verbose = False):
		"""
		Class constructor

		Args:
			verose(bool): True if the execution should run verboselly. False else
		"""
		self._context = None
		self._action = None
		self._path = None
		self._verbose = False
		self.verbose = verbose

	@property
	def context(self):
		"""
		Getter for 'context' property

		Returns:
			string: Execution context.
		"""
		return self._context

	@context.setter
	def context(self, value):
		"""
		Setter for 'context' property

		Args:
			value (str): Execution context.

		"""
		if value is not None:
			self._context = value.lower()
		else:
			self._context = value

	@property
	def verbose(self):
		"""
		Getter for 'verbose' property

		Returns:
			bool: Verbose flag.
		"""
		return self._verbose

	@verbose.setter
	def verbose(self, value):
		"""
		Setter for 'verbose' property

		Args:
			value (bool): Verbose flag.

		"""
		if value is not None and value:
			self._verbose = True
		else:
			self._verbose = False

	@property
	def action(self):
		"""
		Getter for 'action' property

		Returns:
			string: Action to execute.
		"""
		return self._action

	@action.setter
	def action(self, value):
		"""
		Setter for 'context' property

		Args:
			value (str): Action to execute.

		"""
		if value is not None:
			self._action = value.lower()
		else:
			self._action = value

	@property
	def path(self):
		"""
		Getter for 'path' property

		Returns:
			string: Path value.
		"""
		return self._path

	@path.setter
	def path(self, value):
		"""
		Setter for 'path' property

		Args:
			value (str): Path value.

		"""
		if value is not None and os.path.exists(value):
			self._path = os.path.abspath(value)
		else:
			self._path = value

	@property
	def name(self):
		"""
		Getter for 'name' property

		Returns:
			string: Project's name.
		"""
		return self._name

	@name.setter
	def name(self, value):
		"""
		Setter for 'name' property

		Args:
			value (str): Project's name.

		"""
		self._name = value



	def getPlugins(self, path, classArgs = None):
		"""
		Gets the plugins data. Find all the *.py files in <path> and returns his plugin name and description.

		Args:
			path(str): 	Path to find python files
			classArgs(str): Class arguments to instanciate the class

		Returns:
			dict:	Dictionary which contains the plugin's name as key, and the plugin's description as value.
		"""
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
		"""
		Prints the plugins into <path>.

		Args:
			path(str): 	Path to find python files
			classArgs(str): Class arguments to instanciate the class
		"""
		if classArgs is None:
			classArgs = {}

		items = self.getPlugins(path, classArgs)
		for k in items.keys():
			print "%-20s\t%-60s" % (k, items[k])

	def showCheckers(self):
		"""
		Prints all the checkers.
		"""
		print ""
		print "%-20s\t%-60s" % ("Name", "Description")
		print "-"*90
		self._show(path = AtomShieldsScanner.CHECKERS_DIR, classArgs = {})
		print ""

	def showReports(self):
		"""
		Prints all the reports.
		"""
		print ""
		print "%-20s\t%-60s" % ("Name", "Description")
		print "-"*90
		self._show(path = AtomShieldsScanner.REPORTS_DIR, classArgs = {})


	def printBanner(self):
		rows, columns = map(int, os.popen('stty size', 'r').read().split())
		import atomshieldscli.banner as banner
		print banner.small

	def execute(self):
		"""
		Perform the needed tasks
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

				# Print banner
				self.printBanner()
				instance = AtomShieldsScanner(self.path, verbose=self.verbose)
				instance.project = self.name
				instance.run()
			else:
				raise Exception("Invalid context. Allowed values: {values}".format(values=str(AtomshieldsCli.CONTEXTS)))

if __name__ == "__main__":

	# Get Args
	parser = argparse.ArgumentParser(prog=AtomshieldsCli.COMMAND, add_help=True,
		formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=50, width=120),
		description="""Performs an action into a context. The actions are defines in the first argument, and the context in the second. You also can set options.""",
		epilog="""For more documentation, please visit https://github.com/ElevenPaths/AtomShields-cli\n\n""")
	parser.add_argument("action", action="store", default="show", help="Set the action to do. Allowed values are: {actions}".format(actions=', '.join(AtomshieldsCli.ACTIONS)))
	parser.add_argument("context", nargs='?', action="store", default=None, help="Set the context to operate with checkers. Allowed values are: {contexts}".format(contexts=', '.join(AtomshieldsCli.CONTEXTS)))
	parser.add_argument("-t", "--target", action="store", metavar="path_to_scan", help="Set the target folder to scan. If action is install/uninstall, this value should be the absolute path to plugin. For uninstall action could be the plugin name.")
	parser.add_argument("-n", "--name", action="store", required=False, metavar="project_name", help="Set the project (repository) name")
	parser.add_argument("-v","--verbose", action="store_true", help="Run verbosely")
	args = parser.parse_args()


	# Check if action is allowed
	if args.action.lower() not in AtomshieldsCli.ACTIONS:
		raise Exception("Invalid action. Allowed values: {actions}".format(actions=str(AtomshieldsCli.ACTIONS)))



	cli = AtomshieldsCli(verbose = args.verbose)
	cli.context = args.context
	cli.action = args.action
	cli.path = args.target
	cli.name = args.name
	cli.execute()
