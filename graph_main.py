# 1.导包
import pandas as pd
from df_neo4j import DataToNeo4j
# 2.1数据获取及基本处理
def data_extraction(file):
    """
    节点数据抽取
    """
    # buy_list,money_list,sell_list
    buy_list = []
    money_list = []
    sell_list = []
    # 读取源数据并遍历
    source = pd.read_excel(file)
    for i in range(len(source.index)):
        buy_list.append(source.iloc[i, 6]) # 提取发票买方名称
        money_list.append(source.iloc[i, 19]) # 提取发票金额档次
        sell_list.append(source.iloc[i, 10]) # 提取发票卖方名称
    # 将数据中int类型全部转成string
    sell_list = [str(i) for i in sell_list]
    buy_list = [str(i) for i in buy_list]
    money_list = [str(i) for i in money_list]
        
    data_extractor = {} # dict() 也可以
    data_extractor['buy'] = buy_list
    data_extractor['money'] = money_list
    data_extractor['sell'] = sell_list
    df_extractor = pd.DataFrame(data_extractor) # DataFrame F 大写
    return df_extractor

# __main__
file = 'Invoice_data_Demo.xls'
# 1.从数据源提取数据，返回df
data = data_extraction(file)
print(data.head())
# 2.创建图
url = "bolt://localhost:7687"
username = "neo4j" # 修改neo4j数据库用户名
pwd = "neo4jXXXXX" # 修改neo4j数据库密码
create_graph = DataToNeo4j(url,username, pwd)
# 节点创建
create_graph.create_node(data['buy'].tolist(), data['sell'].tolist())
# 关系创建 
create_graph.create_relation(data)  
