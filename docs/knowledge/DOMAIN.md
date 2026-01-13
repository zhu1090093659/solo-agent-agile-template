# Domain Knowledge

## Business Overview

### What We Do

[Brief description of the business domain and what problem this product solves]

### Target Users

| User Type | Description | Primary Goals |
|-----------|-------------|---------------|
| [Type 1] | [Who they are] | [What they want to achieve] |
| [Type 2] | [Who they are] | [What they want to achieve] |

---

## Core Domain Concepts

### [Concept 1: e.g., Order]

**Definition**: [Clear definition of what this concept means in this domain]

**Properties**:
- [Property 1]: [Description]
- [Property 2]: [Description]

**Business Rules**:
- [Rule 1]: [Description]
- [Rule 2]: [Description]

**Lifecycle**:
```
Created -> Pending -> Processing -> Completed
                  \-> Cancelled
```

---

### [Concept 2: e.g., User]

**Definition**: [Clear definition]

**Types**:
| Type | Description | Permissions |
|------|-------------|-------------|
| Admin | [Desc] | Full access |
| Member | [Desc] | Limited access |
| Guest | [Desc] | Read only |

---

## Business Processes

### [Process 1: e.g., Checkout Flow]

```
1. User adds items to cart
2. User initiates checkout
3. System validates inventory
4. User enters payment info
5. System processes payment
6. System creates order
7. System sends confirmation
```

**Edge Cases**:
- [Edge case 1]: [How to handle]
- [Edge case 2]: [How to handle]

---

### [Process 2: e.g., Refund Process]

```
1. User requests refund
2. Admin reviews request
3. If approved:
   a. System processes refund
   b. System updates inventory
   c. System notifies user
4. If rejected:
   a. System notifies user with reason
```

---

## Business Rules

### Pricing Rules

| Rule | Condition | Action |
|------|-----------|--------|
| Bulk Discount | Quantity >= 10 | 10% off |
| Member Discount | User is premium | 5% off |
| [Rule] | [Condition] | [Action] |

### Validation Rules

| Entity | Field | Rule |
|--------|-------|------|
| User | email | Must be valid email format |
| Order | total | Must be > 0 |
| [Entity] | [Field] | [Rule] |

---

## External Integrations

### [Integration 1: e.g., Payment Provider]

**Purpose**: Process payments
**Provider**: [e.g., Stripe]
**Documentation**: [Link]

**Key Concepts**:
- [Concept 1]: [Explanation]
- [Concept 2]: [Explanation]

---

## Industry Context

### Regulations

| Regulation | Applies To | Requirements |
|------------|------------|--------------|
| [GDPR] | User data | [Requirements] |
| [PCI-DSS] | Payments | [Requirements] |

### Industry Terms

See @GLOSSARY.md for complete terminology.

---

## Historical Context

### Why Certain Decisions Were Made

| Decision | Reason | Date |
|----------|--------|------|
| [Decision 1] | [Business reason] | [When] |
| [Decision 2] | [Business reason] | [When] |

---

## Metrics and KPIs

### Business Metrics

| Metric | Definition | Target |
|--------|------------|--------|
| Conversion Rate | Orders / Visitors | > 3% |
| [Metric] | [Definition] | [Target] |

### Technical Metrics

| Metric | Definition | Target |
|--------|------------|--------|
| Response Time (p95) | 95th percentile latency | < 200ms |
| Error Rate | Errors / Requests | < 0.1% |

---

## FAQs

### Q: [Common question about the domain]

A: [Answer explaining the business logic]

### Q: [Another common question]

A: [Answer]
