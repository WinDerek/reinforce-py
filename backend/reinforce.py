import numpy as np


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
    print(reward(0, 65, grid_data_list))
    for state_index, grid_data in enumerate(grid_data_list):
        grid_data_list[state_index]['stateValue'] = np.sum([grid_data['policy'][action] * (reward(action, state_index, grid_data_list) + GAMMA * grid_data_list[state_transition(action, state_index, grid_data_list)]['stateValue']) for action in actions_given_state(state_index)])
    return [grid_data['stateValue'] for grid_data in grid_data_list]
