import random
import colorsys





#Changed 4/5/2026 -------------------------------------------
#class SandParticle:
#    def __init__(self):
#        self.color = random_color(
#            hue_range=(0.1, 0.12),
#            saturation_range=(0.5, 0.7),
#            value_range=(0.7, 0.9),
#        )
#
#    def update(self, grid, row, column):
#        if grid.is_cell_empty(row + 1, column):
#            return row + 1, column
#
#        else:
#            offsets = [-1, 1]
#            random.shuffle(offsets)
#            for offset in offsets:
#                new_column = column + offset
#                if grid.is_cell_empty(row + 1, new_column):
#                    return row + 1, new_column
#
#            return row, column
# ------------------------------------------------------------------------
# Added 4/5/2026 ---------------------------------------------------------
class SandParticle:
    def __init__(self):
        self.color = random_color(
            hue_range=(0.1, 0.12),
            saturation_range=(0.5, 0.7),
            value_range=(0.7, 0.9),
        )
        self.cooldown = 0

    def update(self, grid, row, column):
        if self.cooldown > 0:
            self.cooldown -= 1
            return row, column
        self.cooldown = 1  # sand moves fast

        if grid.is_cell_empty(row + 1, column):
            return row + 1, column

        offsets = [-1, 1]
        random.shuffle(offsets)
        for offset in offsets:
            if grid.is_cell_empty(row + 1, column + offset):
                return row + 1, column + offset

        return row, column
#-------------------------------------------------------------------------

class RockParticle:
    def __init__(self):
        self.color = random_color(
            hue_range=(0.0, 0.1),
            saturation_range=(0.1, 0.3),
            value_range=(0.3, 0.5),
        )

    def update(self, grid, row, column):
        # rock doesn't move
        return row, column


def random_color(hue_range: object, saturation_range: object, value_range: object) -> tuple[int, int, int]:
    hue = random.uniform(*hue_range)
    saturation = random.uniform(*saturation_range)
    value = random.uniform(*value_range)
    r, g, b = colorsys.hsv_to_rgb(hue, saturation, value)
    return int(r * 255), int(g * 255), int(b * 255)

# Added 4/5/2026 ------------------------------------------------------------
class WaterParticle:
    def __init__(self):
        self.color = random_color(
            hue_range=(0.55, 0.65),      # blue
            saturation_range=(0.5, 0.9),
            value_range=(0.7, 1.0),
        )
        self.cooldown = 4  # sand moves fast

    def update(self, grid, row, column):
        # 1. Down
        if grid.is_cell_empty(row + 1, column):
            return row + 1, column
        self.cooldown = 3  # adjust this number to change speed

        # 2. Down-left / Down-right
        offsets = [-1, 1]
        random.shuffle(offsets)
        for offset in offsets:
            if grid.is_cell_empty(row + 1, column + offset):
                return row + 1, column + offset

        # 3. Sideways flow
        for offset in offsets:
            if grid.is_cell_empty(row, column + offset):
                return row, column + offset

        return row, column


class LavaParticle:
    def __init__(self):
        self.color = random_color(
            hue_range=(0.0, 0.05),
            saturation_range=(0.7, 1.0),
            value_range=(0.7, 1.0),
        )
        self.cooldown = 0  # slows lava movement

    def update(self, grid, row, column):
        # Slow lava movement
        if self.cooldown > 0:
            self.cooldown -= 1
            return row, column
        self.cooldown = 2  # adjust to change speed

        # 1. Lava + water = rock
        neighbors = [(1, 0), (1, -1), (1, 1), (0, -1), (0, 1)]
        for dr, dc in neighbors:
            nr, nc = row + dr, column + dc
            neighbor = grid.get_cell(nr, nc)
            if isinstance(neighbor, WaterParticle):
                grid.set_cell(row, column, RockParticle())
                grid.set_cell(nr, nc, RockParticle())
                return row, column

        # 2. Downward flow (only into non-lava, non-rock)
        below = grid.get_cell(row + 1, column)
        if not isinstance(below, (RockParticle, LavaParticle)):
            return row + 1, column

        # 3. Diagonal flow (same rule)
        offsets = [-1, 1]
        random.shuffle(offsets)
        for offset in offsets:
            diag = grid.get_cell(row + 1, column + offset)
            if not isinstance(diag, (RockParticle, LavaParticle)):
                return row + 1, column + offset

        # 4. Sideways flow ONLY if diagonal below that direction is open
        for offset in offsets:
            side = grid.get_cell(row, column + offset)
            diag_below = grid.get_cell(row + 1, column + offset)

            if (
                not isinstance(side, (RockParticle, LavaParticle))
                and not isinstance(diag_below, (RockParticle, LavaParticle))
            ):
                return row, column + offset

        # 5. Otherwise lava stays put → builds up
        return row, column
# --------------------------------------------------------------------------