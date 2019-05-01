function meta = pktest1( fname )
%UNTITLED Summary of this function goes here
%   Detailed explanation goes here
toInt = @(x) javaObject('ome.xml.model.primitives.PositiveInteger', ...
                        javaObject('java.lang.Integer', x));
toFloat = @(x) javaObject('ome.xml.model.primitives.PositiveFloat', ...
                        javaObject('java.lang.Double', x));
tojlD = @(x) javaObject('java.lang.Double', x);

data = randn(128,128,3,2,1, 'single');

power488 = 1;
power561 = 1;

dx = ome.units.quantity.Length(java.lang.Double(0.243), ome.units.UNITS.MICROMETER);
dz = ome.units.quantity.Length(java.lang.Double(1.5), ome.units.UNITS.MICROMETER);
meta = createMinimalOMEXMLMetadata(data, 'XYZCT');

meta.setPixelsPhysicalSizeX(dx, 0)
meta.setPixelsPhysicalSizeY(dx, 0)
meta.setPixelsPhysicalSizeZ(dz, 0)   
 
% Instrument info
dt = ome.xml.model.enums.handlers.DetectorTypeEnumHandler;
bt = ome.xml.model.enums.handlers.BinningEnumHandler;
mt = ome.xml.model.enums.handlers.MicroscopeTypeEnumHandler;
meta.setInstrumentID('LightSheet',0);
meta.setMicroscopeModel('LSM',0);
meta.setMicroscopeManufacturer('NA', 0);
%metadata.'setMicroscopeSerialNumber',
%meta.setMicroscopeType(mt.getEnumeration('Other'), 0) % useless
% image
meta.setImageID('test',0);

% Objective
ot = ome.xml.model.enums.handlers.ImmersionEnumHandler;
meta.setObjectiveID('1', 0, 0);
% metadata.setObjectiveCalibratedMagnification
% metadata.setObjectiveCorrection 
meta.setObjectiveImmersion(ot.getEnumeration('Water'), 0, 0);
meta.setObjectiveLensNA(tojlD(0.5), 0, 0);
meta.setObjectiveManufacturer('Olympus', 0, 0);
% 'setObjectiveModel',
meta.setObjectiveNominalMagnification(tojlD(20), 0, 0);
% 'setObjectiveSerialNumber',
wd = ome.units.quantity.Length(java.lang.Double(3.3), ome.units.UNITS.MM);
meta.setObjectiveWorkingDistance(wd, 0, 0);      

% Detector        
meta.setDetectorID('1', 0, 0)
meta.setDetectorModel('Orca Flash 4.0', 0, 0)
%'setDetectorAmplificationGain',
%'setDetectorGain',
meta.setDetectorManufacturer('Hamamatsu', 0, 0)
meta.setDetectorType(dt.getEnumeration('CMOS'), 0, 0)
%'setDetectorOffset',
%'setDetectorSerialNumber',
meta.setDetectorSettingsID('1',0, 0)
meta.setDetectorSettingsBinning(bt.getEnumeration('1x1'), 0, 0)
%meta.setDetectorSettingsGain(jldouble(emccdgain), 0, 0)
%'setDetectorSettingsOffset',
%'setDetectorSettingsReadOutRate',
%'setDetectorSettingsVoltage',    
%'setDetectorVoltage',
%'setDetectorZoom',

% Color channels
% setup both channels green and red
amtypes = {'WideField', 'LaserScanningConfocalMicroscopy', 'SpinningDiskConfocal', ...
               'SlitScanConfocal', 'MultiPhotonMicroscopy', 'StructuredIllumination', ...
               'SingleMoleculeImaging', 'TotalInternalReflection', 'FluorescenceLifetime', ...
               'SpectralImaging', 'FluorescenceCorrelationSpectroscopy', 'NearFieldScanningOptcalMicroscopy', ...
               'SecondHarmonicGenerationImaging', 'PALM', 'STORM', 'STED', 'TIRF', ...
               'LCM', 'Other'};
