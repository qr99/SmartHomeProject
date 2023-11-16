import py_trees
import random
import time


class EspressoBehaviour(py_trees.behaviour.Behaviour):
    def __init__(self, name, key, values=None, val_range=None):
        super(EspressoBehaviour, self).__init__(name)
        self.key = key
        self.values = values
        self.range = val_range
        self.min_val = None
        self.max_val = None
        self.confirmed = False

        self.blackboard = self.attach_blackboard_client()
        self.blackboard.register_key(key=key, access=py_trees.common.Access.WRITE)
        self.blackboard.set(key, 'Test')

    def setup(self):
        self.logger.debug("%s [setup()]" % self.name)
        self.confirmed = None
        if self.values == None:
            if self.range != None and type(self.range) is tuple:
                self.min_val = self.range[0]
                self.max_val = self.range[1]
            else:
                self.logger.debug(
                    "%s: error during setup: key values are not a list, but range of int values is not given.")
        elif self.range != None:
            self.logger.debug("%s: error during setup: for key a list and a range of int values is given.")

        self.logger.debug("%s: [setup()] complete." % self.name)

    def initialise(self):
        self.logger.debug("%s [initialise()]" % self.name)
        self.feedback_message = None

    def update(self):
        if self.confirmed:
            self.logger.debug("%s schon gesetzt." % self.name)
            return py_trees.common.Status.SUCCESS
        else:
            set_button_now = True  # Set to True to always use values from the form
            if set_button_now:
                if self.values is None:
                    if self.range is not None and type(self.range) is tuple:
                        chosen_value = self.blackboard.get(self.key)  # Use value from the form
                    else:
                        self.logger.debug(
                            "%s: error during update: key values are not a list, but range of int values is not given.")
                else:
                    chosen_value = self.blackboard.get(self.key)  # Use value from the form

                self.logger.debug("%s will einen %s" % (self.name, chosen_value))
                self.confirmed = True
                self.blackboard.set(self.key, chosen_value)

                return py_trees.common.Status.SUCCESS
            else:
                self.logger.debug("%s no input: status is %s" % (self.name, py_trees.common.Status.RUNNING))
                return py_trees.common.Status.RUNNING

    def terminate(self, new_status):
        self.logger.debug(
            "%s [EspressoBehavior::terminate().terminate()][%s->%s]" % (self.name, self.status, new_status))


class ProgramBehaviour(EspressoBehaviour):
    def __init__(self, name, key, values=None, val_range=None):
        super(ProgramBehaviour, self).__init__(name, key, values=values)


class TemperatureBehaviour(EspressoBehaviour):
    def __init__(self, name, key, values=None, val_range=None):
        super(TemperatureBehaviour, self).__init__(name, key, values=values)


class StrengthBehaviour(EspressoBehaviour):
    def __init__(self, name, key, values=None, val_range=None):
        super(StrengthBehaviour, self).__init__(name, key, values=values)


class FillQuantityBehaviour(EspressoBehaviour):
    def __init__(self, name, key, values=None, val_range=None):
        super(FillQuantityBehaviour, self).__init__(name, key, val_range=val_range)

class StartButtonBehaviour(py_trees.behaviour.Behaviour):
    def __init__(self, name):
        super(StartButtonBehaviour, self).__init__(name)

    def setup(self):
        self.logger.debug("%s [setup()]" % self.name)

    def initialise(self):
        self.logger.debug("%s [initialise()]" % self.name)

    def update(self):
        self.logger.debug("%s pressed" % self.name)
        return py_trees.common.Status.SUCCESS

    def terminate(self, new_status):
        self.logger.debug("%s [StartButtonBehaviour::terminate()][%s->%s]" % (self.name, self.status, new_status))


def create_parameter_setters(blackboard) -> py_trees.behaviour.Behaviour:
    blackboard.register_key(key="program", access=py_trees.common.Access.WRITE)
    blackboard.set('program', 'Test')
    blackboard.register_key(key="temperature", access=py_trees.common.Access.WRITE)
    blackboard.temperature = 'default'
    blackboard.register_key(key="strength", access=py_trees.common.Access.WRITE)
    blackboard.strength = 'default'
    blackboard.register_key(key="fill_quantity", access=py_trees.common.Access.WRITE)
    blackboard.fill_quantity = 0

    tree = py_trees.composites.Parallel(name="Set All Parameters",
                                        policy=py_trees.common.ParallelPolicy.SuccessOnAll())
    tree.add_child(ProgramBehaviour("Program",
                                    "program",
                                    values=['Espresso', 'Espresso Macchiato', 'Coffee', 'Cappuccino', 'Latte Macchiato', 'Caffè Latte']))

    tree.add_child(TemperatureBehaviour("Temperature",
                                       "temperature",
                                       values=['normal', 'high', 'very high']))

    tree.add_child(StrengthBehaviour("Strength",
                                     "strength",
                                     values=['very mild', 'mild', 'normal', 'strong', 'very strong', 'double shot', 'double shot plus', 'double shot plus plus']))

    tree.add_child(FillQuantityBehaviour("Quantity",
                                         "fill_quantity",
                                         val_range=(1, 251)))

    start_button = StartButtonBehaviour("StartButton")
    tree.add_child(start_button)

    return tree


def espresso_automat_main(program=None, temperature=None, strength=None, quantity=None):
    py_trees.logging.level = py_trees.logging.Level.DEBUG
    blackboard = py_trees.blackboard.Client(name="Tree")

    bt = py_trees.trees.BehaviourTree(root=create_parameter_setters(blackboard))
    bt.setup()

    try:
        if program:
            blackboard.set('program', program)
        if temperature:
            blackboard.set('temperature', temperature)
        if strength:
            blackboard.set('strength', strength)
        if quantity is not None:
            blackboard.set('fill_quantity', quantity)

        i = 0
        while bt.root.status != py_trees.common.Status.SUCCESS:
            bt.tick()
            i += 1
            print(f"Task state: {bt.root.status}")
    except KeyboardInterrupt:
        print("")
        pass

    return blackboard.program, blackboard.strength, blackboard.temperature, blackboard.fill_quantity
