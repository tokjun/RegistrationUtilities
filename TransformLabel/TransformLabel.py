import os
import unittest
from __main__ import vtk, qt, ctk, slicer

#
# TransformLabel
#

class TransformLabel:
  def __init__(self, parent):
    parent.title = "TransformLabel" # TODO make this more human readable by adding spaces
    parent.categories = ["Examples"]
    parent.dependencies = []
    parent.contributors = ["Jean-Christophe Fillion-Robin (Kitware), Steve Pieper (Isomics)"] # replace with "Firstname Lastname (Org)"
    parent.helpText = """
    This is an example of scripted loadable module bundled in an extension.
    """
    parent.acknowledgementText = """
    This file was originally developed by Jean-Christophe Fillion-Robin, Kitware Inc. and Steve Pieper, Isomics, Inc.  and was partially funded by NIH grant 3P41RR013218-12S1.
""" # replace with organization, grant and thanks.
    self.parent = parent

    # Add this test to the SelfTest module's list for discovery when the module
    # is created.  Since this module may be discovered before SelfTests itself,
    # create the list if it doesn't already exist.
    try:
      slicer.selfTests
    except AttributeError:
      slicer.selfTests = {}
    slicer.selfTests['TransformLabel'] = self.runTest

  def runTest(self):
    #tester = TransformLabelTest()
    #tester.runTest()
    pass

#
# qTransformLabelWidget
#

class TransformLabelWidget:
  def __init__(self, parent = None):
    if not parent:
      self.parent = slicer.qMRMLWidget()
      self.parent.setLayout(qt.QVBoxLayout())
      self.parent.setMRMLScene(slicer.mrmlScene)
    else:
      self.parent = parent
    self.layout = self.parent.layout()
    if not parent:
      self.setup()
      self.parent.show()

  def setup(self):
    # Instantiate and connect widgets ...

    #
    # Reload and Test area
    #
    reloadCollapsibleButton = ctk.ctkCollapsibleButton()
    reloadCollapsibleButton.text = "Reload && Test"
    self.layout.addWidget(reloadCollapsibleButton)
    reloadFormLayout = qt.QFormLayout(reloadCollapsibleButton)

    # reload button
    # (use this during development, but remove it when delivering
    #  your module to users)
    self.reloadButton = qt.QPushButton("Reload")
    self.reloadButton.toolTip = "Reload this module."
    self.reloadButton.name = "TransformLabel Reload"
    reloadFormLayout.addWidget(self.reloadButton)
    self.reloadButton.connect('clicked()', self.onReload)

    #
    # Parameters Area
    #
    parametersCollapsibleButton = ctk.ctkCollapsibleButton()
    parametersCollapsibleButton.text = "Parameters"
    self.layout.addWidget(parametersCollapsibleButton)

    # Layout within the dummy collapsible button
    parametersFormLayout = qt.QFormLayout(parametersCollapsibleButton)

    #
    # input volume selector
    #
    self.inputSelector = slicer.qMRMLNodeComboBox()
    self.inputSelector.nodeTypes = ( ("vtkMRMLScalarVolumeNode"), "" )
    self.inputSelector.addAttribute( "vtkMRMLScalarVolumeNode", "LabelMap", 1)
    self.inputSelector.selectNodeUponCreation = False
    self.inputSelector.addEnabled = False
    self.inputSelector.removeEnabled = False
    self.inputSelector.noneEnabled = True
    self.inputSelector.showHidden = False
    self.inputSelector.showChildNodeTypes = False
    self.inputSelector.setMRMLScene( slicer.mrmlScene )
    self.inputSelector.setToolTip( "Pick the input to the algorithm." )
    parametersFormLayout.addRow("Input Volume: ", self.inputSelector)

    #
    # output volume selector
    #
    self.outputSelector = slicer.qMRMLNodeComboBox()
    self.outputSelector.nodeTypes = ( ("vtkMRMLScalarVolumeNode"), "" )
    self.outputSelector.addAttribute( "vtkMRMLScalarVolumeNode", "LabelMap", 1)
    self.outputSelector.selectNodeUponCreation = True
    self.outputSelector.addEnabled = True
    self.outputSelector.removeEnabled = True
    self.outputSelector.noneEnabled = True
    self.outputSelector.showHidden = False
    self.outputSelector.showChildNodeTypes = False
    self.outputSelector.setMRMLScene( slicer.mrmlScene )
    self.outputSelector.setToolTip( "Pick the output to the algorithm." )
    parametersFormLayout.addRow("Output Volume: ", self.outputSelector)

    #
    # reference volume selector
    #
    self.referenceSelector = slicer.qMRMLNodeComboBox()
    self.referenceSelector.nodeTypes = ( ("vtkMRMLScalarVolumeNode"), "" )
    self.referenceSelector.addAttribute( "vtkMRMLScalarVolumeNode", "LabelMap", 0)
    self.referenceSelector.selectNodeUponCreation = False
    self.referenceSelector.addEnabled = True
    self.referenceSelector.removeEnabled = True
    self.referenceSelector.noneEnabled = True
    self.referenceSelector.showHidden = False
    self.referenceSelector.showChildNodeTypes = False
    self.referenceSelector.setMRMLScene( slicer.mrmlScene )
    self.referenceSelector.setToolTip( "Pick the reference to the algorithm." )
    parametersFormLayout.addRow("Reference Volume: ", self.referenceSelector)

    #
    # First Transform
    #
    self.firstTransformSelector = slicer.qMRMLNodeComboBox()
    self.firstTransformSelector.nodeTypes = ( ("vtkMRMLBSplineTransformNode"), "" )
    self.firstTransformSelector.selectNodeUponCreation = False
    self.firstTransformSelector.addEnabled = True
    self.firstTransformSelector.removeEnabled = True
    self.firstTransformSelector.noneEnabled = True
    self.firstTransformSelector.showHidden = False
    self.firstTransformSelector.showChildNodeTypes = False
    self.firstTransformSelector.setMRMLScene( slicer.mrmlScene )
    self.firstTransformSelector.setToolTip( "Pick the output to the algorithm." )
    parametersFormLayout.addRow("1st Transform: ", self.firstTransformSelector)

    #
    # Apply Button
    #
    self.applyButton = qt.QPushButton("Apply")
    self.applyButton.toolTip = "Run the algorithm."
    self.applyButton.enabled = False
    parametersFormLayout.addRow(self.applyButton)

    # connections
    self.applyButton.connect('clicked(bool)', self.onApplyButton)
    self.inputSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)
    self.outputSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)

    # Add vertical spacer
    self.layout.addStretch(1)

  def cleanup(self):
    pass

  def onSelect(self):
    if self.inputSelector.currentNode() != 0:
      if self.outputSelector.currentNode() != 0:
        self.applyButton.enabled = self.inputSelector.currentNode() and self.outputSelector.currentNode()

  def onApplyButton(self):
    logic = TransformLabelLogic()
    print("Run the algorithm")
    logic.run(self.inputSelector.currentNode(), self.outputSelector.currentNode(), self.referenceSelector.currentNode(), self.firstTransformSelector.currentNode())

  def onReload(self,moduleName="TransformLabel"):
    """Generic reload method for any scripted module.
    ModuleWizard will subsitute correct default moduleName.
    """
    import imp, sys, os, slicer

    widgetName = moduleName + "Widget"

    # reload the source code
    # - set source file path
    # - load the module to the global space
    filePath = eval('slicer.modules.%s.path' % moduleName.lower())
    p = os.path.dirname(filePath)
    if not sys.path.__contains__(p):
      sys.path.insert(0,p)
    fp = open(filePath, "r")
    globals()[moduleName] = imp.load_module(
        moduleName, fp, filePath, ('.py', 'r', imp.PY_SOURCE))
    fp.close()

    # rebuild the widget
    # - find and hide the existing widget
    # - create a new widget in the existing parent
    parent = slicer.util.findChildren(name='%s Reload' % moduleName)[0].parent().parent()
    for child in parent.children():
      try:
        child.hide()
      except AttributeError:
        pass
    # Remove spacer items
    item = parent.layout().itemAt(0)
    while item:
      parent.layout().removeItem(item)
      item = parent.layout().itemAt(0)

    # delete the old widget instance
    if hasattr(globals()['slicer'].modules, widgetName):
      getattr(globals()['slicer'].modules, widgetName).cleanup()

    # create new widget inside existing parent
    globals()[widgetName.lower()] = eval(
        'globals()["%s"].%s(parent)' % (moduleName, widgetName))
    globals()[widgetName.lower()].setup()
    setattr(globals()['slicer'].modules, widgetName, globals()[widgetName.lower()])


