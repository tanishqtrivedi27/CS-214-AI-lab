import ast #to convert input string to a list
import copy #to generate deepcopy required for moveGen function
import sys #to process command-line arguments

# STACK
class Stack:
    def __init__(self):
        self.list = []

    def push(self,item):
        self.list.append(item)

    def pop(self):
        return self.list.pop()

    def isEmpty(self):
        return len(self.list) == 0

    def contains(self, item):
        for i in self.list:
            if (i == item):
                return True
        return False


# BLOCK WORLD DOMAIN
class blockObject:

    def __init__(self, st1, st2, st3, fn):
        h_val = 0
        self.list1 = Stack()
        self.list2 = Stack()
        self.list3 = Stack()

        self.list1.list = st1
        self.list2.list = st2
        self.list3.list = st3

        self.fn = fn # fn is heuristic function

    def __eq__(self, other):
        if((self.list1.list == other.list1.list) and (self.list2.list == other.list2.list) and (self.list3.list == other.list3.list)):
            return 1
        else:
            return 0
    
    def __str__(self):
        return ''.join(self.list1.list) + " " + ''.join(self.list2.list) + " " + ''.join(self.list3.list) + " "

    #HEURISTIC FUNCTION
    def heuristic_function(self, goal_state, fn):

        """
        HEURISTIC FUNCTION 2
            If the position is correct this heuristic assigns +1000.
            If the postion is incorrect but it is in correct stack then +100 is assigned
        """
        if (fn == 2):
            val = 0
            for i in range(len(goal_state.list1.list)):
                temp1 = goal_state.list1.list[i]

                try:
                    temp2 = self.list1.list[i]
                except:
                    temp2 = -1
                
                if (temp1 == temp2):
                    val = val + 1000
                elif (goal_state.list1.contains(temp2)):
                    val = val + 100
                else:
                    break


            for i in range(len(goal_state.list2.list)):
                temp1 = goal_state.list2.list[i]

                try:
                    temp2 = self.list2.list[i]
                except:
                    temp2 = -1
                
                if (temp1 == temp2):
                    val = val + 1000
                elif (goal_state.list1.contains(temp2)):
                    val = val + 100
                else:
                    break


            for i in range(len(goal_state.list3.list)):
                temp1 = goal_state.list3.list[i]

                try:
                    temp2 = self.list3.list[i]
                except:
                    temp2 = -1
                
                if (temp1 == temp2):
                    val = val + 1000
                elif (goal_state.list1.contains(temp2)):
                    val = val + 100
                else:
                    break

            return val
        """
        HEURISTIC FUNCTION 1
            + height of block if the position is correct
            - height of block if the position is incorrect
        """
        if (fn == 1):
            val = 0
            for i in range(len(self.list1.list)):
                temp1 = self.list1.list[i]

                try:
                    temp2 = goal_state.list1.list[i]
                except:
                    temp2 = -1
                
                if (temp1 == temp2):
                    val = val + i + 1
                elif (temp1 != temp2):
                    val = val - (i + 1)


            for i in range(len(self.list2.list)):
                temp1 = self.list2.list[i]

                try:
                    temp2 = goal_state.list2.list[i]
                except:
                    temp2 = -1
                
                if (temp1 == temp2):
                    val = val + i + 1
                elif (temp1 != temp2):
                    val = val - (i + 1)


            for i in range(len(self.list3.list)):
                temp1 = self.list3.list[i]

                try:
                    temp2 = goal_state.list3.list[i]
                except:
                    temp2 = -1
                
                if (temp1 == temp2):
                    val = val + i + 1
                elif (temp1 != temp2):
                    val = val - (i + 1)
                
            return val



    #  MOVE GEN ALGORTIHM (GENERATE NEIGHBOURS)
    def moveGen(self, goal_state, fn):
        next_states = []

        if(not self.list1.isEmpty()):
            stateCopy1 = copy.deepcopy(self)
            stateCopy2 = copy.deepcopy(self)
            temp1 = stateCopy1.list1.pop()
            stateCopy1.list2.push(temp1)
            temp1 = stateCopy2.list1.pop()
            stateCopy2.list3.push(temp1)
            next_states.append(stateCopy1)
            next_states.append(stateCopy2)

        if(not self.list2.isEmpty()):
            stateCopy3 = copy.deepcopy(self)
            stateCopy4 = copy.deepcopy(self)
            temp1 = stateCopy3.list2.pop()
            stateCopy3.list1.push(temp1)
            temp1 = stateCopy4.list2.pop()
            stateCopy4.list3.push(temp1)
            next_states.append(stateCopy3) 
            next_states.append(stateCopy4)

        if(not self.list3.isEmpty()):
            stateCopy5 = copy.deepcopy(self)
            stateCopy6 = copy.deepcopy(self)
            temp1 = stateCopy5.list3.pop()
            stateCopy5.list1.push(temp1)
            temp1 = stateCopy6.list3.pop()
            stateCopy6.list2.push(temp1)
            next_states.append(stateCopy5)
            next_states.append(stateCopy6)


        next_states.sort(key = lambda x : x.heuristic_function(goal_state, fn), reverse = True)
        return next_states[0]

# GOAL TEST ALGORITHM
def goalTest(current_state, goal_state):
    return current_state == goal_state

# HILL CLIMBING ALGORITHM
def hillClimbing(current_state, goal_state):

    while(not goalTest(current_state, goal_state)):
        # print(current_state)
        temp_hval = current_state.heuristic_function(goal_state, current_state.fn)
        current_state = current_state.moveGen(goal_state, current_state.fn)

        # Break from the loop if peak (max heuristic value) is reached
        if (temp_hval >= current_state.heuristic_function(goal_state, current_state.fn)):
            break

    # print(current_state)
    return current_state




def main():
    # input of start_state and goal_state
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    fn = int(sys.argv[3])
    file1 = open(input_file, "r")
    file1.readline()
    initial_state = blockObject(ast.literal_eval(file1.readline()), ast.literal_eval(file1.readline()), ast.literal_eval(file1.readline()), fn)
    file1.readline()
    goal_state = blockObject(ast.literal_eval(file1.readline()), ast.literal_eval(file1.readline()), ast.literal_eval(file1.readline()), fn)
    file1.close()

    # Hill climbing
    final_state = hillClimbing(initial_state, goal_state)

    file1 = open(output_file, "w")
    file1.write("output state :\n")
    file1.write("[")
    for i in final_state.list1.list:
            file1.write("\'"+i+"\' ")
    file1.write("]\n")
    file1.write("[")
    for i in final_state.list2.list:
            file1.write("\'"+i+"\' ")
    file1.write("]\n")
    file1.write("[")
    for i in final_state.list3.list:
            file1.write("\'"+i+"\' ")
    file1.write("]\n")

    if (final_state != goal_state):
        file1.write("\nGoal state can't be reached\n")
    else : 
        file1.write("\nGoal state was reached\n")
    file1.close()





main()