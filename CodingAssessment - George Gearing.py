#Coding Assessment (Water) | George Gearing | 04/08/2022

FLOW_RATE = 100 #Global constant for the tap rate of flow in ml
WALK_TIME = 2 #Global constant for the time taken for each walk

def FillTime(people, numTaps): #Original Challenge function with input validation
    #Input Validation
    valid = True #Validation boolean
    if not isinstance(numTaps,int) or numTaps < 0 : #Makes sure numTaps is a positive integer
        print("Please enter a positive integer value for the number of taps.")
        valid = False
    else:
        if all([isinstance(x, int) for x in people]): #Checks all elements in people are integers
            for i in range(len(people)): #Checks all elements are positive
                if people[i] <= 0:
                    print("ERROR: Water bottle sizes must greater than 0 ml.")
                    valid = False
        else:
            print("ERROR: Water bottle sizes must be an array of positive integers.")
            valid = False
            
    if valid: #Calculate fill time once inputs have been validated   
        totalTime = 0
        taps = list() #Array will represent the taps and contain the times it will take each person at the taps to finish
        for i in range(numTaps): 
            taps.append(people[0]/FLOW_RATE) #Adds the time taken by the person at the front of the queue
            people.pop(0) #Removes first element in array and shifts queue

        while sum(taps) > 0: #Repeat while at least one tap is occupied       
            taps.sort() #Sorts tap times in ascending order
            for i in range(numTaps): #Gets the non-zero minimum of the taps array i.e the first person to finish next
                if taps[i] > 0: #Excludes empty taps
                    minValue = taps[i]
                    break #Stop once minimum found
            totalTime += minValue
        
            for x in range(numTaps): #Populates taps that are now free
                if taps[x] > 0: #If tap is not indefinitely free
                    taps[x] -= minValue #Items with value of minValue are now 0 i.e "free"
                    if taps[x] == 0 and len(people) > 0: 
                        taps[x] = people[0]/FLOW_RATE #Place next person in queue into free tap
                        people.pop(0) #Remove front element in people array, queue shifts down
        return totalTime
    else:
        return 0 #If validation failed, function outputs zero so as not to cause further errors if function is used without error handling

#NOTE: COMMENTS FOR AMENDED FUNCTIONS ARE ONLY FOR PIECES OF CODE DIFFERING FROM THE ORIGINAL CHALLENGE

def FillTimeWithWalk(people,numTaps): #Original Function with walk time taken into account (assuming initial people start at tap)
    #Input Validation
    valid = True
    if not isinstance(numTaps,int) or numTaps < 0 : 
        print("Please enter a positive integer value for the number of taps.")
        valid = False
    else:
        if all([isinstance(x, int) for x in people]): 
            for i in range(len(people)): 
                if people[i] <= 0:
                    print("ERROR: Water bottle sizes must greater than 0 ml.")
                    valid = False
        else:
            print("ERROR: Water bottle sizes must be an array of positive integers.")
            valid = False
            
    if valid:     
        totalTime = 0
        taps = list()
        for i in range(numTaps): 
            taps.append(people[0]/FLOW_RATE) 
            people.pop(0) 

        while sum(taps) > 0:            
            taps.sort()
            for i in range(len(taps)):
                if taps[i] > 0:
                    minValue = taps[i]
                    break
                
            totalTime += minValue
        
            for x in range(len(taps)): 
                if taps[x] > 0: 
                    taps[x] -= minValue 
                    if taps[x] == 0 and len(people) > 0: 
                        taps[x] = (people[0]/FLOW_RATE)+ WALK_TIME #Add fixed walk time for each person walking to a free tap
                        people.pop(0) 
        return totalTime
    else:
        return 0
    
#Walk time function with different tap pressures taken into account
def FillTimeDiffFlow(people, tapPressures):  # Takes two integer arrays for bottle sizes of each person and pressures of each tap
    numTaps = len(tapPressures) #Gets number of taps implicitly 
    #Input Validation:
    valid = True
    if all([isinstance(x, int) for x in people]) and all([isinstance(x, int) for x in tapPressures]): #Checks all elements in people and tapPressures are integers
        for i in range(len(people)): #Checks all elements of people are positive
            if people[i] <= 0:
                print("ERROR: Water bottle sizes must greater than 0 ml.")
                valid = False
        for i in range(numTaps):  #Checks all elements of tapPressures are positive
            if tapPressures[i] <= 0:
                print("ERROR: Tap pressures must be positive.")
                valid = False
    else:
        print("ERROR: Input arrays must be given as arrays of positive integers.")
        valid = False
    
    if valid: 
        totalTime = 0
        taps = list()
        for i in range(numTaps): 
            taps.append(people[0]/tapPressures[i]) #Adds the time taken by the first person in the queue which now depending on the pressure of the tap
            people.pop(0) 

        while sum(taps) > 0: 
            sortedTaps = taps.copy() #Order of the taps matters now; indices preserved through duplication (python passes reference by value)
            sortedTaps.sort() #Sort in ascending order
            for i in range(numTaps): #Gets the non-zero minimum of the sortedTaps array
                if sortedTaps[i] > 0:
                    minValue = sortedTaps[i]
                    break

            totalTime += minValue
        
            for x in range(numTaps): 
                if taps[x] > 0: 
                    taps[x] -= minValue 
                    if taps[x] == 0 and len(people) > 0: 
                        taps[x] = (people[0]/tapPressures[x]) + WALK_TIME #Replaces free tap with time taken by the next person in the queue depending on the tap's pressure plus the time taken to walk to the tap
                        people.pop(0) 
        return totalTime
    else:
        return 0 
    
# Faster taps, slower time:
# If one increases the flow rate of at least one tap then the slowest total time to fill
# all bottles is the same as the case where all taps run at the same rate. An example of
# this is given below:
print(FillTimeWithWalk([1000,300,400],2))
print(FillTimeDiffFlow([1000,300,400],[100,200]))
# In this scenario the flow rate of the second tap is inconsequential to the total time
# taken as the longest job is the first person with their litre bottle which in both cases
# takes 10s.
# I am unsure of how to prove rigourously that is it otherwise not possible to get a slower time with
# faster tap times. My reasoning is that due to the faster tap, no matter the sizes of the bottles
# of the order of the people in the queue, the time will always be the same or faster than if
# all the taps flowed at the same rate. This is because there are no bottles being filled slower than
# the usual case, but there are some being filled faster which results in a faster time.
