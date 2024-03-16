import re
import pymem
import pymem.process
import tkinter
import tkinter.ttk
import ctypes
import ctypes.wintypes


class CheatEngine():
    def __init__(self):
        self.root = tkinter.Tk()

        self.tree_scan_view = tkinter.ttk.Treeview(self.root)
        self.tree_address_view = tkinter.ttk.Treeview(self.root)

        self.Value_Entry = tkinter.StringVar()

        self.Found_number = 0

        self.data_addresses = []

        self.SetupGUI()

    def add_tree_scan_view(self):
        self.tree_scan_view.place(relx=0.001, rely=0.04, relwidth=0.5, relheight=0.5)

        self.tree_scan_view["columns"] = ("1", "2", "3")
        self.tree_scan_view.column("#0", width=120, minwidth=100, stretch=tkinter.NO)
        self.tree_scan_view.column("1", width=120, minwidth=100, stretch=tkinter.NO)
        self.tree_scan_view.column("2", width=120, minwidth=100, stretch=tkinter.NO)

        self.tree_scan_view.heading("#0", text="Address", anchor=tkinter.W)
        self.tree_scan_view.heading("1", text="Value", anchor=tkinter.W)
        self.tree_scan_view.heading("2", text="Previous", anchor=tkinter.W)

        self.tree_scan_view.insert("", "0", "item1", text="Item 1")
        # self.tree_scan_view.insert("item1", "end", text="Subitem 1")
        self.tree_scan_view.insert("", "1", "item2", text="Item 2")
        # self.tree_scan_view.insert("item2", "end", text="Subitem 2")

    def add_tree_address_view(self):
        self.tree_address_view.place(relx=0.001, rely=0.545, relwidth=0.999, relheight=0.5)

        self.tree_address_view["columns"] = ("1", "2", "3", "4")
        self.tree_address_view.column("#0", width=150, minwidth=100, stretch=tkinter.NO)
        self.tree_address_view.column("1", width=150, minwidth=100, stretch=tkinter.NO)
        self.tree_address_view.column("2", width=150, minwidth=100, stretch=tkinter.NO)
        self.tree_address_view.column("3", width=150, minwidth=100, stretch=tkinter.NO)

        self.tree_address_view.heading("#0", text="Description", anchor=tkinter.W)
        self.tree_address_view.heading("1", text="Address", anchor=tkinter.W)
        self.tree_address_view.heading("2", text="Type", anchor=tkinter.W)
        self.tree_address_view.heading("3", text="Value", anchor=tkinter.W)

        self.tree_address_view.insert("", "0", "item1", text="Item 1")
        # self.tree_address_view.insert("item1", "end", text="Subitem 1")
        self.tree_address_view.insert("", "1", "item2", text="Item 2")
        # self.tree_address_view.insert("item2", "end", text="Subitem 2")

    def SetupGUI(self):
        self.root.title("Cheat Engine 0.1.0")
        self.root.geometry("700x600")

        self.add_tree_scan_view()
        self.add_tree_address_view()

        self.First_Scan_button = tkinter.ttk.Button(self.root, text="First Scan", command=self.First_Scan_program)
        self.First_Scan_button.place(relx=0.54, rely=0.05)
        self.Next_Scan_button = tkinter.ttk.Button(self.root, text="Next Scan", command=self.Next_Scan_program)
        self.Next_Scan_button.place(relx=0.66, rely=0.05)

        self.Value_Entry_display = tkinter.ttk.Entry(self.root, textvariable=self.Value_Entry)
        self.Value_Entry_display.place(relx=0.54, rely=0.12, relwidth=0.3)

        self.Found_text_label = tkinter.Label(self.root, text=f"Found: {self.Found_number}")
        self.Found_text_label.place(x=0, y=0)

        self.root.mainloop()

    def First_Scan_program(self):
        value = int(self.Value_Entry.get())

        pm = pymem.Pymem("cs2.exe")
        print(pm)

        module = pymem.process.module_from_name(pm.process_handle, "cs2.exe")
        print(module)

        bytes_read = pm.read_bytes(module.lpBaseOfDll, module.SizeOfImage)

        byte_list = list(bytes_read)

        health_bytes = value.to_bytes(4, byteorder='little')

        addresses = []

        for i in range(len(byte_list) - 3):
            if byte_list[i:i+4] == list(health_bytes):
                address = module.lpBaseOfDll + i
                addresses.append(address)

        print("Addresses with the health value:")
        for address in addresses:
            print(hex(address))
            self.data_addresses.append([address, str(pm.read_int(address)), "hello"])
            self.tree_scan_view.insert("", "0", f"{hex(address)}", text=f"{hex(address)}", values=(str(pm.read_int(address)), "hello"))

    def Next_Scan_program(self):
        pm = pymem.Pymem("cs2.exe")
        print(pm)

        for i in range(len(self.data_addresses)):
            try:
                if pm.read_int(self.data_addresses[i][0]) != int(self.self.Value_Entry.get()):
                    del self.data_addresses[i]
                else:
                    print(self.data_addresses[i][0])

            except:
                pass

    def GetModules(self):
        pm = pymem.Pymem("cs2.exe")

        modules = pm.list_modules()

        for module in modules:
            print(module.name)


