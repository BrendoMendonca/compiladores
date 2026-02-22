
def avaliar(no):
    if isinstance(no, Const):
        return no.valor
    
    if isinstance(no, OpBin):
        esq = avaliar(no.opEsq)
        dir = avaliar(no.opDir)
        
        if no.operador == '+': return esq + dir
        if no.operador == '-': return esq - dir
        if no.operador == '*': return esq * dir
        if no.operador == '/':
            if dir == 0: raise ZeroDivisionError("Divisão por zero")
            return esq // dir