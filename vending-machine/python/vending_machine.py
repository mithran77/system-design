from inventory import Inventory
from state.vending_machine_state import VendingMachineState
from state.idle_state import IdleState
from state.ready_state import ReadyState
from state.dispense_state import DispenseState
from state.return_change_state import ReturnChangeState
from product import Product
from constants.coin import Coin
from constants.note import Note

# Singleton
class VendingMachine:
    _instance = None

    def __init__(self):
        if VendingMachine._instance is not None:
            raise Exception("This is a singleton")
        else:
            VendingMachine._instance = self
            self.inventory = Inventory()
            self.idle_state = IdleState(self)
            self.ready_state = ReadyState(self)
            self.dispence_state = DispenseState(self)
            self.return_change_state = ReturnChangeState(self)
            self.current_state = self.idle_state
            self.selected_product = None
            self.total_payment = 0.0

    @staticmethod
    def get_instance():
        if VendingMachine._instance is None:
            VendingMachine()
        return VendingMachine._instance

    def select_product(self, product: Product):
        self.current_state.select_product(product)

    def insert_coin(self, coin: Coin):
        self.current_state.insert_coin(coin)

    def insert_note(self, note: Note):
        self.current_state.insert_note(note)

    def dispense_product(self):
        self.current_state.dispense_product()

    def return_change(self):
        self.current_state.return_change()

    def set_state(self, state: VendingMachineState):
        self.current_state = state

    def add_coin(self, coin: Coin):
        self.total_payment += coin.value

    def add_note(self, note: Note):
        self.total_payment += note.value

    def reset_payment(self):
        self.total_payment = 0.0

    def reset_selection(self):
        self.selected_product = None

