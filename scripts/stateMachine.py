#!/usr/bin/env python

import rospy
import smach
import sys

# define state Foo
class Human(smach.State):
    def __init__(self):
        smach.State.__init__(self,
                            outcomes=['robot_turn', 'exit_success'],
                            input_keys=['human_letter'],
                            output_keys=['human_letter'])

    def execute(self, userdata):
        rospy.loginfo('Executing state HUMAN')
        turn = raw_input("Welcome to ISpy! type either (H)uman or (R)obot to continue: ")

        if turn == "h" or turn == "H":
            print("you chose Human")
            userdata.human_letter = raw_input("type the first letter of the object: ")
            print("you selected: " + userdata.human_letter)
            return 'robot_turn'

        elif turn == "r" or turn == "R": 
            print("you chose Robot")

        # loop until correct usage instead of crashing the program
        else:
            sys.exit("usage: H/h || R/r")

        return 'exit_success'


# define state Bar
class Robot(smach.State):
    def __init__(self):
        smach.State.__init__(self,
                            outcomes=['human_turn'],
                            input_keys=['human_letter_to_robot'])

    def execute(self, userdata):
        print("Robot searching for an object that starts with <<" + userdata.human_letter_to_robot + ">>...")
        #rospy.loginfo('Executing state ROBOT')
        return 'human_turn'
        



# main
def main():
    rospy.init_node('ISpy_state_machine')

    # Create a SMACH state machine
    sm = smach.StateMachine(outcomes=['failed', 'successfull'])
    sm.userdata.sm_letter = ""
    sm.userdata.guess = ""

    # Open the container
    with sm:
        # Add states to the container
        smach.StateMachine.add('HUMAN', Human(), 
                               transitions={'robot_turn' : 'ROBOT' ,
                                            'exit_success' : 'successfull'},
                               remapping={'human_letter' : 'sm_letter'})

        smach.StateMachine.add('ROBOT', Robot(), 
                               transitions={'human_turn' : 'successfull'},
                               remapping={"human_letter_to_robot" : "sm_letter"})

    # Execute SMACH plan
    outcome = sm.execute()


if __name__ == '__main__':
    main()
