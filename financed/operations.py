from .model import fund_graph,currency_rate
from .records import number

def direct_positions(book,as_of):
    securities={r['id']:r['data'] for r in book.rows('security',as_of)}
    funds=fund_graph(book,as_of);details=[]
    for row in book.rows('position',as_of):
        d=row['data'];target=d['target']
        if target not in securities and target not in funds:raise ValueError('未知头寸标的')
        amount=number(d['amount'])*currency_rate(book,as_of,d['currency'],d['day'])
        details.append({'position':row['id'],'target':target,'value':amount,
                        'kind':'security' if target in securities else 'fund'})
    return details

def disclosure(book,as_of):
    graph=fund_graph(book,as_of)
    return {fund:{'disclosed':sum((w for _,w,_ in edges),number(0)),
                  'undisclosed':1-sum((w for _,w,_ in edges),number(0)),
                  'direct_funds':[t for t,_,_ in edges if t in graph]} for fund,edges in sorted(graph.items())}

def describe(book,as_of):
    return {'direct_positions':direct_positions(book,as_of),'fund_disclosure':disclosure(book,as_of)}
