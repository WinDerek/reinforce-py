import numpy as np
import time
from backend.random_utils import true_with_probability, choose_randomly
from random import randrange
from backend.mlp import TwoLayerNet


BORDER_LENGTH = 10
N_STATES = BORDER_LENGTH * BORDER_LENGTH
STARTING_STATE = 0
GAMMA = 0.9


def actions_given_state(state):
    """
    Returns: a list of int. The elements of the list represent the indices of all the legal actions given the state.
    
    Args:
    - state: int. The index of the state.
    """

    row = state // BORDER_LENGTH
    column = state % BORDER_LENGTH
    
    action_list = []
    if row != 0:
        action_list.append(0)
    if column != BORDER_LENGTH - 1:
        action_list.append(1)
    if row != BORDER_LENGTH - 1:
        action_list.append(2)
    if column != 0:
        action_list.append(3)

    return action_list


def state_transition(action, state_from, grid_data_list, deviation_probability=0.0):
    """
    Args:
    - action: int. The index of the action. Must be legal! (Not checked here for better performance)
    - state_from: int. The index of the current state.
    """

    if grid_data_list[state_from]['goal']:
        if true_with_probability(deviation_probability):
            non_wall_grid_index_list = []
            for grid_data in grid_data_list:
                if not grid_data['wall'] and not grid_data['goal']:
                    non_terminal_states_index_list.append(grid_data['gridIndex'])
            return non_terminal_states_index_list[randrange(len(non_terminal_states_index_list))]
        else:
            return STARTING_STATE

    row = state_from // BORDER_LENGTH
    column = state_from % BORDER_LENGTH

    # Up
    if action == 0:
        row -= 1
    # End
    elif action == 1:
        column += 1
    # Down
    elif action == 2:
        row += 1
    # Start
    elif action == 3:
        column -= 1
    else:
        raise ValueError("Illegal action: {:d}".format(action))

    # Check if the state_to is a wall
    state_to = row * BORDER_LENGTH + column
    if grid_data_list[state_to]['wall']:
        return state_from
    else:
        return state_to


def reward(action, state_from, grid_data_list):
    return grid_data_list[state_from]['reward']


def evaluate_policy_by_one_sweep(grid_data_list):
    # time.sleep(1.0)
    for state_index, grid_data in enumerate(grid_data_list):
        grid_data_list[state_index]['stateValue'] = np.sum([grid_data['policy'][action] * (reward(action, state_index, grid_data_list) + GAMMA * grid_data_list[state_transition(action, state_index, grid_data_list)]['stateValue']) for action in actions_given_state(state_index)])
    return [grid_data['stateValue'] for grid_data in grid_data_list]


def improve_policy(grid_data_list):
    for state_index, grid_data in enumerate(grid_data_list):
        q_list = []
        actions = actions_given_state(state_index)
        for action in actions:
            state_to = state_transition(action, state_index, grid_data_list)
            q_list.append(reward(action, state_index, grid_data_list) + GAMMA * grid_data_list[state_to]['stateValue'])
        
        optimal_q = max(q_list)

        for index, action in enumerate(actions):
            grid_data_list[state_index]['policy'][action] =  1.0 if (q_list[index] == optimal_q) else 0.0
        
        sum_value = sum(grid_data_list[state_index]['policy'])
        for index, policy in enumerate(grid_data_list[state_index]['policy']):
            grid_data_list[state_index]['policy'][index] /= sum_value

    return [grid_data['policy'] for grid_data in grid_data_list]


