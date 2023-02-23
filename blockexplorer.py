import requests
import tkinter as tk
import awesometkinter as atk

# Create the tkinter GUI
root = tk.Tk()
root.configure(background='black')
root.title('BTC Explorer')


def popup(event):
    try:
        menu.entryconfig('Paste', font=('Roboto 14'), command=lambda: paste(event.widget)) # Set the command for the 'Paste' option
        menu.tk_popup(event.x_root, event.y_root) # Pop the menu up in the given coordinates
    finally:
        menu.grab_release() # Release it once an option is selected

def paste(widget):
    clipboard = root.clipboard_get() # Get the copied item from system clipboard
    widget.insert('end', clipboard) # Insert the item into the widget

menu = tk.Menu(root,tearoff=0) # Create a menu

def get_addr_data():
    addr = addr_input.get()
    try:
        response = requests.get(f"https://blockchain.info/rawaddr/{addr}", timeout=15)
        response.raise_for_status()
        # Code here will only run if the request is successful
        j = response.json()
        address = j['address']
        n_tx = j['n_tx']
        total_received = j['total_received']
        total_sent = j['total_sent']
        final_balance = j['final_balance']

        # Create a new window to display the output
        addr_window = tk.Toplevel(root)
        addr_window.title("Address Data")

        addr_label = tk.Label(addr_window, text=f"Address: {address}\n"
                                                 f"Number of Tx's: {n_tx}\n"
                                                 f"Total Received: {total_received}\n"
                                                 f"Total Sent: {total_sent}\n"
                                                 f"Final Balance: {final_balance}\n"
                              )
        addr_label.pack()

    except requests.exceptions.HTTPError as errh:
        err_window = tk.Toplevel(root)
        err_window.title("ERROR")
        addr_data_label = tk.Label(err_window, text=f"HTTP error: {errh}")
        addr_data_label.pack()

    except requests.exceptions.ConnectionError as errc:
        err_window = tk.Toplevel(root)
        err_window.title("ERROR")
        addr_data_label = tk.Label(err_window, text=f"Connection error: {errc}")
        addr_data_label.pack()

    except requests.exceptions.Timeout as errt:
        err_window = tk.Toplevel(root)
        err_window.title("ERROR")
        addr_data_label = tk.Label(err_window, text=f"Timeout error: {errt}")
        addr_data_label.pack()

    except requests.exceptions.RequestException as err:
        err_window = tk.Toplevel(root)
        err_window.title("ERROR")
        addr_data_label = tk.Label(err_window, text=f"Request error: {err}")
        addr_data_label.pack()


def get_block_data():
    blk_hash = block_input.get()
    try:
        response = requests.get(f"https://blockchain.info/rawblock/{blk_hash}", timeout=15)
        response.raise_for_status()
        # Code here will only run if the request is successful
        j = response.json()
        blk_hash = j['hash']
        prev_blk = j['prev_block']
        merkle = j['mrkl_root']
        blocktime = j['time']
        num_tx = j['n_tx']
        main_chain = j['main_chain']
        blk_height = j['height']

        # Create a new window to display the output
        block_window = tk.Toplevel(root)
        block_window.title("Block Data")

        block_label = tk.Label(block_window, text=f"Blockhash: {blk_hash}\n"
                                   f"Block height: {blk_height}\n"
                                   f"Blocktime: {blocktime}\n"
                                   f"Previous Block: {prev_blk}\n"
                                   f"Merkle Root: {merkle}\n"
                                   f"Main Chain: {main_chain}\n"
                                   f"Number of TX's: {num_tx}\n"
                              )
        block_label.pack()

    except requests.exceptions.HTTPError as errh:
        err_window = tk.Toplevel(root)
        err_window.title("ERROR")
        block_data_label = tk.Label(err_window, text=f"HTTP error: {errh}")
        block_data_label.pack()

    except requests.exceptions.ConnectionError as errc:
        err_window = tk.Toplevel(root)
        err_window.title("ERROR")
        block_data_label = tk.Label(err_window, text=f"Connection error: {errc}")
        block_data_label.pack()

    except requests.exceptions.Timeout as errt:
        err_window = tk.Toplevel(root)
        err_window.title("ERROR")
        block_data_label = tk.Label(err_window, text=f"Timeout error: {errt}")
        block_data_label.pack()

    except requests.exceptions.RequestException as err:
        err_window = tk.Toplevel(root)
        err_window.title("ERROR")
        block_data_label = tk.Label(err_window, text=f"Request error: {err}")
        block_data_label.pack()

def popup(event):
    try:
        menu.entryconfig('Paste', font=('Roboto 14'), command=lambda: paste(event.widget)) # Set the command for the 'Paste' option
        menu.tk_popup(event.x_root, event.y_root) # Pop the menu up in the given coordinates
    finally:
        menu.grab_release() # Release it once an option is selected

def paste(widget):
    clipboard = root.clipboard_get() # Get the copied item from system clipboard
    widget.insert('end', clipboard) # Insert the item into the widget

