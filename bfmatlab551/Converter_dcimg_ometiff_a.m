function out = dcimgConverter(filename)
% This Function Converts a dcimg file to a series of ome-tiff files 
% each ome-tiff file should be less than 4GB
% with metadata from ini file
% This version is for two-color 2D time-series

pyversion % check if matlab is aware of python
% use pyversion path to point matlab to python.exe
% check java
if bfCheckJavaPath() == 0
    out = 0;
    return;
end
% filename stuff
[pathstr,name,ext] = fileparts(filename);
if strcmp(ext,'.dcimg')==0
    fprintf('this is not a dcimg file!\n');
    out = 0;
    return;
end
filenameini = [pathstr '\' name '.ini'];
% read in dcimg file using python module dcimg_reader, dcimg_defs
df = py.dcimg_reader.dcimg_reader(filename);
df.getinfo();
% figure out how many frames, etc.
framebytes = df.width*df.height*df.pixelsize;
frames_per_file = 4*(1024^3)/framebytes;
if (mod(frames_per_file,2)==1)
    frames_per_file = frames_per_file - 1;
end
no_files = df.totalframes/frames_per_file;

% test metadata, ini file
fprintf('testing metadata...\n');
meta = CreateLSM_Metadata(filenameini, zeros(df.width, df.height, 1, 2, frames_per_file/2, 'uint16'));
% start creating output files
fprintf('Creating output files.\n');
frame_beg = 0;
frame_end = frames_per_file-1;
outno = 0;
for m = 1:floor(no_files)
    fprintf('file %d / %d\n',m,floor(no_files));
    % initialize array (XYZCT)
    mdata = zeros(df.width, df.height, 1, 2, frames_per_file/2, 'uint16');
    p = 1;
    for k = frame_beg:2:frame_end
        fprintf('(%d / %d) ',k, frame_end);
        df.getFrame(int16(k));
        mdata(:,:,1,1,p) = reshape(uint16(py.array.array('d',py.numpy.nditer(df.data))),[df.width, df.height]);
        df.getFrame(int16(k+1));
        mdata(:,:,1,2,p) = reshape(uint16(py.array.array('d',py.numpy.nditer(df.data))),[df.width, df.height]);
        p = p + 1;
    end
    fprintf('\n');
    % save 
    filenameout = [pathstr '\' name sprintf('_%d', outno) '.ome.tif'];
    meta = CreateLSM_Metadata(filenameini, mdata);
    bfsave(mdata, filenameout, 'dimensionOrder', 'XYZCT', 'metadata', meta);
    outno = outno + 1;
    % increment
    frame_beg = m*frames_per_file;
    frame_end = frame_beg + frames_per_file - 1;
end
% do last file
fprintf('last file:\n');
frame_end = df.totalframes-1;
mdata = zeros(df.width, df.height, 1, 2, int16((frame_end-frame_beg+1)/2), 'uint16');
disp(size(mdata));
p = 1;
for k = frame_beg:2:frame_end
    fprintf('%d ',k);
    df.getFrame(int16(k));
    mdata(:,:,1,1,p) = reshape(uint16(py.array.array('d',py.numpy.nditer(df.data))),[df.width, df.height]);
    df.getFrame(int16(k+1));
    mdata(:,:,1,2,p) = reshape(uint16(py.array.array('d',py.numpy.nditer(df.data))),[df.width, df.height]);
    p = p + 1;
end  
fprintf('\n');
% save last file
filenameout = [pathstr name sprintf('_%d', outno) '.ome.tif'];
meta = CreateLSM_Metadata(filenameini, mdata);
bfsave(mdata, filenameout, 'dimensionOrder', 'XYZCT', 'metadata', meta);

out = 1;

end