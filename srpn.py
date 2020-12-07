#STANDARD REVERSE POLISH NOTATION CALCULATOR 

#Declaration: The following is my original work and thought

#Design Overview: For loop which iterates over the user input string, character by character
#Program utilises a temporary stack to hold integers as it iterates, until an operator (or similar character) require the temp_stack to push onto the main stack
#All calculations occur on the main stack 
#Code written from micro to macro level design

#------------------------------------------------import modules--------------------------------------------------------------------------------------------------
import operator
#---------------------------------------------define variables --------------------------------------------------------------------------------------------------

standard_operations = {'+': operator.add, '-': operator.sub, '*':operator.mul , '/':operator.floordiv, '%':operator.mod, '^': operator.pow}

extra_operations=['d','=','r','', ' ']

stack = [] 

global temp_stack
temp_stack=[]

global comment_count
comment_count=0

global r_count
r_count= 0


r_values = [1804289383,
846930886,
1681692777,
1714636915,
1957747793,
424238335,
719885386,
1649760492,
596516649,
1189641421,
1025202362,
1350490027,
783368690,
1102520059,
2044897763,
1967513926,
1365180540,
1540383426,
304089172,
1303455736,
35005211,
521595368]

       
        
#---------------------------------------------reusable functions---------------------------------------------------------------------------------------------------------------------------


#check for stack overflow       
def stack_overflow():
    if len(stack) == 23:
        return True
    else:
        return False
    

#function to handle signed 32bit maximum limit on integers 
def max32bit(num):
    if num > 2147483647: 
        return 2147483647
    elif num < -2147483648:
        return -2147483648
    else:
        return num
    
    
#secondary function to check if input is integer                 
def int_check(char):
    try:
        int(char)
        return True
    except:
        return False
    
    
#zero division error check
def zero_div_check():
    try: 
        stack[-2]/stack[-1]
        return True
    except:
        return False
    
#calculation function: performs calculation and appends result to top of stack
def calculation(user_input):
                global operand_1
                operand_1 = stack.pop()
                operand_2 = stack.pop()
                result = standard_operations[user_input](operand_2, operand_1)
                result = max32bit(result)
                stack.append(result)
                
                
                
#when user inputs '=' return last calculation result
def equal_operator(user_input, i):
    if not stack:
        print('Stack empty.')
  
    if stack and (i-1)>=0 and user_input[i-1]!= ' ':
        global operand_1
        print(operand_1)

    
    elif stack:
        print (stack[-1])
        
        
#when user inputs 'd', print current stack vertically (neg 32 bit max val when stack empty)
def d_operator():
    if not stack: 
        print(-2147483648)
    if stack:
        for num in stack:
            print(num)

#when user inputs 'r', loop through random integer list and append to stack     
def r_operator():
    global temp_stack
    global r_count
    
    if stack_overflow():
            print('Stack overflow.')
            temp_stack = []
        
    else:
        if r_count==22:
            r_count = 0
            stack.append(r_values[r_count])
        else:
            stack.append(r_values[r_count])
            r_count +=1
                
                
                
    
#update what is in the temporary stack, simultaneously checking for stack overflow
#mainly used when the operator/character iterated in the user input requires the temp_stack to push onto the main stack
def main_stack_update():
    global temp_stack

    #check for overflow
    if temp_stack and stack_overflow():
            print ('Stack overflow.')
            temp_stack=[]
        
    #add digits in temp stack to stack
    elif temp_stack and not stack_overflow():
        stack.append(max32bit(int("".join(temp_stack))))
        temp_stack = []
    

    
#--------------------------------------------stand alone functions used in for loop-----------------------------------------------------------------

#check if input is a comment
def comment_check(user_input, i): 
        global comment_count
        
        #end of comment, revert comment count to 0 to indicate comment finish
        if user_input[i] == '#' and comment_count==1 and user_input[i-1] == ' ':
            comment_count = 0 
            return True
        
        #middle of comment   
        elif comment_count==1:
            return True
        
        #start of comment, increment comment count by 1 to indicate comment start
        elif user_input[i] =='#' and ((i+1)<len(user_input)) and user_input[i+1] == ' ' and comment_count==0:
            comment_count=1
            return True

    
#if the first character is a minus, and the second character an integer, treat it as a negative number
def minus_check(user_input, i):
    if (i)==0 and (user_input[i] == '-') and ((i+1)<len(user_input)) and user_input[i+1].isdigit():
        global temp_stack
        temp_stack.append(user_input[i])
        return True
            

#check if last character in user input is a digit, if so append to stack
#special case as last character, so need to append to temp stack before the main stack
def last_char(user_input, i):
    global temp_stack

    if (user_input[i].isdigit() and ((i+1) == len(user_input))):
                
                    if stack_overflow():
                        print('Stack overflow.')
                        temp_stack = []
                        return True
                        
                    else:
                        temp_stack.append(user_input[i])
                        stack.append(max32bit(int("".join(temp_stack))))
                        temp_stack=[]
                        return True


#if character is a digit append to temp stack
def integer_check(user_input, i):
    global temp_stack
    
    if user_input[i].isdigit():
        temp_stack.append(user_input[i])
        return True



#check if user inputs one of the extra operators       
def check_extra_operator(user_input,i):
    
    if user_input[i] in extra_operations:
        global temp_stack
        
        main_stack_update()
            
        #if user inputs '=' return last calculation result from stack
        if user_input[i] == '=':
            equal_operator(user_input, i)
            return True

        #if user inputs 'd', print stack vertically
        elif user_input[i] == 'd':
            d_operator()
            return True
        
        #if user inputs 'r', return integer from r values
        elif user_input[i] =='r':
            r_operator()
            return True
        
        else:
            return True
        

    
        
#check if user inputs standard operator
def standard_operations_func(user_input,i):
    if user_input[i] in standard_operations:   
        global temp_stack
        
        main_stack_update()

            
        #edge case 1: Stack underflow
        if len(stack) <=1: 
            print('Stack underflow.')
            return True


        #edge case 2: Zero Division Error
        if user_input[i] in ['/','%'] and zero_div_check() == False:
            print('Divide by 0.')
            return True

        
        #when all edge cases passed, perform calculation
        else:
            calculation(user_input[i])
            return True
        
        

#all other unrecognised characters should provide a warning message, highlighting the character in question
def unrecognised(user_input, i):
    global temp_stack

    main_stack_update()

    print('Unrecognised operator or operand "{}".'.format(user_input[i]))
    return True

        
#main function to check user input------------------------------------------------------------------------------
def main(user_input):
    
    for i in range(len(user_input)):
        
        #check if input is a comment
        if comment_check(user_input, i): 
            continue
        
        #check if minus number
        elif minus_check(user_input, i):
            continue
        
        #check if last character in user input
        elif last_char(user_input, i):
            continue
        
        #check if character is an integer in user input
        elif integer_check(user_input, i):
            continue
        
        #check if character is one of the extra operators
        elif check_extra_operator(user_input, i):
            continue
            
        #if character in standard operations, perform operation              
        elif standard_operations_func(user_input,i):
            continue
        
        #check if user input is unrecognised
        else:
            unrecognised(user_input,i)
            continue

#----------------------------main continuous loop to handle input into calculator --------------------------------------------------------------------------------------------------------------

while True: 
    user_input = input('')
    
    #if user input valid, continue
    main(user_input)
    