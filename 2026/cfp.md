---
layout: edition
edition: 2026
section: cfp
title: Call for Papers
nav_order: 2
---

{% assign edition = site.data.editions | where: "year", page.edition | first %}

## Dates and location

{% include edition-facts.html year=page.edition %}

## Overview

The Workshop on Sustainable Computer Systems aims to engage researchers and practitioners in a lively discussion on new ideas to improve the sustainability of computer systems. The research community has had a relentless focus on the implications of increased scale and raw performance of consumer devices, cloud systems and datacenters, as well as networks. We must address the negative aspects of computing's proliferation---through innovative approaches to how we build, deploy, operate, and retire our creations. For example, software-driven hardware obsolescence that increases e-waste and embodied carbon suggests we must challenge computing's endemic upgrade and throwaway practices.

## Scope

We solicit research and position papers that address sustainability and/or the carbon footprint of computer and networked systems. An ideal submission has the potential to open a line of inquiry that results in multiple conference papers by different authors in related venues rather than a single follow-up conference paper. Position papers that frame larger new challenges and opportunities are encouraged. The program committee will explicitly favor papers likely to stimulate reflection and discussion, addressing the root causes of unsustainability in current designs.

By its very nature, HotCarbon takes a broad view of systems research, relevant metrics, and intertwined infrastructure and software. Its scope includes, among others:

- operating systems
- storage
- distributed systems
- mobile/embedded systems
- virtualization
- programming languages
- networking
- security
- dependability
- manageability
- systems issues in sustainable AI, including those that span the life cycle of AI models, specialized AI systems, data, and ecosystems

as well as new systems contributions influenced by other fields such as

- hardware design
- machine learning
- verification
- economics
- social organization
- biological or other nontraditional computing systems.

Because of the nature of sustainability, research that connects to other complex infrastructures, such as

- power grids
- electronic supply chains
- circular economies
- right-to-repair
- demanufacturing
- embedded costs

is directly relevant.

## Policies

Research and position paper submissions must be no longer than **five pages**, including figures and tables, plus as many pages as needed for references.
Appendices are not allowed.
Submissions must be in PDF format and formatted according to the official ACM Proceedings format. Word and LaTeX templates are available on the [ACM Publications Website](https://www.acm.org/publications/proceedings-template). Please use the template `sigconf`. The conference acronym is `HotCarbon'26, July 16-17th, 2026, Seattle, WA.`.

Submissions will be **double-blind**. The title and an abstract should appear on the first page; author names should not. Authors must make a good-faith effort to anonymize their submissions, and they should not identify themselves either explicitly or by implication (e.g., through references or acknowledgments).

HotCarbon will also feature **panels and events** to inspire discussion of future research directions independent of any specific work. Panels and events may have many formats, from conventional panel discussions to breakouts to games. If you are interested in hosting or proposing an event, please submit a 1-page proposal (using the same format above) describing the topic, format, and length (up to 90 minutes), plus as many pages as necessary for references and supporting letters from planned participants. The committee will evaluate proposals based on the topic's relevance and potential to engage the audience. Panel submissions are single-blind.

All submissions must be received by the hard deadline listed above. Papers and proposals should be submitted via the [submission site](#submission-site) as PDF files. Please identify your submission type in the form (paper or proposal). Simultaneous submission of the same work to multiple venues, submission of previously published work, or plagiarism constitutes dishonesty or fraud.

Revised versions of all accepted papers will be published in the [ACM Digital Library](https://dl.acm.org).

- By submitting your article to an ACM Publication, you are hereby acknowledging that you and your co-authors are subject to all ACM Publications Policies, including ACM's new Publications Policy on Research Involving Human Participants and Subjects. Alleged violations of this policy or any ACM Publications Policy will be investigated by ACM and may result in a full retraction of your paper, in addition to other potential penalties, as per ACM Publications Policy.
- Please ensure that you and your co-authors obtain an ORCID ID, so you can complete the publishing process for your accepted paper. ACM has been involved in ORCID from the start and we have recently made a commitment to collect ORCID IDs from all of our published authors. We are committed to improve author discoverability, ensure proper attribution and contribute to ongoing community efforts around name normalization; your ORCID ID will help in these efforts.

In addition, all accepted papers will be available **open-access** on the workshop's website, along with slides of the presentation and, in some cases, a discussion summary.

This workshop will adhere to the [ACM Code of Ethics](https://www.acm.org/code-of-ethics).

HotCarbon is **designed primarily as an in-person workshop**, but **with optional remote attendance**. We believe that in-person attendance is essential to the discussion and interaction that is expected of a workshop. At the same time, we recognize that authors may have issues with the carbon footprint of the required travel, obtaining visas, or have other obstacles to in-person attendance. To support such cases, we accept submissions that do not intend to attend the workshop in-person. In these cases, we ask authors of accepted submissions to record a presentation video. We will make every effort to discuss such submissions at the workshop, but we reserve the right to release the publication and associated video direct-to-proceedings to allow for more interactive discussion of in-person presentations if necessary.

## Program committee

### Chairs

{% include people.html people=edition.chairs %}

### Committee

{% include people.html people=edition.committee %}

## Contact

You can contact the program chairs [by email](mailto:yiding@purdue.edu,Fonseca.Rodrigo@microsoft.com) for any question about the technical program.

## Submission site

[{{ edition.links.submission | remove: "https://" | remove: "/" }}]({{ edition.links.submission }})
