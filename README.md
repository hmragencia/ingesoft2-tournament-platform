# Youth Football Tournament Platform — Public Module

Course project for **Software Engineering II** (2026-II), Computer Engineering Program, Universidad Nacional de Colombia. Lecturer: Liliana Marcela Olarte Mesa.

The project extends an existing tournament-management platform for youth football, already in production with a real organizer. This semester the team builds the **Public Module**: the public website, embeddable widgets and installable app (PWA), with sponsorship and commerce features. The module reads the data that the management platform already collects and approves.

**Team:** Nicolás Molano Barón (Product Owner), Luis Gabriel Peraza Muñoz (Scrum Master), Rafael Otero Erazo, Sebastián Clavijo Tocasuchyl and Nicolás Gómez Lozano (Developers).

## Project deliverables

| Deliverable | Folder | Language |
|---|---|---|
| Project proposal (approved) and Annex A, functionality breakdown | [Proposal/](Proposal/) | Spanish |
| Workshop 1: requirements, user stories and story map | [Workshop-1/](Workshop-1/README.md) | Spanish |
| Workshop 2: design artifacts and system modeling (part 1: domain, CRC, classes, database, mockups; part 2: BPMN processes, architecture) | [Workshop-2/](Workshop-2/README.md) | English |

## Other course work

| Assignment | Folder |
|---|---|
| Use cases | [Course-work/Workshop-1-Use-cases/](Course-work/Workshop-1-Use-cases/) |
| Story maps, planning and estimation | [Course-work/Workshop-2-Story-maps-and-estimation/](Course-work/Workshop-2-Story-maps-and-estimation/) |
| SOLID lab | [Course-work/SOLID-lab/](Course-work/SOLID-lab/) |

## Tools

`python3 tools/build_workshop_pdf.py Workshop-2` compiles the numbered sections of a workshop into a single PDF; `--sections` and `--out` select a subset (part 2 of Workshop 2). `python3 tools/build_bpmn.py Workshop-2/bpmn` generates the BPMN 2.0 files and their SVG images. Both need Google Chrome: Markdown, Mermaid and BPMN are rendered in the browser.
