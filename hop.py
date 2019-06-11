import numpy as np
import matplotlib.pyplot as plt
import random
np.set_printoptions(threshold=np.inf)

noise_pixel=0
make_max=10

class hopfield:
    patterns=[]
    resultx=[]
    resulty=[]
    wdiv=0

    def __init__(self,height,width):
        self.height=height
        self.width=width
        self.el=height*width
        self.test_times=int(height*width*0.3)
        self.weight=np.zeros((self.el,self.el))

    def import_pattern(self,pattern):
        for i in self.patterns:
            if self.dist(i,pattern)==0:
                return 0
        #if not pattern in self.patterns:
        self.patterns.append(pattern.reshape(self.el,1))
        return 1

    def putnoise(self,pattern):
        pattern=pattern.reshape((self.el,1))
        times=noise_pixel
        for _ in range(times):
            pattern[random.randrange(self.el)][0]=-pattern[random.randrange(self.el)][0]
        return pattern

    def learning(self):
        weight=np.zeros((self.el,self.el))
        for pat in self.patterns:
            for i in range(self.el):
                for j in range(self.el):
                    if i!=j:
                        weight[i][j]+=pat[i][0]*pat[j][0]
            self.wdiv+=1
        #print(weight)
        self.weight=weight
        print("###end learning")
        return weight

    def learn_add(self,pattern):
        pat=pattern.reshape((self.el,1))
        for i in range(self.el):
            for j in range(self.el):
                if i!=j:
                    self.weight[i][j]+=pat[i][0]*pat[j][0]
        self.wdiv+=1
        print("### end learning ###")

    def make_randmat(self):
        mat=np.zeros((self.el,1))
        for i in range(self.el):
            mat[i][0]=random.uniform(-100,100)
        mat=np.sign(mat)
        for i in range(self.el):
            if mat[i][0]==0:
                mat[i][0]=1
        return mat

    def printmat(self,mat):
        mat=mat.reshape((self.el,1))
        for y in range(self.height):
            row=""
            for x in range(self.width):
                if mat[y*self.width+x][0]==1:
                    row+='#'
                elif mat[y*self.width+x][0]==-1:
                    row+='.'
                else:
                    row+='?'
            print(row,end="\n")
        print("")
    
    def making(self,test):
        make_times=make_max
        nt1=test
        for _ in range(make_times):
            nt2=np.zeros((self.el,1))
            for i in range(self.el):
                for j in range(self.el):
                    nt2[i][0]+=self.weight[i][j]/self.wdiv*nt1[j][0]
            print(nt2.reshape(self.height,self.width))
            nt2=np.sign(nt2)
            for i in range(self.el):
                if nt2[i][0]==0:
                    nt2[i][0]=1
            if self.dist(nt1,nt2)==0:
                break
            nt1=nt2
            self.printmat(nt2.reshape(self.height,self.width))
        print("----------------------------------------------------------")
        self.printmat(nt2.reshape(self.height,self.width))
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    
    def make1(self,test,ans):
        make_times=make_max
        nt1=test
        for _ in range(make_times):
            nt2=np.zeros((self.el,1))
            for i in range(self.el):
                for j in range(self.el):
                    nt2[i][0]+=self.weight[i][j]/self.wdiv*nt1[j][0]
            nt2=np.sign(nt2)
            for i in range(self.el):
                if nt2[i][0]==0:
                    nt2[i][0]=1
            if self.dist(nt1,nt2)==0:
                break
            nt1=nt2
            #self.printmat(nt2.reshape(self.height,self.width))
            #print(self.mat_cos(ans,nt2))
        #print("----------------------------------------------------------")
        #self.printmat(nt2.reshape(self.height,self.width))
        #self.printmat(ans.reshape(self.height,self.width))
        #print(self.mat_cos(ans,nt2))
        cos=self.mat_cos(ans,nt2)
        #print(cos)
        return cos

    def mat_cos(self,mat1,mat2):
        mat1=mat1.reshape((self.el,1))
        mat2=mat2.reshape((self.el,1))
        a=0
        for i in range(self.el):
            a+=mat1[i][0]*mat2[i][0]
        a/=self.el
        return a

    def dist(self,mat1,mat2):
        mat1=mat1.reshape((self.el,1))
        mat2=mat2.reshape((self.el,1))
        a=0
        for i in range(self.el):
            a+=(mat1[i][0]!=mat2[i][0])
        return a

    def test(self):
        times=self.test_times
        for i in range(times):
            while not self.import_pattern(self.make_randmat()):
                continue
            self.learn_add(self.patterns[len(self.patterns)-1])
            #anspat=self.patterns[random.randrange(i+1)].reshape((el,1))
            anspat=self.patterns[0].reshape((self.el,1))
            #testpat=self.putnoise(anspat)
            testpat=anspat
            #path="./result"+str(i)+".txt"
            print("pattern_size : "+str(len(self.patterns))+", i : "+str(i))
            #f=open(path,mode="w")
            #cos=self.make2(testpat,anspat,f)
            cos=self.make1(testpat,anspat)
            #f.close()
            print("###"+str(cos))
            #plt.plot(i+1,cos)
            self.resultx.append((i+1)/self.el)
            self.resulty.append(cos)
        plt.plot(self.resultx,self.resulty)
        plt.vlines([0.138],0,1,"blue",linestyles="dashed")
        plt.show()
        #for i in self.patterns:
        #    self.printmat(i)

        wei=self.weight
        wei2=self.learning()
        judge=1
        for i in range(self.el):
            for j in range(self.el):
                if wei[i][j]!=wei2[i][j]:
                    judge=0
        if judge==1:
            print("weight ok")
        else:
            print("weight error")


