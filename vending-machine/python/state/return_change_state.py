from state.vending_machine_state import VendingMachineState

class ReturnChangeState(VendingMachineState):
    def __init__(self, vending_machine):
        super().__init__(vending_machine)

    def select_product(self, product):
        print("Please collect the change first.")

    def insert_coin(self, coin):
        print("Please collect the change first.")

    def insert_note(self, note):
        print("Please collect the change first.")

    def dispense_product(self):
        print("Product already dispensed. Please collect the change.")

    def return_change(self):
        change = self.vending_machine.total_payment - self.vending_machine.selected_product.price
        if change > 0:
            print(f"Change returned: ${change:.2f}")
            self.vending_machine.reset_payment()
        else:
            print(f"No change to return")
        self.vending_machine.reset_selection()
        self.vending_machine.set_state(self.vending_machine.idle_state)
