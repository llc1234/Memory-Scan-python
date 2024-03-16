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
