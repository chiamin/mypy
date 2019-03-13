import sys, os
sys.path.append('/home/chiamic/mypy')
import setinput_localmuh as localmuh
import setinput_delta as setdel

def get_para (para,key,typ=str):
    for line in para:
        if key in line:
            tmp = line.strip().split()
            return typ(tmp[-1])
    print 'Cannot find key:',key
    raise KeyError

def set_para (para,key,val):
    i = 0
    while i < len(para):
        if key in para[i]:
            tmp = para[i].strip().split()[-1]
            j = para[i].find (tmp)
            para[i] = para[i][:j]+str(val)+'\n'
            return para
        i += 1
    print 'Cannot find key:',key
    raise KeyError

def para_move_to (para, i, key, skiplines=0):
    while i < len(para):
        if key in para[i]:
            break
        i += 1
    return para, i+skiplines

def remove_bracket (para,key,skipline=1):
    i = 0
    para,i = para_move_to (para,i,key)
    para,i = para_move_to (para,i,'{')

    i += skipline+1
    while '}' not in para[i]:
        del para[i]
    return para,i

def replace_key (para,i,key,newkey):
    para,i = para_move_to (key)
    para[i] = newkey
    return para,i

def set_localmuh (para, muh):
    i = 0
    para,i = para_move_to (para, i, 'localmuh')
    para[i] = '    localmuh\n'
    para,i = remove_bracket (para,'localmuh')

    for x,y,mode,mu,h in reversed(muh):
        para.insert (i,'        '+str(x)+'    '+str(y)+'      '+str(mu)+'      '+str(h)+'\n')
    return para

def set_delpot (para, delpot):
    i = 0
    para,i = para_move_to (para,i,'delta_potential')
    if delpot == 0:
        para[i] = '    delta_potentialX\n'
    else:
        para[i] = '    delta_potential\n'
        para,i = remove_bracket (para,'delta_potential')
        for x1,y1,x2,y2,d in reversed(delpot):
            para.insert (i,'        '+str(x1)+'   '+str(y1)+'   '+str(x2)+'   '+str(y2)+'   '+str(d)+'\n')
    return para

def set_sweeps (para):
    para,i = remove_bracket (para,'sweeps')
    sweeps = [\
    '        64     1E-10    10     0',\
    '        128    1E-10    8      0',\
    '        200    1E-12    7      0',\
    '        300    1E-12    6      0',\
    '        500    1E-12    5      0',\
    '        800    1E-12    5      0',\
    '        1400   1E-12    4      0',\
    '        2400   1E-12    4      0',\
    '        4000   1E-12    4      0',\
    '        5500   1E-12    4      0',\
    '        7000   1E-12    4      0',\
    '        9000   1E-12    4      0',\
    '        11000  1E-12    3      0',\
    '        13000  1E-12    3      0',\
    '        15000  1E-12    3      0',\
    ]
    for sw in reversed(sweeps):
        para.insert (i,sw+'\n')
    return para

if __name__ == '__main__':
    para_base = sys.argv[1]
    f = open (para_base)
    para = f.readlines()
    f.close()

    lx = 16
    ly = 4
    U  = 6
    tp = 0
    mu = 0
    N_up = 0
    N_dn = 0
    gc = 'yes'
    write = 'no'
    out_minm = 800
    nsweep_tmp = 2

    suffix = suffixdel = ''

    # Set values
    para = set_para (para,'Lx',lx)
    para = set_para (para,'Ly',ly)
    para = set_para (para,'U',U)
    para = set_para (para,'tpr',tp)
    para = set_para (para,'mu',mu)
    para = set_para (para,'N_up',N_up)
    para = set_para (para,'N_dn',N_dn)
    para = set_para (para,'grand_canonical',gc)
    para = set_para (para,'write_to_file',write)
    para = set_para (para,'out_minm',out_minm)
    para = set_para (para,'nsweep_tmp',nsweep_tmp)
    para = set_para (para,'outdir',os.getcwd())

    # Set sweeps
    set_sweeps (para)

    # Set localmuh
    muh, suffix = localmuh.linear_mu (lx,ly,mu1=1.4,mu2=2.2, mode='permanent')
    set_localmuh (para, muh)

    # Set delta_potential
    delpot, suffixdel = setdel.delta_all (lx,ly,delta=0.25)
    set_delpot (para,delpot)


    if gc:
        nname = 'mu'+str(mu)
    else:        
        n = (N_up+N_dn) / (lx*ly)
        nname = 'n'+str(n)[:5]

    ofname = 'huben'+str(lx)+'x'+str(ly)+'_U'+str(U).rstrip('0').rstrip('.')+'_'+nname+'_tp'+str(tp)+'_'+suffix+'_'+suffixdel+'.in'
    out_suffix = ofname[5:-3]
    para = set_para (para,'out_suffix',out_suffix)


    f = open (ofname,'w')
    for line in para:
        f.write (line)
    f.close()
