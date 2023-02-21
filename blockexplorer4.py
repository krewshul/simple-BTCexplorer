import tkinter as tk
import requests


class BlockchainInfoAPI:
    BASE_URL = "https://blockchain.info"

    def get_info(self, url_suffix):
        url = f"{self.BASE_URL}/{url_suffix}"
        response = requests.get(url)
        return response.json()


class BlockSearchWindow:
    def __init__(self, master):
        self.master = master
        self.entry_widget = None
        master.title("BTC EXPLORER")
        master.geometry("400x225")
        master.configure(bg='black')

        # Create the block hash search section
        self.block_hash_entry = self.create_input_section("Enter block hash:", "Get Block Info", self.get_block_info)

        # Create the transaction hash search section
        self.tx_hash_entry = self.create_input_section("Enter transaction hash:", "Get Transaction Info", self.get_tx_info)

        # Create the address search section
        self.address_entry = self.create_input_section("Enter address:", "Get Address Info", self.get_address_info)

    def create_input_section(self, label_text, button_text, command_func):
        label = tk.Label(self.master, text=label_text, fg="white", bg="black")
        label.pack()
        entry = tk.Entry(self.master, width=40)
        entry.pack()
        self.entry_widget = entry
        button = tk.Button(self.master, text=button_text, command=command_func, fg="white", bg="black")
        button.pack()
        return entry

    def get_block_info(self):
        block_hash = self.block_hash_entry.get()
        api = BlockchainInfoAPI()
        block_info = api.get_info(f"rawblock/{block_hash}")
        self.display_json(block_info)

    def get_tx_info(self):
        tx_hash = self.tx_hash_entry.get()
        api = BlockchainInfoAPI()
        tx_info = api.get_info(f"rawtx/{tx_hash}")
        self.display_json(tx_info)

    def get_address_info(self):
        address = self.address_entry.get()
        api = BlockchainInfoAPI()
        address_info = api.get_info(f"rawaddr/{address}")
        self.display_json(address_info)

    def get_input(self):
        return self.entry_widget.get()

    def display_json(self, json_data):
        top = tk.Toplevel(self.master)
        top.title("RESULTS PAGE")
        top.geometry("650x200")

        text = tk.Text(top, wrap="none")
        text.pack(side="left", fill="both", expand=True)

        vsb = tk.Scrollbar(top, orient="vertical", command=text.yview)
        vsb.pack(side="right", fill="y")

        text.configure(yscrollcommand=vsb.set)

        for key, value in json_data.items():
            if key in ["hash", "block_height", "block_time", "vin_sz", "vout_sz", "double_spend",
                       "result", "time", "height", "main_chain", "mrkl_root", "n_tx", "next_block",
                       "prev_block", "address", "total_received", "total_sent", "final_balance"]:
                text.insert("1.0", f"{key.title().replace('_', ' ')}: {value}\n")


if __name__ == "__main__":
    root = tk.Tk()
    app = BlockSearchWindow(root)
    root.mainloop()
