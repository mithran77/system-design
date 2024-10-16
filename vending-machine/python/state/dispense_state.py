from state.vending_machine_state import VendingMachineState

class DispenseState(VendingMachineState):
    def __init__(self, vending_machine):
        super().__init__(vending_machine)

    def select_product(self, product):
        print("Product already selected. Please collect the dispenced product first")

    def insert_coin(self, coin):
        print("Payment already made. Please collect the dispenced product first")

    def insert_note(self, note):
        print("Payment already made. Please collect the dispenced product first")

    def dispense_product(self):
        product = self.vending_machine.selected_product
        self.vending_machine.inventory.update_quantity(
            product, self.vending_machine.inventory.get_quantity(product) - 1
        )
        print(f"Product dispensed: {product.name}")
        self.vending_machine.set_state(self.vending_machine.return_change_state)

    def return_change(self):
        print("Please collect the dispenced product first")
