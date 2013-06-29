from Tkinter import *
from tkFileDialog import *
from subprocess import call

defGridOps = {"padx" : 4, "pady" : 2}

class Application:
	def addButton(self, opts, column=None, row=None):
		defColumn, defRow = self.tk.grid_size()
		if column == None:
			column = 0
		if row == None:
			row = defRow
		b = Button(self.tk, **opts)
		b.grid(row=row, column=column, **defGridOps)
		return b
		
	def addButtons(self):
		nextRow = self.tk.grid_size()[1]
		self.newButton = self.addButton({"text":"New schedule", "command":
			self.showNewCmd}, row=nextRow, column=1)
		self.updateButton = self.addButton({"text":"Update schedule", 
			"command":self.showUpdateCmd}, row=nextRow, column=2)
		self.quitButton = self.addButton({"text":"QUIT", "fg":"red",
			"command":self.tk.quit}, row=nextRow, column=0)
			
	def addInputFields(self):
		(self.titleLabel, self.titleEntry) = \
			self.addField("Title", {"width":50})
		(self.columnLabel, self.columnEntry) = \
			self.addField("Columns", {"width":2})
		(self.pageLabel, self.pageEntry) = \
			self.addField("Page", {"width":3})
		(self.startLabel, self.startEntry) = \
			self.addField("Start date", {"width":10})
		(self.endLabel, self.endEntry) = \
			self.addField("End date", {"width":10})
		(self.stopFileEntry, self.stopFileButton) = \
			self.addFileField("Stop file", askopenfilename,
			eops={"width":50}, bops={"width":20})
		(self.outFileEntry, self.outFileButton) = \
			self.addFileField("Output file", asksaveasfilename, 
			eops={"width":50}, bops={"width":20})
		(self.dataFileEntry, self.dataFileButton) = \
			self.addFileField("Data file", askopenfilename,
			eops={"width":50}, bops={"width":20})
			
	def addField(self, l, opts={}):
		column, row = self.tk.grid_size()
		label = Label(self.tk)
		label["text"] = l
		label.grid(row=row, column=0, sticky=W, **defGridOps)
		entry = Entry(self.tk, **opts)
		entry.grid(row=row, column=1, sticky=W, columnspan=2, **defGridOps)
		return (label, entry)
		
	def addFileField(self, l, fun, column=None, row=None, bops={}, eops={}):
		defColumn, defRow = self.tk.grid_size()
		if column == None:
			column = defColumn
		if row == None:
			row = defRow
		entry = Entry(self.tk, **eops)
		entry.grid(row=row, column=1, sticky=W, columnspan=2, **defGridOps)
		button = Button(self.tk, text=l, 
			command=lambda l=entry, f=fun: self.showFileName(l, f), **bops)
		button.grid(row=row, column=0, sticky=W, **defGridOps)
		return (entry, button)

	def showFileName(self, entry, fun):
		entry.delete(0,END)
		entry.insert(END, fun())
		return entry.get()
		
	def showNewCmd(self):
		stop = self.stopFileEntry.get()
		end = self.endEntry.get()
		title = self.titleEntry.get()
		cols = self.columnEntry.get()
		start = self.startEntry.get()
		out = self.outFileEntry.get()

		fString = "\"C:/src/Book Schedule/new_schedule.py\" -p \"{0}\" -e {1}"
		if title:
			fString += " -t \"{2}\""
		if cols:
			fString += " -c {3}"
		if start:
			fString += " -s {4}"
		if out:
			fString += " -o \"{5}\""

		cmd = fString.format(stop, end, title, cols, start, out)
		self.status["text"] = cmd
		call(cmd, shell=True)
		
	def showUpdateCmd(self):
		df = self.dataFileEntry.get()
		title = self.titleEntry.get()
		cols = self.columnEntry.get()
		pages = self.pageEntry.get()
		
		fString = "\"C:/src/Book Schedule/update_schedule.py\" -d \"{0}\""
		if title:
			fString += " -t \"{1}\""
		if cols:
			fString += " -c {2}"
		if pages:
			fString += " -p {3}"

		cmd = fString.format(df, title, cols, pages)
		self.status["text"] = cmd
		call(cmd, shell=True)
	
	def showCommand(self):
		print self.message.get()
		self.l["text"] = self.title.get()
		
	def createWidgets(self):
		self.addInputFields()
		self.addButtons()
		nextRow = self.tk.grid_size()[1]
		self.status = Label()
		self.status.grid(row=nextRow, column=0, columnspan=3)

	def __init__(self, master=None):
		self.tk = master
		if (master != None):
			master.title("Book schedule")
		self.createWidgets()
		
root = Tk()

app = Application(master=root)
mainloop()
root.destroy()
