---
title: SLA de Suporte ao Produto
tenant: fcai
product: fcai-cloud
plan: all
doc_type: sla
version: 2026-01
status: published
visibility: internal
---

# SLA de Suporte ao Produto

Este documento define os níveis de serviço (SLA) do suporte ao **FCAI Cloud**. Ele
descreve as severidades de chamados (P1, P2 e P3), os tempos de resposta por plano, os
canais de atendimento, o processo de escalonamento, as janelas de manutenção, as metas
de disponibilidade, a política de créditos de SLA e as responsabilidades do cliente.
Todos os prazos e valores são fictícios e servem como exemplo para a base de
conhecimento.

## Definições

- **Tempo de resposta:** intervalo entre a abertura do chamado e a primeira resposta
  qualificada de um analista de suporte.
- **Tempo de contorno:** intervalo até a disponibilização de uma solução de contorno
  (workaround) que restabeleça a operação, ainda que temporariamente.
- **Tempo de resolução:** intervalo até a correção definitiva do problema.
- **Horário comercial:** de segunda a sexta, das 9h às 18h (horário de Brasília),
  exceto feriados nacionais.
- **24x7:** atendimento em tempo integral, todos os dias, incluindo finais de semana e
  feriados, aplicável apenas a chamados críticos de clientes Enterprise.

## Severidades

### P1 — Crítico

A severidade **P1** representa indisponibilidade total do serviço ou falha que impede a
ingestão e a visualização de dados para toda a organização. O impacto é grave e não há
contorno viável. Exemplos:

- Painel completamente fora do ar para todos os usuários.
- Ingestão de métricas e logs interrompida em produção.
- Alertas não disparando durante um incidente real.
- Falha de autenticação impedindo o acesso de todos os usuários.

### P2 — Alto

A severidade **P2** representa degradação relevante do serviço, com contorno possível.
O impacto é significativo, mas parte da operação continua funcional. Exemplos:

- Atraso perceptível na ingestão de logs.
- Lentidão em dashboards e consultas.
- Falha em um conector ou integração específica.
- Notificações de alerta chegando com atraso.

### P3 — Baixo

A severidade **P3** representa dúvidas gerais e problemas de baixo impacto, sem prejuízo
relevante à operação. Exemplos:

- Dúvidas de configuração e de uso da plataforma.
- Ajustes cosméticos em dashboards.
- Solicitações de melhoria e esclarecimentos de documentação.
- Perguntas sobre boas práticas de instrumentação.

### Classificação e Reclassificação

A severidade é sugerida pelo cliente na abertura do chamado e validada pelo time de
suporte. Se o impacto real for diferente do informado, o suporte pode reclassificar a
severidade, comunicando o motivo ao cliente. Chamados podem ser rebaixados de P1 para
P2 quando um contorno é aplicado e a operação é parcialmente restabelecida.

## Tempo de Resposta por Plano

### Plano Starter

O plano Starter **não possui SLA de resposta garantido**. O atendimento ocorre via base
de conhecimento e comunidade, sem prazo formal para P1, P2 ou P3.

### Plano Pro

Atendimento em horário comercial, de segunda a sexta-feira:

- **P1:** resposta em até 8 horas úteis.
- **P2:** resposta em até 1 dia útil.
- **P3:** resposta em até 3 dias úteis.

### Plano Enterprise

Atendimento com canal dedicado e cobertura ampliada:

- **P1:** resposta em até 1 hora, com atendimento 24x7.
- **P2:** resposta em até 4 horas úteis.
- **P3:** resposta em até 1 dia útil.

Chamados **P1** e **P2** do Enterprise contam com acompanhamento do gerente de conta.

### Tabela Resumo

| Severidade | Starter | Pro | Enterprise |
| --- | --- | --- | --- |
| P1 | sem SLA | 8 horas úteis | 1 hora (24x7) |
| P2 | sem SLA | 1 dia útil | 4 horas úteis |
| P3 | sem SLA | 3 dias úteis | 1 dia útil |

## Canais de Atendimento

