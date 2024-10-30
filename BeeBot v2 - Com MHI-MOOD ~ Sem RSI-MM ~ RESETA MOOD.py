import time
from iqoptionapi.stable_api import IQ_Option
from datetime import datetime
import logging

logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',
                    filename='beebot.log', level=logging.INFO)

Iq = IQ_Option("EMAIL", "SENHA")
Iq.connect()

goal = "EURJPY"
money = 200
resetmoney = 200
balance_type = "PRACTICE"
Iq.change_balance(balance_type)
initialmoney = Iq.get_balance()
soros = 0
martingales = 0

fechamento5m = {
    "compra": int(0),
    "venda": int(0)
}

fechamento1m = {
    "compra": int(0),
    "venda": int(0)
}

fechamento30s = {
    "compra": int(0),
    "venda": int(0)
}

historico = {
    "ganho": int(0),
    "perda": int(0),
    "empate": int(0)
}

callorput = []


def CompraOuVenda5m():
    candle = Iq.get_candles(goal, 300, 5, time.time())
    for i in candle:
        if i['open'] < i['close']:
            fechamento5m['compra'] = fechamento5m['compra'] + 1
        else:
            fechamento5m['venda'] = fechamento5m['venda'] + 1
    Iq.start_mood_stream(goal)
    mood = Iq.get_traders_mood(goal)
    logging.info("Mood: " + str(mood))
    logging.info(candle)
    Iq.stop_mood_stream(goal)
    if mood > 0.5:
        conta1 = fechamento5m['compra'] * (mood * 2)
        conta2 = fechamento5m['venda'] * ((1 - mood) * 2)
        if conta1 > conta2:
            callorput.append("call")
        else:
            callorput.append("put")
    else:
        conta1 = fechamento5m['venda'] * ((1 - mood) * 2)
        conta2 = fechamento5m['compra'] * (mood * 2)
        if conta1 > conta2:
            callorput.append("put")
        else:
            callorput.append("call")

    fechamento5m['compra'] = 0
    fechamento5m['venda'] = 0


def CompraOuVenda1m():
    candle = Iq.get_candles(goal, 60, 5, time.time())
    for i in candle:
        if i['open'] < i['close']:
            fechamento1m['compra'] = fechamento1m['compra'] + 1
        else:
            fechamento1m['venda'] = fechamento1m['venda'] + 1
    Iq.start_mood_stream(goal)
    mood = Iq.get_traders_mood(goal)
    logging.info("Mood: " + str(mood))
    logging.info(candle)
    Iq.stop_mood_stream(goal)
    if mood > 0.5:
        conta1 = fechamento1m['compra'] * (mood * 2)
        conta2 = fechamento1m['venda'] * ((1 - mood) * 2)
        if conta1 > conta2:
            callorput.append("call")
        else:
            callorput.append("put")
    else:
        conta1 = fechamento1m['venda'] * ((1 - mood) * 2)
        conta2 = fechamento1m['compra'] * (mood * 2)
        if conta1 > conta2:
            callorput.append("put")
        else:
            callorput.append("call")

    fechamento1m['compra'] = 0
    fechamento1m['venda'] = 0


def CompraOuVenda30s():
    candle = Iq.get_candles(goal, 30, 5, time.time())
    for i in candle:
        if i['open'] < i['close']:
            fechamento30s['compra'] = fechamento30s['compra'] + 1
        else:
            fechamento30s['venda'] = fechamento30s['venda'] + 1
    Iq.start_mood_stream(goal)
    mood = Iq.get_traders_mood(goal)
    logging.info("Mood: " + str(mood))
    logging.info(candle)
    Iq.stop_mood_stream(goal)
    if mood > 0.5:
        conta1 = fechamento30s['compra'] * (mood * 2)
        conta2 = fechamento30s['venda'] * ((1 - mood) * 2)
        if conta1 > conta2:
            callorput.append("call")
        else:
            callorput.append("put")
    else:
        conta1 = fechamento30s['venda'] * ((1 - mood) * 2)
        conta2 = fechamento30s['compra'] * (mood * 2)
        if conta1 > conta2:
            callorput.append("put")
        else:
            callorput.append("call")

    fechamento30s['compra'] = 0
    fechamento30s['venda'] = 0


while True:
    minute = datetime.now().minute
    atualmoney = Iq.get_balance()
    if (minute + 1) % 5 == 0:
        Id = 0
        winorlose = ''
        print("\n")
        time.sleep(31)
        saldoEntrada = Iq.get_balance()
        CompraOuVenda30s()
        CompraOuVenda1m()
        CompraOuVenda5m()
        result1 = callorput.count("call")
        result2 = callorput.count("put")
        print("Call: " + str(result1) + " Put: " + str(result2))
        logging.info("Call: " + str(result1) + " Put: " + str(result2))
        callorput.clear()
        if soros >= 2:
            money = resetmoney
            soros = 0
        print("Aposta atual: " + str(money) + " Reais")
        if result1 > result2:
            print("Compra")
            check, iD = Iq.buy(money, goal, "call", 1)
            print(check, iD)
            if not check:
                print("Erro ao comprar")
                break
            winorlose = Iq.check_win_v4(iD)
        else:
            print("Venda")
            check, iD = Iq.buy(money, goal, "put", 1)
            print(check, iD)
            if not check:
                print("Erro ao comprar")
                break
            winorlose = Iq.check_win_v4(iD)
        saldoFechamento = Iq.get_balance()
        # *                                                                 WIN(saldoEntrada < saldoFechamento)
        if winorlose[0] == 'win':
            print("Money Inicial: " + str(initialmoney) + " Reais")
            print("Money Atual: " + str(saldoFechamento) + " Reais")
            if saldoFechamento > saldoEntrada + 20:
                break
            if martingales > 0:
                money = resetmoney
                martingales = 0
                soros = 0
            else:
                money = money + (saldoFechamento - saldoEntrada)
                soros = soros + 1
            logging.info("Win - " + "Soros: " + str(soros) +
                         " Martingales: " + str(martingales))
            print("Win - " + "Soros: " + str(soros) +
                  " Martingales: " + str(martingales))
            historico['ganho'] = historico['ganho'] + 1
        # *                                                                 WIN(saldoEntrada < saldoFechamento)

        # ?                                                                 EMPATE(saldoEntrada == saldoFechamento)
        elif saldoEntrada == saldoFechamento:
            historico['empate'] = historico['empate'] + 1
        # ?                                                                 EMPATE(saldoEntrada == saldoFechamento)

        # !!                                                                LOSE(saldoEntrada > saldoFechamento)
        else:
            print("Money Inicial: " + str(initialmoney) + " Reais")
            print("Money Atual: " + str(saldoFechamento) + " Reais")
            if soros > 0:
                money = resetmoney
                soros = 0
            if martingales > 4:
                money = resetmoney
                martingales = 0
                break
            else:
                soros = 0
                money = money + (saldoEntrada - saldoFechamento)
                martingales = martingales + 1
            logging.info("Lose - " +
                         "Soros: " + str(soros) + " Martingales: " + str(martingales))
            print("Lose - " + "Martingales: " +
                  str(martingales) + " Soros: " + str(soros))
            historico['perda'] = historico['perda'] + 1
        winorlose = ''
        logging.info(historico)
        print(winorlose)
        print(historico)
        print("\n")
        # !!                                                                 LOSE(saldoEntrada > saldoFechamento)
