---
title: Past editions
permalink: /past/
---

All papers, slides and talk recordings of past editions stay online.

<ul class="edition-list">
{%- for edition in site.data.editions %}
{%- assign key = "y" | append: edition.year %}
{%- if site.data.program[key] %}
  <li>
    <a href="{{ '/' | append: edition.year | append: '/' | relative_url }}">HotCarbon {{ edition.year }}</a>
    <span class="muted">{% if edition.dates %}{{ edition.dates }} &middot; {% endif %}{% if edition.location %}{{ edition.location }} &middot; {% endif %}{{ site.data.program[key].papers.size }} papers</span>
  </li>
{%- endif %}
{%- endfor %}
</ul>
