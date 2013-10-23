import os
import unittest
from __main__ import vtk, qt, ctk, slicer

#
# MakeHiResLabel
#

class MakeHiResLabel:
  def __init__(self, parent):
    parent.title = "MakeHiResLabel" # TODO make this more human readable by adding spaces
    parent.categories = ["Examples"]
    parent.dependencies = []
    parent.contributors = ["Junichi Tokuda (BWH)"]
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
    slicer.selfTests['MakeHiResLabel'] = self.runTest

  def runTest(self):
    tester = MakeHiResLabelTest()
    tester.runTest()

#
# qMakeHiResLabelWidget
#

class MakeHiResLabelWidget:
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
    self.reloadButton.name = "MakeHiResLabel Reload"
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
    self.inputSelector.addAttribute( "vtkMRMLScalarVolumeNode", "LabelMap", 1 )
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
    self.outputSelector.selectNodeUponCreation = False
    self.outputSelector.addEnabled = True
    self.outputSelector.removeEnabled = True
    self.outputSelector.noneEnabled = True
    self.outputSelector.showHidden = False
    self.outputSelector.showChildNodeTypes = False
    self.outputSelector.setMRMLScene( slicer.mrmlScene )
    self.outputSelector.setToolTip( "Pick the output to the algorithm." )
    parametersFormLayout.addRow("Output Volume: ", self.outputSelector)

    #
    # Pixel size
    #
    self.pixelSizeX = qt.QDoubleSpinBox()
    self.pixelSizeX.setSingleStep(0.1);
    self.pixelSizeX.setValue(1.0);
    parametersFormLayout.addRow("PixelSize Factor (X): ", self.pixelSizeX)

    self.pixelSizeY = qt.QDoubleSpinBox()
    self.pixelSizeY.setSingleStep(0.1);
    self.pixelSizeY.setValue(1.0);
    parametersFormLayout.addRow("PixelSize Factor (Y): ", self.pixelSizeY)

    self.pixelSizeZ = qt.QDoubleSpinBox()
    self.pixelSizeZ.setSingleStep(0.1);
    self.pixelSizeZ.setValue(1.0);
    parametersFormLayout.addRow("PixelSize Factor (Z): ", self.pixelSizeZ)

    #
    # Apply Button
    #
    self.applyButton = qt.QPushButton("Apply")
    self.applyButton.toolTip = "Run the algorithm."
    self.applyButton.enabled = False
    parametersFormLayout.addRow(self.applyButton)

    # connections
    self.applyButton.connect('clicked(bool)', self.onApplyButton)
    self.inputSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelectInput)
    self.outputSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelectOutput)

    # Add vertical spacer
    self.layout.addStretch(1)

  def cleanup(self):
    pass

  def onSelectInput(self):
    if self.inputSelector.currentNode() != 0:
      if self.outputSelector.currentNode() != 0:
        self.applyButton.enabled = self.inputSelector.currentNode() and self.outputSelector.currentNode()

      inode = self.inputSelector.currentNode()
      pixelSize = inode.GetSpacing()
      self.pixelSizeX.setValue(pixelSize[0]);
      self.pixelSizeY.setValue(pixelSize[1]);
      self.pixelSizeZ.setValue(pixelSize[2]);

  def onSelectOutput(self):
    if self.inputSelector.currentNode() != 0 and self.outputSelector.currentNode() != 0:
      self.applyButton.enabled = self.inputSelector.currentNode() and self.outputSelector.currentNode()

  def onApplyButton(self):
    logic = MakeHiResLabelLogic()
    pixelSizeX = self.pixelSizeX.value;
    pixelSizeY = self.pixelSizeY.value;
    pixelSizeZ = self.pixelSizeZ.value;
    print("Run the algorithm")
    logic.run(self.inputSelector.currentNode(), self.outputSelector.currentNode(), pixelSizeX, pixelSizeY, pixelSizeZ)


  def onReload(self,moduleName="MakeHiResLabel"):
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
# MakeHiResLabelLogic
#

