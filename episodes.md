---
layout: default
title: Episodes
permalink: /episodes/
---

<section class="grid">
  <div class="wrap">
    <h2 class="section-title">All Episodes</h2>
    <div class="cards">
      {% assign eps = site.posts | where_exp: "p", "p.categories contains 'episodes'" %}
      {% for post in eps %}
        <a class="card" href="{{ post.url | relative_url }}">
          {% if post.cover %}<img src="{{ post.cover }}" alt="">{% endif %}
          <div class="card-body">
            <h3>{{ post.title }}</h3>
            <p class="muted">{{ post.date | date: "%b %-d, %Y" }}{% if post.duration %} · {{ post.duration }}{% endif %}</p>
            <p class="line-clamp">{{ post.excerpt }}</p>
          </div>
        </a>
      {% endfor %}
    </div>
  </div>
</section>
