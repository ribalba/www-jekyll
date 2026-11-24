---
title: News
permalink: /news/
---

{% for post in site.posts %}
<article class="news-item">
  <p class="date"><time datetime="{{ post.date | date_to_xmlschema }}">{{ post.date | date: "%b %-d, %Y" }}</time></p>
  <h2><a href="{{ post.url | relative_url }}">{{ post.title }}</a></h2>
  {{ post.content }}
</article>
{% endfor %}
