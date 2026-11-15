from .records import number

def fund_graph(book,as_of):
    funds={r['id'] for r in book.rows('fund',as_of)}
    securities={r['id'] for r in book.rows('security',as_of)}
    graph={f:[] for f in funds}
    for row in book.rows('holding',as_of):
        d=row['data'];w=number(d['weight'])
        if d['fund'] not in funds or d['target'] not in funds|securities|{'cash'} or w<0:
            raise ValueError('基金成分非法')
        graph[d['fund']].append((d['target'],w,row['id']))
    for fund,edges in graph.items():
        if sum((w for _,w,_ in edges),number(0))>1:raise ValueError('基金成分超过净资产')
    return graph

def currency_rate(book,as_of,currency,day):
    found=[r for r in book.rows('fx',as_of) if r['data']['currency']==currency and r['data']['day']==day]
    if len(found)!=1:raise ValueError('估值日汇率缺失或冲突')
    value=number(found[0]['data']['value'])
    if value<=0:raise ValueError('汇率须为正')
    return value
