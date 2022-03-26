for i in p_data:
  for j in c_data:
    gmx_md_flow(p_data, c_data, conf)

    
## 卷积层 ##
W_conv2 = weight_variable([5,5, 32, 64]) 
b_conv2 = bias_variable([64])
h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2)
## 池化层 ##
h_pool2 = max_pool_2x2(h_conv2)

## 全连接层 ##
W_fc1 = weight_variable([7*7*64, 1024])
b_fc1 = bias_variable([1024])
## Dropout层 ##
h_fc1_drop = tf.nn.dropout(b_fc1, keep_prob)






# Build the Complex
cmd = "gmx editconf -f jz4_ini.pdb -o jz4.gro"
os.system(cmd)
cmd = "%s merge_complex_gro.py -t 3HTB_processed.gro -l jz4.gro" % py
os.system(cmd)
cmd = "%s topol_modify.py -l jz4" % py
os.system(cmd)

# Defining the Unit Cell & Adding Solvent
cmd = "gmx editconf -f complex.gro -o newbox.gro -bt dodecahedron -d 1.0 " + box
os.system(cmd)
cmd = "gmx solvate -cp newbox.gro -cs spc216.gro -p topol.top -o solv.gro"
os.system(cmd)
# Adding Ions
cmd = "gmx grompp -f ions.mdp -c solv.gro -p topol.top -o ions.tpr"
os.system(cmd)
cmd = "echo '15\n'|gmx genion -s ions.tpr -o solv_ions.gro 
            -p topol.top -pname NA -nname CL -neutral"
os.system(cmd)

# Energy Minimization
cmd = "gmx grompp -f em.mdp -c solv_ions.gro -p topol.top -o em.tpr"
os.system(cmd)
cmd = "gmx mdrun -v -deffnm em"
os.system(cmd)
# Equilibration NVT
……  省略一些数据转换操作
cmd = "gmx grompp -f nvt.mdp -c em.gro -r em.gro -p topol.top -n index.ndx -o nvt.tpr"
os.system(cmd)
cmd = "gmx mdrun -deffnm nvt"
os.system(cmd)
# Equilibration NPT
os.system("gmx grompp -f npt.mdp -c nvt.gro -t nvt.cpt -r nvt.gro -p topol.top -n index.ndx -o npt.tpr")
os.system("gmx mdrun -deffnm npt")
# Production MD
os.system("gmx grompp -f md.mdp -c npt.gro -t npt.cpt -p topol.top -n index.ndx -o md_0_10.tpr")
os.system("gmx mdrun -deffnm md_0_10")
