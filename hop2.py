import numpy as np
import matplotlib.pyplot as plt
import random
np.set_printoptions(threshold=np.inf)

class hopfield:
    patterns=[]
    resultx=[]
    resulty=[]
    wdiv=0
    learn_num=0
    noise_pixel=0
    make_max=10

    def __init__(self,height,width):
        self.height=height
        self.width=width
        self.el=height*width
        self.test_times=int(height*width*0.3)
        self.weight=np.zeros((self.el,self.el))

    def import_pattern(self,pattern):
        pattern=pattern.reshape((self.el,1))
        for i in self.patterns:
            if self.dist(i,pattern)==0:
                return 0
        self.patterns.append(pattern.reshape(self.el,1))
        return 1

    def putnoise(self,pattern):
        pattern=pattern.reshape((self.el,1))
        times=self.noise_pixel
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
        self.weight=weight
        self.learn_num=len(self.patterns)
        print("###end learning")
        return weight

    def learn_add(self):
        pat=self.patterns[self.learn_num].reshape((self.el,1))
        for i in range(self.el):
            for j in range(self.el):
                if i!=j:
                    self.weight[i][j]+=pat[i][0]*pat[j][0]
        self.wdiv+=1
        self.learn_num+=1
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
    
    def make1(self,mat):
        mat=mat.reshape((self.el,1))
        test=mat
        ans=mat
        make_times=self.make_max
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
        cos=self.mat_cos(ans,nt2)
        return cos

    def mat_cos(self,mat1,mat2):
        mat1=mat1.reshape((self.el,1))
        mat2=mat2.reshape((self.el,1))
        dif=self.dist(mat1,mat2)
        sam=self.el-dif
        return (sam-dif)/self.el

    def dist(self,mat1,mat2):
        mat1=mat1.reshape((self.el,1))
        mat2=mat2.reshape((self.el,1))
        a=0
        for i in range(self.el):
            if mat1[i][0]!=mat2[i][0]:
                a+=1
        return a

    def test(self):
        times=self.test_times
        for i in range(times):
            while not self.import_pattern(self.make_randmat()):
                continue
            self.learn_add()
            testpat=self.patterns[0].reshape((self.el,1))
            print("pattern_size : "+str(len(self.patterns))+", i : "+str(i))
            cos=self.make1(testpat)
            print("###"+str(cos))
            self.resultx.append((i+1)/self.el)
            self.resulty.append(cos)
        plt.plot(self.resultx,self.resulty)
        plt.vlines([0.138],0,1,"blue",linestyles="dashed")
        plt.ylabel("Overlap")
        plt.xlabel("Loading Rate")
        plt.show()

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

model=hopfield(20,35)
model.test()