class MakeHiResLabelLogic:
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

  def takeScreenshot(self,name,description,type=-1):
    # show the message even if not taking a screen shot
    self.delayDisplay(description)

    if self.enableScreenshots == 0:
      return

    lm = slicer.app.layoutManager()
    # switch on the type to get the requested window
    widget = 0
    if type == -1:
      # full window
      widget = slicer.util.mainWindow()
    elif type == slicer.qMRMLScreenShotDialog().FullLayout:
      # full layout
      widget = lm.viewport()
    elif type == slicer.qMRMLScreenShotDialog().ThreeD:
      # just the 3D window
      widget = lm.threeDWidget(0).threeDView()
    elif type == slicer.qMRMLScreenShotDialog().Red:
      # red slice window
      widget = lm.sliceWidget("Red")
    elif type == slicer.qMRMLScreenShotDialog().Yellow:
      # yellow slice window
      widget = lm.sliceWidget("Yellow")
    elif type == slicer.qMRMLScreenShotDialog().Green:
      # green slice window
      widget = lm.sliceWidget("Green")

    # grab and convert to vtk image data
    qpixMap = qt.QPixmap().grabWidget(widget)
    qimage = qpixMap.toImage()
    imageData = vtk.vtkImageData()
    slicer.qMRMLUtils().qImageToVtkImageData(qimage,imageData)

    #annotationLogic = slicer.modules.annotations.logic()

  def run(self,inputVolume,outputVolume,pixelSizeX,pixelSizeY,pixelSizeZ):
    """
    Run the actual algorithm
    """

    #Run Label Map Smoothing Module: Smooth the moving label with Max RMs Err = 1 and Sigma =2.
    tmpImageLMS = slicer.vtkMRMLScalarVolumeNode()
    tmpImageLMS.SetName('tmp_LMS')
    slicer.mrmlScene.AddNode(tmpImageLMS)

    self.delayDisplay('Label Map Smoothing')
    lms = slicer.modules.labelmapsmoothing
    parameters = {}
    parameters['labelToSmooth'] = -1
    parameters['numberOfIterations'] = 50
    parameters['maxRMSError'] = 1.0
    parameters['gaussianSigma'] = 2.0
    parameters['inputVolume'] = inputVolume.GetID()
    parameters['outputVolume'] = tmpImageLMS.GetID()
    slicer.cli.run(lms, None, parameters, True)

    #Run Resample Scalar Volume Module:Increase the resolution of the output of previous step by dividing the third entity by 2.
    tmpImageRSV = slicer.vtkMRMLScalarVolumeNode()
    tmpImageLMS.SetName('tmp_RSV')
    slicer.mrmlScene.AddNode(tmpImageRSV)

    self.delayDisplay('Resample Scalar Volume')
    rsv = slicer.modules.resamplescalarvolume
    parameters = {}
    parameters['outputPixelSpacing'] = "%f,%f,%f" % (pixelSizeX, pixelSizeY, pixelSizeZ)
    parameters['interpolationType'] = 'linear'
    parameters['InputVolume'] = tmpImageLMS.GetID()
    parameters['OutputVolume'] = tmpImageRSV.GetID()
    slicer.cli.run(rsv, None, parameters, True)

    #Run Label Smoothing Module: Smooth the output of previous step with Max RMs Err = 0.5 and Sigma =1.
    self.delayDisplay('Label Map Smoothing')
    parameters = {}
    parameters['labelToSmooth'] = -1
    parameters['numberOfIterations'] = 50
    parameters['maxRMSError'] = 0.5
    parameters['gaussianSigma'] = 1
    parameters['inputVolume'] = tmpImageRSV.GetID()
    parameters['outputVolume'] = outputVolume.GetID()
    slicer.cli.run(lms, None, parameters, True)

    #Remove temporary nodes.
    slicer.mrmlScene.RemoveNode(tmpImageLMS)
    slicer.mrmlScene.RemoveNode(tmpImageRSV)

    #Run Image Resample module: Use your Transformation and apply it on the output of the previous step.
    #Registration Metric: Calculate HD and DSC.

    return True


