
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
        print(self.cfg_print)
        self.rules(self.cfg_print)

        file=open("output.txt","w")
        for i in self.cfg_print:
            file.write(i)
            file.write("\n")

    def derive(self, trans_func, transition, rules, input, counter):
        counter1 = 0
        len_rules = len(rules)
        while counter1 != len(transition):
            if trans_func[1][1:8] == transition[counter1][0]:
                if input[counter] == transition[counter1][1][0] or transition[counter1][1][0] == '_':
                    rules.append(transition[counter1])
                    counter1 += 1
                else:
                    counter1 += 1
            else:
                counter1 += 1
        if len_rules == len(rules):
            rules.pop()
            len_rules = len(rules)
            counter1 = 0
        else:
            while len(rules) != len_rules:
                if len(rules[-1][1]) != 1:
                    rules.pop()
            counter1 = 0
        while counter1 != len(transition):
            if trans_func[1][8:15] == transition[counter1][0]:
                if input[counter] == transition[counter1][1][0] or transition[counter1][1][0] == '_':
                    rules.append(transition[counter1])
                    counter1 += 1
                else:
                    counter1 += 1
            else:
                counter1 += 1
        if len_rules == len(rules):
            rules.pop()
            len_rules = len(rules)
            counter1 = 0

        else:
            while len(rules) != len_rules:
                rules.pop()
            counter1 = 0

    def derivation(self, initial, transition, input):
        rules = []
        len_rules = 0
        string = []
        counter = 0
        counter1 = 0
        initials = []
        for rule in transition:
            initials.append(rule[0])
        for rule in transition:
            if initial == rule[0]:
                if input[counter] == rule[1][0] and rule[1][1:8] in initials and rule[1][8:15] in initials:
                    rules.append(rule)
                    if input[counter] in string:
                        continue
                    else:
                        string.append(input[counter])
                else:
                    continue
        if len(string) == 0:
            return False
        else:
            counter += 1
            len_rules = len(rules)

        while counter != len(input) - 1:
            for rule in rules:
                if len(rule[1]) != 1:
                    while counter1 != len(transition):
                        if rule[1][1:8] == transition[counter1][0]:
                            try:
                                if input[counter] == transition[counter1][1][0] and transition[counter1][1][0] != '_':
                                    rules.append(transition[counter1])
                                    counter1 += 1
                                else:
                                    counter1 += 1
                            except IndexError:
                                print('Input :' + input)
                                print('Output :')
                                print('False')
                                return False
                        else:
                            counter1 += 1
                    if len_rules == len(rules):
                        rules.remove(rule)
                        len_rules = len(rules)
                        counter1 = 0
                        break
                    else:
                        counter += 1
                        counter1 = 0
                    while counter1 != len(transition):
                        if rule[1][8:15] == transition[counter1][0]:
                            if input[counter] == transition[counter1][1][0] and transition[counter1][1][0] != '_':
                                rules.append(transition[counter1])
                                if len(transition[counter1][0]) > 1:
                                    self.derive(transition[counter1], transition, rules, input, counter)
                                counter1 += 1
                            else:
                                counter1 += 1
                        else:
                            counter1 += 1
                    if len_rules == len(rules):
                        rules.remove(rule)
                        len_rules = len(rules)
                        counter1 = 0
                        break
                    else:
                        counter += 1
                        counter1 = 0
                    if counter == len(input) - 1:
                        break
                    else:
                        continue
                else:
                    continue
        for rule in transition:
            if rules[counter - 1][1][1:8] == rule[0]:
                if len(rule[1]) == 1 or rule[1] == '_':
                    rules.append(rule)
        for rule1 in transition:
            if rules[counter - 1][1][8:15] == rule1[0]:
                if len(rule1[1]) == 1 or rule1[1] == '_':
                    rules.append(rule1)
        print(rules)
        self.print_derivation(rules, input)

    def print_derivation(self, rules, input):
        counter = 0
        print('Input :' + input)
        print('Output :')
        print('True')
        print(rules[0][0] + '=>' + rules[0][1], end="")
        d = '('
        rule_split = [d + e for e in rules[0][1].split(d) if len(e) != 1]
        del rules[0]
        for rule in rules:
            rule_split1 = []
            if rule[0] in rule_split and rule[1] != '_':
                index = rule_split.index(rule[0])
                if len(rule[1]) > 1:
                    rule_split1 = [d + e for e in rule[1].split(d) if len(e) != 1]
                    rule_split1.insert(0, input[counter])
                    rule_split.remove(rule[0])
                    for i in rule_split1:
                        rule_split.append(i)
                    counter += 1
                else:
                    rule_split[index] = rule[1]
                    counter += 1
            elif rule[1] == '_' and counter == len(input) - 1:
                rule_split.pop()
            print('=>' + input[0] + ''.join(rule_split), end="")

    def rules(self, transition):
        rules = []
        while len(transition) > 0:
            string = transition[0][11:]
            if len(string) > 1:
                rules.append((transition[0][0:7], string[: string.index('|')]))
                rules.append((transition[0][0:7], string[string.index('|') + 1:]))
            else:
                rules.append((transition[0][0:7], string))
            transition.remove(transition[0])
        self.derivation('(q0$q1)', rules, 'abb')


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
    NPDA(my_states,my_alph,my_stack_alph,my_stack_pointer,my_init,my_trans,my_statesNO,my_finals)