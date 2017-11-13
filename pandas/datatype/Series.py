import pandas as pd
import numpy as np

data = pd.Series(np.arange(10),index=np.arange(10,20))
print(data)
print(data.values[1:5])