pyversion % check if matlab is aware of python
% use pyversion path to point matlab to python.exe

df = py.dcimg_reader.dcimg_reader('test2.dcimg');
df.getinfo();
df.getFrame(int8(0));
mdata = uint16(py.array.array('d',py.numpy.nditer(df.data)));
mdata = reshape(mdata,[df.width, df.height]);

