import pandas as pd
import numpy as np
file = 'recursos/Tableros2.xlsx'
def read_file(n):

  sheet_name = "N="+str(n)
  
  table = pd.read_excel(file, sheet_name=sheet_name, header=None)
  table = table.to_numpy()

  positions = list()

  id = 1

  for row , v in np.ndenumerate(table):
    my_list= list(row)

    if(v == 'x' or v == 'X'):        
      my_list.append(id)
      id = id + 1
    else:
      my_list.append(0)

    positions.append(my_list)    
  
  return positions

if (__name__ == "__main__"):
  init = read_file(4)
