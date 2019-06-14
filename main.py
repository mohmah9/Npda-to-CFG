
class NPDA :

    def __init__(self ,states,alphabet,stack_alphabet,stack_pointer,initial,trans_func ,state_num, finals):
        self.state_num=state_num
        self.states=states
        self.alphabet=alphabet
        self.initial=initial
        self.finals=finals
        self.trans_func = trans_func
        self.stack_alphabet=stack_alphabet
        self.stack_pointer=stack_pointer
        self.cfg=[]
        self.cfg_print=[]
        self.to_dic()

    def to_dic(self):
        my_npda={}
        my_npda["states"] = self.states
        my_npda["state_num"] = self.state_num
        my_npda["alphabet"] = self.alphabet
        my_npda["func"]=self.trans_func
        my_npda["initial"]=self.initial
        my_npda["finals"]=self.finals
        my_npda["stack_pointer"]=self.stack_pointer
        my_npda["stack_alphabet"]=self.stack_alphabet
        print("NPDA Done.")
        self.to_cfg()

    def to_cfg(self):
        for tran in self.trans_func:
            if tran[3] == "_" :
                temp=[tran[0],tran[2],tran[4],tran[1]]
                self.cfg.append(temp)
            else:
                for k in self.states:
                    for j in self.states:
                        temp=[tran[0],tran[2],k ,tran[1],tran[0],tran[3][0],j,j,tran[3][1],k]
                        self.cfg.append(temp)
        for i in self.cfg:
            if len(i)!=4:
                for j in self.cfg:
                    if len(j)!=4 and i!=j:
                        if i[0]==j[0] and i[1]==j[1] and i[2]==j[2] and i[3]==j[3]:
                            for k in range(3,len(j)):
                                i.append(j[k])
                            self.cfg.remove(j)


        for i in self.cfg:
            if len(i)==4:
                self.cfg_print.append("(%s%s%s) -> %s" %tuple(i))
            elif len(i)==10:
                self.cfg_print.append("(%s%s%s) -> %s(%s%s%s)(%s%s%s)" % tuple(i))
            else:
                self.cfg_print.append("(%s%s%s) -> %s(%s%s%s)(%s%s%s)|%s(%s%s%s)(%s%s%s)" % tuple(i))
        print(len(self.cfg),self.cfg)
        print(self.cfg_print)

        file=open("output.txt","w")
        for i in self.cfg_print:
            file.write(i)
            file.write("\n")

if __name__ =='__main__':
    file = open("input.txt" , "r")
    contents = file.readlines()
    file.close()
    for i in range(len(contents)):
        contents[i]=contents[i].strip()
    my_statesNO = int(contents[0])
    my_alph = contents[1].split(",")
    my_stack_alph = contents[2].split(",")
    my_stack_pointer = contents[3]
    for i in contents[4:]:
        if i[0:2] == "->":
            my_init = i.split(',')[0][2:]
    my_finals=[]
    for i in contents[4:]:
        j = i.split(",")
        for k in j:
            if k[0] == "*":
                my_finals.append(k[1:])
    my_finals = list(set(my_finals))
    contents2=contents[4:]
    for i in range(len(contents2)):
        contents2[i] = contents2[i].replace("->", "")
        contents2[i] = contents2[i].replace("*", "")
    my_trans=[]
    for i in contents2:
        my_trans.append(i.split(','))
    my_states=[]
    for i in my_trans:
        my_states.append(i[0])
        my_states.append(i[4])
    my_states = list(set(my_states))
    q = my_states.index(my_init)
    my_states[0], my_states[q] = my_states[q], my_states[0]
    print(my_statesNO,my_alph,my_stack_alph,my_stack_pointer,my_finals,my_init,my_states,my_trans)
    NPDA(my_states,my_alph,my_stack_alph,my_stack_pointer,my_init,my_trans,my_statesNO,my_finals)