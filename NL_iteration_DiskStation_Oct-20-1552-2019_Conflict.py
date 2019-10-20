

class NL_Iteration(object):
    def __init__(self, infos):
        self.infos = infos
        self.init_value = self.infos.Init_val
        self._delta_P_PQ = []
        self._delta_Q_PQ = []
        self._delta_P_PV = []
        self._delta_U_PV = []
        

    def _calc_delta_val(self):
        for i, node in enumerate(self.infos.Node_infos):
            if node["node_type"] == "SLACK":
                continue
            e_i = 0
            f_i = 0
            P_i = 0
            Q_i = 0
            for item in self.init_value:
                if item[0] == (i+1):
                    e_i = item[1]["e"]
                    f_i = item[1]["f"]
                    break            
            
            if node["node_type"] == "PQ":
                P_i = node["P"]
                Q_i = node["Q"]

                temp = 0
                for j, init_val in enumerate(self.init_value):
                    temp += e_i * (self.infos.G[i][j] * init_val[1]["e"] - self.infos.B[i][j] * init_val[1]["f"]) + f_i * (self.infos.G[i][j] * init_val[1]["f"] + self.infos.B[i][j] * init_val[1]["e"])
                self._delta_P_PQ.append(P_i - temp)

                temp = 0
                for j, init_val in enumerate(self.init_value):
                    temp += f_i * (self.infos.G[i][j] * init_val[1]["e"] - self.infos.B[i][j] * init_val[1]["f"]) - e_i * (self.infos.G[i][j] * init_val[1]["f"] + self.infos.B[i][j] * init_val[1]["e"])
                self._delta_Q_PQ.append(Q_i - temp)


            if node["node_type"] == "PV":
                P_i = node["P"]

                temp = 0
                for j, init_val in enumerate(self.init_value):
                    temp += e_i * (self.infos.G[i][j] * init_val[1]["e"] - self.infos.B[i][j] * init_val[1]["f"]) + f_i * (self.infos.G[i][j] * init_val[1]["f"] + self.infos.B[i][j] * init_val[1]["e"])
                self._delta_P_PV.append(P_i - temp)

                temp = node["V"]**2 - (self.init_value[i][1]["e"]**2 + self.init_value[i][1]["f"]**2)
                self._delta_U_PV.append(temp)
        

    def gen_J_mat(self):
        for i, node_i in enumerate(self.infos.Node_infos):
            if node_i["node_type"] == "SLACK":
                continue
            e_i, f_i = 0, 0
            for item in self.init_value:
                if item[0] == (i+1):
                    e_i = item[1]["e"]
                    f_i = item[1]["f"]
                    break
            for j, node_j in enumerate(self.infos.Node_infos):
                if node_j["node_type"] == "SLACK":
                    continue
                if i == j :
                    H_ii, N_ii, J_ii, L_ii, R_ii, S_ii = 0, 0, 0, 0, 0, 0
                    for k, item in enumerate(self.init_value):
                        H_ii += self.infos.G[i][k] * item[1]["f"] + self.infos.B[i][k] * item[1]["e"]
                        N_ii += self.infos.G[i][k] * item[1]["e"] - self.infos.B[i][k] * item[1]["f"]
                    J_ii +=  N_ii - self.infos.B[i][i] * self.init_value[i][1]["f"] - self.infos.G[i][i] * self.init_value[i][1]["e"]
                    L_ii += -H_ii + self.infos.G[i][i] * self.init_value[i][1]["f"] - self.infos.B[i][i] * self.init_value[i][1]["e"]
                    H_ii += -self.infos.B[i][i] * self.init_value[i][1]["e"] + self.infos.G[i][i] * self.init_value[i][1]["f"]
                    N_ii +=  self.infos.G[i][i] * self.init_value[i][1]["e"] + self.infos.B[i][i] * self.init_value[i][1]["f"]
                    R_ii = 2 * self.init_value[i][1]["f"]
                    S_ii = 2 * self.init_value[i][1]["e"]
                    
                    t = [[H_ii, N_ii], [J_ii, L_ii]]
                    # print(t)

                else:
                    H_ij = -self.infos.B[i][j] * e_i + self.infos.G[i][j] * f_i
                    N_ij =  self.infos.G[i][j] * e_i + self.infos.B[i][j] * f_i
                    J_ij = -N_ij
                    L_ij =  H_ij
                    R_ij = 0
                    S_ij = 0
                    t = [[H_ij, N_ij], [J_ij, L_ij]]
                    print(t)
            
