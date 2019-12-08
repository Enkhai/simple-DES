import permutationMappings
import textwrap


def permutation(data, type):
    mapping = None
    if type == "initial":
        mapping = permutationMappings.initial_perm_map
    elif type == "compression":
        mapping = permutationMappings.compression_perm_map
    elif type == "expansion":
        mapping = permutationMappings.expansion_perm_map
    elif type == "pBox":
        mapping = permutationMappings.pBox_perm_map
    elif type == "inverse":
        mapping = permutationMappings.inverseInitial_perm_map

    try:
        return ''.join([data[i - 1] for i in mapping])
    except:
        print("Wrong permutation type!")


def sBox_permutation(data):
    blocks = textwrap.wrap(data, 6)
    for block_num, block in enumerate(blocks):
        mapping = permutationMappings.sBox_perm_map[block_num]
        i = int(block[0] + block[5], 2)
        j = int(''.join([block[x] for x in range(1, 5)]), 2)
        block = ("{0:b}".format(mapping[i][j])).zfill(4)
        blocks[block_num] = block

    return ''.join(blocks)
