function [meta, out] = CreateLSM_Metadata( filename, data )
%  [meta, out] = CreateLSM_Metadata( filename )
%  creates metadata from .ini file for Light Sheet Microscope Data

% check filename
[pathstr,name,ext] = fileparts(filename);
if strcmp(ext,'.ini')==0
    out = 0;
    return;
end

green_channel = 1;
red_channel = 0;

% read ini file
temp = inifile(filename,'read',{'system','','timestamp'});
timestamp = getTimeStampString(temp{1});
temp = inifile(filename,'read',{'Stack Parameters','','Step Size'});
dx = ome.units.quantity.Length(java.lang.Double(0.243), ome.units.UNITS.MICROMETER);
dz = ome.units.quantity.Length(java.lang.Double(temp), ome.units.UNITS.MICROMETER);
cameramodel = inifile(filename,'read',{'Camera Info','','Camera Model'});
camerasn = inifile(filename,'read',{'Camera Info','','Camera ID'});
exposuretime = inifile(filename,'read',{'Camera Info','','Exposure Time'});
LaserWavelength488 = inifile(filename,'read',{'OBIS 488','','Laser Wavelength(nm)'});
LaserPower488 = inifile(filename,'read',{'OBIS 488','','Laser Power(mW)'});
LaserWavelength561 = inifile(filename,'read',{'OBIS 561','','Laser Wavelength(nm)'});
LaserPower561 = inifile(filename,'read',{'OBIS 561','','Laser Power(mW)'});

% metadata definitions, etc
toInt = @(x) javaObject('ome.xml.model.primitives.PositiveInteger', ...
                        javaObject('java.lang.Integer', x));
toFloat = @(x) javaObject('ome.xml.model.primitives.PositiveFloat', ...
                        javaObject('java.lang.Double', x));
tojlD = @(x) javaObject('java.lang.Double', x);

toTime = @(x) javaObject('ome.xml.model.primitives.Timestamp', ...
                        javaObject('java.lang.String', x));
% create metadata;
meta = createMinimalOMEXMLMetadata(data, 'XYZCT');
% Instrument info
dt = ome.xml.model.enums.handlers.DetectorTypeEnumHandler;
bt = ome.xml.model.enums.handlers.BinningEnumHandler;
mt = ome.xml.model.enums.handlers.MicroscopeTypeEnumHandler;
meta.setInstrumentID('LightSheet',0);
meta.setMicroscopeModel('LSM',0);
meta.setMicroscopeManufacturer('NA', 0);
%metadata.'setMicroscopeSerialNumber',
%meta.setMicroscopeType(mt.getEnumeration('Other'), 0) % useless
% physical info
meta.setPixelsPhysicalSizeX(dx, 0);
meta.setPixelsPhysicalSizeY(dx, 0);
meta.setPixelsPhysicalSizeZ(dz, 0);  
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
meta.setDetectorID('1', 0, 0);
meta.setDetectorModel(cameramodel, 0, 0);
%'setDetectorAmplificationGain',
%'setDetectorGain',
meta.setDetectorManufacturer('Hamamatsu', 0, 0);
meta.setDetectorType(dt.getEnumeration('CMOS'), 0, 0);
%'setDetectorOffset',
meta.setDetectorSerialNumber(camerasn, 0, 0);
meta.setDetectorSettingsID('1',0, 0);
meta.setDetectorSettingsBinning(bt.getEnumeration('1x1'), 0, 0);
%meta.setDetectorSettingsGain(jldouble(emccdgain), 0, 0)
%'setDetectorSettingsOffset',
%'setDetectorSettingsReadOutRate',
%'setDetectorSettingsVoltage',    
%'setDetectorVoltage',
%'setDetectorZoom',
% Plane Info
exp = ome.units.quantity.Time(java.lang.Double(exposuretime), ome.units.UNITS.S);
meta.setPlaneExposureTime(exp, 0, 0);
% Image Info
meta.setImageAcquisitionDate(toTime(timestamp),0);

% setup both channels green and red
amtypes = {'WideField', 'LaserScanningConfocalMicroscopy', 'SpinningDiskConfocal', ...
               'SlitScanConfocal', 'MultiPhotonMicroscopy', 'StructuredIllumination', ...
               'SingleMoleculeImaging', 'TotalInternalReflection', 'FluorescenceLifetime', ...
               'SpectralImaging', 'FluorescenceCorrelationSpectroscopy', 'NearFieldScanningOptcalMicroscopy', ...
               'SecondHarmonicGenerationImaging', 'PALM', 'STORM', 'STED', 'TIRF', ...
               'LCM', 'Other'};
ct = ome.xml.model.enums.handlers.AcquisitionModeEnumHandler;

%second channel
% meta.setChannelID('red', 0, 1)
meta.setChannelAcquisitionMode(ct.getEnumeration(amtypes(1)), 0, red_channel);
%'setChannelAnnotationRef',
%'setChannelContrastMethod',
wem = ome.units.quantity.Length(java.lang.Double(600), ome.units.UNITS.NM);
wex = ome.units.quantity.Length(java.lang.Double(LaserWavelength561), ome.units.UNITS.NM);
meta.setChannelEmissionWavelength(wem, 0, red_channel);
meta.setChannelExcitationWavelength(wex, 0, red_channel);
meta.setChannelFluor('RFP', 0, red_channel);
% Laser
meta.setLaserID('L561', 0, red_channel);
meta.setLaserManufacturer('Coherent', 0, red_channel);
meta.setLaserModel('OBIS', 0, red_channel);
pl = ome.units.quantity.Power(java.lang.Double(LaserPower561), ome.units.UNITS.MW);
meta.setLaserPower(pl, 0, red_channel);
%'setLaserSerialNumber',
meta.setLaserWavelength(wex, 0, red_channel);

% first channel
% metadata.setChannelID('green', 0, 0)
meta.setChannelAcquisitionMode(ct.getEnumeration(amtypes(1)), 0, green_channel);
%'setChannelAnnotationRef',
%'setChannelContrastMethod',
wem = ome.units.quantity.Length(java.lang.Double(510), ome.units.UNITS.NM);
wex = ome.units.quantity.Length(java.lang.Double(LaserWavelength488), ome.units.UNITS.NM);
meta.setChannelEmissionWavelength(wem, 0, green_channel);
meta.setChannelExcitationWavelength(wex, 0, green_channel)
%'setChannelFilterSetRef',
meta.setChannelFluor('GCAMP5', 0, green_channel);
% Laser
meta.setLaserID('L488', 0, green_channel);
meta.setLaserManufacturer('Coherent', 0, green_channel);
meta.setLaserModel('OBIS', 0, green_channel);
pl = ome.units.quantity.Power(java.lang.Double(LaserPower488), ome.units.UNITS.MW);
meta.setLaserPower(pl, 0, green_channel);
%'setLaserSerialNumber',
meta.setLaserWavelength(wex, 0, green_channel);

end

function strout = getTimeStampString(strin)
%disp(strin);
values = sscanf(strin,'"%d/%d/%d %d:%d:%d %s"',[1 6]);
month = values(1);
day = values(2);
year = values(3);
hour = values(4);
minute = values(5);
second = values(6);
strout = sprintf('%d-%d-%dT%d:%d:%d',year,month,day,hour,minute,second);
%disp(strout);
end