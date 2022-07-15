class Category:
  """@AUTHOR Cheryl Vadivello.
  
  This class is part of a budget app which instantiates object
  of different budget categories such as food,entertainment etc.
  It keeps tracks of all deposits and withdrawals in a ledger which 
  it then returns as a string."""

  def __init__(self,name=""):
    """Attributes
       ----------
    name : str, the budget category name
    ledger : dict, records all transactions
    balance : int, records the actual total of the category"""
    
    self.name = name
    self.ledger = []
    self.balance = 0
    
  def ledgerFormat(self,amount, description):
    self.ledger.append({"amount": amount,"description": description})
  
  def check_funds(self,amount):
    if amount > self.balance:
      return False
    else:
      return True
    
  def deposit(self, amount, description=""):
    self.ledgerFormat(amount, description)
    self.balance += amount
    
  def withdraw(self, amount, description=""):
    if self.check_funds(amount) :
      a = -amount
      self.ledgerFormat(a, description)
      self.balance -= amount
      return True
    
    return False

  def get_balance(self):
    return self.balance

  def transfer(self, amount, other) :
    if self.check_funds(amount) :
      description = "Transfer to " + other.name
      self.withdraw(amount,description)
      description = "Transfer from " + self.name
      other.deposit(amount,description)
      return True
    
    return False

  def __str__(self) :
    """Provides a visual interpretation of the category, displaying
    deposits and withdrawals along with their corresponding descriptions.
    Displays the current balance."""
    
    title = self.name.center(30,"*") + "\n"  #Restricts the line to 30 characters
    body = self.ledgerItems()
    total = "\n" + "Total: " + f'{self.balance:.2f}'
    printObject = title + body + total
    return printObject

  def ledgerItems(self) :
    """Raises exception if the length of the recorded ledger
    amount is greater than 7 characters. Returns the ledger as
    a string."""
    
    ledger = []
    for item in self.ledger:
      amount,description = item.values()
      a = description[:23]
      b = f'{amount:.2f}'
      try:
        len(b)<= 7
      except:
        raise Exception("Uh Oh!")
      finally:
        space = " "*(30 - (len(a) + len(b)))
        toAdd = f'{a + space + b}'
        ledger.append(toAdd)
        
    return '\n'.join(ledger)  


  
def create_spend_chart(categories):
  """This function returns a barchart of percentage spent 
  per category as a string, when a list of Category 
  instances are passed to it."""
  
  spent= []
  percent_to_nearest10 = []
  percent_display = []
  percent = []
  names = []
  
  for x in range(100,-10,-10):
   percent.append(x)
   s = str(x) + "| "
   if x==100:
     percent_display.append(s)
   elif x==0:
     percent_display.append(" "*2 + s)
   else:
       percent_display.append(" " + s) 
       
  for category in categories:
    a = []
    name = category.name
    names.append(name)
    for num in category.ledger:
       if num['amount'] < 0:
         a.append(num['amount'])
    total = round(sum(a),2)
    spent.append(total)
  
  j = sum(spent)
  
  for i in spent: #Rounds percentage spent to nearest 10
    x = round((i/j * 100),2)
    x10 = round(x/10)*10
    percent_to_nearest10.append(x10)
    
  n10_barchart_display = [[] for x in range(len(percent_to_nearest10))]
  for i in percent_to_nearest10:
    c= percent_to_nearest10.index(i)
    while i >= 0:
      n10_barchart_display[c].append(i)
      i-= 10

  chart = "Percentage spent by category\n"
  spacing = len(categories) + (2*len(categories))
  divline = " "*4 + "-"*(spacing+1) + "\n"

  i = 0
  for pd in percent_display:
    chart+= pd
    exist,flag = check(percent_to_nearest10, percent[i],n10_barchart_display)
    if not exist and not flag:
      chart+= " "*spacing +'\n'
      if i < len(percent)-1:
        i+= 1
      continue
    else:
      for p in percent_to_nearest10:
        a = percent_to_nearest10.index(p)
        if p == percent[i] or percent[i] in n10_barchart_display[a]:
          chart+= "o  "
        else:
          chart+= " "*3
        if a == len(percent_to_nearest10) - 1:
          i+=1
          chart+= "\n"
          
  chart+= divline + " "*5   
   
  longest = max(names,key=len)
  i = len(longest)
  
  for x in range(i):
    for name in names:
      try:
        character = name[x]
        chart+= character + " "*2
      except:
        chart+= " "*3
      if names.index(name) == len(names)-1 and x<i-1:
        chart+= "\n" + " "*5

  return chart

def check(aList,num,bList)  :
  """Returns boolean values to show whether a given number
  is an item of given lists."""
  
  exist = num in aList
  flag = False
  for i in range(len(bList)):
    flag = num in bList[i]
    if flag:
      break
  
  return exist,flag
  