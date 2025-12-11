---
layout: cards
title: Browse the Cards
permalink: /cards/
---

<div style="display: flex; flex-direction: row; justify-content: center">

<hr style="flex: 1 1 auto; margin-right: 5px">

<h3 style="text-align: center"><i> click a card to visit its page and learn more </i></h3>
<hr style="flex: 1 1 auto; margin-left: 5px">

</div>

[//]: # (---)

<div class="card-directory-col-wrapper">
{%- for page in site.pages -%}
    {%- if page.card_page == true and page.card_type == "detector" -%}  
        <a class="card-directory-img" href="{{ page.url | relative_url}}">
        <img
             src="{{ page.image_url | default: 'https://placehold.co/500x700/A78BFA/FFFFFF?text=Placeholder+Image' }}"
             alt="{{ page.image_alt | default: 'Descriptive Image' }}">
        </a>
    {%- endif -%}  
{%- endfor -%}
{%- for page in site.pages -%}
    {%- if page.card_page == true and page.card_type == "analysis" -%}  
        <a class="card-directory-img" href="{{ page.url | relative_url}}">
        <img
             src="{{ page.image_url | default: 'https://placehold.co/500x700/A78BFA/FFFFFF?text=Placeholder+Image' }}"
             alt="{{ page.image_alt | default: 'Descriptive Image' }}">
        </a>
    {%- endif -%}  
{%- endfor -%}
{%- for page in site.pages -%}
    {%- if page.card_page == true and page.card_type == "special" -%}  
        <a class="card-directory-img" href="{{ page.url | relative_url}}">
        <img
             src="{{ page.image_url | default: 'https://placehold.co/500x700/A78BFA/FFFFFF?text=Placeholder+Image' }}"
             alt="{{ page.image_alt | default: 'Descriptive Image' }}">
        </a>
    {%- endif -%}  
{%- endfor -%}
{%- for page in site.pages -%}
    {%- if page.card_page == true and page.card_type == "physics" -%}  
        <a class="card-directory-img" href="{{ page.url | relative_url}}">
        <img
             src="{{ page.image_url | default: 'https://placehold.co/500x700/A78BFA/FFFFFF?text=Placeholder+Image' }}"
             alt="{{ page.image_alt | default: 'Descriptive Image' }}">
        </a>
    {%- endif -%}  
{%- endfor -%}
{%- for page in site.pages -%}
    {%- if page.card_page == true and page.card_type == "token" -%}  
        <a class="card-directory-img" href="{{ page.url | relative_url}}">
        <img
             src="{{ page.image_url | default: 'https://placehold.co/500x700/A78BFA/FFFFFF?text=Placeholder+Image' }}"
             alt="{{ page.image_alt | default: 'Descriptive Image' }}">
        </a>
    {%- endif -%}  
{%- endfor -%}
{%- for page in site.pages -%}
    {%- if page.card_page == true and page.card_type == "placeholder" -%}  
        <a class="card-directory-img" href="{{ page.url | relative_url}}">
        <img
             src="{{ page.image_url | default: 'https://placehold.co/500x700/A78BFA/FFFFFF?text=Placeholder+Image' }}"
             alt="{{ page.image_alt | default: 'Descriptive Image' }}">
        </a>
    {%- endif -%}  
{%- endfor -%}
</div>