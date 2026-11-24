---
title: Organizers
permalink: /organizers/
---

## Steering committee

{% include people.html people=site.data.people.steering %}

## Publicity chair

{% include people.html people=site.data.people.publicity %}

## Program chairs

{% for edition in site.data.editions %}{% if edition.chairs.size > 0 %}
### {{ edition.year }}

{% include people.html people=edition.chairs %}
{% if edition.contact %}
<p class="contact-line"><a href="mailto:{{ edition.contact }}">Email the {{ edition.year }} program chairs</a></p>
{% endif %}
{% endif %}{% endfor %}

The full program committee of each edition is listed in its call for papers.
