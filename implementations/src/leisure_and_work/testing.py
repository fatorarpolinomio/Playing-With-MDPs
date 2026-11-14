import environment


def one_work_test():
    w0 = [0, 0, 0, 0, 0]
    w1 = [0, 4, 0.37, 0.16, 0.4]

    works = [w0, w1]
    actions = [w0, w1]

    s0 = [w0, [w0]]
    s1 = [w0, [w0, w1]]
    s2 = [w1, [w0]]
    s3 = [w1, [w0, w1]]

    states = [s0, s1, s2, s3]

    return actions, states, works

def log_test(actions: list, states: list, works : list):
    for action in actions:
        print("-----------")
        for start_state in states:
            line = []
            for target_state in states:
                result = environment.transfunc_LW2(target_state, start_state, works, action)
                line.append(result)
                #print(start_state, "->", target_state, " : ", result)
            print(line)


actions, states, works = one_work_test()
log_test(actions, states, works)
