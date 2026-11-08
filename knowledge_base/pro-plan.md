---
title: Plano Pro
tenant: fcai
product: fcai-cloud
plan: pro
doc_type: plan
version: 2026-01
status: published
visibility: internal
---

# Plano Pro

O plano **Pro** do FCAI Cloud é o plano pago self-service, voltado para times em
produção que precisam de limites maiores, SLA de suporte em horário comercial e
cobrança previsível por cartão. Este documento detalha para quem o plano é indicado,
seus limites, recursos, segurança, suporte, condições comerciais, disponibilidade e as
diferenças em relação aos planos Starter e Enterprise. Todos os números são fictícios!

## Para Quem é o Pro

O Pro atende organizações que:

- Já operam serviços em produção e dependem de observabilidade no dia a dia.
- Têm um time de engenharia de tamanho médio, com até 20 pessoas na plataforma.
- Precisam de histórico de dados maior do que os 7 dias do Starter.
- Querem prazo de resposta formal do suporte, mesmo que em horário comercial.
- Preferem contratar sozinhas, sem negociação comercial nem contrato.
- Aceitam cobrança recorrente por cartão de crédito.

## Limites do Plano

- **Até 20 usuários** na organização.
- **Retenção de dados de 30 dias** para métricas, logs e traces.
- **Ingestão de 100 GB de logs por mês**, com cobrança de excedente por GB.
- **Múltiplos times** dentro da organização, sem cotas por time.
- **Alertas avançados** e integrações com canais de notificação.
- **Dashboards personalizados**, sem limite de quantidade.

## Consumo Excedente

Diferente do Starter, o Pro **não pausa a ingestão** ao atingir o limite: o volume que
ultrapassa a cota do plano é cobrado como **consumo excedente**, medido por GB no
fechamento do ciclo.

- Notificações são enviadas ao atingir **80%** e **100%** da cota do plano.
- O painel de uso mostra o consumo atual e projeta o excedente estimado do ciclo.
- É possível definir alertas de consumo para evitar surpresas na fatura.
- O consumo excedente já faturado **não é reembolsável**.

### Exemplo de Cálculo (fictício)

Se a organização consome 130 GB em um ciclo, os 30 GB acima dos 100 GB inclusos são
cobrados como excedente, conforme o preço por GB vigente, no fechamento do ciclo
(ver política de faturamento).

## Recursos Incluídos

- Coleta de **métricas, logs e traces**, com correlação entre os três pilares.
- **Tracing distribuído** com amostragem configurável.
- **Alertas** com múltiplos destinos de notificação.
- **Portal de chamados** e **e-mail de suporte** para abertura de tickets.
- **Painel de uso** com projeção de consumo e excedente do ciclo.

## Segurança

- **Criptografia** de dados em trânsito e em repouso, igual aos demais planos.
- **Autenticação por e-mail e senha**, com verificação em duas etapas opcional.
- **Sem Single Sign-On (SSO)** e **sem provisionamento via SCIM**.
- **Sem controle de acesso baseado em papéis (RBAC)** e **sem trilhas de auditoria**.
- Sem restrição de acesso por rede ou lista de IPs permitidos.

SSO, SCIM, RBAC, auditoria e políticas de governança de dados são exclusivos do plano
Enterprise. Organizações com essa exigência devem avaliar o upgrade.

## Gestão de Usuários e Acessos

- Convite de até 20 usuários por e-mail.
- Organização de usuários em **times**, para separar dashboards e alertas.
- Permissões simplificadas, sem papéis customizáveis por recurso.
- Provisionamento e desprovisionamento **manuais**, sem SCIM.

## Onboarding e Adoção

O onboarding do Pro é **self-service**, com apoio da documentação:

1. **Upgrade:** contratação direta no painel, com cartão de crédito.
2. **Instalação do agente:** guia de início rápido e integrações prontas.
3. **Configuração de alertas:** modelos de alerta para os serviços mais comuns.
4. **Acompanhamento:** o próprio time acompanha adoção pelo painel de uso.

