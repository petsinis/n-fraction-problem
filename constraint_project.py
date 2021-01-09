# -*- coding: utf-8 -*-
"""
Created on Sun Dec  6 11:44:17 2020

@author: petsi

This is a python programm solving n-franction (for n in [2..6]) problem using constraint satisfaction problem
"""

from constraint import *


problem = Problem() #init a constrait problem
n=6 #set n value, i.e. n=3: X1/(Y1Z1)+X2/(Y2Z2)+X3/(Y3Z3) = 1 

print("Set variables and constraints for n-fraction problem with n = "+str(n)+".")
print()

for k in range(n):
    problem.addVariable(str(k+1), [1,2,3,4,5,6,7,8,9]) #X1,X2,...,Xn take values in [1,9] (named as '1','2',..,'n')
    problem.addVariable(str(n+k+1), [1,2,3,4,5,6,7,8,9]) #Y1,Y2,...,Yn  take values in [1,9] (named as 'n+1','n+2',..,'2n')
    problem.addVariable(str(2*n+k+1), [1,2,3,4,5,6,7,8,9]) #Z1,Z2,...,Zn  take values in [1,9] (named as '2n+1','2n+2',..,'3n')



min_rem_sum=sum([i+1 for i in range(3*n-9)]) 
max_rem_sum=sum([9-i for i in range(3*n-9)])
if(n>2):
    problem.addConstraint(MinSumConstraint(45+min_rem_sum)) #Min sum of all variables (45 is set cause 1+2+3+...+9 = 45 and must be fixed)
else:                                                     #cause of the constraint that all values from 1 to 9 must be included for n>2,
    problem.addConstraint(MinSumConstraint(21))           #and for n = 2 the sum 1+2+3+4+5+6=21 is the min sum.
                                                          #The min_rem_sum is the minimum sum for the remaining variables.

if(n>2): 
    problem.addConstraint(MaxSumConstraint(45+max_rem_sum)) #Max sum of all variables (45 is set cause 1+2+3+...+9 = 45 and must be fixed)
else:                                                     #cause of the constraint that all values from 1 to 9 must be included for n>2,
    problem.addConstraint(MaxSumConstraint(39))           #and for n = 2 the sum 4+5+6+7+8+9=39 is the max sum.
                                                          #The max_rem_sum is the maximum sum for the remaining variables.
if(n==6):
    for k in range(9):
        problem.addConstraint(SomeNotInSetConstraint([(i+1)  for i in range(9) if (i!=k)]
                                                     , n=2, exact=True)) #[0..9] at exactly two times
elif(n>2): 
    for k in range(9):
        problem.addConstraint(SomeNotInSetConstraint([(i+1)  for i in range(9) if (i!=k)])) #[0..9] at least one time 
    for k in range(9):
        problem.addConstraint(SomeNotInSetConstraint([(k+1)],n=(3*n-2))) #[0..9] at most 2 times (this works for n>2 and n<=6, it's ok for our exercise)

for k in range(n-1):   
    problem.addConstraint(lambda a, b: a >= b,(str(k+2), str(k+1))) #set X1<=X2<=..<=Xn 





#Use lamda expression to add constraint for the equality 
#---------------------------------------------------------------------------------------------------------------------    
#lambda variables    
lambda_var=''
for k in range(n):
    lambda_var=lambda_var+"\""+str(k+1)+"\","
for k in range(n):
     lambda_var=lambda_var+"\""+str(n+k+1)+"\","
for k in range(n):
     lambda_var=lambda_var+"\""+str(2*n+k+1)+"\","            
lambda_var=lambda_var[0:(len(lambda_var)-1)]   

#lambda parameters
lambda_par=''
for k in range(n):
    lambda_par=lambda_par+"X"+str(k+1)+","
for k in range(n):
     lambda_par=lambda_par+"Y"+str(k+1)+","
for k in range(n):
     lambda_par=lambda_par+"Z"+str(k+1)+","            
