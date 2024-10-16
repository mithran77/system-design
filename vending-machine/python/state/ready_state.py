from state.vending_machine_state import VendingMachineState
from constants.coin import Coin
from constants.note import Note

class ReadyState(VendingMachineState):
    def __init__(self, vending_machine):
        super().__init__(vending_machine)

    def select_product(self, product):
        print("Product already selected. Please Make payment")

    def insert_coin(self, coin: Coin):
        self.vending_machine.add_coin(coin)
        print(f"Coin inserted: {coin}")
        self.check_payment_status()

    def insert_note(self, note: Note):
        self.vending_machine.add_note(note)
        print(f"Note inserted: {note}")
        self.check_payment_status()

    def dispense_product(self):
        print("Please make payment first")

    def return_change(self):
        change = self.vending_machine.total_payment
        if change > 0:
            print(f"Change returned: ${change:.2f}")
            self.vending_machine.reset_payment()
        else:
            print("No change to return.")
        self.vending_machine.reset_selection()
        self.vending_machine.set_state(self.vending_machine.idle_state)

    def check_payment_status(self):
        if self.vending_machine.total_payment >= self.vending_machine.selected_product.price:
            self.vending_machine.set_state(self.vending_machine.dispence_state)