# CheatEngine()
            
































import time
import pymem
import threading


results = []
done = 0
found = 0

def First_find_memory_values(pm, start, end, value, chunk_size=4000):
    global done, found

    time.sleep(25)

    i = start
    while (i < end):
        try:
            chunk = pm.read_bytes(i, chunk_size)
            for j in range(0, chunk_size):
                v = int.from_bytes(chunk[j:j + 4], byteorder='little')
                if v == value:
                    print(f"Address: {hex(i + j)}, value: {v}")
                    found += 1
                    
            i += chunk_size - 5
        except:
            i += int(chunk_size / 4)
    
    done += 1

def main():
    pm = pymem.Pymem("cs2.exe")
    print(pm)
    
    threads_number = 50

    start_address = 0x1A500000000
    end_address =   0x1A800000000
    ink = int((end_address - start_address) / threads_number)

    how_many = 0

    i = 0
    for p in range(start_address, end_address, ink):
        i += 1
        print(f"thread {i} start AT: {hex(p)}, sizeof scan: {ink}")
        
        threading.Thread(target=lambda:First_find_memory_values(pm, p, p+ink, 9650)).start()
        how_many += 1

    while True:
        if how_many == done:
            print(f"Found: {found}")
            break


if __name__ == "__main__":
    main()



























































"""
import pymem


results = []

def First_find_memory_values(pm, start, end, value, chunk_size=4000):
    global results
    
    found = 0
    i = start
    
    while (i < end):
        try:
            chunk = pm.read_bytes(i, chunk_size)
            for j in range(0, chunk_size):
                v = int.from_bytes(chunk[j:j + 4], byteorder='little')
                if v == value:
                    if not v in results:
                        results.append([i + j, v])
                        print(f"Address: {hex(i + j)}, value: {v}")
                        found += 1

            i += chunk_size - 5
        except:
            i += int(chunk_size / 4)

        

    print(f"Found: {found}")
    
def Next_find_memory_values(pm, value):
    global results

    found = 0
    resu = []

    for addr in results:
        if pm.read_int(addr[0]) != value:
            results.remove(addr)
        else:
            found += 1
            print(f"Address: {hex(addr[0])}, value: {pm.read_int(addr[0])}")
            resu.append([addr[0], addr[1]])

    results = resu

    print(f"Found: {found}")

def main():
    pm = pymem.Pymem("cs2.exe")
    print(pm)

    start_address = 0x1A500000000
    end_address =   0x1A75ADAAAAA

    while True:
        com = input("->").split(" ")
        if com[0] == "first":
            First_find_memory_values(pm, start_address, end_address, int(com[1]))
        elif com[0] == "next":
            Next_find_memory_values(pm, int(com[1]))



if __name__ == "__main__":
    main()  
"""