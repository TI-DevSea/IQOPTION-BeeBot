# BeeBot v2 - Bot de Trading IQ Option

## 📋 Descrição

Bot automatizado para operações na IQ Option que utiliza análise multi-timeframe (MHI) combinada com análise de humor do mercado (Market Mood) para tomar decisões de trading.

## 🔧 Requisitos de Sistema

- Python 3.6 ou superior
- Biblioteca iqoptionapi
- Conexão estável com a internet
- Conta na IQ Option

## ⚙️ Instalação

1. Clone o repositório
2. Instale as dependências:

```bash
pip install iqoptionapi datetime
```

## 🚀 Configuração

Edite as seguintes variáveis no arquivo principal:

- `email`: Seu email da IQ Option
- `senha`: Sua senha da IQ Option
- `goal`: Par de moedas (padrão: "EURJPY")
- `money`: Valor inicial da aposta (padrão: 2)
- `balance_type`: Tipo de conta ("PRACTICE" ou "REAL")

## 💡 Funcionalidades

### Análise Multi-Timeframe

- Análise de velas em 3 timeframes:
  - 5 minutos
  - 1 minuto
  - 30 segundos

### Gerenciamento de Risco

- Sistema Soros até 2 níveis
- Sistema Martingale até 4 níveis
- Stop gain automático (+20 unidades monetárias)
- Reset de valores após sequências

### Análise de Mercado

- Integração com Market Mood
- Análise de tendência por timeframe
- Confirmação multi-período

### Logging e Monitoramento

- Log automático de operações
- Histórico de ganhos/perdas
- Acompanhamento de saldo

## 📊 Parâmetros Configuráveis

| Parâmetro   | Descrição                    | Valor Padrão |
| ----------- | ---------------------------- | ------------ |
| money       | Valor inicial da aposta      | 2            |
| resetmoney  | Valor para reset             | 2            |
| martingales | Número máximo de martingales | 4            |
| soros       | Número máximo de soros       | 2            |

## ⚠️ Avisos Importantes

1. **Risco**: Trading envolve risco de perda de capital
2. **Teste**: Sempre teste primeiro em conta demo
3. **Segurança**: Nunca compartilhe suas credenciais
4. **Conexão**: Necessária conexão estável com a internet

## 🔍 Funcionamento do Bot

### Estratégia de Entrada

1. Analisa velas em 3 timeframes diferentes
2. Verifica o humor do mercado (Market Mood)
3. Combina as análises para decisão final
4. Executa entrada quando há confirmação

### Gerenciamento Monetário

- Soros: Aumenta posição após ganhos
- Martingale: Aumenta posição após perdas
- Stop: Para operações após lucro definido

## 📝 Logs

O bot gera logs detalhados em `beebot.log` contendo:

- Horário das operações
- Resultados (Win/Loss)
- Níveis de Soros e Martingale
- Humor do mercado

## 🤝 Contribuição

Sinta-se livre para contribuir com o projeto através de:

- Reporte de bugs
- Sugestões de melhorias
- Pull requests

## 📫 Suporte

Para suporte, abra uma issue no repositório ou entre em contato.

## 📜 Licença

Este projeto está sob licença MIT.
