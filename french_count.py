import sys
from fst import FST
from fsmutils import composewords

kFRENCH_TRANS = {0: "zero", 1: "un", 2: "deux", 3: "trois", 4:
    "quatre", 5: "cinq", 6: "six", 7: "sept", 8: "huit",
                 9: "neuf", 10: "dix", 11: "onze", 12: "douze", 13:
                     "treize", 14: "quatorze", 15: "quinze", 16: "seize",
                 20: "vingt", 30: "trente", 40: "quarante", 50:
                     "cinquante", 60: "soixante", 100: "cent"}

kFRENCH_AND = 'et'

def prepare_input(integer):
    assert isinstance(integer, int) and integer < 1001 and integer >= 0, \
        "Integer out of bounds"
    return list("%03i" % integer)

def french_count():
    f = FST('french')

    f.add_state('start')
    f.add_state('final')
    f.initial_state = 'start'

    f.set_final('final')



    # for iii in xrange(0,10):
    #     for ii in xrange(0,10):
    #         for i in xrange(0,10):
    #             num = iii * 100 + ii * 10 + i
    #             f.add_state(str(num))

    f.add_state('hun')
    f.add_state('hun0')
    f.add_arc('start', 'hun0', ('0'), ())
    f.add_state('ten0')
    f.add_arc('hun0', 'ten0', ('0'),())
    f.add_state('digit0')
    f.add_arc('ten0','digit0', ('0'), kFRENCH_TRANS[0])
    f.add_arc('digit0', 'final', (), ())
    f.add_arc('start', 'hun', ('0'), ())
    for iii in xrange(1,10):
        hun = ''

        if iii == 1:
            hun = kFRENCH_TRANS[100]
        elif iii > 1:
            hun = kFRENCH_TRANS[iii] + ' ' + kFRENCH_TRANS[100]
        f.add_arc('start', 'hun', (str(iii)), [hun])

    f.add_state('ten')
    f.add_state('ten1')
    f.add_arc('hun','ten1',(str(1)),())

    f.add_arc('hun','ten',(str(0)),())
    for i in xrange(0,7):
        f.add_arc('ten1','final',(str(i)),[kFRENCH_TRANS[10+i]])
    for i in xrange(7,10):
        f.add_arc('ten1','final',(str(i)),[kFRENCH_TRANS[10]+' '+kFRENCH_TRANS[i]])


    f.add_state('tenand')
    f.add_state('ten9')
    for ii in xrange(2,10):
        ten = ''
        if ii <= 6:
            ten = kFRENCH_TRANS[ii * 10]
            f.add_arc('hun','tenand',(str(ii)),[ten])
        elif ii < 8:
            ten = kFRENCH_TRANS[60]
            f.add_arc('hun','tenand',(str(ii)),[ten])
        elif ii == 8:
            ten = kFRENCH_TRANS[4] +' '+ kFRENCH_TRANS[20]
            f.add_arc('hun','ten',(str(ii)),[ten])
        else:
            ten = kFRENCH_TRANS[4] +' '+ kFRENCH_TRANS[20]
            f.add_arc('hun','ten9',(str(ii)),[ten])

    f.add_state('digit')
    f.add_arc('ten','digit',('0'),())

    for i in xrange(1,10):
        digit = kFRENCH_TRANS[i]
        f.add_arc('ten','digit',(str(i)),[digit])
    for i in xrange(1,7):
        f.add_arc('ten9','digit',(str(i)),[kFRENCH_TRANS[i+10]])
    for i in xrange(7,10):
        f.add_arc('ten9','digit',(str(i)),[kFRENCH_TRANS[10]+' '+kFRENCH_TRANS[i]])

    for i in xrange(1,10):
        digit = kFRENCH_TRANS[i]
        if i == 1:
            f.add_arc('tenand','digit',(str(i)),[kFRENCH_AND+' '+digit])
        else:
            f.add_arc('tenand','digit',(str(i)),[digit])

    f.add_arc('digit','final',(),())

    return f


if __name__ == '__main__':
    string_input = raw_input()
    user_input = int(string_input)
    f = french_count()

    if string_input:
        print user_input, '-->',
        print " ".join(f.transduce(prepare_input(user_input)))