def sarsa_one_step(grid_data_list, current_state, current_action, epsilon, alpha, deviation_probability=0.0):
    # State transition
    r = reward(current_action, current_state, grid_data_list)
    state_to = state_transition(current_action, current_state, grid_data_list, deviation_probability=deviation_probability)
    
    # Update the policy
    q_list = []
    actions = actions_given_state(state_to)
    for action in actions:
        q_list.append(grid_data_list[state_to]['q'][action])
    optimal_q = max(q_list)
    count = 0
    for action in actions:
        if grid_data_list[state_to]['q'][action] == optimal_q:
            count += 1
    for action in actions:
        if grid_data_list[state_to]['q'][action] == optimal_q:
            grid_data_list[state_to]['policy'][action] = epsilon / len(actions) + (1 - epsilon) / count
        else:
            grid_data_list[state_to]['policy'][action] = epsilon / len(actions)
            print(grid_data_list[state_to]['policy'][action])

    action_to = choose_randomly({ action: grid_data_list[state_to]['policy'][action] for action in actions})
    old_q = grid_data_list[current_state]['q'][current_action]
    new_q = old_q + alpha * (r + GAMMA * grid_data_list[state_to]['q'][action_to] - old_q)

    # Calculate the two new state values
    stateValueFrom = sum([grid_data_list[current_state]['policy'][action] * grid_data_list[current_state]['q'][action] for action in actions_given_state(current_state)])
    stateValueTo = sum([grid_data_list[state_to]['policy'][action] * grid_data_list[state_to]['q'][action] for action in actions_given_state(state_to)])

    return {\
        'newQ': new_q,\
        'newPolicy': grid_data_list[state_to]['policy'],\
        'stateValueFrom': stateValueFrom,\
        'stateValueTo': stateValueTo,\
        'stateTo': state_to,\
        'actionTo': action_to\
    }


def q_learning_one_step(grid_data_list, current_state, epsilon, alpha, deviation_probability=0.0):
    # Update the policy
    q_list = []
    actions = actions_given_state(current_state)
    for action in actions:
        q_list.append(grid_data_list[current_state]['q'][action])
    optimal_q = max(q_list)
    count = 0
    for action in actions:
        if grid_data_list[current_state]['q'][action] == optimal_q:
            count += 1
    for action in actions:
        if grid_data_list[current_state]['q'][action] == optimal_q:
            grid_data_list[current_state]['policy'][action] = epsilon / len(actions) + (1 - epsilon) / count
        else:
            grid_data_list[current_state]['policy'][action] = epsilon / len(actions)
            print(grid_data_list[current_state]['policy'][action])

    action = choose_randomly({ action: grid_data_list[current_state]['policy'][action] for action in actions})
    state_to = state_transition(action, current_state, grid_data_list, deviation_probability=deviation_probability)
    r = reward(action, current_state, grid_data_list)
    old_q = grid_data_list[current_state]['q'][action]
    new_q = old_q + alpha * (r + GAMMA * max([grid_data_list[state_to]['q'][a] for a in actions_given_state(state_to)]) - old_q)

    # Calculate the two new state values
    newStateValue = sum([grid_data_list[current_state]['policy'][action] * grid_data_list[current_state]['q'][action] for action in actions_given_state(current_state)])

    return {\
        'newQ': new_q,\
        'newPolicy': grid_data_list[current_state]['policy'],\
        'newStateValue': newStateValue,\
        'action': action,\
        'stateTo': state_to
    }


def learn_from_transitions(weights, hidden_size, transitions, clamp, gamma):
    if weights is not None:
        w1 = np.array(weights['w1'])
        b1 = np.array(weights['b1'])
        w2 = np.array(weights['w2'])
        b2 = np.array(weights['b2'])
        net = TwoLayerNet(8, hidden_size, 5, w1=w1, b1=b1, w2=w2, b2=b2)
    else:
        net = TwoLayerNet(8, hidden_size, 5)

    # print("transitions count: {:d}".format(len(transitions)))
    # print(transitions)
    latest_td_error = None
    for transition in transitions:
        s0 = np.array([transition[0]])
        a0 = int(transition[1])
        r1 = transition[2]
        s1 = np.array([transition[3]])

        # print("Before training:")
        # print(net.forward(s1, requires_grad=False)[0])
        oracle = r1 + gamma * max(net.forward(s1, requires_grad=False)[0])

        td_error = net.forward(s0, requires_grad=True, oracle=oracle, a0=a0, clamp=clamp)

        if latest_td_error is None:
            latest_td_error = td_error

        updated_weights = net.backward()
    
    # print("After training:")
    # print(net.forward(s1, requires_grad=False)[0])

    a1 = int(np.argmax(net.forward(s1, requires_grad=False)[0]))
    print(a1)

    return { 'weights': updated_weights, 'a1': a1, 'latestTdError': latest_td_error }
