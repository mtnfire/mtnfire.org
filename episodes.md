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
      RSS path: group by itunes season (no filters inside group_by_exp).
      Any items without season will have an empty group name; we label as Season 0.
      {%- endcomment -%}
      {% assign by_season = rss_items | group_by_exp: "it", "it.season" %}
      {% assign by_season = by_season | sort: "name" | reverse %}

      <nav class="season-nav">
        {% for g in by_season %}
          {% assign season_name = g.name %}
          {% if season_name == "" or season_name == nil %}
            {% assign season_name = 0 %}
          {% endif %}
          <a href="#season-{{ season_name }}">Season {{ season_name }}</a>
        {% endfor %}
      </nav>

      <div class="seasons">
        {% for g in by_season %}
          {% assign season_name = g.name %}
          {% if season_name == "" or season_name == nil %}
            {% assign season_name = 0 %}
          {% endif %}

          {%- assign eps_sorted = g.items | sort: "episode" -%}
          {%- assign has_numbers = false -%}
          {%- for x in eps_sorted -%}
            {%- if x.episode -%}{%- assign has_numbers = true -%}{%- break_