ct = ome.xml.model.enums.handlers.AcquisitionModeEnumHandler;
% first channel
% metadata.setChannelID('green', 0, 0)
meta.setChannelAcquisitionMode(ct.getEnumeration(amtypes(1)), 0, 0);
%'setChannelAnnotationRef',
%'setChannelContrastMethod',
wem = ome.units.quantity.Length(java.lang.Double(510), ome.units.UNITS.NM);
wex = ome.units.quantity.Length(java.lang.Double(488), ome.units.UNITS.NM);
meta.setChannelEmissionWavelength(wem, 0, 0);
meta.setChannelExcitationWavelength(wex, 0, 0)
%'setChannelFilterSetRef',
meta.setChannelFluor('GCAMP5', 0, 0);
% Laser
meta.setLaserID('L488', 0, 0);
meta.setLaserManufacturer('Coherent', 0, 0);
meta.setLaserModel('OBIS', 0, 0);
pl = ome.units.quantity.Power(java.lang.Double(power488), ome.units.UNITS.MW);
meta.setLaserPower(pl, 0, 0);
%'setLaserSerialNumber',
meta.setLaserWavelength(wex, 0, 0);

%second channel
% meta.setChannelID('red', 0, 1)
meta.setChannelAcquisitionMode(ct.getEnumeration(amtypes(1)), 0, 1);
%'setChannelAnnotationRef',
%'setChannelContrastMethod',
wem = ome.units.quantity.Length(java.lang.Double(600), ome.units.UNITS.NM);
wex = ome.units.quantity.Length(java.lang.Double(561), ome.units.UNITS.NM);
meta.setChannelEmissionWavelength(wem, 0, 1);
meta.setChannelExcitationWavelength(wex, 0, 1);
meta.setChannelFluor('RFP', 0, 1);
% Laser
meta.setLaserID('L561', 0, 1);
meta.setLaserManufacturer('Coherent', 0, 1);
meta.setLaserModel('OBIS', 0, 1);
pl = ome.units.quantity.Power(java.lang.Double(power561), ome.units.UNITS.MW);
meta.setLaserPower(pl, 0, 1);
%'setLaserSerialNumber',
meta.setLaserWavelength(wex, 0, 1);

bfsave(data, fname, 'dimensionOrder', 'XYZCT', 'metadata', meta);

end

