import pandas as pd
import numpy as np


date = pd.date_range('20171113', periods=7)
print(date)
date2 = pd.DataFrame(np.random.randint(1,7),index=date,columns=["星期一","星期二","星期三","星期四","星期五","星期六","星期天"])
print(date2)
date2.drop("星期一", axis=1)
# date2.drop(0,axis=0)
date2.rename="课表"
print(date2)
date2.head(2)
date2.tail(1)
print(date2.describe())
print(date2.T)