Não há kickoff assistido, plano de sucesso nem gerente de conta neste plano — esses
recursos são exclusivos do Enterprise.

## Suporte

Atendimento em **horário comercial**, de segunda a sexta-feira (ver documento de SLA de
suporte):

- **P1:** resposta em até 8 horas úteis.
- **P2:** resposta em até 1 dia útil.
- **P3:** resposta em até 3 dias úteis.

Canais disponíveis:

- **E-mail de suporte:** suporte@fcai.example.com.
- **Portal de chamados:** abertura e acompanhamento de tickets.
- **Base de conhecimento** e comunidade.

Não há cobertura 24x7, canal dedicado, telefone de emergência para P1, gerente de conta
nem relatório de causa raiz — todos exclusivos do Enterprise.

## Condições Comerciais

- **Preço: R$ 499/mês** na cobrança mensal, ou **R$ 5.090/ano** na cobrança anual.
- A contratação **anual** tem **15% de desconto** em relação ao valor mensal equivalente.
- Contratação **self-service**, sem contrato comercial.
- **Cobrança recorrente por cartão de crédito**, com emissão de nota fiscal.
- **Trial de 14 dias** dos recursos do Pro, sem necessidade de cartão de crédito.
- **Reembolso** em até **7 dias corridos** após a contratação, conforme o direito de
  arrependimento. Após esse prazo, não há reembolso proporcional.

### Upgrade e Downgrade

O upgrade a partir do Starter é imediato, com cobrança proporcional (pro rata) ao
período restante do ciclo. No cancelamento, o acesso permanece ativo até o fim do ciclo
já pago, no plano mensal, ou até o fim do período contratado, no plano anual.

## Disponibilidade

O Pro tem meta de disponibilidade de **99,5%** ao mês, **informativa e sem crédito de
SLA**. A política de créditos é exclusiva do Enterprise, que tem meta de 99,9%. A
disponibilidade é medida mensalmente, excluindo janelas de manutenção programada, e
reportada na central de status.

## Diferenças em Relação aos Planos Starter e Enterprise

| Aspecto | Starter | Pro | Enterprise |
| --- | --- | --- | --- |
| Usuários | 3 | até 20 | ilimitados |
| Retenção de dados | 7 dias | 30 dias | até 15 meses |
| Ingestão de logs | 5 GB/mês | 100 GB/mês | por contrato |
| Consumo excedente | não (ingestão pausada) | cobrado por GB | conforme contrato |
| Suporte | comunidade | SLA padrão (comercial) | SLA reduzido, 24x7 |
| SSO / RBAC / Auditoria | não | não | sim |
| Faturamento | — | cartão | corporativo por contrato |
| Gerente de conta | não | não | sim |
| Meta de disponibilidade | — | 99,5% (informativa) | 99,9% (com crédito) |

Em resumo, o Pro é o meio-termo: limites de produção e SLA formal em horário comercial,
mantendo a simplicidade do self-service. Quem precisa de segurança avançada, suporte
24x7, crédito de SLA ou faturamento corporativo deve avaliar o Enterprise.

## Perguntas Frequentes

**Quanto custa o plano Pro?**
R$ 499/mês na cobrança mensal ou R$ 5.090/ano na cobrança anual, com 15% de desconto.

**Quantos usuários o Pro permite?**
Até 20 usuários na mesma organização.

**Qual é o tempo de resposta para P1 no Pro?**
Até 8 horas úteis, em horário comercial, de segunda a sexta-feira.

**O Pro tem SSO?**
Não. SSO, SCIM, RBAC e trilhas de auditoria são exclusivos do plano Enterprise.

**O que acontece se eu ultrapassar os 100 GB de ingestão?**
O volume adicional é cobrado como consumo excedente, por GB, no fechamento do ciclo.

**O Pro tem crédito de SLA?**
Não. A meta de 99,5% é informativa. O crédito de SLA é exclusivo do Enterprise.
