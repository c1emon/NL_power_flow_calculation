from input_data import input_net_args

# 1.数据输入
Line_arg = [
#   导线首端    导线末端    串联电阻    串联电抗    并联电导    并联电纳
    [1 , 2 , 0.02 , 0.06 , 0 , 0],
    [1 , 3 , 0.08 , 0.24 , 0 , 0],
    [2 , 3 , 0.06 , 0.18 , 0 , 0],
    [2 , 4 , 0.06 , 0.18 , 0 , 0],
    [2 , 5 , 0.04 , 0.12 , 0 , 0],
    [3 , 4 , 0.01 , 0.03 , 0 , 0],
    [4 , 5 , 0.08 , 0.24 , 0 , 0]
]

# 数据处理
myarg = input_net_args(Line_arg)

mat_real, mat_imag = myarg.gen_node_admittance_matrix()
print(mat_real, mat_imag)