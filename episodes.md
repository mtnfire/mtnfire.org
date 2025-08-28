---
layout: default
title: Episodes
permalink: /episodes/
---

{% assign rss_items = site.data.episodes.items | default: nil %}

<section class="grid">
  <div class="wrap">
    <h2 class="section-title">All Episodes</h2>

    {% if rss_items %}
      {%- comment -%}
      RSS PATH (from _data/episodes.json created by build step)
      Group by season; unknown seasons go to 0.
      Sort seasons DESC; episodes ASC (fallback to pubDate)
      {%- endcomment -%}
      {% assign by_season = rss_items | group_by_exp: "it", "it.season | default: 0" %}
      {% assign by_season = by_season | sort: "name" | reverse %}

      <nav class="season-nav">
        {% for g in by_season %}
          <a href="#season-{{ g.name }}">Season {{ g.name }}</a>
        {% endfor %}
      </nav>

      <div class="seasons">
        {% for g in by_season %}
          {%- assign eps_sorted = g.items | sort: "episode" -%}
          {%- assign has_numbers = false -%}
          {%- for x in eps_sorted -%}
            {%- if x.episode -%}{%- assign has_numbers = true -%}{%- break -%}{%- endif -%}
          {%- endfor -%}
          {%- if has_numbers == false -%}
            {%- assign eps_sorted = g.items | sort: "pubDate" -%}
          {%- endif -%}

          <section id="season-{{ g.name }}" class="season">
            <details {% if forloop.first %}open{% endif %}>
              <summary>
                <span class="season-title">Season {{ g.name }}</span>
                <span class="count">({{ g.items | size }} episodes)</span>
              </summary>

              <div class="cards">
                {% for e in eps_sorted %}
                  <a class="card" href="{{ e.link }}" target="_blank" rel="noopener">
                    {% if e.image %}<img src="{{ e.image }}" alt="">{% endif %}
                    <div class="card-body">
                      <h3>
                        {% if e.season %}S{{ e.season }}{% endif %}{% if e.episode %}·E{{ e.episode }}{% endif %}
                        {% i
