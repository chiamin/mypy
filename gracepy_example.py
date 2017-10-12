import grace

x = [1,2,3,4,5,6]
y = [i*i for i in x]
e = [0.1]*6

# See the script grace.py for more options.
pl = grace.new()
pl.plot (x,x,ls=1,legend='y1')
pl.errorbar (x,y,e,ls=4,legend='y2')
pl.setp (xlabel='x',ylabel='|\\phi\\rangle')

# The argument <name> set the file name of xmgrace plot.
# If <name> is not given, the default name is .temp, and the temporary file .temp.agr will be deleted after the script execution finished.
# If <name> is given, the file <name>.agr will remain after the script excution. However one should still save the file explicitly (using ctrl+s) to save the configuration; otherwise the remained file <name>.agr will use the default configuration of xmgrace.
grace.show ()
