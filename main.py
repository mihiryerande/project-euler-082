# Problem 82:
#     Path Sum: Three Ways
#
# Description:
#     NOTE: This problem is a more challenging version of Problem 81.
#
#     The minimal path sum in the 5 by 5 matrix below,
#       by starting in any cell in the left column and finishing in any cell in the right column,
#       and only moving up, down, and right, is indicated in red and bold;
#       the sum is equal to 994.
#
#         |  131   673  [234] [103] [ 18] |
#         | [201] [ 96] [342]  965   150  |
#         |  630   803   746   422   111  |
#         |  537   699   497   121   956  |
#         |  805   732   524    37   331  |
#
#     Find the minimal path sum from the left column to the right column in matrix.txt
#      (right click and "Save Link/Target As..."), a 31K text file containing an 80 by 80 matrix.

from numpy import inf


def main(filename):
    """
    Returns the minimal path sum in the given `filename`
      starting from any cell in the left-most column and
      finishing in the right-most column,
      only taking steps up, right, or down.
    Also returns the path taken,
      specified by the starting y-coordinate in the left-most column,
      and a list of subsequent step directions from {'R', 'U', 'D'}.

    Args:
        filename (str): File name containing integer matrix

    Returns:
        (Tuple[int, int, List[str]]):
            Tuple of ...
              * Minimal path sum walking from left column to right column in matrix
              * Starting y-coordinate of minimal path
              * Minimal path represented as a list of steps from {'R', 'U', 'D'}

    Raises:
        AssertError: if incorrect args are given
    """
    assert type(filename) == str

    # Idea:
    #     Use dynamic programming to only keep track of minimal subpaths
    #       landing within the matrix and use then use those to further compute longer subpaths.
    #     Calculate subpaths landing at each subsequent column in two alternating steps:
    #         1) Subpaths landing in column by taking a step right
    #         2) Subpaths landing in column by stepping up or down

    with open(filename, 'r') as f:
        m = list(map(lambda line: list(map(int, line.split(','))), f.readlines()))

    # Assume given matrix is square
    n = len(m)

    # Grid to keep track of minimal sub-path sum ending at that coordinate in matrix
    trellis_sum = [[inf for _ in range(n)] for _ in range(n)]
    for i in range(n):
        trellis_sum[i][0] = m[i][0]

    # Grid to keep track of what was the previous point in minimal sub-path ending at current point
    trellis_dir = [['' for _ in range(n)] for _ in range(n)]

    # Fill in trellises by iterating through columns
    for px in range(1, n):
        # # Fill in values for subpaths stepping right into this column
        # for y in range(n):
        #     trellis_sum[y][x] = trellis_sum[y][x-1] + m[y][x]
        #     trellis_dir[y][x] = 'L'

        # Compare with subpaths stepping up/down within same column,
        #   by checking adjacent cells until no more change occurs
        update = True
        i = 1
        while update:
            update = False

            # Update top-most cell of column
            py = 0
            curr_elt = m[py][px]
            choices = [(py, px-1, 'L'), (py+1, px, 'D')]
            min_choice = min(choices, key=lambda c: trellis_sum[c[0]][c[1]])
            qy, qx = min_choice[:2]
            new_sum = curr_elt + trellis_sum[qy][qx]
            if new_sum < trellis_sum[py][px]:
                update = True
                trellis_dir[py][px] = min_choice[2]
                trellis_sum[py][px] = new_sum
            else:
                pass

            # Update top-most cell of column
            py = n-1
            curr_elt = m[py][px]
            choices = [(py, px-1, 'L'), (py-1, px, 'U')]
            min_choice = min(choices, key=lambda c: trellis_sum[c[0]][c[1]])
            qy, qx = min_choice[:2]
            new_sum = curr_elt + trellis_sum[qy][qx]
            if new_sum < trellis_sum[py][px]:
                update = True
                trellis_dir[py][px] = min_choice[2]
                trellis_sum[py][px] = new_sum
            else:
                pass

            # Update column-internal cells
            for py in range(1, n-1):
                curr_elt = m[py][px]
                choices = [(py, px-1, 'L'), (py-1, px, 'U'), (py+1, px, 'D')]
                min_choice = min(choices, key=lambda c: trellis_sum[c[0]][c[1]])
                qy, qx = min_choice[:2]
                new_sum = curr_elt + trellis_sum[qy][qx]
                if new_sum < trellis_sum[py][px]:
                    update = True
                    trellis_dir[py][px] = min_choice[2]
                    trellis_sum[py][px] = new_sum
                else:
                    pass
            i += 1

    # Walk backwards through trellises, right-most column to left-most, enumerating minimal path
    px = n-1
    py = min(range(n), key=lambda y: trellis_sum[y][px])
    path_sum = trellis_sum[py][px]
    fwd_path = []
    while px > 0:
        if trellis_dir[py][px] == 'L':
            fwd_dir = 'R'
            px -= 1
        elif trellis_dir[py][px] == 'U':
            fwd_dir = 'D'
            py -= 1
        else:
            fwd_dir = 'U'
            py += 1
        fwd_path.append(fwd_dir)
    fwd_path.reverse()
    return path_sum, py, fwd_path


if __name__ == '__main__':
    matrix_filename = 'matrix.txt'
    minimal_path_sum, minimal_starting_y, minimal_path = main(matrix_filename)
    print('Minimal path sum in "{}":'.format(matrix_filename))
    print('  {}'.format(minimal_path_sum))
    print('Path producing that sum:')
    print('  Start at ({}, 0) -> {}'.format(minimal_starting_y, ' -> '.join(minimal_path)))
