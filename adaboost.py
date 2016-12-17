import math

print "Enter name of the file"
dataset= raw_input(">")
inputs=[]
file = open(dataset,"r")
a=file.readline()
b=a.split(' ')
t_iterations = int(b[0])
n_examples = int(b[1])
epsilon_val = float(b[2])
#print t_iterations,n_examples,epsilon_val
c=file.readline()
d=(c.split())
for i in range(0,len(d)):
    inputs.append(float(d[i]))
#print "inputs: ",inputs
e = file.readline()
e=e.split()
output=[]
for i in range(0,len(e)):
    output.append(int(e[i]))
#print "outputs ",output
prob=[]
f = file.readline()
f=f.split()
for i in range(0,len(f)):
    prob.append(float(f[i]))
#print "probalilities ",prob

size_hypothesis = (n_examples * 2)+2
#print size_hypothesis
def hypo(inputs, output,size,prob,f_t1):
    store_e_less=[]
    store_e_plus=[]
    prob_n=0
    prob_p=0
    k=2
    h_neg=[]
    h_plus=[]
    h_neg_plus=[]
    h_plus_plus=[]
    hypoth=[]
    #for hypothesis <
         #for h <
    for l in range(0,len(inputs)):
        if (l==0):
            hyp= inputs[l]-0.5
        else:
            hyp = (inputs[l-1]+inputs[l])/2
        hypoth.append(hyp)

    hypoth.append(inputs[len(inputs)-1]+0.5)
    #print "hypothesis ",hypoth
    #for < hypothesis
    for val in hypoth:
        prob_n=0
        for i in range(0,len(output)):
            if(inputs[i]<=val):
                if(output[i] == -1):
                    
                    prob_n=prob_n+prob[i]
                    
        h_neg.append(prob_n)
    
    for val in hypoth:
        prob_p=0
        for i in range(0,len(output)):
            if(inputs[i]>=val):
                #print"ii",inputs[i]
                if(output[i] == 1):
                    prob_p=prob_p+prob[i]
        h_plus.append(prob_p)
    #print "h_neg ",h_neg
    #print "h_plus ",h_plus
    for i in range(0,len(h_neg)):
        store_e_less.append(h_neg[i]+h_plus[i])
    
    # for > hypothesis
    
    for val in hypoth:
        prob_n=0
        for i in range(0,len(output)):
            if(inputs[i]<=val):
                if(output[i] == 1):
                    prob_n=prob_n+prob[i]
        h_neg_plus.append(prob_n)
    
    for val in hypoth:
        prob_p=0
        for i in range(0,len(output)):
            if(inputs[i]>=val):
                if(output[i] == -1):
                    prob_p=prob_p+prob[i]
        h_plus_plus.append(prob_p)
    #print "h_neg ",h_neg_plus
    #print "h_plus ",h_plus_plus
    
    for i in range(0,len(h_neg)):
        store_e_plus.append(h_neg_plus[i]+h_plus_plus[i])
    #print "total error count for less ",store_e_less
    #print "total error count for plus ",store_e_plus
    min_1 = min(store_e_less)
    min_2 = min(store_e_plus)
    minimum = min(min_1,min_2)

    goodness = (0.5)*math.log((1-minimum)/minimum)
    #print "goodness ",goodness
    q_right = math.exp(-goodness)
    q_wrong = math.exp(goodness)
    counter=0
    for i in range(0,len(store_e_less)):
        #print store_e_less[i]," ",minimum
        if(store_e_less[i] == minimum):
            #print "yes"
            index = i
            counter+=1
            break
            
            
    if(counter == 0):
        for i in range(0,len(store_e_plus)):
            if(store_e_plus[i] == minimum):
                index = i
                break
    
    hypoth_select = hypoth[index]
    prob_n=0
    #print "counter", counter
    if(counter != 0):
        for i in range(0,len(prob)):
            if(inputs[i]<=hypoth_select):
                if(output[i] == -1):
                    prob[i]=prob[i]*q_wrong
                else:
                    prob[i]=prob[i]*q_right
            else:
                if(output[i] == 1):
                    prob[i]=prob[i]*q_wrong
                else:
                    prob[i]=prob[i]*q_right
    else:
        for i in range(0,len(prob)):
            if(inputs[i]<=hypoth_select):
                if(output[i] == 1):
                    prob[i]=prob[i]*q_wrong
                else:
                    prob[i]=prob[i]*q_right
            else:
                if(output[i] == -1):
                    prob[i]=prob[i]*q_wrong
                else:
                    prob[i]=prob[i]*q_right
    #print "new_prob",prob
    z=0                   
    for i in range(0,len(prob)):
        z+=prob[i]
    #print "z= ",z

    for i in range(0,len(prob)):
        prob[i]=prob[i]/z
    if(counter!=0):
        print "The selected weak classifier: x<",hypoth_select
    else:
        print "The selected weak classifier: x>",hypoth_select

    print "The error of Ht: ",minimum
    print "The weight of Ht: ",goodness
    print "The probabilities normalization factor: ",z
        
    print "The probabilities after normalization",prob
    if(counter!=0):
        #k.append(str(goodness) +"*Ix<" + str(hypoth_select))
        print "The values ft(xi) for each one of the examples: ",goodness,"*I(x<",hypoth_select,")"
    else:
        #k.append(str(goodness) +"*Ix>" + str(hypoth_select))
        print "The values ft(xi) for each one of the examples: ",goodness,"*I(x>",hypoth_select,")"
    #k.append(str(goodness) + "*I(x<" + str(hypoth_select) + ")")
    #print "k : ",k
    if(counter!=0):
        for i in range(0,len(prob)):
            if(inputs[i]<=hypoth_select):
                f_t1[i]=f_t1[i]+(goodness*1)
            else:
                f_t1[i]=f_t1[i]+(goodness*(-1))
    else:
        for i in range(0,len(prob)):
            if(inputs[i]>=hypoth_select):
                f_t1[i]=f_t1[i]+(goodness*1)
            else:
                f_t1[i]=f_t1[i]+(goodness*(-1))
                           
    #print "The boosted classifier: ",f_t1

    e_t=0.0
    for i in range(0,len(output)):
        if(f_t1[i] >=0.0 and output[i] == -1):
            #print"ft :",f_t[i]
            e_t+=1
        elif(f_t1[i] <0.0 and output[i] == 1):
            #print"ft :",f_t[i]
            e_t+=1
    #print"e_t",e_t
    #print"total errors: ",e_t
    e_t = e_t/len(output)
    print "The error of the boosted classifier Et: ",e_t
    
    
    return z