lambda_par=lambda_par[0:(len(lambda_par)-1)]  

#lambda expression
lambda_exp=''
for k in range(n):
    lambda_exp=lambda_exp+"X"+str(k+1)+"/(10*Y"+str(k+1)+"+Z"+str(k+1)+")+"      
lambda_exp=lambda_exp[0:(len(lambda_exp)-1)] 


exec("problem.addConstraint(lambda "+lambda_par+": "+lambda_exp+"==1, ("+lambda_var+"))") #add equality constraint
#---------------------------------------------------------------------------------------------------------------------



#make list with variable names i.e. for n=3 -> ["1","2","3","4","5","6","7","8","9"]
string="["    
for k in range(3*n):
    string=string+"\""+str(k+1)+"\","
string=string[0:-1]+"]" 

#add eqeuality and frequency constraint to the problem       
#exec("problem.addConstraint(FunctionConstraint(constr_all),"+string+")")





#find one solution to the problem (if you want to find all solutions use problem.getSolutions())
print("Find solution for n-fraction problem with n = "+str(n)+"...")
sol=problem.getSolution() #X1/(Y1*Z1)+X2/(Y2*Z2)+X3/(Y3*Z3) = 1 <=> '1'/('4''7')+'2'/('5''8')+'3'/('6''9') = 1
                          #a solution can be {'1':5, '2':7, '3':9, '4':3, '5':6, '6':1, '7':4, '8':8, '9':2} 
                          #so 5/(34)+7/(68)+9/(12) = 1
                        
                           
print(f"The solution is: {sol}")
    
#Similarly for n=2 we have:
#X1/(Y1*Z1)+can/(Y2*Z2) = 1 <=> '1'/('3''5')+'2'/('4''6') = 1
#a solution can be {'1':8, '2':9, '3':2, '4':1, '5':6, '6':3} 
#so 8/(26)+9/(13) = 1


#Similarly for n=4 we have:
#X1/(Y1*Z1)+X2/(Y2*Z2)+X3/(Y3*Z3)+X4/(Y4*Z4) = 1 <=> '1'/('5''9')+'2'/('6''10')+'3'/('7''11')+'4'/('8''12') = 1
#a solution can be {'2': 8, '3': 8, '4': 9, '1': 7, '10': 6, '11': 3, '12': 4, '5': 5, '6': 9, '7': 1, '8': 5, '9': 2}
#so 7/(52)+8/(96)+8/(13)+9/(54) = 1


#Similarly for n=5 we have:
#X1/(Y1*Z1)+X2/(Y2*Z2)+X3/(Y3*Z3)+X4/(Y4*Z4)+X5/(Y5*Z5) = 1 <=> 
#'1'/('6''11')+'2'/('7''12')+'3'/('8''13')+'4'/('9''14')+'5'/('10''15') = 1
#a solution can be {'1': 4, '6': 5, '11': 6, '2': 7, '7': 9, '12': 8, '3': 7, '8': 2, '13': 1, '4': 8, '9': 2, '14': 1, '5': 9, '10': 6, '15': 3}
#so 4/(56)+7/(98)+7/(21)+8/(21)+9/(63) = 1


#Similarly for n=6 we have:
#X1/(Y1*Z1)+X2/(Y2*Z2)+X3/(Y3*Z3)+X4/(Y4*Z4)+X5/(Y5*Z5)+X6/(Y6*Z6) = 1 <=> 
#'1'/('7''13')+'2'/('8''14')+'3'/('9''15')+'4'/('10''16')+'5'/('11''17')+'6'/('12''18') = 1
#a solution can be {{'2': 7, '3': 7, '4': 8, '5': 8, '6': 9, '1': 6, '10': 9, '11': 3, '12': 5, '13': 1, '14': 4, '15': 2, '16': 6, '17': 2, '18': 1, '7': 5, '8': 3, '9': 4}
#so 6/(51)+7/(34)+7/(42)+8/(96)+8/(32)+9/(51) = 1



