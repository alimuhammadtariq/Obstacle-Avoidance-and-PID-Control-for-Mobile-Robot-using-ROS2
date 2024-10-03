
class Fuzzyrightedge:

    def __init__(self,RB_dist,RF_dist):
        self.RB_dist=RB_dist
        self.RF_dist=RF_dist

fuzzy_instance = Fuzzyrightedge(10, 10)

RB_dist=fuzzy_instance.RB_dist
RF_dist=fuzzy_instance.RF_dist




#----------------STEP1 MAPPING OF INPUT AND OUTPUT SPACE-------------------
class Membershipfunction:

    def __init__(self, Points, label):
        # Takes four point as input (Points) for the trapozial membership. The center triangle is special case of
        # trpozide where two points are same forming the triangle [0.25, 0.5, 0.5, 0.75], labels gives labels for
        # the member values ie far, medium, near

        self.points = Points
        self.linguistic_label = label

    def getMemberValue(self, input_value):  # to get membership value from input sensor value

        # if input value outside the trapozidal Range the return is zero
        if input_value < self.points[0] or input_value > self.points[3]:
            return 0.01

        # Rising edge formula implementation (x-a)/(b-a) since self.point is list extract value by index
        elif input_value >= self.points[0] and input_value < self.points[1]:
            return (input_value - self.points[0]) / (self.points[1] - self.points[0])

        # Falling edge formula implementation (c-x)/(c-b) since self.point is list extract value by index
        elif input_value > self.points[2] and input_value < self.points[3]:
            return (self.points[3] - input_value) / (self.points[3] - self.points[2])

        # if input value at the plateue of trapozid return 1
        elif input_value >= self.points[1] and input_value <= self.points[2]:
            return 1.0

        return 0.0


# assigning range to close, medium and fast


close_RB_Dist = Membershipfunction([0.0, 0.0, 0.25, 0.5], 'close')
close_RF_Dist = Membershipfunction([0.0, 0.0, 0.25, 0.5], 'close')

med_RB_Dist = Membershipfunction([0.25, 0.5, 0.5, 0.75], 'med')
med_RF_Dist = Membershipfunction([0.25, 0.5, 0.5, 0.75], 'med')

far_RB_Dist = Membershipfunction([0.5, 0.75, 1.0, 1.0], 'far')
far_RF_Dist = Membershipfunction([0.5, 0.75, 1.0, 1.0], 'far')


#Step 2------------Define the rule Base----------------


class rule:

    def __init__(self, i, o):
        # Makes the rule base. where i=inputs RFS and RBS ( and o=outputs (Turning and speed). The rule base is initiated
        # blow this block of code. Check blew this code blow to check input and outputs
        self.inputs = i
        self.outputs = o

    def getFir(self, list_Values):
        # to get firing strength: List value are  List of [RFS, RBS] where the list is has two elemnts each dictonary
        # if RB_dist = 0.3 and RF_dist = 0.6 as in lab example its prints out list with two dictionaries
        #list_Values= [{'close': 0.0, 'med': 0.6000000000000001, 'far': 0.3999999999999999},{'close': 0.8, 'med': 0.19999999999999996, 'far': 0.0}]
        list_memValues = []
        for i in range(len(self.inputs)):
            list_memValues.append(list_Values[i][self.inputs[i]])#iterrate over list ie first dictionary and second and pulls the value of [self.inputs[i] string from first and second dictionary. Strings are the keys
        return min(list_memValues)


#            RULEBASE

#             input i           output O
#            [RFS  RBS]       [ TURNING, SPEED]
r1 = rule(['close', 'close'], ['left', 'slow'])
r2 = rule(['close', 'med'], ['left', 'slow'])
r3 = rule(['close', 'far'], ['left', 'med'])
r4 = rule(['med', 'close'], ['right', 'med'])
r5 = rule(['med', 'med'], ['med', 'med'])
r6 = rule(['med', 'far'], ['left', 'med'])
r7 = rule(['far', 'close'], ['right', 'slow'])
r8 = rule(['far', 'med'], ['right', 'slow'])
r9 = rule(['far', 'far'], ['right', 'slow'])





# initaite the dictionary to store the string value assosiated with Close mid far (RBS = {}  and RFS = {})
# as keys and value of Key is membership value y
RBS = {}
RBS['close'] = close_RB_Dist.getMemberValue(RB_dist)
RBS['med'] = med_RB_Dist.getMemberValue(RB_dist)
RBS['far'] = far_RB_Dist.getMemberValue(RB_dist)
RFS = {}
RFS['close'] = close_RF_Dist.getMemberValue(RF_dist)
RFS['med'] = med_RF_Dist.getMemberValue(RF_dist)
RFS['far'] = far_RF_Dist.getMemberValue(RF_dist)
list_Values = [RFS, RBS]


#Determine all rule firing strength some will have firing strength zero other will have vlaue so nine
#element of the list startting with rule 1 and emd at 9. so value at rulebase[0] is fire rule firing value
rulebase = [r1.getFir(list_Values), r2.getFir(list_Values), r3.getFir(list_Values), r4.getFir(list_Values),
            r5.getFir(list_Values), r6.getFir(list_Values), r7.getFir(list_Values), r8.getFir(list_Values),
            r9.getFir(list_Values)]

turn_out = [1, 1, 0.5, -0.5, 0, 0.5, -1, -1, -0.5]

vel_out = [0.2, 0.2, 0.3, 0.3, 0.3, 0.3, 0.2, 0.3, 0.4]

firing_strengths = []
vel = []
turn = []
for i in range(len(rulebase)):
    if rulebase[i] > 0:  # firing strenght > 0 that means that rule is firing
        firing_strengths.append(rulebase[i])
        vel.append(vel_out[i])      #velocity against that rule from list vel_out
        turn.append(turn_out[i])    #turning against that rule from list turn_out

class rulebase:

    def __init__(self, rules):
        self.rules = rules

#defizification
    def Defuz(self, firing_strengths, turn, vel):

        speed = []
        for i in range(len(firing_strengths)):
            a = firing_strengths[i] * vel[i]
            speed.append(a)
        speed = sum(speed) / sum(firing_strengths)

        turning = []
        for i in range(len(firing_strengths)):
            b = firing_strengths[i] * turn[i]
            turning.append(b)
        turning = sum(turning) / sum(firing_strengths)

        return (speed, turning)









r_b = rulebase([])

velocity, turning = r_b.Defuz(firing_strengths, turn, vel)



# print('velocity', velocity, '\nturning', turning)

print('\nvelocity {}\nturning {}'.format(velocity, turning))


