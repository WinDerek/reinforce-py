import numpy as np
import time
from backend.random_utils import choose_randomly


BORDER_LENGTH = 10
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


def state_transition(action, state_from, grid_data_list):
    """
    Args:
    - action: int. The index of the action. Must be legal! (Not checked here for better performance)
    - state_from: int. The index of the current state.
    """

    if grid_data_list[state_from]['goal']:
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


def sarsa_one_step(grid_data_list, current_state, current_action, epsilon, alpha):
    # State transition
    r = reward(current_action, current_state, grid_data_list)
    state_to = state_transition(current_action, current_state, grid_data_list)
    
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
