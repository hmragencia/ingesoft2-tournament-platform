# Workshop 2 — Design Artifacts and System Modeling

**Public Module** of the youth football tournament platform: public website, embeddable widgets and installable app (PWA), with sponsorship and commerce features. Software Engineering II, 2026-II, Universidad Nacional de Colombia.

**Team:** Nicolás Molano Barón (Product Owner), Luis Gabriel Peraza Muñoz (Scrum Master), Rafael Otero Erazo, Sebastián Clavijo Tocasuchyl and Nicolás Gómez Lozano (Developers).
**Lecturer:** Liliana Marcela Olarte Mesa.

The workshop was delivered in two parts, as instructed by the lecturer:

- **Part 1** (October 15, 2026): sections 1 to 5, up to the mockups (main screens only).
- **Part 2** (October 30, 2026): sections 6 and 7, business processes and architecture.

| Section | File |
|---|---|
| **Part 1 — single PDF** | [Workshop-2.pdf](Workshop-2.pdf) |
| 1. System domain: context, actors, business rules | [01-system-domain.md](01-system-domain.md) |
| 2. CRC cards | [02-crc-cards.md](02-crc-cards.md) |
| 3. Class diagram | [03-class-diagram.md](03-class-diagram.md) |
| 4. Relational database model | [04-relational-database-model.md](04-relational-database-model.md) |
| 5. Mockups | [05-mockups.md](05-mockups.md) · images in [mockups/](mockups/) · prompt in [v0-prompt.md](v0-prompt.md) |
| **Part 2 — single PDF** | [Workshop-2-part-2.pdf](Workshop-2-part-2.pdf) |
| 6. Business process models (BPMN 2.0) | [06-business-processes.md](06-business-processes.md) · sources in [bpmn/](bpmn/) (`.bpmn` opens in bpmn.io or Camunda Modeler) |
| 7. Architecture | [07-architecture.md](07-architecture.md) |
| 8. Use of AI and references (both parts) | [08-ai-usage-and-references.md](08-ai-usage-and-references.md) |

Traceability: every business rule, class, screen, process and architectural decision points back to the requirements (RF/RNF) and user stories (HU) of [Workshop 1](../Workshop-1/README.md).

**Regenerating the files:**

```bash
python3 tools/build_bpmn.py Workshop-2/bpmn
python3 tools/build_workshop_pdf.py Workshop-2 --sections 06 07 08 --out Workshop-2-part-2.pdf
```

The first command rebuilds the `.bpmn` and `.svg` files from their `.json` specs; the second compiles the part 2 PDF. Run both from the repository root.
