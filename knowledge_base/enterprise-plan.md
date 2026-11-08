---
title: Plano Enterprise
tenant: fcai
product: fcai-cloud
plan: enterprise
doc_type: plan
version: 2026-01
status: published
visibility: internal
---

# Plano Enterprise

O plano **Enterprise** do FCAI Cloud é voltado para empresas com times grandes, alto
volume de dados e requisitos avançados de segurança, governança e suporte. Este
documento detalha benefícios, segurança e conformidade, gestão de usuários e acessos,
onboarding, suporte diferenciado, condições comerciais, SLA e as diferenças em relação
aos planos Starter e Pro. Todos os números são fictícios.

## Para Quem é o Enterprise

O Enterprise atende organizações que:

- Possuem muitos times e serviços monitorados simultaneamente.
- Precisam de retenção longa de dados por exigência interna ou regulatória.
- Exigem controles de segurança como SSO e RBAC.
- Necessitam de suporte com SLA reduzido e cobertura 24x7.
- Preferem faturamento corporativo em vez de cobrança por cartão.
- Requerem governança centralizada e relatórios executivos.

## Benefícios

- **Usuários ilimitados** e organização estruturada em múltiplos times.
- **Retenção de dados configurável**, de até 15 meses.
- **Volume de ingestão** de métricas e logs negociado por contrato.
- **Ambiente com isolamento dedicado** disponível sob demanda.
- **Detecção de anomalias** e alertas avançados incluídos.
- **Relatórios executivos** de uso, disponibilidade e adoção.
- **Cotas por time**, evitando que um time consuma toda a capacidade.

## Segurança e Conformidade

- **Criptografia** de dados em trânsito e em repouso.
- **Single Sign-On (SSO)** via SAML, integrando com o provedor de identidade do cliente.
- **Provisionamento automático** de usuários via SCIM.
- **Controle de acesso baseado em papéis (RBAC)**, com papéis customizáveis.
- **Trilhas de auditoria** das ações dos usuários na plataforma.
- **Política de retenção e exclusão** de dados configurável conforme exigências
  internas do cliente.
- **Relatórios de conformidade** disponibilizados sob acordo de confidencialidade.
- **Restrição de acesso por rede** (lista de IPs permitidos), quando aplicável.

### Governança de Dados

O Enterprise permite definir políticas de retenção e mascaramento de dados sensíveis em
logs, além de controlar quais times têm acesso a quais fontes de dados. Essas políticas
são configuradas pelo administrador da organização e auditadas via trilhas de acesso.

## Gestão de Usuários e Acessos

O plano Enterprise oferece um painel de administração central que permite:

- Criar e gerenciar múltiplos times dentro da mesma organização.
- Atribuir papéis e permissões por time e por recurso.
- Provisionar e desprovisionar usuários automaticamente via SCIM.
- Definir políticas de acesso, como restrição por domínio de e-mail corporativo.
- Consultar trilhas de auditoria para fins de segurança e governança.

### Papéis Padrão (fictícios)

- **Administrador:** gerencia a organização, times, cobrança e segurança.
- **Editor:** cria e edita dashboards, alertas e integrações.
- **Analista:** consulta dados e dashboards, sem alterar configurações.
- **Somente leitura:** acesso de visualização para stakeholders.

## Onboarding e Adoção

Clientes Enterprise contam com um processo de onboarding assistido, fictício, que
inclui:

1. **Kickoff:** alinhamento de objetivos, escopo de monitoramento e responsáveis.
2. **Implantação:** configuração de agentes, integrações e primeiros dashboards.
3. **Capacitação:** treinamento dos times na plataforma.
4. **Acompanhamento:** revisões periódicas de adoção com o gerente de conta.

### Plano de Sucesso

O gerente de conta define, junto ao cliente, um plano de sucesso com metas de adoção,
marcos de implantação e indicadores de valor. Revisões trimestrais avaliam o progresso
e ajustam o plano conforme a evolução do uso.

## Suporte Diferenciado

- Suporte **24x7** para chamados críticos.
- **SLA reduzido:** P1 com resposta em até 1 hora (ver documento de SLA de suporte).
- **Canal dedicado** de atendimento e telefone de emergência para P1.
- **Gerente de conta** responsável pelo acompanhamento da conta e dos chamados P1 e P2.
- **Relatório de causa raiz** (post-mortem) para incidentes críticos.

## Condições Comerciais

- Contrato comercial com condições personalizadas.
- **Faturamento corporativo**, com emissão de nota fiscal conforme o acordo.
- Descontos por volume de usuários e de ingestão.
- Prazos de pagamento e formas de cobrança negociados (ver política de faturamento).
- Cláusulas de renovação e reajuste definidas em contrato.
- Possibilidade de faturamento por centro de custo ou unidade de negócio.

## Disponibilidade e Créditos

O Enterprise conta com meta de disponibilidade de **99,9%** ao mês e política de
créditos de SLA quando a meta não é atingida, conforme detalhado no documento de SLA de
suporte. Os créditos são aplicados como desconto na fatura seguinte.

## Diferenças em Relação aos Planos Starter e Pro

| Aspecto | Starter | Pro | Enterprise |
| --- | --- | --- | --- |
| Usuários | 3 | até 20 | ilimitados |
| Retenção de dados | 7 dias | 30 dias | até 15 meses |
| Ingestão de logs | 5 GB/mês | 100 GB/mês | por contrato |
| Suporte | comunidade | SLA padrão | SLA reduzido, 24x7 |
| SSO / RBAC / Auditoria | não | não | sim |
| Faturamento | — | cartão | corporativo por contrato |
| Gerente de conta | não | não | sim |
| Crédito de SLA | não | não | sim |

Em resumo, o Enterprise se diferencia por escala (usuários e retenção ilimitados ou
amplamente configuráveis), segurança avançada (SSO, RBAC e auditoria), suporte com
cobertura 24x7 e um modelo comercial baseado em contrato corporativo, em vez de
cobrança recorrente por cartão.

## Perguntas Frequentes

**O Enterprise tem limite de usuários?**
Não. O plano oferece usuários ilimitados.

**Como funciona o SSO?**
Via SAML, integrando com o provedor de identidade do cliente, com provisionamento por
SCIM.

**Existe gerente de conta?**
Sim. O Enterprise inclui um gerente de conta dedicado.

**Qual a retenção máxima de dados?**
Configurável em até 15 meses, conforme o contrato.
