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
        <p><strong>MTN.fire is where real stories meet the unshakable truth of the Gospel.
Each episode blends raw testimony, scripture, and honest conversation — no sugarcoating, no watered-down faith. From the Appalachian mountains to the ends of the earth, this is about carrying the fire of God into everyday life.

We talk about the valleys and the victories, the moments when faith feels easy and the nights when it’s a fight to keep believing. Whether it’s diving into the book of Job, unpacking personal trials, or sharing how God’s moved in powerful ways, MTN.fire is here to remind you: Jesus still changes everything.

If you’re looking for bold truth, gritty hope, and a spark to keep your faith alive — welcome to the fire.</p>
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
