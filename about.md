---
layout: default
title: About
permalink: /about/
---

<section class="about">
  <div class="wrap about-wrap">
    <div class="about-main">
      <h1>About MTN.fire</h1>

      <!-- 📝 Paste your Podpage “About” text between the markers below -->
      <div class="prose">
        <!-- START: YOUR ABOUT TEXT -->
        <p><strong>Paste the exact text you like from Podpage here.</strong> You can keep paragraphs, line breaks, and links—this section will style them nicely.</p>
        <!-- END: YOUR ABOUT TEXT -->
      </div>

      <div class="about-cta">
        {% if site.podcast.rss %}
          <a class="pill" href="{{ site.podcast.rss }}" target="_blank" rel="noopener">Subscribe via RSS</a>
        {% endif %}
        {% if site.socials.email %}
          <a class="pill outline" href="{{ site.socials.email }}">Email</a>
        {% endif %}
      </div>

      <h2 class="section-title" style="margin-top:24px">Connect</h2>
      {% include social-icons.html %}
    </div>

    <!-- Optional side column (auto-hides if there’s nothing to show) -->
    <aside class="about-aside">
      {% if site.logo_image %}
        <img class="about-logo" src="{{ site.baseurl }}{{ site.logo_image }}" alt="{{ site.title }} logo">
      {% endif %}
      {% if site.about_image %}
        <img class="about-photo" src="{{ site.baseurl }}{{ site.about_image }}" alt="About photo">
      {% endif %}
    </aside>
  </div>
</section>
