import os
from tkinter import *

class AttributeRow(Frame):
    def __init__(self, master, attributeName, inputType, recallFunction, options=None):
        super().__init__(master, bg="#111111")
        self.pack(fill="x", pady=2)
        
        self.nameLabel = Label(self, text=attributeName, bg="#111111", fg="white")
        self.nameLabel.pack(side="left", padx=5)
        
        self.inputType = inputType
        self.recallFunction = recallFunction
        self.lastValue = None
        
        if inputType.lower() == "string":
            self.inputWidget = Entry(self, bg="#333333", fg="white", insertbackground="white")
            self.inputWidget.pack(side="right", expand=True, fill="x", padx=5)
            self.inputWidget.bind("<FocusOut>", self.checkChange)
            self.inputWidget.bind("<Return>", self.checkChange)
            
        elif inputType.lower() == "integer":
            self.inputWidget = Spinbox(self, from_=0, to=100, bg="#333333", fg="white", buttonbackground="#222222")
            self.inputWidget.pack(side="right", expand=True, fill="x", padx=5)
            self.inputWidget.config(command=lambda: self.checkChange(None))
            self.inputWidget.bind("<FocusOut>", self.checkChange)
            self.inputWidget.bind("<Return>", self.checkChange)

        elif inputType.lower() == "float":
            self.inputWidget = Spinbox(self, from_=0.0, to=100.0, increment=0.1, bg="#333333", fg="white", buttonbackground="#222222")
            self.inputWidget.pack(side="right", expand=True, fill="x", padx=5)
            self.inputWidget.config(command=lambda: self.checkChange(None))
            self.inputWidget.bind("<FocusOut>", self.checkChange)
            self.inputWidget.bind("<Return>", self.checkChange)
            
        elif inputType.lower() == "boolean":
            self.inputWidget = BooleanVar(value=False)
            self.checkButton = Checkbutton(self, variable=self.inputWidget, bg="#111111", activebackground="#111111", onvalue=True, offvalue=False)
            self.checkButton.pack(side="right", padx=5)
            self.checkButton.config(command=lambda: self.checkChange(None))
            
        else:
            self.inputWidget = Label(self, text="[Unknown Type]", bg="#111111", fg="red")
            self.inputWidget.pack(side="right", padx=5)
            
        self.lastValue = self.getWidgetValue()

    def getWidgetValue(self):
        if not hasattr(self, 'inputWidget') or self.inputWidget is None:
            return ""
            
        if isinstance(self.inputWidget, BooleanVar):
            return bool(self.inputWidget.get())
            
        if hasattr(self.inputWidget, 'get'):
            raw_value = self.inputWidget.get()
            
            if self.inputType.lower() == "integer":
                try:
                    return int(raw_value)
                except ValueError:
                    return int(self.lastValue) if isinstance(self.lastValue, int) else 0

            elif self.inputType.lower() == "float":
                try:
                    return round(float(raw_value), 2)
                except ValueError:
                    return float(self.lastValue) if isinstance(self.lastValue, (int, float)) else 0.0
                    
            elif self.inputType.lower() == "string":
                return str(raw_value)
                
        return ""

    def checkChange(self, event=None):
        currentValue = self.getWidgetValue()
        
        if self.inputType.lower() in ["integer", "float"] and hasattr(self.inputWidget, 'delete'):
            if str(currentValue) != self.inputWidget.get():
                self.setValue(currentValue, trigger_recall=False)

        if currentValue != self.lastValue:
            self.lastValue = currentValue
            self.recallFunction(currentValue)

    def setValue(self, value, trigger_recall=True):
        if not hasattr(self, 'inputWidget'):
            return

        if self.inputType.lower() == "boolean" and isinstance(self.inputWidget, BooleanVar):
            self.inputWidget.set(bool(value))
            
        elif self.inputType.lower() in ["string", "integer", "float"] and hasattr(self.inputWidget, 'delete'):
            self.inputWidget.delete(0, "end")
            self.inputWidget.insert(0, str(value))
            
        self.lastValue = self.getWidgetValue()
        
        if trigger_recall:
            self.recallFunction(self.lastValue)

class CategoryPanel(Frame):
    def __init__(self, master=None, title="Category"):
        super().__init__(master, bg="#111111")
        self.pack(fill="x", padx=2, pady=2)
        
        self.headerFrame = Frame(self, bg="#222222")
        self.headerFrame.pack(fill="x", expand=True)
        self.titleLabel = Label(self.headerFrame, text=title, bg="#222222", fg="white", font=("Arial", 10, "bold"))
        self.titleLabel.pack(side="left", padx=2, pady=2)
        
        self.isCollapsed = False
        self.collapseBtn = Button(self.headerFrame, text="▲", width=3, command=self.toggleCollapse, bg="#333333", fg="white", relief="flat")
        self.collapseBtn.pack(side="right", padx=2, pady=2)
        
        self.contentFrame = Frame(self, bg="#111111")
        self.contentFrame.pack(fill="both", expand=True, padx=2, pady=2)
        
        self.attributes = {}

    def toggleCollapse(self):
        if self.isCollapsed:
            self.contentFrame.pack(fill="both", expand=True, padx=2, pady=2)
            self.collapseBtn.config(text="▲")
            self.isCollapsed = False
        else:
            self.contentFrame.pack_forget()
            self.collapseBtn.config(text="▼")
            self.isCollapsed = True

    def addAttribute(self, attributeName, inputType, recallFunction):
        attributeInstance = AttributeRow(self.contentFrame, attributeName, inputType, recallFunction)
        self.attributes[attributeName] = attributeInstance
        return attributeInstance

    def clearAttributes(self):
        for attributeInstance in self.attributes.values():
            attributeInstance.destroy()
        self.attributes.clear()

class AttributePanel(Frame):
    def __init__(self, master=None, *args, **kwargs):
        super().__init__(master, bg="#111111", *args, **kwargs)
        self.titleLabel = Label(self, text='Attribute Panel', bg="#111111", fg="white", font=("Arial", 14, "bold"))
        self.titleLabel.pack(anchor="w", pady=5)
        self.pack_propagate(False)
        
        self.categories = {}

    def setTitle(self, title):
        self.titleLabel.config(text=title)

    def addCategory(self, categoryName):
        self.categories[categoryName] = CategoryPanel(self, title=categoryName)
        return self.categories[categoryName]

    def clearCategories(self):
        for categoryPanel in self.categories.values():
            categoryPanel.destroy()
        self.categories.clear()

if __name__ == "__main__":
    root = Tk()
    root.title("Attribute Test")
    root.geometry("400x400")
    root.configure(bg="#111111")
    
    panel = AttributePanel(root)
    panel.setTitle("Engine Settings")
    panel.pack(fill="both", expand=True, padx=2, pady=2)
    cat1 = panel.addCategory("Graphics")
    cat1.addAttribute("Resolution", "string", print)
    cat1.addAttribute("Anti-Aliasing", "boolean", print)
    
    cat2 = panel.addCategory("Audio")
    cat2.addAttribute("Master Volume", "integer", print)
    cat2.addAttribute("Volume Factor", "float", print)
    
    root.mainloop()