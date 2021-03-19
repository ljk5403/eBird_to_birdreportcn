#!/usr/bin/env python3
import pandas as pd
import sys
import code

r=sys.argv[1]
#显示所有列
pd.set_option('display.max_columns', None)
#显示所有行
pd.set_option('display.max_rows', None)
a=pd.read_excel(r)
print(a)

code.interact(local=locals())