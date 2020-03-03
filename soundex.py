from fst import FST
import string, sys
from fsmutils import composechars, trace

def letters_to_numbers():
    """
    Returns an FST that converts letters to numbers as specified by
    the soundex algorithm
    """

    noninitial = "aehiouwy"
    dics = "bfpvcgjkqsxzdtlmnr"
    diclist = ["bfpv","cgjkqsxz","dt","l","mn","r"]

    # dic = {'b':1,'f':1,'p':1,'v':1,'c':2,'g':2,'j':2,'k':2,'q':2,'s':2,'x':2,'z':2,'d':3,'t':3,'l':4,'m':5,'n':5,'r':6}

    # Let's define our first FST
    f1 = FST('soundex-generate')

    # Indicate that '1' is the initial state
    f1.add_state('start')
    f1.add_state('s1')
    f1.add_state('s2')
    for i in range(len(diclist)):
        f1.add_state(str(i))

    for i in range(len(diclist)):
        for j in range(len(diclist)):
            if i != j:
                for k in diclist[j]:
                    f1.add_arc(str(i),str(j),k,str(j+1))
            else:
                for k in diclist[j]:
                    f1.add_arc(str(i),str(j),k,())

    for i in range(len(diclist)):
        for j in noninitial:
            f1.add_arc(str(i),str(i),j,())

    # f1.add_state('next')
    f1.initial_state = 'start'
    # for letter in string.ascii_letters:
    #     f1.add_arc('start','next',(letter),(letter))
    # Set all the final states
    # f1.set_final('next')
    f1.set_final("s1")
    for i in range(len(diclist)):
        f1.set_final(str(i))

    # Add the rest of the arcs
    for letter in string.ascii_letters:
        f1.add_arc('start', 's1', (letter), (letter))
        # f1.add_arc('next', '1', (letter), ('0'))
    # for letter in noninitial:
    #     f1.add_arc('6','7', (letter),())
    for i in range(len(diclist)):
        for j in diclist[i]:
            f1.add_arc('s1', str(i), j, str(i+1))
    for j in noninitial:
        f1.add_arc('s1','s1',j,())



    return f1


    # The stub code above converts all letters except the first into '0'.
    # How can you change it to do the right conversion?


def truncate_to_three_digits():
    """
    Create an FST that will truncate a soundex string to three digits
    """

    # Ok so now let's do the second FST, the one that will truncate
    # the number of digits to 3
    f2 = FST('soundex-truncate')

    # Indicate initial and final states
    # f2.add_state('1')
    f2.add_state('2')
    f2.add_state('3')
    f2.add_state('4')
    f2.add_state('5')
    f2.initial_state = '2'
    f2.set_final('2')
    f2.set_final('5')
    f2.set_final('4')
    f2.set_final('3')

    # Add the arcs
    for letter in string.letters:
        f2.add_arc('2', '2', (letter), (letter))


    for n in range(10):
        f2.add_arc('2', '3', (str(n)), (str(n)))
        f2.add_arc('3', '4', (str(n)), (str(n)))
        f2.add_arc('4','5',(str(n)), (str(n)))
        f2.add_arc('5','5',(str(n)), ())

    return f2

    # The above stub code doesn't do any truncating at all -- it passes letter and number input through
    # what changes would make it truncate digits to 3?


def add_zero_padding():
    # Now, the third fst - the zero-padding fst
    f3 = FST('soundex-padzero')

    f3.add_state('1')
    f3.add_state('2')
    f3.add_state('3')
    f3.add_state('4')
    f3.add_state('5')
    f3.add_state('10')
    f3.add_state('20')
    f3.add_state('30')


    f3.initial_state = '1'
    f3.set_final('5')
    f3.set_final('30')

    for letter in string.letters:
        f3.add_arc('1', '2', (letter), (letter))
    for number in xrange(10):
        f3.add_arc('2', '3', (str(number)), (str(number)))
        f3.add_arc('3', '4', (str(number)), (str(number)))
        f3.add_arc('4', '5', (str(number)), (str(number)))

    f3.add_arc('2', '10', (), ('0'))
    f3.add_arc('10', '20', (), ('0'))
    f3.add_arc('20', '30', (), ('0'))
    f3.add_arc('3', '20', (), ('0'))
    f3.add_arc('4', '30', (), ('0'))



    return f3

    # The above code adds zeroes but doesn't have any padding logic. Add some!


if __name__ == '__main__':
    user_input = raw_input().strip()
    f1 = letters_to_numbers()
    f2 = truncate_to_three_digits()
    f3 = add_zero_padding()
    # print (f1.transduce("s d s e f s d".split()))
    if user_input:
        # print("%s -> %s" % (user_input, composechars(tuple(user_input), f1, f2, f3)))

        print("%s -> %s" % (user_input, composechars(tuple(user_input), f1,f2,f3)))
