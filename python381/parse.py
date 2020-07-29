#!/usr/bin/env python
#coding:utf-8

grapcode = '''#coding:utf-8
from graphviz import Digraph

'''


def main():
    global grapcode

    with open('./grammar.txt') as fp:
        lines = fp.readlines()
    n = len(lines)
    i = 0
    while i < n:
        li = lines[i]
        li = li.strip()
        if li.startswith('Dump of DFA for'):
            dfaname = li.strip().split(' ')[-1]
            print('dfa = %s' % dfaname)

            grapcode += "%s = Digraph('%s', filename='%s.gv')\n" % (dfaname, dfaname, dfaname)
            grapcode += "%s.attr(rankdir='LR', size='8,5')\n" % dfaname
            j = i + 1
            current_state = 0
            while j < n:
                nli = lines[j].strip()
                if '->' not in nli and 'State' not in nli:
                    break
                if 'State' in nli:
                    current_state = int(nli.split(' ')[1])
                    is_final = True if 'final' in nli else False
                    if is_final:
                        grapcode += "%s.node('%s',  shape='doublecircle')\n" % (dfaname, current_state)
                    else:
                        grapcode += "%s.node('%s',  shape='circle')\n" % (dfaname, current_state)
                else:
                    labels = nli.rsplit('->',1)
                    print(nli, labels)
                    if len(labels) == 1:
                        tran_label = ''
                        tran_state = int(labels[0])
                    else:
                        tran_label = labels[0].strip().replace("'",'')
                        tran_state = int(labels[1])
                    grapcode += "%s.edge('%s', '%s', label='%s')\n" % (dfaname, current_state, tran_state, tran_label)
                j += 1
            i = j
            grapcode += '%s.render("%s", directory="png", cleanup=True, format="png")\n' % (dfaname, dfaname)
        else:
            i += 1



    with open('grapcode.py', 'w') as fp:
        fp.write(grapcode)




if __name__ == "__main__":
    main()
