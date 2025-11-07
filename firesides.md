---
layout: default
title: Fireside Chats
permalink: /fireside/
---

<section class="episodes">
  <div class="wrap">
    <h1 class="section-title">Fireside Chats</h1>

    <!-- Filter bar -->
    <div class="filter-bar">
      <input id="fs-search" type="search" placeholder="Search fireside…" aria-label="Search fireside">
      <div class="spacer"></div>
      <button id="expand-all" class="pill outline" type="button">Expand all</button>
      <button id="collapse-all" class="pill outline" type="button">Collapse all</button>
    </div>

    {%- comment -%}
      Collect posts in reverse-chronological order without using where_exp.
    {%- endcomment -%}
    {%- assign posts_sorted = site.posts | sort: "date" | reverse -%}

    {%- comment -%}
      Count Season 99 items (Fireside) without where_exp.
    {%- endcomment -%}
    {%- assign fireside_count = 0 -%}
    {%- for post in posts_sorted -%}
      {%- if post.categories contains 'episodes' -%}
        {%- assign s = post.season | default: post.itunes_season | default: post.itunes.season | default: 0 | plus: 0 -%}
        {%- if s == 99 -%}
          {%- assign fireside_count = fireside_count | plus: 1 -%}
        {%- endif -%}
      {%- endif -%}
    {%- endfor -%}

    <details class="season" data-season="99" open>
      <summary>
        <span class="season-title">Fireside Chats (S99)</span>
        <span class="muted">({{ fireside_count }} episodes)</span>
      </summary>

      <div class="cards">
        {%- for post in posts_sorted -%}
          {%- if post.categories contains 'episodes' -%}
            {%- assign summary = post.excerpt | strip_html | strip -%}
            {%- if summary == "" -%}
              {%- assign summary = post.content | markdownify | strip_html | strip | truncate: 180 -%}
            {%- endif -%}

            {%- assign s = post.season | default: post.itunes_season | default: post.itunes.season | default: 0 | plus: 0 -%}
            {%- assign e = post.episode | default: post.itunes_episode | default: post.itunes.episode | default: 0 | plus: 0 -%}

            {%- if s == 99 -%}
              <a class="card episode-card"
                 href="{{ post.url | relative_url }}"
                 data-text="{{ post.title | downcase | escape }} {{ summary | downcase | escape }} s{{ s }} e{{ e }}">
                {% if post.cover %}<img loading="lazy" src="{{ post.cover }}" alt="">{% endif %}
                <div class="card-body">
                  <h3>{{ post.title }}</h3>
                  <p class="muted">
                    {{ post.date | date: "%b %-d, %Y" }}
                    {% if post.duration %} · {{ post.duration }}{% endif %}
                    · S{{ s }}{% if e > 0 %}E{{ e }}{% endif %}
                  </p>
                  <p class="line-clamp">{{ summary }}</p>
                </div>
              </a>
            {%- endif -%}
          {%- endif -%}
        {%- endfor -%}
      </div>
    </details>
  </div>
</section>

<script>
  (function(){
    const q = document.getElementById('fs-search');
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
        if (term && anyVisible) sec.open = true;
      });
    }

    q.addEventListener('input', applySearch);
    btnExpand?.addEventListener('click', () => { seasons.forEach(sec => sec.open = true); });
    btnCollapse?.addEventListener('click', () => { seasons.forEach(sec => sec.open = false); });
  })();
</script>