menu = tk.Menu(root,tearoff=0) # Create a menu

def get_tx_data():
    tx_hash = tx_input.get()
    try:
        response = requests.get(f"https://blockchain.info/rawtx/{tx_hash}", timeout=15)
        response.raise_for_status()
        # Code here will only run if the request is successful
        j = response.json()
        txhash = j['hash']
        blk_height = j['block_height']
        num_send = j['vin_sz']
        num_rec = j['vout_sz']
        inputs_data = []
        for i in range(num_send):
            input_data = {}
            input_data['address'] = j['inputs'][i]['prev_out']['addr']
            input_data['spent'] = j['inputs'][i]['prev_out']['spent']
            input_data['value'] = j['inputs'][i]['prev_out']['value']
            inputs_data.append(input_data)
        outputs_data = []
        for i in range(num_rec):
            output_data = {}
            output_data['address'] = j['out'][i]["addr"]
            output_data['spent'] = j['out'][i]["spent"]
            output_data['value'] = j['out'][i]["value"]
            outputs_data.append(output_data)

        # Create a new window to display the output
        tx_window = tk.Toplevel(root)
        tx_window.title("TX Data")

        tx_label = tk.Label(tx_window, text=f"Transaction hash: {txhash}\n"
                                   f"Block height: {blk_height}\n"
                                   f"Number of inputs: {num_send}\n"
                                   f"Number of outputs: {num_rec}\n")
        tx_label.pack()

        # Display input data
        input_frame = tk.Frame(tx_window, bg='white')
        input_label = tk.Label(input_frame, text="Inputs:", bg='white', font=('Roboto', 14, 'bold'))
        input_label.pack()
        for input_data in inputs_data:
            input_address = input_data['address']
            input_spent = input_data['spent']
            input_value = input_data['value']
            input_info = f"Address: {input_address}\n" \
                         f"Spent: {input_spent}\n" \
                         f"Value: {input_value}\n"
            input_info_label = tk.Label(input_frame, text=input_info, bg='white')
            input_info_label.pack()
        input_frame.pack(side='left', padx=10, pady=10)

        # Display output data
        output_frame = tk.Frame(tx_window, bg='white')
        output_label = tk.Label(output_frame, text="Outputs:", bg='white', font=('Roboto', 14, 'bold'))
        output_label.pack()
        for output_data in outputs_data:
            output_address = output_data['address']
            output_spent = output_data['spent']
            output_value = output_data['value']
            output_info = f"Address: {output_address}\n" \
                          f"Spent: {output_spent}\n" \
                          f"Value: {output_value}\n"
            output_info_label = tk.Label(output_frame, text=output_info, bg='white')
            output_info_label.pack()
        output_frame.pack(side='left', padx=10, pady=10)

    except requests.exceptions.HTTPError as errh:
        err_window = tk.Toplevel(root)
        err_window.title("ERROR")
        tx_data_label = tk.Label(err_window, text=f"HTTP error: {errh}")
        tx_data_label.pack()

    except requests.exceptions.ConnectionError as errc:
        err_window = tk.Toplevel(root)
        err_window.title("ERROR")
        tx_data_label = tk.Label(err_window, text=f"Connection error: {errc}")
        tx_data_label.pack()

    except requests.exceptions.Timeout as errt:
        err_window = tk.Toplevel(root)
        err_window.title("ERROR")
        tx_data_label= tk.Label(err_window, text=f"Timeout error: {errt}")
        tx_data_label.pack()

    except requests.exceptions.RequestException as err:
        err_window = tk.Toplevel(root)
        err_window.title("ERROR")
        tx_data_label = tk.Label(err_window, text=f"Request error: {err}")
        tx_data_label.pack()

# Add an input field for the Bitcoin address
addr_input = tk.Entry(root, font=('Roboto 14'), width=60)
addr_input.bind('<Button-3>',popup) # Bind a func to right click
addr_input.pack()

# Add a button to retrieve the address data and binding "paste" to right click
addr_button = atk.Button3d(root,
                           width=60,
                           text="Get Address Data",
                           command=get_addr_data)
addr_button.pack()


# Add an input field for the block hash
block_input = tk.Entry(root, font=('Roboto 14'), width=60)
block_input.bind('<Button-3>',popup)
block_input.pack()

# Add a button to retrieve the block data
block_button = atk.Button3d(root,
                            width=60,
                            text="Get Block Data",
                            command=get_block_data)
block_button.pack()


# Add an input field for the tx hash and binding "paste" to right click
tx_input = tk.Entry(root, font=('Roboto 14'), width=60)
tx_input.bind('<Button-3>',popup)
tx_input.pack()

# Add a button to retrieve the tx data
tx_button = atk.Button3d(root,
                         width=60,
                         text="Get TX Data",
                         command=get_tx_data)
tx_button.pack()

menu.add_command(label='Paste') # Add the 'Paste' option to the menu

# Start the GUI main loop
root.mainloop()
