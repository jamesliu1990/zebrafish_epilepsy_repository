function meta = LSM_metadata( data )
%UNTITLED Summary of this function goes here
%   Detailed explanation goes here

meta = createMinimalOMEXMLMetadata(data, 'XYZCT');
meta.setInstrumentID('2',0);
meta.setMicroscopeModel('LSM a',0);
meta.setDetectorID('1', 0, 0);
meta.setDetectorModel('Orca', 0, 0);

end