#
# TransformLabelLogic
#

class TransformLabelLogic:
  """This class should implement all the actual 
  computation done by your module.  The interface 
  should be such that other python code can import
  this class and make use of the functionality without
  requiring an instance of the Widget
  """
  def __init__(self):
    pass

  def hasImageData(self,volumeNode):
    """This is a dummy logic method that 
    returns true if the passed in volume
    node has valid image data
    """
    if not volumeNode:
      print('no volume node')
      return False
    if volumeNode.GetImageData() == None:
      print('no image data')
      return False
    return True

  def delayDisplay(self,message,msec=1000):
    #
    # logic version of delay display
    #
    print(message)
    self.info = qt.QDialog()
    self.infoLayout = qt.QVBoxLayout()
    self.info.setLayout(self.infoLayout)
    self.label = qt.QLabel(message,self.info)
    self.infoLayout.addWidget(self.label)
    qt.QTimer.singleShot(msec, self.info.close)
    self.info.exec_()

  def run(self,inputVolume,outputVolume,referenceVolume,firstTransformNode):
    """
    Run the actual algorithm
    """
    if inputVolume == 0 or outputVolume == 0 or referenceVolume == 0 or firstTransformNode == 0:
      return False


    #Run BRAINS Resample Image module: Use your Transformation and apply it on the output of the previous step.
    self.delayDisplay('BRAINS Resample Image')
    bri = slicer.modules.brainsresample
    
    parameters = {}
    parameters['inputVolume'] = inputVolume
    parameters['referenceVolume'] = referenceVolume
    parameters['outputVolume'] = outputVolume
    parameters['pixelType'] = 'ushort'
    parameters['warpTransform'] = firstTransformNode
    parameters['interpolationMode'] = 'Linear'
    parameters['inverseTransform'] = None
    parameters['defaultValue'] = 0.0
    parameters['numberOfThreads'] = -1
    slicer.cli.run(bri, None, parameters, True)
  
    return True
