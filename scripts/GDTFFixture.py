import traceback

import pygdtf

from CallbacksExt import CallbacksExt
from TDStoreTools import StorageManager
TDF = op.TDModules.mod.TDFunctions

class GDTFFixture(CallbacksExt):
	"""
	GDTFFixture description
	"""
	def __init__(self, ownerComp):
		# the component to which this extension is attached
		self.ownerComp = ownerComp
		# the component to which data is stored
		self.dataComp = ownerComp.op('data')

		# init callbacks
		self.callbackDat = self.ownerComp.par.Callbackdat.eval()
		try:
			CallbacksExt.__init__(self, ownerComp)
		except:
			self.ownerComp.addScriptError(traceback.format_exc() + \
					"Error in CallbacksExt __init__. See textport.")
			print()
			print("Error initializing callbacks - " + self.ownerComp.path)
			print(traceback.format_exc())
		# run onInit callback
		try:
			self.DoCallback('onInit', {'exampleExt':self})
		except:
			self.ownerComp.addScriptError(traceback.format_exc() + \
					"Error in custom onInit callback. See textport.")
			print(traceback.format_exc())

		# properties
		# TDF.createProperty(self, 'MyProperty', value=0, dependable=True,
		# 				   readOnly=False)

		# stored items (persistent across saves and re-initialization):
		storedItems = [
			# Only 'name' is required...
			{'name': 'Data', 'default': None, 'readOnly': False,
			 						'property': True, 'dependable': True},
		]
		self.fixture = None
		self.stored = StorageManager(self, self.dataComp, storedItems)

	# do something in the future
	def _future(self, attrib, args=(), group_name=None, delayMilliSeconds=0, delayFrames=0):
		if group_name == None:
			group_name = self.ownerComp.name
		self.ownerComp.op('future').run(attrib, args, group=group_name, delayFrames=delayFrames, delayMilliSeconds=delayMilliSeconds)

	# kill all runs with group name
	def _killRuns(self, group_name):
		for r in runs:
			if r.group == group_name:
				r.kill()

	def Load(self, file=None):
		if file is None:
			file = self.ownerComp.par.Gdtffile.eval()
		self.fixture = pygdtf.FixtureType(file)

		print(self.fixture.dmx_profiles[0])

	# example method with callback
	def Start(self):
		self.DoCallback('onStart', {'data': 'start'})
		self._future('done', delayFrames=1)

	# example method with callback
	def done(self):
		self.DoCallback('onDone', {'data': 'start'})

	# example pulse parameter handler
	def pulse_Editextension(self):
		self.ownerComp.op('GDTFFixture').par.edit.pulse()

	def pulse_Start(self):
		self.Start()

	def pulse_Load(self):
		self.Load()