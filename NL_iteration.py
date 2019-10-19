

class NL_Iteration(object):
    def __init__(self, infos):
        self.infos = infos
        self.init_value = self.infos.Init_val
        self.delta_P = []
        self.delta_Q = []
        

    def calc_delta_val(self):
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
            if node["node_type"] == "PV":
                P_i = node["P"]  

            
            temp = 0
            for j, init_val in enumerate(self.init_value):
                temp += e_i * (self.infos.G[i][j] * init_val[1]["e"] - self.infos.B[i][j] * init_val[1]["f"]) + f_i * (self.infos.G[i][j] * init_val[1]["f"] + self.infos.B[i][j] * init_val[1]["e"])
            self.delta_P.append(P_i - temp)

            temp = 0
            for j, init_val in enumerate(self.init_value):
                temp += f_i * (self.infos.G[i][j] * init_val[1]["e"] - self.infos.B[i][j] * init_val[1]["f"]) - e_i * (self.infos.G[i][j] * init_val[1]["f"] + self.infos.B[i][j] * init_val[1]["e"])
            self.delta_Q.append(Q_i - temp)