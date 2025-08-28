---
layout: default
title: Episodes
permalink: /episodes/
---

<!-- Raw HTML inside Markdown is fine in Jekyll -->
<section class="episodes">
  <div class="wrap">
    <h1 class="section-title">Episodes</h1>

    <!-- Filter bar -->
    <div class="filter-bar">
      <input id="ep-search" type="search" placeholder="Search episodes…" aria-label="Search episodes">
      <div class="spacer"></div>
      <button id="expand-all" class="pill outline" type="button">Expand all</button>
      <button id="collapse-all" class="pill outline" type="button">Collapse all</button>
    </div>

    {%- assign eps = site.posts | where_exp: "p", "p.categories contains 'episodes'" -%}
    {%- assign eps_sorted = eps | sort: "date" | reverse -%}

    {%- comment -%}
      Group by season: prefer p.season, then p.itunes_season (from RSS), else 0 ("Other")
    {%- endcomment -%}
    {%- assign groups = eps_sorted
        | group_by_exp: "p", "p.season | default: p.itunes_season | default: 0 | plus: 0"
      -%}
    {%- assign groups_desc = groups | sort: "name" | reverse -%}

    {%- for g in groups_desc -%}
      {%- assign label = g.name -%}
      {%- if g.name == 0 -%}{% assign label = "Other" %}{% endif -%}

      <details class="season" data-season="{{ g.name }}" {% if forloop.first and g.name != 0 %}open{% endif %}>
        <summary>
          <span class="season-title">{% if g.name == 0 %}Other{% else %}Season {{ g.name }}{% endif %}</span>
          <span class="muted">({{ g.items | size }} episodes)</span>
        </summary>

        <div class="cards">
          {%- assign items = g.items | sort: "date" | reverse -%}
          {%- for post in items -%}
            {%- assign summary = post.excerpt | strip_html | strip -%}
            {%- if summary == "" -%}
              {%- assign summary = post.content | markdownify | strip_html | strip | truncate: 180 -%}
            {%- endif -%}
            <a class="card episode-card"
               href="{{ post.url | relative_url }}"
               data-text="{{ post.title | downcase | escape }} {{ summary | downcase | escape }}">
              {% if post.cover %}<img loading="lazy" src="{{ post.cover }}" alt="">{% endif %}
              <div class="card-body">
                <h3>{{ post.title }}</h3>
                <p class="muted">
                  {{ post.date | date: "%b %-d, %Y" }}
                  {% if post.duration %} · {{ post.duration }}{% endif %}
                  {% if post.season or post.itunes_season %}
                    · S{% if post.season %}{{ post.season }}{% else %}{{ post.itunes_season }}{% endif %}
                  {% endif %}
                </p>
                <p class="line-clamp">{{ summary }}</p>
              </div>
            </a>
          {%- endfor -%}
        </div>
      </details>
    {%- endfor -%}
  </div>
</section>

<script>
  (function(){
    const q = document.getElementById('ep-search');
    const seasons = Array.from(document.querySelectorAll('.season'));
    const btnExpand = document.getElementById('expand-all');
    const btnCollapse = document.getElementById('collapse-all');

    function applySearch(){
      const term = (q.value || "").trim().toLowerCase();
      seasons.forEach(sec => {
        let anyVisible = false;
        const cards = sec.querySelectorAll('.episode-card');
        cards.forEach(card => {
          const text = (card.dataset.text || "");
          const match = !term || text.includes(term);
          card.style.display = match ? "" : "none";
          if (match) anyVisible = true;
        });
        sec.style.display = anyVisible ? "" : "none";
        if (term && anyVisible) sec.open = true; // open sections that have matches
      });
    }

    q.addEventListener('input', applySearch);

    btnExpand?.addEventListener('click', () => { seasons.forEach(sec => sec.open = true); });
    btnCollapse?.addEventListener('click', () => { seasons.forEach(sec => sec.open = false); });
  })();
</script>
