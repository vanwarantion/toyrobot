# Settings:

ROBOT_DIRECTION_NAMES = [
    'NORTH',
    'SOUTH',
    'EAST',
    'WEST',
]
TABLE_DIMENSIONS = (5, 5)


import sys # For args and reading from stdin

class Robot():
    current_xy = [None, None]
    current_f = None
    _placed = False

    def face_txt(self):
        """
        :return: String name of current direction
        """
        return ROBOT_DIRECTION_NAMES[self.current_f]

    def report(self):
        """
        :return: String of current location and direction. Or NOT PLACED if robot has not yet placed successfully
        """

        if self._placed:
            print "OUTPUT: %d, %d, %s" % (self.current_xy[0], self.current_xy[1], self.face_txt())

    def valid_location(self, xy):
        """
        Returns True if provided location is valid.

        :param xy: X, Y coordinates
        :return: True if location is within the table dimensions
        """

        for _ in [0,1]:
            if xy[_] > TABLE_DIMENSIONS[_] - 1 or xy[_] < 0:
                return False

        return True

    def place(self, x, y, f):
        """
        Place the robot at given coordinates and cartesian direction.

        :param x: X value of the coordinates
        :param y: Y value of the coordinates
        :param f: Direction name (NORTH, SOUTH, EAST, WEST)
        """

        try:
            X, Y, F = int(x), int(y), ROBOT_DIRECTION_NAMES.index(f.upper())
        except:
            print "COULD NOT PLACE:", x, y, f
            return None

        if self.valid_location([X, Y]):

            # Set location and direction
            self.current_xy, self.current_f = [X, Y], F

            # Mark robot as placed
            self._placed = True

    def move(self):
        """
        Move the robot forward
        """

        if not self._placed:
            return None

        # Movement values per each direction
        cardinal_directions = [
            [0, 1],     # North
            [0, -1],    # South
            [1, 0],     # East
            [-1, 0],    # West
        ]

        # Select direction and set target position
        movement = cardinal_directions[self.current_f]
        target_pos = [self.current_xy[0], self.current_xy[1]]

        # Apply movement based on movement directions
        for _ in [0,1]:
            target_pos[_] += movement[_]

        # Set current_xy if target position is valid
        if self.valid_location(target_pos):
            self.current_xy = target_pos

    def rotate(self, amount):
        """
        Rotates the robot (amount * 90) degrees clockwise.


         Resulting directions for each initial direction are below;

         Initial D  | Left  | Right | Left Index | Right Index
         -----------|-------|-------|------------|-------------
         North      | West  | East  |          3 |           2
         South      | East  | West  |          2 |           3
         East       | North | South |          0 |           1
         West       | South | North |          1 |           0



        :param amount: Amount of 90 degree turns to be applied
        """

        # Abort if not placed
        if not self._placed:
            return None

        # Right turn indexes
        rotational_directions = [2,3,1,0]

        # Apply rotation
        for i in range(amount):
            self.current_f = rotational_directions[self.current_f]

    def set_cmd(self, cmd):
        """
        Process command. Print error message if necessary

        :param cmd: Text input
        """

        # Available Commands
        commands = {
            'place': {'action': self.place, 'req_args_len': 3},
            'move': {'action': self.move},
            'left': {'action': self.rotate, 'arg': 3},
            'right': {'action': self.rotate, 'arg': 1},
            'report': {'action': self.report},
        }

        # Check if command is valid
        my_cmd = cmd.split(" ", 1)
        command_key = my_cmd[0].lower()
        if command_key not in commands.keys():
            print "Invalid command:", command_key
            return None

        # Find required parameters
        action_params = commands[command_key]

        if 'req_args_len' in action_params.keys():
            # Multiple arguments are required

            if len(my_cmd) == 1:
                # No arguments given
                print "Arguments required:", command_key
                return None

            my_args = my_cmd[1].split(',')

            if len(my_args) < action_params['req_args_len']:
                print "Insufficient arguments:", command_key
                return None

            # Create list of args and call target function
            action_params['action'](*[_.strip() for _ in my_args])

        elif 'arg' in action_params.keys():
            # Argument is provided in action_params

            action_params['action'](action_params['arg'])

        else:
            # Command does not require any arguments
            action_params['action']()


if __name__ == '__main__':
    r = Robot()

    # Redneck testing
    if len(sys.argv) > 1:
        if sys.argv[1] == '--test':
            print "No input. Just running some commands"
            cmds = [
                'SELF DESTRUCT', 'LEFT', 'MOVE', 'REPORT', 'PLACE 0,0, NORTH', 'LEFT', 'MOVE', 'REPORT', 'PLACE 2,3, SOUTH',
                'MOVE', 'REPORT', 'RIGHT', 'MOVE', 'MOVE', 'REPORT', 'RIGHT', 'RIGHT', 'MOVE', 'MOVE', 'MOVE', 'MOVE',
                'REPORT',
            ]

            for _ in cmds:
                print "Running:", _
                r.set_cmd(_)
        sys.exit()


    # Check if we are working with a file or terminal
    if sys.stdin.isatty():
        print "Toy Robot Sim. Welcome!\n"

        # User commands
        while True:
            try:
                user_cmd = raw_input("Toy Robot> ")
                r.set_cmd(user_cmd)
            except KeyboardInterrupt:
                print "\nBye!"
                sys.exit()

    else:
        # Read lines & run commands
        for line in sys.stdin:
            cmd_to_run = line.strip()
            # Ignore empty lines
            if cmd_to_run == '':
                continue
            print "Command:", cmd_to_run
            r.set_cmd(cmd_to_run)