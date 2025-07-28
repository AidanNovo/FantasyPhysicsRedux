---
layout: page
title: Cards
permalink: /cards/
---

This is where all the cards go.
I am imagining a bunch of floating card images that you can click on
in order to go to the cards' pages.

This also should maybe not be a markdown formatted page.
Look into the ways that some themes do those portfolio pages!

**Card Page Directory (temporary)**
* [IceCube]({{ 'cards/icecube' | relative_url}})
* [Super-Kamiokande]({{ 'cards/super_k' | relative_url}})

Also, ideally this whole thing would be automatically-populated, which will surely be easy to do.

Auto-populated list of card pages with links. (Works by including card_page: true in frontmatter)

---

<div class="card-directory-col-wrapper">
{%- for page in site.pages -%}
    {%- if page.card_page == true -%}  
        <a class="card-directory-img" href="{{ page.url | relative_url}}">
        <img
             src="{{ page.image_url | default: 'https://placehold.co/1200x800/A78BFA/FFFFFF?text=Placeholder+Image' }}"
             alt="{{ page.image_alt | default: 'Descriptive Image' }}">
        </a>
    {%- endif -%}  
{%- endfor -%}
</div>