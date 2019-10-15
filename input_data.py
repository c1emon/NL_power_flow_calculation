class input_net_args:

    def __init__(self, arg_line):
        self.Line = arg_line
        self._line_admittance = []
        self.node_admittance_matrix_real = []
        self.node_admittance_matrix_imag = []
        self._line_args_conv()

    # 复数倒数    
    def _complx_reciprocal(self, real, imag):
        mod = real*real + imag*imag
        return real/mod, imag/mod
    # 阻抗转导纳
    def impedance2admittance(self, R, X):
        return self._complx_reciprocal(R, X)
    # 导纳转阻抗
    def admittance2impedance(self, G, B):
        return self._complx_reciprocal(G, B)

    def _line_args_conv(self):
        for item in self.Line:
            temp = item
            temp[2], temp[3] = self.impedance2admittance(item[2], item[3])
            self._line_admittance.append(temp)


    # 生成导纳矩阵
    def gen_node_admittance_matrix(self):
        temp = []
        for item in self.Line:
            temp.append(item[0])
            temp.append(item[1])

        # 导纳矩阵阶数
        order = max(temp)

        for i in range(0, order):
            temp_1 = []
            temp_2 = []
            for j in range(0, order):
                if i == j:
                    val_real = 0
                    val_imag = 0
                    for item in self.Line:
                        if ( item[0] == (j + 1) or item[1] == (j + 1) ):
                            val_real += item[2] + item[4]
                            val_imag += item[3] + item[5]
                    temp_1.append(val_real)  
                    temp_2.append(-val_imag)                  
                else:
                    val_real = 0
                    val_imag = 0
                    for item in self.Line:
                        if ( item[0] == (i + 1) and item[1] == (j + 1) ) or ( item[1] == (i + 1) and item[0] == (j + 1) ):
                            val_real += -item[2]
                            val_imag += -item[3]
                    temp_1.append(val_real)
                    temp_2.append(-val_imag)                  
            self.node_admittance_matrix_real.append(temp_1)
            self.node_admittance_matrix_imag.append(temp_2)
        return self.node_admittance_matrix_real, self.node_admittance_matrix_imag
            

if __name__ == "__main__":
    
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