def hypo_real(inputs,output,size_hypothesis,prob_real,f_t,subs):
    #print "above",f_t
    store_e_less=[]
    store_e_plus=[]
    prob_n=0
    prob_p=0
    k=2
    h_neg=[]
    h_plus=[]
    h_neg_plus=[]
    h_plus_plus=[]
    hypoth=[]
    pr_plus=[]
    pr_minus=[]
    pw_plus=[]
    pw_minus=[]
    #for hypothesis <
         #for h <
    for l in range(0,len(inputs)):
        if (l==0):
            hyp= inputs[l]-0.5
        else:
            hyp = (inputs[l-1]+inputs[l])/2
        hypoth.append(hyp)

    hypoth.append(inputs[len(inputs)-1]+0.5)
    #print hypoth
    
    for val in hypoth:
        prob_n=0
        for i in range(0,len(output)):
            if(inputs[i]<=val):
                if(output[i] == -1):
                    prob_n=prob_n+prob_real[i]
        pw_minus.append(prob_n)

    for val in hypoth:
        prob_p=0
        for i in range(0,len(output)):
            if(inputs[i]<=val):
                if(output[i] == 1):
                    prob_p=prob_p+prob_real[i]
        pr_plus.append(prob_p)

    for val in hypoth:
        prob_p=0
        for i in range(0,len(output)):
            if(inputs[i]>=val):
                if(output[i] == -1):
                    prob_p=prob_p+prob_real[i]
        pr_minus.append(prob_p)

    for val in hypoth:
        prob_p=0
        for i in range(0,len(output)):
            if(inputs[i]>=val):
                if(output[i] == 1):
                    prob_p=prob_p+prob_real[i]
        pw_plus.append(prob_p)
    
    #print pr_plus
    #print pw_minus
    #print pr_minus
    #print pw_plus
    g1=[]
    for i in range(0,len(hypoth)):
        g1.append(math.sqrt(pr_plus[i]*pw_minus[i])+ math.sqrt(pw_plus[i]*pr_minus[i]))
    #print g1


    #g2
    pr_plus_g2=[]
    pr_minus_g2=[]
    pw_plus_g2=[]
    pw_minus_g2=[]
    for val in hypoth:
        prob_n=0
        for i in range(0,len(output)):
            if(inputs[i]>=val):
                if(output[i] == -1):
                    prob_n=prob_n+prob_real[i]
        pw_minus_g2.append(prob_n)

    for val in hypoth:
        prob_p=0
        for i in range(0,len(output)):
            if(inputs[i]>=val):
                if(output[i] == 1):
                    prob_p=prob_p+prob_real[i]
        pr_plus_g2.append(prob_p)

    for val in hypoth:
        prob_p=0
        for i in range(0,len(output)):
            if(inputs[i]<=val):
                if(output[i] == -1):
                    prob_p=prob_p+prob_real[i]
        pr_minus_g2.append(prob_p)

    for val in hypoth:
        prob_p=0
        for i in range(0,len(output)):
            if(inputs[i]<=val):
                if(output[i] == 1):
                    prob_p=prob_p+prob_real[i]
        pw_plus_g2.append(prob_p)

    g2=[]
    for i in range(0,len(hypoth)):
        g2.append(math.sqrt(pr_plus_g2[i]*pw_minus_g2[i])+ math.sqrt(pw_plus_g2[i]*pr_minus_g2[i]))
    #print g2
    
    min_1 = min(g1)
    min_2 = min(g2)
    minimum = min(min_1,min_2)
    #print "G:  ",minimum
    counter=0
    for i in range(0,len(g1)):
        if(g1[i]==minimum):
            counter+=1
            index =i
            #print "index",index
            break
    for j in range(0,len(g2)):
        if(g2[j]==minimum):
            index =j
    #print "index",index
    #print "pr_plus",pr_plus[3]
    if(counter!=0):
        #print pr_plus[index]
        #print pw_minus[index]
        c_t_plus=0.5*math.log((pr_plus[index] + epsilon_val)/(pw_minus[index] + epsilon_val))
        c_t_minus=0.5*math.log((pw_plus[index] + epsilon_val)/(pr_minus[index] + epsilon_val))
        
    else:
        c_t_plus=0.5*math.log((pr_plus_g2[index] + epsilon_val)/(pw_minus_g2[index] + epsilon_val))
        c_t_minus=0.5*math.log((pw_plus_g2[index] + epsilon_val)/(pr_minus_g2[index] + epsilon_val))
    hypoth_select=hypoth[index]
    if(counter!=0):
        print "The selected weak classifier Ht x<",hypoth_select
    else:
        print "The selected weak classifier Ht x>",hypoth_select
    
    print "The G error value of Ht: ",minimum       
    print "The weights Ct+,Ct-:",c_t_plus,c_t_minus
    
    
    #updating probabilities
    if(counter != 0):
        for i in range(0,len(prob_real)):
            if(inputs[i]<=hypoth_select):
                prob_real[i] = prob_real[i] * math.exp(-output[i]*c_t_plus)
                
            else:
                prob_real[i] = prob_real[i] * math.exp(-output[i]*c_t_minus)
                
    else:
        for i in range(0,len(prob)):
            if(inputs[i]<=hypoth_select):
                prob_real[i] = prob_real[i] * math.exp(-output[i]*c_t_minus)
            else:
                prob_real[i] = prob_real[i] * math.exp(-output[i]*c_t_plus)
    z_real =0
    for i in range(0,len(prob_real)):
        z_real = z_real +prob_real[i] 
    #print z_real
    for i in range(0,len(prob_real)):
        prob_real[i] = prob_real[i]/z_real
    print "The probabilities normalization factor Zt: ",z_real
    print "The probabilities after normalization: ",prob_real
    
    if(counter != 0):
        for i in range(0,len(prob_real)):
            if(inputs[i]<=hypoth_select):
                f_t[i] = f_t[i] + c_t_plus
            else:
                f_t[i] = f_t[i] +c_t_minus
    else:
        for i in range(0,len(prob_real)):
            if(inputs[i]>=hypoth_select):
                f_t[i] = f_t[i] + c_t_plus
            else:
                f_t[i] = f_t[i] +c_t_minus
    print "The values ft(xi) for each one of the examples: ",f_t
    
    
    e_t=0.0
    for i in range(0,len(output)):
        if(f_t[i] >=0.0 and output[i] == -1):
            #print"ft :",f_t[i]
            e_t+=1
        elif(f_t[i] <0.0 and output[i] == 1):
            #print"ft :",f_t[i]
            e_t+=1
    #print"e_t",e_t
    e_t = e_t/len(output)
    print "The error of the boosted classifier Et: ",e_t
            
            
    
    
                    
    #above
        
    

    return z_real








bound = []
f_t1=[]
for i in range(0,len(prob)):
    f_t1.append(0.0)

for i in range(0,t_iterations):
    print ""
    print "Iteration ",i+1
    print" "
    z=hypo(inputs,output,size_hypothesis,prob,f_t1)
    bound.append(z)
    multi =1
    for j in range(0,len(bound)):
        multi = multi*bound[j]
    print "The bound on Et: ",multi
#print bound
bound_2=[]
prob_real=[]
for i in range(0,len(f)):
    prob_real.append(float(f[i]))
print""
print "The following output is for Real Adaboosting."
f_t=[]

for i in range(0,len(prob_real)):
    f_t.append(0.0)
#print"f_t: ",f_t
subs=0
for i in range(0,t_iterations):
    print ""
    print "Iteration ",i+1
    print" "
    subs=subs+1
    z2=hypo_real(inputs,output,size_hypothesis,prob_real,f_t,subs)
    bound_2.append(z2)
    multi =1
    
    for j in range(0,len(bound_2)):
        multi = multi*bound_2[j]
    print "The bound on Et: ",multi
    

    




