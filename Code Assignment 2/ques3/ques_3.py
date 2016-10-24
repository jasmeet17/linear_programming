import sys
import numpy as np
from numpy import genfromtxt

class Linear_Prog(object):

    def __init__(self):
        if len(sys.argv)!=5:
            print "Please pass all the files."
            self.dataEntered = False
            return

        self.dict_A = genfromtxt(sys.argv[1], delimiter=',')
        self.vec_c = genfromtxt(sys.argv[2], delimiter=',')
        self.vec_b = genfromtxt(sys.argv[3], delimiter=',')
        self.vec_x = genfromtxt(sys.argv[4], delimiter=',')
        self.constraints_list = []
        self.dataEntered = True

    def printStandardForm(self):
        #Print Objective Funtion
        self.printObjectiveFunction()
        self.printConstraints()


    def printObjectiveFunction(self):

        max_func = ""

        for c in range(self.vec_c.shape[0]):

            # First Check the signs, If value==Zero ,
            # Just Continue(Beause We Dont want to
            # show varaibles with zero constraints)
            if self.vec_c[c]==0:
                continue
            elif self.vec_c[c]<0:
                max_func +=" - "
            elif max_func!="":
                max_func +=" + "

            max_func += str(np.round(self.vec_c[c], decimals=2))
            max_func += " X"+str(c+1)

        print "MAX"
        print "           %s" % max_func
        print

    def printConstraints(self):
        print "SUBJECT TO"
        k = 0
        for constraint_s in self.dict_A:

            constraint = ""

            for c in range(constraint_s.shape[0]):

                # First Check the signs, If value==Zero ,
                # Just Continue(Beause We Dont want to
                # show varaibles with zero constraints)
                if constraint_s[c]==0:
                    continue
                elif constraint_s[c]<0:
                    constraint +=" - "
                elif constraint!="":
                    constraint +=" + "

                constraint += str(np.round(constraint_s[c], decimals=2))
                constraint += " X"+str(c+1)

            constraint += " <= " + str(np.round(self.vec_b[k], decimals=2))
            k = k+1
            print "           %s" % constraint
            self.constraints_list.append(constraint)

        # now print vars >= zero
        zero_conts = ""
        x_vars = []
        for x in range(self.vec_x.shape[0]):
            x_vars.append("X"+str(x+1))

        constraint = ", ".join(x_vars ) +" >= 0.0"
        print "           %s" % constraint

    def checkMatrices(self):
        if self.dict_A.size == 0 or self.dict_A.shape[0]!=self.vec_b.shape[0] or self.dict_A.shape[1]>self.vec_c.shape[0]:
            print "Please Check Matrice A in the File."
            return False
        elif self.vec_b.size == 0:
            print "Please Check Vector B in the File."
            return False
        elif self.vec_c.size == 0 or self.vec_c.size != self.vec_x.size:
            print "Please Check Vector C in the File."
            return False
        elif self.vec_x.size == 0:
            print "Please Check Vector X in the File."
            return False
        return True


    def runAssignmentTest(self):

        # test 1
        print "Part 1"
        print "****Check Matrices and Vectors****"

        if not self.checkMatrices():
            return
        else :
            print "Matrices and Vectors are in standard form."

        # test 2
        print "\nPart 2"
        if self.checkMatrices():
            print "In standard form."
        else:
            print "Not in standard form."

        # test 3 - print standard form
        print "\nPart 3"
        print "*******IN STANARD FORM*******"
        self.printStandardForm()

        # test 4 - Check given solution feasible
        print "\nPart 4"
        print "*******Check Given Solution*******\n\n"

        # Now check if some constraint is voilated
        voilated_constraints = []
        for a in range(self.dict_A.shape[0]):
            value = np.dot(self.dict_A[a],self.vec_x)
            if value>self.vec_b[a]:
                voilated_constraints.append(self.constraints_list[a])

        #voilated constraints for x values only
        for x in range(self.vec_x.shape[0]):
            if self.vec_x[x]<0:
                s = "X"+str(x+1)+" >= 0"
                voilated_constraints.append(s)


        if len(voilated_constraints)==0:
            print "None constraints voilated"
            objective_value = np.dot(self.vec_c,self.vec_x)
            print "Value of the Objective Function : %s" % objective_value
        else:
            print "Solution is not feasible beacuse\nFollowing constraints are voilated"
            for x in voilated_constraints:
                print x




# create an object of Linear_Prog class
linear_prog = Linear_Prog()

# run assignment Tests
if linear_prog.dataEntered:
    linear_prog.runAssignmentTest()



