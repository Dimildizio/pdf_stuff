"""a UI tool to cut pdfs"""


from tkinter import *  
from tkinter import messagebox
from tkinter.simpledialog import askstring
from tkinter.filedialog import askopenfilename, askdirectory
import os
from PyPDF2 import PdfWriter, PdfReader



lablefont = ("Helvetica", 15)
buttonfont = ("Helvetica", 10)


class ImGUI:
	def __init__(self):
		self.root = Tk()
		self.root.geometry("1024x780")
		self.title = self.root.title("PDF chainsaw")

		self.fileaddress = ''
		self.saveaddress = os.getcwd()
		self.cutrow = 0
		self.entries = []
		self.name = '_part_01'
		self.text1 = StringVar()
		self.text1.set(f'Current file: \n{self.fileaddress if self.fileaddress else "not selected"}')
		self.label1 = Label(self.root, textvariable=self.text1, font = lablefont)
		self.label1.pack(side=TOP,pady=10)
		self.button1 = Button(text="Select file", height = 2, width = 10, command = self.getfilename)
		self.button1.pack(side = TOP, pady = 10)
		self.text2 = StringVar()
		self.text2.set("Save to: \n"+self.saveaddress)
		self.label2 = Label(self.root, textvariable=self.text2, font = buttonfont)
		self.label2.pack(side=TOP, pady=10)
		self.button2 = Button(text="Save to", height = 2, width = 10, command = self.change_save_address)
		self.button2.pack(side = TOP, pady = 10)

		self.text5 = StringVar()
		self.text5.set(f"Filename: \n{self.name}.pdf")
		self.label5 = Label(self.root, textvariable=self.text5, font = buttonfont)
		self.label5.pack(side=TOP, pady=10)
		self.button5 = Button(text="Rename", height = 2, width = 10, command = self.rename)
		self.button5.pack(side = TOP, pady = 10)

		self.label3 = Label(self.root, font = buttonfont)
		self.label3.pack(side=TOP)

		self.button3 = Button(text="Add more", height = 2, width = 10, command = self.add_cut_pages)
		self.button3.pack(side = TOP, pady = 10)
	
		self.button4 = Button(text="CUT", height = 2, width = 25, font = lablefont,  command = self.cutme)
		self.button4.pack(side = TOP, pady = 10)
		self.add_cut_pages()
		mainloop()

	def rename(self):
		name = askstring("Rename", 'Write a new filename:')
		if name: 
			self.name = name
			self.text5.set("Filename: \n"+self.name+'.pdf')
		print()


	def getfilename(self):
		self.fileaddress = askopenfilename()
		self.text1.set('Current file: \n'+self.fileaddress)
		

	def change_save_address(self):
		self.saveaddress = askdirectory()
		self.text2.set("Save to: \n"+self.saveaddress)
		print(self.saveaddress)

	def add_cut_pages(self):
		self.cutrow+=1
		data = [(entry[0].get(), entry[1].get()) for entry in self.entries]


		for x in range(self.cutrow):
			
			labelfrom = Label(self.label3, text='from page: ')
			labelto = Label(self.label3, text='to page: ')
			e1 = Entry(self.label3)
			e2 = Entry(self.label3)
			

			print('DATA',data[x] if len(data)>x else 'NONE')
			mytext = data[x] if len(data) > x else ('','')

			e1.insert(0,mytext[0])
			e2.insert(0,mytext[1])

		
			labelfrom.grid(row=x, column=0)
			labelto.grid(row=x, column=2)
			e1.grid(row=x,column=1)
			e2.grid(row=x,column=3)

			if len(self.entries) > x:
				self.entries[x] = (e1,e2)
			else: self.entries.append((e1,e2))
		
		self.label3.pack(side=TOP)



	def clean_data(self, max_pages):
		checked = []
		for pair in self.entries:
			num1,num2 = pair[0].get(), pair[1].get()
			if num1.isdigit() and num2.isdigit():
				try:
					num1 = min(max(int(num1), 1), max_pages)
					num2 = min(max(int(num2), 1), max_pages)
					data = (num1,num2) if num2 > num1 else (num2, num1)
					checked.append(data)
				except:
					messagebox.showerror(title='Wrong input', message="Only digits allowed")
					return
			else: 
				continue
		return checked




	def cutme(self):
		try:
			print("FILEADDRESS: ", self.fileaddress)
			mypdf = PdfReader(open(self.fileaddress, "rb"))


		except FileNotFoundError: 
			messagebox.showerror(title='File not found', message="Please select a file to work with")
			
		else:	
			pages = self.clean_data(len(mypdf.pages))
			if not pages: return
			print(pages)

			counter = 1
			for pair in pages:
				name = f'{self.saveaddress}\\{self.name}_part_{counter}.pdf' if len(pages)>1 else f'{self.saveaddress}\\{self.name}.pdf'
				print('MYNAME', name)
				my_file=open(name, "wb")
				writer = PdfWriter()

				for page_num in range(pair[0]-1,pair[1]):
					print(page_num)
					page = mypdf.pages[page_num]
					writer.add_page(page)

				counter += 1
				writer.write(my_file)
			messagebox.showinfo('Done', "Files cut successfully")


a = ImGUI()
