import json

from automata.tm.dtm import DTM


def expand_transitions(config):
    expanded_transitions = {}

    for state, transition_list in config["transitions"].items():
        if len(transition_list) > 0:
            expanded_transitions[state] = {}

            for transition in transition_list:
                read_symbols = transition["read"]
                write_symbols = transition.get("write", read_symbols)
                move_direction = transition["move_to"]
                next_state = transition.get("next_state", state)

                if len(write_symbols) != len(read_symbols):
                    raise ValueError(
                        f"Error in state '{state}': 'write' must have the same number of symbols as 'read'"
                    )

                for read_symbol, write_symbol in zip(read_symbols, write_symbols):
                    expanded_transitions[state][read_symbol] = (
                        next_state,
                        write_symbol,
                        move_direction
                    )

    return expanded_transitions


def load_tm(json_path: str):
    with open(json_path, 'r') as file:
        config = json.load(file)

    states = set(config["all_states"])
    input_symbols = set(config["input_symbols"])
    tape_symbols = set(config["tape_symbols"])
    transitions = expand_transitions(config)
    initial_state = config["initial_state"]
    blank_symbol = config["blank_symbol"]
    final_states = set(config["final_states"])

    turing_machine = DTM(
        states=states,
        input_symbols=input_symbols,
        tape_symbols=tape_symbols,
        transitions=transitions,
        initial_state=initial_state,
        blank_symbol=blank_symbol,
        final_states=final_states
    )

    return turing_machine