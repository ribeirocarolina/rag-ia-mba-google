---
title: Política de Faturamento
tenant: fcai
product: fcai-cloud
plan: all
doc_type: policy
version: 2026-01
status: published
visibility: internal
---

# Política de Faturamento

Este documento descreve as formas de pagamento do **FCAI Cloud**, os ciclos de
cobrança, a cobrança por consumo excedente, a emissão de notas fiscais, o tratamento de
falhas de cobrança, o processo de regularização de acesso, a retenção de dados após
suspensão e as regras de reembolso. Todos os valores e prazos são fictícios e servem
como exemplo.

## Princípios de Faturamento

- Cobrança previsível, com valores e ciclos claros antes da contratação.
- Notificação de consumo antes de qualquer cobrança de excedente.
- Preservação de dados e configurações durante o período de regularização.
- Restabelecimento automático do acesso após a quitação de pendências.

## Formas de Pagamento

### Cartão de Crédito

O plano **Pro** é cobrado por cartão de crédito de forma recorrente, mensal ou anual. A
confirmação da cobrança é imediata, e o acesso permanece ativo enquanto o pagamento for
aprovado. O cliente pode atualizar os dados do cartão a qualquer momento no painel de
faturamento. Recomenda-se manter um cartão de backup para evitar interrupções.

### Boleto Bancário

Empresas podem optar por **boleto** em contratações anuais. Regras principais:

- A compensação do boleto pode levar até **3 dias úteis**.
- A emissão de um novo ciclo depende da confirmação do pagamento anterior.
- Boletos vencidos precisam ser reemitidos no portal de faturamento.

### Pagamento Corporativo (Enterprise)

No plano **Enterprise**, o pagamento é feito de forma corporativa, com faturamento por
contrato. As condições incluem:

- Emissão de nota fiscal conforme o acordo comercial.
- Prazos de pagamento negociados (por exemplo, 15, 30 ou 45 dias).
- Possibilidade de faturamento por centro de custo ou por unidade de negócio.
- Envio das faturas para os contatos financeiros cadastrados.

## Ciclos de Cobrança

- **Mensal:** a cobrança ocorre na data de aniversário da assinatura, a cada mês.
- **Anual:** a cobrança ocorre uma vez a cada 12 meses, com desconto em relação ao
  mensal.
- **Enterprise:** o ciclo é definido em contrato, podendo ser mensal, trimestral ou
  anual.

A data de início do ciclo é a data de ativação do plano pago. Alterações de plano
podem gerar cobrança proporcional (pro rata), conforme a política comercial.

## Cobrança por Consumo Excedente

Nos planos **Pro** e **Enterprise**, o volume de ingestão que ultrapassar o limite do
plano é cobrado como **consumo excedente**:

- O excedente é medido por **GB** de ingestão, no fechamento de cada ciclo.
- O painel de uso mostra o consumo atual e projeta o excedente estimado do ciclo.
- Notificações são enviadas ao atingir **80%** e **100%** da cota do plano.
- No **Enterprise**, as regras e os valores de excedente seguem o contrato.

O consumo excedente já faturado não é reembolsável. É possível definir alertas de
consumo para evitar surpresas na fatura.

### Exemplo de Cálculo (fictício)

Se o plano Pro inclui 100 GB de ingestão de logs e a organização consome 130 GB no
ciclo, os 30 GB adicionais são cobrados como excedente, conforme o preço por GB vigente,
no fechamento do ciclo.

## Impostos e Notas Fiscais

- Os preços divulgados podem não incluir impostos, que são aplicados conforme a
  legislação vigente e o endereço de cobrança.
- A **nota fiscal** é emitida a cada cobrança e disponibilizada no portal de
  faturamento.
- Clientes corporativos podem configurar dados fiscais específicos, como razão social,
  CNPJ e endereço de faturamento.
- Ajustes de dados fiscais devem ser feitos antes do fechamento do ciclo para constar
  na nota daquele período.

## Falha de Cobrança

Em caso de falha na cobrança — por recusa do cartão, boleto não pago ou fatura
corporativa em atraso — a FCAI adota o seguinte fluxo fictício:

1. **Notificação:** o responsável financeiro é notificado por e-mail sobre a falha.
2. **Reprocessamento:** cobranças por cartão são reprocessadas automaticamente por até
   **3 tentativas**, em intervalos de alguns dias.
3. **Período de tolerância:** a conta permanece ativa durante um período de tolerância
   para regularização.
4. **Restrição de acesso:** persistindo a inadimplência, a conta entra em modo restrito.

## Modo Restrito e Suspensão

Durante a pendência financeira, a conta pode entrar em **modo restrito**, com:

- Ingestão de novos dados **suspensa**.
- Acesso **somente leitura** aos dados ainda retidos.
- Alertas e integrações pausados.

Se a pendência não for resolvida dentro do prazo, a conta pode ser **suspensa** e, após
prazo adicional, os dados podem ser removidos conforme a política de retenção.

### Linha do Tempo (fictícia)

- **Dia 0:** falha de cobrança e notificação.
- **Dias 1 a 7:** período de tolerância, conta ativa.
- **Dia 8:** modo restrito, ingestão suspensa.
- **Dia 30:** suspensão da conta.
- **Dia 60:** possível remoção de dados conforme a retenção.

Os prazos acima são ilustrativos e podem variar conforme o plano e o contrato.

## Regularização de Acesso

Após a confirmação do pagamento pendente:

- O acesso é restabelecido **automaticamente**, sem necessidade de nova contratação.
- As configurações, dashboards e integrações são preservados, desde que a conta não
  tenha sido removida.
- A ingestão de dados é retomada a partir do momento da regularização; dados do período
  de suspensão podem não ser recuperados.

## Retenção e Exclusão de Dados

Após o cancelamento ou a suspensão definitiva, os dados entram em um processo de
retenção e depois são excluídos conforme a política vigente. Clientes Enterprise podem
solicitar a exportação dos dados antes da exclusão, dentro do prazo previsto em
contrato.

## Reembolso e Créditos

- O reembolso do plano **Pro** segue a política comercial: até **7 dias corridos** após
  a contratação.
- **Créditos de SLA** (Enterprise) são aplicados na fatura seguinte e não são
  convertidos em dinheiro (ver documento de SLA de suporte).
- Ajustes de cobrança por erro de faturamento são corrigidos na próxima fatura ou por
  nota de crédito, conforme o caso.

## Perguntas Frequentes

**O que acontece se meu cartão falhar?**
Você é notificado e a cobrança é reprocessada em até 3 tentativas antes de restringir o
acesso.

**Perco meus dados se a conta for suspensa?**
Durante o modo restrito os dados ficam em somente leitura; a remoção só ocorre após os
prazos de suspensão e retenção.

**Consigo nota fiscal?**
Sim. A nota é emitida a cada cobrança e fica disponível no portal de faturamento.

**Como evito cobrança de excedente?**
Acompanhe o painel de uso e configure alertas de consumo em 80% e 100% da cota.
