class Block():

    def __init__(self, block_type, position):
        '''
        This function initializes the block.

        **Paramters**
           block_type: str

        **Returns**
            none
        '''
        self.block_type = block_type
        self.position = position

    def lazor_contacts(self):
        '''
        This function determines the possible cooridnates the
        lazor could intersect.

        **Paramters**
           x: x position of block
           y: y position of block

        **Returns**
            lazor_hits: array containing possible positions the lazor
                can hit around a block.
        '''
        x = self.position[0]
        y = self.position[1]
        lazor_hits = [[(x - 1) * 2, 1 + ((y - 1) * 2)], [1 + ((x - 1) * 2), (y - 1) * 2],
                      [2 + ((x - 1) * 2), 1 + ((y - 1) * 2)], [1 + ((x - 1) * 2), 2 + ((y - 1) * 2)]]

        return lazor_hits

    def lazor_updates(self, block):
        '''
        This function provides grid positions of lazor contact points.

        **Paramters**
           x: x position of block
           y: y position of block

        **Returns**
           block: Matrix containing lazor contact positions
        '''
        x = self.position[0]
        y = self.position[1]
        block[((y - 1) * 2)][1 + ((x - 1) * 2)] = 1  # above
        block[2 + ((y - 1) * 2)][1 + ((x - 1) * 2)] = 2  # below
        block[1 + ((y - 1) * 2)][((x - 1) * 2)] = 3  # left
        block[1 + ((y - 1) * 2)][2 + ((x - 1) * 2)] = 4  # right

    def lazor_results(self, horizontal_dir, vertical_dir, contact_point):
        '''
        This function determines the new direction for the lazor
        based on what side of a block it hits or where the block is located.
        It also determines whether the lazor line will be deleted from it's
        old direction.

        **Paramters**
           horizontal_dir: horizontal or x direction of lazor
           vertical_dir: vertical or y direction of the lazor
           contact_point: where the lazor hits the block

        **Returns**
            new_h_dir: new horizontal or x direction of lazor
            new_v_dir: new vertical or y direction of the lazor
            rm_lazor: True or False statement
        '''
        if contact_point == 1 or contact_point == 2:
            new_v_dir = vertical_dir * -1  # make it go in the opposite direction
            new_h_dir = horizontal_dir
        elif contact_point == 3 or contact_point == 4:
            new_h_dir = horizontal_dir * -1  # make it go in the opposite direction
            new_v_dir = vertical_dir

        if block_type == "opaque":
            rm_lazor = True
        elif block_type == "reflect":
            rm_lazor = True
        elif block_type == "refract":
            rm_lazor = False

        return new_h_dir, new_v_dir, rm_lazor
