import tkinter as tk
import webbrowser
import requests


class BlockchainInfoAPI:
    BASE_URL = "https://blockchain.info"

    def get_block_info_by_hash(self, block_hash):
        url = f"{self.BASE_URL}/rawblock/{block_hash}"
        response = requests.get(url)
        return response.json()

    def get_tx_info(self, tx_hash):
        url = f"{self.BASE_URL}/rawtx/{tx_hash}"
        response = requests.get(url)
        return response.json()

    def get_address_info(self, address):
        url = f"{self.BASE_URL}/rawaddr/{address}"
        response = requests.get(url)
        return response.json()


class BlockSearchWindow:
    def __init__(self, master):
        self.master = master
        master.title("BTC EXPLORER")
        master.geometry("400x225")
        master.configure(bg='black')

        # Create the block hash search section
        self.block_hash_label = tk.Label(master, text="Enter block hash:", fg="white", bg="black")
        self.block_hash_label.pack()
        self.block_hash_entry = tk.Entry(master, width=40)
        self.block_hash_entry.pack()
        self.block_hash_button = tk.Button(
            master, text="Get Block Info", command=self.get_block_info, fg="white", bg="black"
        )
        self.block_hash_button.pack()

        # Create the transaction hash search section
        self.tx_hash_label = tk.Label(master, text="Enter transaction hash:", fg="white", bg="black")
        self.tx_hash_label.pack()
        self.tx_hash_entry = tk.Entry(master, width=40)
        self.tx_hash_entry.pack()
        self.tx_hash_button = tk.Button(
            master, text="Get Transaction Info", command=self.get_tx_info, fg="white", bg="black"
        )
        self.tx_hash_button.pack()

        # Create the address search section
        self.address_label = tk.Label(master, text="Enter address:", fg="white", bg="black")
        self.address_label.pack()
        self.address_entry = tk.Entry(master, width=40)
        self.address_entry.pack()
        self.address_button = tk.Button(
            master, text="Get Address Info", command=self.get_address_info, fg="white", bg="black"
        )
        self.address_button.pack()

    def get_block_info(self):
        block_hash = self.block_hash_entry.get()
        api = BlockchainInfoAPI()
        block_info = api.get_block_info_by_hash(block_hash)
        self.display_json(block_info)

    def get_tx_info(self):
        tx_hash = self.tx_hash_entry.get()
        api = BlockchainInfoAPI()
        tx_info = api.get_tx_info(tx_hash)
        self.display_json(tx_info)

    def get_address_info(self):
        address = self.address_entry.get()
        api = BlockchainInfoAPI()
        address_info = api.get_address_info(address)
        self.display_json(address_info)

    def display_json(self, json_data):
        top = tk.Toplevel(self.master)
        top.title("RESULTS PAGE")
        top.geometry("600x200")

        text = tk.Text(top, wrap="none")
        text.pack(side="left", fill="both", expand=True)

        vsb = tk.Scrollbar(top, orient="vertical", command=text.yview)
        vsb.pack(side="right", fill="y")

        text.configure(yscrollcommand=vsb.set)

        lines = []
        if "hash" in json_data:
            lines.append(f"Hash: {json_data['hash']}")
        if "block_height" in json_data:
            lines.append(f"Block Height: {json_data['block_height']}")
        if "block_time" in json_data:
            lines.append(f"Block Time: {json_data['block_time']}")
        if "vin_sz" in json_data:
            lines.append(f"Number of Input Transactions: {json_data['vin_sz']}")
        if "vout_sz" in json_data:
           lines.append(f"Number of Output Transactions: {json_data['vout_sz']}")
        if "double_spend" in json_data:
           lines.append(f"Double Spend: {json_data['double_spend']}")
        if "result" in json_data:
           lines.append(f"Transaction Result: {json_data['result']}")
        if "time" in json_data:
           lines.append(f"Time: {json_data['time']}")
        if "height" in json_data:
            lines.append(f"Block Height: {json_data['height']}")
        if "main_chain" in json_data:
            lines.append(f"Main Chain: {json_data['main_chain']}")
        if "mrkl_root" in json_data:
            lines.append(f"Merkle Root: {json_data['mrkl_root']}")
        if "n_tx" in json_data:
            lines.append(f"Number of Transactions: {json_data['n_tx']}")
        if "next_block" in json_data:
            lines.append(f"Next Block Hash: {json_data['next_block']}")
        if "prev_block" in json_data:
            lines.append(f"Previous Block Hash: {json_data['prev_block']}")
        if "address" in json_data:
            lines.append(f"Address: {json_data['address']}")
        if "total_received" in json_data:
            lines.append(f"Total Satoshi's Received: {json_data['total_received']}")
        if "total_sent" in json_data:
            lines.append(f"Total Satoshi's Sent: {json_data['total_sent']}")
        if "final_balance" in json_data:
            lines.append(f"Final Balance: {json_data['final_balance']}")

        text.insert("1.0", "\n".join(lines))

if __name__ == "__main__":
    root = tk.Tk()
    app = BlockSearchWindow(root)
    root.mainloop()