- **Base de conhecimento:** disponível para todos os planos, incluindo o Starter.
- **E-mail de suporte:** suporte@fcai.example.com, para planos Pro e Enterprise.
- **Portal de chamados:** abertura e acompanhamento de tickets para Pro e Enterprise.
- **Canal dedicado:** disponível para Enterprise, com contato direto do time de suporte
  e do gerente de conta.
- **Telefone de emergência:** disponível para chamados P1 do Enterprise, 24x7.

## Processo de Escalonamento

1. O chamado é aberto e classificado por severidade pelo cliente.
2. O time de suporte valida a severidade e inicia o atendimento dentro do SLA.
3. Chamados **P1** são escalonados imediatamente para o time de plantão (on-call).
4. Se o tempo de contorno não for cumprido, o chamado é escalonado para a liderança de
   suporte e, no Enterprise, comunicado ao gerente de conta.
5. Após a resolução, o cliente recebe um resumo do atendimento; para P1, é elaborado um
   relatório de causa raiz (post-mortem).

### Comunicação Durante Incidentes

Durante incidentes P1, a FCAI publica atualizações na central de status e, para o
Enterprise, envia comunicações diretas ao gerente de conta. As atualizações ocorrem em
intervalos regulares até a normalização do serviço.

## Janelas de Manutenção

Manutenções programadas são comunicadas com antecedência mínima de **72 horas** por
e-mail e na central de status. Sempre que possível, ocorrem em janelas de baixo uso.
Manutenções emergenciais podem ocorrer sem aviso prévio em situações críticas de
segurança ou estabilidade, e são comunicadas o mais rápido possível.

## Disponibilidade (Uptime)

A FCAI mantém uma meta de disponibilidade mensal de:

- **99,9%** para o plano **Enterprise**.
- **99,5%** para o plano **Pro** (meta informativa, sem crédito de SLA).
- Sem meta formal para o plano **Starter**.

A disponibilidade é medida mensalmente, excluindo janelas de manutenção programada, e
reportada na central de status.

## Créditos de SLA

Aplicável exclusivamente ao plano **Enterprise**. Caso a disponibilidade mensal fique
abaixo da meta contratada, o cliente pode solicitar crédito na fatura seguinte,
conforme a tabela fictícia:

- Disponibilidade entre 99,0% e 99,9%: crédito de 5% da mensalidade proporcional.
- Disponibilidade entre 98,0% e 99,0%: crédito de 10%.
- Disponibilidade abaixo de 98,0%: crédito de 20%.

A solicitação de crédito deve ser feita em até 30 dias após o mês de referência. O
crédito não é convertido em reembolso em dinheiro e não se acumula entre meses.

### Exclusões do SLA

Não contam como indisponibilidade para fins de crédito:

- Janelas de manutenção programada comunicadas com antecedência.
- Problemas causados por configuração incorreta do cliente.
- Falhas em ambientes ou integrações fora do controle da FCAI.
- Uso da plataforma fora dos limites do plano contratado.

## Responsabilidades do Cliente

Para que o SLA seja aplicável, o cliente deve:

- Classificar corretamente a severidade dos chamados.
- Fornecer informações suficientes para reprodução do problema.
- Manter os agentes de coleta e SDKs em versões suportadas.
- Utilizar a plataforma conforme os termos de uso e os limites do plano contratado.
- Manter os contatos de suporte e financeiro atualizados no painel.

## Perguntas Frequentes

**Qual é o tempo de resposta para P1 no Enterprise?**
Até 1 hora, com atendimento 24x7.

**O plano Starter tem SLA?**
Não. O Starter é atendido pela comunidade e base de conhecimento, sem prazo garantido.

**Como funciona o crédito de SLA?**
É aplicável ao Enterprise quando a disponibilidade fica abaixo da meta, como desconto na
fatura seguinte, mediante solicitação em até 30 dias.

**Posso reclassificar a severidade de um chamado?**
Sim. A severidade pode ser ajustada pelo suporte conforme o impacto real, com
comunicação do motivo.
