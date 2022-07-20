import tkinter as tk
import tkinter.ttk
import pandas

root = tk.Tk()
root.title('PCBSCalc2Beta')
root.geometry('800x800')
root.maxsize(800,800)
root.minsize(800,800)


CPU_Asset = pandas.read_excel('CPU.xlsx', index_col=0)
CPU_list = list(CPU_Asset.iloc[:]['Part Name'])
GPU_Asset = pandas.read_excel('GPU.xlsx', index_col=0)
GPU_list = list(GPU_Asset.iloc[:]['Part Name'])
CPU_Asset.set_index('Part Name', inplace=True)
GPU_Asset.set_index('Part Name', inplace=True)


class SearchBox:
    def __init__(self, part_type, column):
        global CPU_list

        self.part_type = part_type
        self.column = column

        if part_type == 'CPU':
            self.part_list = CPU_list
        else:
            self.part_list = GPU_list

        self.entry = tk.Entry(root, width=50)
        self.entry.grid(row=1, column=self.column)
        self.entry.bind('<KeyRelease>', self.on_keyrelease)

        self.listbox = tk.Listbox(root, width=50)
        self.listbox.grid(row=2, column=self.column)
        # listbox.bind('<Double-Button-1>', on_select)
        self.listbox.bind('<<ListboxSelect>>', self.on_select)
        self.listbox_update(self.part_list)

        self.listbox.bind('<Double-Button-1>', self.on_doubleclick)

        self.CPU_freq = None
        self.part_name = None
        self.CPU_Core_Multiplier = None
        self.CPU_Mem_Multiplier = None
        self.CPU_Cha_Multiplier = None
        self.CPU_Adjustment = None
        self.CPU_score = None

    def on_keyrelease(self, event):
        # get text from entry
        value = event.widget.get()
        value = value.strip().lower()

        # get data from test_list
        if value == '':
            data = self.part_list
        else:
            data = []
            for item in self.part_list:
                if value in item.lower():
                    data.append(item)

                    # update data in listbox
        self.listbox_update(data)

    def listbox_update(self, data):
        # delete previous data
        self.listbox.delete(0, 'end')

        # sorting data
        data = sorted(data, key=str.lower)

        # put new data
        for item in data:
            self.listbox.insert('end', item)

    def on_select(self, event):
        # display element selected on list
        print('(event) previous:', event.widget.get('active'))
        print('(event)  current:', event.widget.get(event.widget.curselection()))
        print('---')

    def get_CPU_info(self):
        pass
        # get the frequency of selected CPU
        # CPU_Asset.set_index('Part Name', inplace=True)
        self.CPU_freq = CPU_Asset.loc[self.part_name]['Frequency']
        self.CPU_Core_Multiplier = CPU_Asset.loc[self.part_name]['Core Clock Multiplier (TS)']
        self.CPU_Mem_Multiplier = CPU_Asset.loc[self.part_name]['Mem Clock Multiplier (TS)']
        self.CPU_Cha_Multiplier = CPU_Asset.loc[self.part_name]['Mem Channels Multiplier (TS)']
        self.CPU_Adjustment = CPU_Asset.loc[self.part_name]['Final Adjustment (TS)']
        self.CPU_score = round(298 * (self.CPU_Core_Multiplier * self.CPU_freq +
                          self.CPU_Mem_Multiplier * 2133 +
                          self.CPU_Cha_Multiplier * 1 +
                          self.CPU_Adjustment))

    def on_doubleclick(self, event):
        self.entry.delete(0, 'end')
        self.part_name = self.listbox.get(self.listbox.curselection())
        self.entry.insert(0, self.part_name)
        if self.part_type == 'CPU':
            self.get_CPU_info()
            CPU_Freq.set(f'Frequency: {self.CPU_freq}')
            CPU_Score.set(f'CPU Time Spy Score: {self.CPU_score}')


l1 = tk.Label(root, text='选择CPU')
l1.grid(row=0, column=0)
l2 = tk.Label(root, text='选择GPU')
l2.grid(row=0, column=2)
SearchBox('CPU', 0)
SearchBox('GPU', 2)

CPU_Freq = tk.StringVar()
CPU_Score = tk.StringVar()
CPU_Freq.set('Frequency:')
CPU_Score.set('CPU Time Spy Score:')
l3 = tk.Label(root, textvariable=CPU_Freq)
l3.grid(row=3, column=0)
l3 = tk.Label(root, textvariable=CPU_Score)
l3.grid(row=4, column=0)

root.mainloop()
