from enum import Enum


class TableActionEnum(Enum):
    add_back_to_chain = '-A'  # add to the end of the chain
    set_default_chain_policy = '-P'  # setting default chain policy
    delete_from_chain = '-D'  # deleting from the chain