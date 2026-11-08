---
title: Plano Starter
tenant: fcai
product: fcai-cloud
plan: starter
doc_type: plan
version: 2026-01
status: published
visibility: internal
---

# Plano Starter

O plano **Starter** do FCAI Cloud é a porta de entrada gratuita da plataforma, voltada
para times pequenos, projetos individuais e provas de conceito. Este documento detalha
para quem o plano é indicado, seus limites, recursos incluídos, segurança, suporte,
condições comerciais, disponibilidade e as diferenças em relação aos planos Pro e
Enterprise. Todos os números são fictícios.

## Para Quem é o Starter

O Starter atende organizações e pessoas que:

- Estão avaliando o FCAI Cloud antes de contratar um plano pago.
- Monitoram poucos serviços, geralmente um ambiente de desenvolvimento ou um projeto.
- Toleram retenção curta de dados e não têm exigência regulatória de histórico.
- Não precisam de SLA de suporte com prazo garantido.
- Preferem uma configuração autônoma, sem contrato e sem cartão de crédito.

## Limites do Plano

- **Até 3 usuários** na organização.
- **Retenção de dados de 7 dias** para métricas, logs e traces.
- **Ingestão de até 5 GB de logs por mês**, sem cobrança de excedente.
- **Um único time** dentro da organização, sem separação por times.
- **Alertas básicos** por e-mail, sem detecção de anomalias.
- **Dashboards padrão** da plataforma, com personalização limitada.

Ao atingir o limite de ingestão, a coleta de novos dados é pausada até o próximo ciclo.
O Starter **não gera cobrança de consumo excedente**: em vez de faturar o excedente, a
plataforma interrompe a ingestão, como forma de manter o plano gratuito.

## Recursos Incluídos

- Coleta de **métricas, logs e traces** pelos agentes padrão.
- **Exploradores** de métricas e logs para consulta e filtragem.
- **Integrações** com as fontes de dados suportadas pela plataforma.
- **Central de status** e base de conhecimento pública.
- **Notificações de uso** ao se aproximar do limite de ingestão do plano.

## Segurança

- **Criptografia** de dados em trânsito e em repouso, igual aos demais planos.
- **Autenticação por e-mail e senha**, com verificação em duas etapas opcional.
- **Sem Single Sign-On (SSO)** e **sem provisionamento via SCIM**.
- **Sem controle de acesso baseado em papéis (RBAC)** e **sem trilhas de auditoria**.
- Sem restrição de acesso por rede ou lista de IPs permitidos.

Organizações com exigências de SSO, RBAC ou auditoria devem considerar o plano
Enterprise, que concentra os recursos de segurança avançada.

## Gestão de Usuários e Acessos

O Starter oferece uma gestão de usuários simplificada:

- Convite de até 3 usuários por e-mail.
- Todos os usuários compartilham o mesmo nível de acesso à organização.
- Não há papéis customizáveis nem permissões por recurso.
- A remoção de usuários é feita manualmente pelo criador da organização.

## Onboarding e Adoção

O onboarding do Starter é **self-service**, sem participação do time comercial:

1. **Cadastro:** criação da organização diretamente no site, sem cartão de crédito.
2. **Instalação do agente:** guia de início rápido na base de conhecimento.
3. **Primeiro dashboard:** modelos prontos para os serviços mais comuns.
4. **Comunidade:** dúvidas são tiradas no fórum público e na documentação.

Não há kickoff assistido, treinamento dedicado nem gerente de conta neste plano.

## Suporte

- Atendimento pela **base de conhecimento** e pela **comunidade**.
- **Sem SLA de resposta garantido** para P1, P2 ou P3 (ver documento de SLA de suporte).
- **Sem e-mail de suporte** e **sem portal de chamados**, disponíveis a partir do Pro.
- Sem canal dedicado, telefone de emergência ou gerente de conta.

## Condições Comerciais

- **Preço: R$ 0/mês.** O plano é gratuito por tempo indeterminado.
- **Sem contrato** e **sem cartão de crédito** para uso do plano.
- Sem emissão de fatura, já que não há cobrança.
- O upgrade para o Pro pode ser feito a qualquer momento, de forma self-service.
- Ao final do **trial de 14 dias** do plano Pro, a organização que não fizer upgrade
  retorna automaticamente aos limites do Starter.

### Retorno do Trial para o Starter

Quando a organização volta do trial do Pro para o Starter, os dados que excedem os
limites do Starter — como retenção acima de 7 dias — podem ser arquivados ou removidos
conforme a política de retenção descrita na política comercial.

## Disponibilidade

O Starter **não possui meta formal de disponibilidade** nem política de créditos de SLA.
A plataforma é operada com o mesmo padrão de infraestrutura dos demais planos, mas sem
compromisso contratual de disponibilidade para este plano.

## Diferenças em Relação aos Planos Pro e Enterprise

| Aspecto | Starter | Pro | Enterprise |
| --- | --- | --- | --- |
| Usuários | 3 | até 20 | ilimitados |
| Retenção de dados | 7 dias | 30 dias | até 15 meses |
| Ingestão de logs | 5 GB/mês | 100 GB/mês | por contrato |
| Consumo excedente | não (ingestão pausada) | cobrado por GB | conforme contrato |
| Suporte | comunidade | SLA padrão | SLA reduzido, 24x7 |
| SSO / RBAC / Auditoria | não | não | sim |
| Faturamento | — | cartão | corporativo por contrato |
| Meta de disponibilidade | — | 99,5% (informativa) | 99,9% |

Em resumo, o Starter troca garantias por simplicidade: é gratuito e imediato, mas sem
SLA, sem excedente faturável e com retenção curta. O Pro adiciona SLA em horário
comercial e limites maiores; o Enterprise adiciona segurança avançada, suporte 24x7 e
contrato corporativo.

## Perguntas Frequentes

**O Starter é gratuito para sempre?**
Sim. O plano custa R$ 0/mês e não exige cartão de crédito nem contrato.

**Quantos usuários o Starter permite?**
Até 3 usuários na mesma organização.

**O Starter tem SLA de suporte?**
Não. O atendimento ocorre pela comunidade e pela base de conhecimento, sem prazo
garantido para P1, P2 ou P3.

**O que acontece se eu ultrapassar os 5 GB de ingestão?**
A ingestão de novos dados é pausada até o próximo ciclo. Não há cobrança de excedente
no Starter.

**Por quanto tempo os dados ficam disponíveis?**
Por 7 dias. Retenções maiores exigem o plano Pro ou Enterprise.
