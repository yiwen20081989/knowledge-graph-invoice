# 定义类：df->neo4j
from py2neo import Graph,Node,Relationship,NodeMatcher # 写在类中 初始化函数以上什么情况！！！！
class DataToNeo4j(object): # class 小写
    """将df中数据存入neo4j"""
    def __init__(self,url,username, pwd):
        """建立连接"""
        link = Graph(url,username=username, password=pwd)
        self.graph = link
        # 定义label
        self.buy = 'buy'
        self.sell = 'sell'
        self.graph.delete_all()
        self.matcher = NodeMatcher(link)
    # 节点创建
    def create_node(self,buy_list, sell_list): # 注意self本身
        """创建buy和sell的节点"""
        # 去重
        buy_key = list(set(buy_list))
        sell_key = list(set(sell_list))
        for key in buy_key:
            node = Node('buy' , name = key)
            self.graph.create(node)  # 新的文档似乎需要commit 没看到直接create的例子，但是这样的方法测试有效
        for key in sell_key:
            node = Node('sell' , name = key)
            self.graph.create(node)
    # 关系创建
    def create_relation(self,df_data):
        for m in range(len(df_data.index)):
            try: # matcher 支持where子句查询
                r = Relationship(self.matcher.match("buy", name=df_data.loc[m,'buy']).first(),\
                                df_data.loc[m,'money'],\
                                self.matcher.match("sell", name=df_data.loc[m,'sell']).first())
                self.graph.create(r)
            except AttributeError as e:
                print(e,m)