#########################################################

basepat=np.array([[1,1,1,1,1,1,1,1,1,1],
              [1,1,1,1,1,1,1,1,1,1],
              [1,1,1,1,1,1,1,1,1,1],
              [1,1,1,1,1,1,1,1,1,1],
              [1,1,1,1,1,1,1,1,1,1],
              [1,1,1,1,1,1,1,1,1,1],
              [1,1,1,1,1,1,1,1,1,1],
              [1,1,1,1,1,1,1,1,1,1],
              [1,1,1,1,1,1,1,1,1,1],
              [1,1,1,1,1,1,1,1,1,1]])

pat1=np.array([[1,1,1,1,1,1,1,1,1,1],   ##########
              [1,-1,-1,1,1,1,1,1,1,1],  #..#######
              [1,-1,-1,-1,1,1,1,1,1,1], #...######
              [1,1,-1,-1,-1,1,1,1,1,1], ##...#####
              [1,1,1,-1,-1,-1,1,1,1,1], ###...####
              [1,1,1,1,-1,-1,-1,1,1,1], ####...###
              [1,1,1,1,1,-1,-1,-1,1,1], #####...##
              [1,1,1,1,1,1,-1,-1,-1,1], ######...#
              [1,1,1,1,1,1,1,-1,-1,1],  #######..#
              [1,1,1,1,1,1,1,1,1,1]])   ##########

pat2=np.array([[1,1,1,1,1,1,1,1,1,1],        ##########
              [1,-1,-1,-1,-1,-1,-1,-1,-1,1], #........#
              [1,-1,-1,-1,-1,-1,-1,-1,-1,1], #........#
              [1,1,1,1,1,1,1,1,1,1],         ##########
              [1,1,1,1,1,1,1,1,1,1],         ##########
              [1,1,1,1,1,1,1,1,1,1],         ##########
              [1,1,1,1,1,1,1,1,1,1],         ##########
              [1,-1,-1,-1,-1,-1,-1,-1,-1,1], #........#
              [1,-1,-1,-1,-1,-1,-1,-1,-1,1], #........#
              [1,1,1,1,1,1,1,1,1,1]])        ##########

testpat=np.array([[1,1,-1,1,1,-1,1,1,1,1],
              [1,-1,1,1,1,-1,1,-1,-1,1],
              [1,1,1,-1,-1,1,1,1,1,1],
              [1,1,1,-1,-1,1,1,1,-1,1],
              [1,1,1,1,-1,1,-1,1,1,1],
              [1,1,1,1,1,1,1,-1,1,1],
              [1,1,-1,1,1,1,-1,1,-1,1],
              [1,1,1,1,1,1,1,1,-1,1],
              [1,1,1,-1,1,-1,-1,1,-1,1],
              [1,1,1,1,1,1,1,1,1,1]])

t2=np.array([[1,1,1,1,1,1,1,1,1,1],
              [1,-1,-1,-1,1,1,1,1,1,1],
              [1,1,1,1,1,1,1,1,1,1],
              [1,1,1,1,1,1,1,1,1,1],
              [1,1,1,1,1,1,1,1,1,1],
              [1,1,1,1,1,1,1,1,1,1],
              [1,1,1,1,1,1,1,1,1,1],
              [1,1,1,1,1,1,1,1,1,1],
              [1,-1,-1,-1,1,1,-1,-1,-1,1],
              [1,1,1,1,1,1,1,1,1,1]])

#printmat(testpat)


num=0
model=hopfield(10,10)
num+=model.import_pattern(pat1)
model.learn_add(model.patterns[len(model.patterns)-1])
num+=model.import_pattern(pat2)
model.learn_add(model.patterns[len(model.patterns)-1])
model.printmat(testpat)
model.making(testpat.reshape((100,1)))
#model.printmat(t2)
#model.making(t2.reshape((100,1)))
"""

model=hopfield(15,15)
model.test()



model=hopfield(2,10)
model.import_pattern(np.array([[-1,1,1,1,1,1,1,1,1,1],[-1,1,1,1,1,1,1,1,1,1]]))
model.learn_add(model.patterns[0])
print(model.weight)

model.import_pattern(np.array([[1,1,-1,-1,1,-1,-1,1,1,-1],[-1,1,1,1,1,1,1,1,1,1]]))
model.learn_add(model.patterns[1])
print(model.weight)

model.making(np.array([[1,1,1,1,1,-1,-1,1,1,1],[1,1,1,1,1,1,1,1,1,1]]).reshape((20,1)))
"""