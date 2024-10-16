from state.vending_machine_state import VendingMachineState
from product import Product

class IdleState(VendingMachineState):
    def __init__(self, vending_machine):
        super().__init__(vending_machine)

    def select_product(self, product: Product):
        if self.vending_machine.inventory.is_available(product):
            self.vending_machine.selected_product = product
            print(f"Product selected : {product.name}")
            self.vending_machine.set_state(self.vending_machine.ready_state)
        else:
            print(f"Product not available: {product.name}")

    def insert_coin(self, coin):
        print("Please select product first")

    def insert_note(self, note):
        print("Please select product first")

    def dispense_product(self):
        print("Please select product & make payment")

    def return_change(self):
        print("No change to return.")
