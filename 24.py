from fractions import Fraction
import json


class Number(object):
    """整数类"""

    def __init__(self, num, expr=None):
        super(Number, self).__init__()
        self.num = num
        self.expr = expr


class Operate(object):
    """运算类"""

    def __init__(self, oper, func):
        super(Operate, self).__init__()
        self.oper = oper
        self.func = func

    def cal(self, NumA, NumB):
        # 计算
        strA = NumA.num if NumA.expr is None else NumA.expr
        strB = NumB.num if NumB.expr is None else NumB.expr
        return Number(self.func(NumA.num, NumB.num), '(%s %s %s)' % (strA, self.oper, strB))


def find(num, op):
    # 寻找计算方式
    result = None
    l = len(num)
    if l < 2:
        return result
    elif l == 2:
        for k in op:
            r = k.cal(num[0], num[1])
            if r.num == 24:
                result = r.expr
                break
            if num[0] == num[1]:
                continue
            r = k.cal(num[1], num[0])
            if r.num == 24:
                result = r.expr
                break
        return result
    for i in range(l):
        for j in range(i + 1, l):
            for k in op:
                r = k.cal(num[i], num[j])
                num1 = num.copy()
                num1.pop(j)
                num1.pop(i)
                if r.num is not None:
                    num1.append(r)
                    result = find(num1, op)
                    if result is not None:
                        return result
                    num1.pop(-1)
                if num[i] == num[j]:
                    continue
                r = k.cal(num[j], num[i])
                if r.num is not None:
                    num1.append(r)
                    result = find(num1, op)
                    if result is not None:
                        return result
    return result


if __name__ == '__main__':
    pl = Operate('+', lambda x, y: x + y)
    mi = Operate('-', lambda x, y: x - y)
    mu = Operate('*', lambda x, y: x * y)
    di = Operate('/', lambda x, y: None if y == 0 else Fraction(x, y))
    op = [pl, mi, mu, di]
    """
    # 计算例子
    num = [Number(6), Number(6), Number(8), Number(8)]
    print(find(num, op))

    data = []
    l = 14
    # 扑克中不可计算
    for i0 in range(1, l):
        print(i0)
        for i1 in range(i0, l):
            for i2 in range(i1, l):
                for i3 in range(i2, l):
                    r = find([Number(i0), Number(i1), Number(i2), Number(i3)], op)
                    if r is None:
                        data.append((i0, i1, i2, i3))
    print(len(data))  # 4则运算 458组
    with open('uncal.json', 'w') as w:
        json.dump(data, w)
    """
    data7 = []
    with open('uncal.json', 'r') as r:
        uncal = json.load(r)
    mo = Operate('%', lambda x, y: None if y == 0 else x % y)
    dv = Operate('//', lambda x, y: None if y == 0 else x // y)

    def _po(x, y):
        if type(y) is Fraction:
            return None
        else:
            if y > 0:
                z = pow(x, y)
                if abs(z) > 100000:
                    # 太大了就别pow了
                    return None
                else:
                    return z
            elif y == 0:
                return 1
            else:
                if x == 0:
                    return None
                else:
                    z = pow(x, -y)
                    if abs(z) > 100000:
                        # 太大了就别pow了
                        return None
                    else:
                        return Fraction(1, z)
    po = Operate('^', _po)
    op7 = [pl, mi, mu, di, mo, dv, po]
    for d in uncal:
        r = find([Number(d[0]), Number(d[1]), Number(d[2]), Number(d[3])], op7)
        if r is None:
            data7.append(d)
        else:
            print(r)
    print(len(data7))  # 7则运算 126组
    with open('uncal7.json', 'w') as w:
        json.dump(data7, w)