%{ 
metadata methods for ome.tiff files
refer to http://www.openmicroscopy.org/Schemas/

setArcAnnotationRef                                     
setArcID                                                
setArcLotNumber                                         
setArcManufacturer                                      
setArcModel                                             
setArcPower                                             
setArcSerialNumber                                      
setArcType                                              
setBinaryFileFileName                                   
setBinaryFileMIMEType                                   
setBinaryFileSize                                       
setBinaryOnlyMetadataFile                               
setBinaryOnlyUUID                                       
setBooleanAnnotationAnnotationRef                       
setBooleanAnnotationAnnotator                           
setBooleanAnnotationDescription                         
setBooleanAnnotationID                                  
setBooleanAnnotationNamespace                           
setBooleanAnnotationValue                               
setChannelAcquisitionMode                               
setChannelAnnotationRef                                 
setChannelColor                                         
setChannelContrastMethod                                
setChannelEmissionWavelength                            
setChannelExcitationWavelength                          
setChannelFilterSetRef                                  
setChannelFluor                                         
setChannelID                                            
setChannelIlluminationType                              
setChannelLightSourceSettingsAttenuation                
setChannelLightSourceSettingsID                         
setChannelLightSourceSettingsWavelength                 
setChannelNDFilter                                      
setChannelName                                          
setChannelPinholeSize                                   
setChannelPockelCellSetting                             
setChannelSamplesPerPixel                               
setCommentAnnotationAnnotationRef                       
setCommentAnnotationAnnotator                           
setCommentAnnotationDescription                         
setCommentAnnotationID                                  
setCommentAnnotationNamespace                           
setCommentAnnotationValue                               
setDatasetAnnotationRef                                 
setDatasetDescription                                   
setDatasetExperimenterGroupRef                          
setDatasetExperimenterRef                               
setDatasetID                                            
setDatasetImageRef                                      
setDatasetName                                          
setDetectorAmplificationGain                            
setDetectorAnnotationRef                                
setDetectorGain                                         
setDetectorID                                           
setDetectorLotNumber                                    
setDetectorManufacturer                                 
setDetectorModel                                        
setDetectorOffset                                       
setDetectorSerialNumber                                 
setDetectorSettingsBinning                              
setDetectorSettingsGain                                 
setDetectorSettingsID                                   
setDetectorSettingsIntegration                          
setDetectorSettingsOffset                               
setDetectorSettingsReadOutRate                          
setDetectorSettingsVoltage                              
setDetectorSettingsZoom                                 
setDetectorType                                         
setDetectorVoltage                                      
setDetectorZoom                                         
setDichroicAnnotationRef                                
setDichroicID                                           
setDichroicLotNumber                                    
setDichroicManufacturer                                 
setDichroicModel                                        
setDichroicSerialNumber                                 
setDoubleAnnotationAnnotationRef                        
setDoubleAnnotationAnnotator                            
setDoubleAnnotationDescription                          
setDoubleAnnotationID                                   
setDoubleAnnotationNamespace                            
setDoubleAnnotationValue                                
setEllipseAnnotationRef                                 
setEllipseFillColor                                     
setEllipseFillRule                                      
setEllipseFontFamily                                    
setEllipseFontSize                                      
setEllipseFontStyle                                     
setEllipseID                                            
setEllipseLineCap                                       
setEllipseLocked                                        
setEllipseRadiusX                                       
setEllipseRadiusY                                       
setEllipseStrokeColor                                   
setEllipseStrokeDashArray                               
setEllipseStrokeWidth                                   
setEllipseText                                          
setEllipseTheC                                          
setEllipseTheT                                          
setEllipseTheZ                                          
setEllipseTransform                                     
setEllipseVisible                                       
setEllipseX                                             
setEllipseY                                             
setExperimentDescription                                
setExperimentExperimenterRef                            
setExperimentID                                         
setExperimentType                                       
setExperimenterAnnotationRef                            
setExperimenterEmail                                    
setExperimenterFirstName                                
setExperimenterGroupAnnotationRef                       
setExperimenterGroupDescription                         
setExperimenterGroupExperimenterRef                     
setExperimenterGroupID                                  
setExperimenterGroupLeader                              
setExperimenterGroupName                                
setExperimenterID                                       
setExperimenterInstitution                              
setExperimenterLastName                                 
setExperimenterMiddleName                               
setExperimenterUserName                                 
setFilamentAnnotationRef                                
setFilamentID                                           
setFilamentLotNumber                                    
setFilamentManufacturer                                 
setFilamentModel                                        
setFilamentPower                                        
setFilamentSerialNumber                                 
setFilamentType                                         
setFileAnnotationAnnotationRef                          
setFileAnnotationAnnotator                              
setFileAnnotationDescription                            
setFileAnnotationID                                     
setFileAnnotationNamespace                              
setFilterAnnotationRef                                  
setFilterFilterWheel                                    
setFilterID                                             
setFilterLotNumber                                      
setFilterManufacturer                                   
setFilterModel                                          
setFilterSerialNumber                                   
setFilterSetDichroicRef                                 
setFilterSetEmissionFilterRef                           
setFilterSetExcitationFilterRef                         
setFilterSetID                                          
setFilterSetLotNumber                                   
setFilterSetManufacturer                                
setFilterSetModel                                       
setFilterSetSerialNumber                                
setFilterType                                           
setGenericExcitationSourceAnnotationRef                 
setGenericExcitationSourceID                            
setGenericExcitationSourceLotNumber                     
setGenericExcitationSourceManufacturer                  
setGenericExcitationSourceMap                           
setGenericExcitationSourceModel                         
setGenericExcitationSourcePower                         
setGenericExcitationSourceSerialNumber                  
setImageAcquisitionDate                                 
setImageAnnotationRef                                   
setImageDescription                                     
setImageExperimentRef                                   
setImageExperimenterGroupRef                            
setImageExperimenterRef                                 
setImageID                                              
setImageInstrumentRef                                   
setImageMicrobeamManipulationRef                        
setImageName                                            
setImageROIRef                                          
setImagingEnvironmentAirPressure                        
setImagingEnvironmentCO2Percent                         
setImagingEnvironmentHumidity                           
setImagingEnvironmentMap                                
setImagingEnvironmentTemperature                        
setInstrumentAnnotationRef                              
setInstrumentID                                         
setLabelAnnotationRef                                   
setLabelFillColor                                       
setLabelFillRule                                        
setLabelFontFamily                                      
setLabelFontSize                                        
setLabelFontStyle                                       
setLabelID                                              
setLabelLineCap                                         
setLabelLocked                                          
setLabelStrokeColor                                     
setLabelStrokeDashArray                                 
setLabelStrokeWidth                                     
setLabelText                                            
setLabelTheC                                            
setLabelTheT                                            
setLabelTheZ                                            
setLabelTransform                                       
setLabelVisible                                         
setLabelX                                               
setLabelY                                               
setLaserAnnotationRef                                   
setLaserFrequencyMultiplication                         
setLaserID                                              
setLaserLaserMedium                                     
setLaserLotNumber                                       
setLaserManufacturer                                    
setLaserModel                                           
setLaserPockelCell                                      
setLaserPower                                           
setLaserPulse                                           
setLaserPump                                            
setLaserRepetitionRate                                  
setLaserSerialNumber                                    
setLaserTuneable                                        
setLaserType                                            
setLaserWavelength                                      
setLightEmittingDiodeAnnotationRef                      
setLightEmittingDiodeID                                 
setLightEmittingDiodeLotNumber                          
setLightEmittingDiodeManufacturer                       
setLightEmittingDiodeModel                              
setLightEmittingDiodePower                              
setLightEmittingDiodeSerialNumber                       
setLightPathAnnotationRef                               
setLightPathDichroicRef                                 
setLightPathEmissionFilterRef                           
setLightPathExcitationFilterRef                         
setLineAnnotationRef                                    
setLineFillColor                                        
setLineFillRule                                         
setLineFontFamily                                       
setLineFontSize                                         
setLineFontStyle                                        
setLineID                                               
setLineLineCap                                          
setLineLocked                                           
setLineMarkerEnd                                        
setLineMarkerStart                                      
setLineStrokeColor                                      
setLineStrokeDashArray                                  
setLineStrokeWidth                                      
setLineText                                             
setLineTheC                                             
setLineTheT                                             
setLineTheZ                                             
setLineTransform                                        
setLineVisible                                          
setLineX1                                               
setLineX2                                               
setLineY1                                               
setLineY2                                               
setListAnnotationAnnotationRef                          
setListAnnotationAnnotator                              
setListAnnotationDescription                            
setListAnnotationID                                     
setListAnnotationNamespace                              
setLongAnnotationAnnotationRef                          
setLongAnnotationAnnotator                              
setLongAnnotationDescription                            
setLongAnnotationID                                     
setLongAnnotationNamespace                              
setLongAnnotationValue                                  
setMapAnnotationAnnotationRef                           
setMapAnnotationAnnotator                               
setMapAnnotationDescription                             
setMapAnnotationID                                      
setMapAnnotationNamespace                               
setMapAnnotationValue                                   
setMaskAnnotationRef                                    
setMaskBinData                                          
setMaskFillColor                                        
setMaskFillRule                                         
setMaskFontFamily                                       
setMaskFontSize                                         
setMaskFontStyle                                        
setMaskHeight                                           
setMaskID                                               
setMaskLineCap                                          
setMaskLocked                                           
setMaskStrokeColor                                      
setMaskStrokeDashArray                                  
setMaskStrokeWidth                                      
setMaskText                                             
setMaskTheC                                             
setMaskTheT                                             
setMaskTheZ                                             
setMaskTransform                                        
setMaskVisible                                          
setMaskWidth                                            
setMaskX                                                
setMaskY                                                
setMicrobeamManipulationDescription                     
setMicrobeamManipulationExperimenterRef                 
setMicrobeamManipulationID                              
setMicrobeamManipulationLightSourceSettingsAttenuation  
setMicrobeamManipulationLightSourceSettingsID           
setMicrobeamManipulationLightSourceSettingsWavelength   
setMicrobeamManipulationROIRef                          
setMicrobeamManipulationType                            
setMicroscopeLotNumber                                  
setMicroscopeManufacturer                               
setMicroscopeModel                                      
setMicroscopeSerialNumber                               
setMicroscopeType                                       
setObjectiveAnnotationRef                               
setObjectiveCalibratedMagnification                     
setObjectiveCorrection                                  
setObjectiveID                                          
setObjectiveImmersion                                   
setObjectiveIris                                        
setObjectiveLensNA                                      
setObjectiveLotNumber                                   
setObjectiveManufacturer                                
setObjectiveModel                                       
setObjectiveNominalMagnification                        
setObjectiveSerialNumber                                
setObjectiveSettingsCorrectionCollar                    
setObjectiveSettingsID                                  
setObjectiveSettingsMedium                              
setObjectiveSettingsRefractiveIndex                     
setObjectiveWorkingDistance                             
setPixelsBigEndian                                      
setPixelsBinDataBigEndian                               
setPixelsDimensionOrder                                 
setPixelsID                                             
setPixelsInterleaved                                    
setPixelsPhysicalSizeX                                  
setPixelsPhysicalSizeY                                  
setPixelsPhysicalSizeZ                                  
setPixelsSignificantBits                                
setPixelsSizeC                                          
setPixelsSizeT                                          
setPixelsSizeX                                          
setPixelsSizeY                                          
setPixelsSizeZ                                          
setPixelsTimeIncrement                                  
setPixelsType                                           
setPlaneAnnotationRef                                   
setPlaneDeltaT                                          
setPlaneExposureTime                                    
setPlaneHashSHA1                                        
setPlanePositionX                                       
setPlanePositionY                                       
setPlanePositionZ                                       
setPlaneTheC                                            
setPlaneTheT                                            
setPlaneTheZ                                            
setPlateAcquisitionAnnotationRef                        
setPlateAcquisitionDescription                          
setPlateAcquisitionEndTime                              
setPlateAcquisitionID                                   
setPlateAcquisitionMaximumFieldCount                    
setPlateAcquisitionName                                 
setPlateAcquisitionStartTime                            
setPlateAcquisitionWellSampleRef                        
setPlateAnnotationRef                                   
setPlateColumnNamingConvention                          
setPlateColumns                                         
setPlateDescription                                     
setPlateExternalIdentifier                              
setPlateFieldIndex                                      
setPlateID                                              
setPlateName                                            
setPlateRowNamingConvention                             
setPlateRows                                            
setPlateStatus                                          
setPlateWellOriginX                                     
setPlateWellOriginY                                     
setPointAnnotationRef                                   
setPointFillColor                                       
setPointFillRule                                        
setPointFontFamily                                      
setPointFontSize                                        
setPointFontStyle                                       
setPointID                                              
setPointLineCap                                         
setPointLocked                                          
setPointStrokeColor                                     
setPointStrokeDashArray                                 
setPointStrokeWidth                                     
setPointText                                            
setPointTheC                                            
setPointTheT                                            
setPointTheZ                                            
setPointTransform                                       
setPointVisible                                         
setPointX                                               
setPointY                                               
setPolygonAnnotationRef                                 
setPolygonFillColor                                     
setPolygonFillRule                                      
setPolygonFontFamily                                    
setPolygonFontSize                                      
setPolygonFontStyle                                     
setPolygonID                                            
setPolygonLineCap                                       
setPolygonLocked                                        
setPolygonPoints                                        
setPolygonStrokeColor                                   
setPolygonStrokeDashArray                               
setPolygonStrokeWidth                                   
setPolygonText                                          
setPolygonTheC                                          
setPolygonTheT                                          
setPolygonTheZ                                          
setPolygonTransform                                     
setPolygonVisible                                       
setPolylineAnnotationRef                                
setPolylineFillColor                                    
setPolylineFillRule                                     
setPolylineFontFamily                                   
setPolylineFontSize                                     
setPolylineFontStyle                                    
setPolylineID                                           
setPolylineLineCap                                      
setPolylineLocked                                       
setPolylineMarkerEnd                                    
setPolylineMarkerStart                                  
setPolylinePoints                                       
setPolylineStrokeColor                                  
setPolylineStrokeDashArray                              
setPolylineStrokeWidth                                  
setPolylineText                                         
setPolylineTheC                                         
setPolylineTheT                                         
setPolylineTheZ                                         
setPolylineTransform                                    
setPolylineVisible                                      
setProjectAnnotationRef                                 
setProjectDatasetRef                                    
setProjectDescription                                   
setProjectExperimenterGroupRef                          
setProjectExperimenterRef                               
setProjectID                                            
setProjectName                                          
setROIAnnotationRef                                     
setROIDescription                                       
setROIID                                                
setROIName                                              
setROINamespace                                         
setReagentAnnotationRef                                 
setReagentDescription                                   
setReagentID                                            
setReagentName                                          
setReagentReagentIdentifier                             
setRectangleAnnotationRef                               
setRectangleFillColor                                   
setRectangleFillRule                                    
setRectangleFontFamily                                  
setRectangleFontSize                                    
setRectangleFontStyle                                   
setRectangleHeight                                      
setRectangleID                                          
setRectangleLineCap                                     
setRectangleLocked                                      
setRectangleStrokeColor                                 
setRectangleStrokeDashArray                             
setRectangleStrokeWidth                                 
setRectangleText                                        
setRectangleTheC                                        
setRectangleTheT                                        
setRectangleTheZ                                        
setRectangleTransform                                   
setRectangleVisible                                     
setRectangleWidth                                       
setRectangleX                                           
setRectangleY                                           
setRightsRightsHeld                                     
setRightsRightsHolder                                   
setRoot                                                 
setScreenAnnotationRef                                  
setScreenDescription                                    
setScreenID                                             
setScreenName                                           
setScreenPlateRef                                       
setScreenProtocolDescription                            
setScreenProtocolIdentifier                             
setScreenReagentSetDescription                          
setScreenReagentSetIdentifier                           
setScreenType                                           
setStageLabelName                                       
setStageLabelX                                          
setStageLabelY                                          
setStageLabelZ                                          
setTagAnnotationAnnotationRef                           
setTagAnnotationAnnotator                               
setTagAnnotationDescription                             
setTagAnnotationID                                      
setTagAnnotationNamespace                               
setTagAnnotationValue                                   
setTermAnnotationAnnotationRef                          
setTermAnnotationAnnotator                              
setTermAnnotationDescription                            
setTermAnnotationID                                     
setTermAnnotationNamespace                              
setTermAnnotationValue                                  
setTiffDataFirstC                                       
setTiffDataFirstT                                       
setTiffDataFirstZ                                       
setTiffDataIFD                                          
setTiffDataPlaneCount                                   
setTimestampAnnotationAnnotationRef                     
setTimestampAnnotationAnnotator                         
setTimestampAnnotationDescription                       
setTimestampAnnotationID                                
setTimestampAnnotationNamespace                         
setTimestampAnnotationValue                             
setTransmittanceRangeCutIn                              
setTransmittanceRangeCutInTolerance                     
setTransmittanceRangeCutOut                             
setTransmittanceRangeCutOutTolerance                    
setTransmittanceRangeTransmittance                      
setUUID                                                 
setUUIDFileName                                         
setUUIDValue                                            
setWellAnnotationRef                                    
setWellColor                                            
setWellColumn                                           
setWellExternalDescription                              
setWellExternalIdentifier                               
setWellID                                               
setWellReagentRef                                       
setWellRow                                              
setWellSampleID                                         
setWellSampleImageRef                                   
setWellSampleIndex                                      
setWellSamplePositionX                                  
setWellSamplePositionY                                  
setWellSampleTimepoint                                  
setWellType                                             
setXMLAnnotationAnnotationRef                           
setXMLAnnotationAnnotator                               
setXMLAnnotationDescription                             
setXMLAnnotationID                                      
setXMLAnnotationNamespace                               
setXMLAnnotationValue     

%}