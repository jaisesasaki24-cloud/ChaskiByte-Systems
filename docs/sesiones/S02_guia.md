Title: Live Content

Description: Fetched live

Source: https://262dist.github.io/pagatu/sesiones/S02_Configuracion_Centralizada_Ambientes/

---


<!doctype html>
<html lang="en" class="no-js">
  <head>
    
      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width,initial-scale=1">
      
      
      
        <link rel="canonical" href="https://262dist.github.io/pagatu/sesiones/S02_Configuracion_Centralizada_Ambientes/">
      
      
        <link rel="prev" href="../S01_Construccion_Servicio_Base/">
      
      
        <link rel="next" href="../S03_Registro_Descubrimiento_Ejecucion_Concurrente/">
      
      
        
      
      
      <link rel="icon" href="../../assets/images/favicon.png">
      <meta name="generator" content="mkdocs-1.6.1, mkdocs-material-9.7.7">
    
    
  
    <title>Pagatu - S2 - Gestión centralizada de configuración y ambientes</title>
  

    
      <link rel="stylesheet" href="../../assets/stylesheets/main.ec1eaa64.min.css">
      
      


    
    
      
    
    
      
        
        
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Roboto:300,300i,400,400i,700,700i%7CRoboto+Mono:400,400i,700,700i&display=fallback">
        <style>:root{--md-text-font:"Roboto";--md-code-font:"Roboto Mono"}</style>
      
    
    
    <script>__md_scope=new URL("../..",location),__md_hash=e=>[...e].reduce(((e,_)=>(e<<5)-e+_.charCodeAt(0)),0),__md_get=(e,_=localStorage,t=__md_scope)=>JSON.parse(_.getItem(t.pathname+"."+e)),__md_set=(e,_,t=localStorage,a=__md_scope)=>{try{t.setItem(a.pathname+"."+e,JSON.stringify(_))}catch(e){}}</script>
    
      

    
    
  </head>
  
  
    <body dir="ltr">
  
    
    <input class="md-toggle" data-md-toggle="drawer" type="checkbox" id="__drawer" autocomplete="off">
    <input class="md-toggle" data-md-toggle="search" type="checkbox" id="__search" autocomplete="off">
    <label class="md-overlay" for="__drawer"></label>
    <div data-md-component="skip">
      
        
        <a href="#s2-gestion-centralizada-de-configuracion-y-ambientes" class="md-skip">
          Skip to content
        </a>
      
    </div>
    <div data-md-component="announce">
      
    </div>
    
    
      

  

<header class="md-header md-header--shadow" data-md-component="header">
  <nav class="md-header__inner md-grid" aria-label="Header">
    <a href="../.." title="Pagatu" class="md-header__button md-logo" aria-label="Pagatu" data-md-component="logo">
      
  
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M12 8a3 3 0 0 0 3-3 3 3 0 0 0-3-3 3 3 0 0 0-3 3 3 3 0 0 0 3 3m0 3.54C9.64 9.35 6.5 8 3 8v11c3.5 0 6.64 1.35 9 3.54 2.36-2.19 5.5-3.54 9-3.54V8c-3.5 0-6.64 1.35-9 3.54"/></svg>

    </a>
    <label class="md-header__button md-icon" for="__drawer">
      
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M3 6h18v2H3zm0 5h18v2H3zm0 5h18v2H3z"/></svg>
    </label>
    <div class="md-header__title" data-md-component="header-title">
      <div class="md-header__ellipsis">
        <div class="md-header__topic">
          <span class="md-ellipsis">
            Pagatu
          </span>
        </div>
        <div class="md-header__topic" data-md-component="header-topic">
          <span class="md-ellipsis">
            
              S2 - Gestión centralizada de configuración y ambientes
            
          </span>
        </div>
      </div>
    </div>
    
    
      <script>var palette=__md_get("__palette");if(palette&&palette.color){if("(prefers-color-scheme)"===palette.color.media){var media=matchMedia("(prefers-color-scheme: light)"),input=document.querySelector(media.matches?"[data-md-color-media='(prefers-color-scheme: light)']":"[data-md-color-media='(prefers-color-scheme: dark)']");palette.color.media=input.getAttribute("data-md-color-media"),palette.color.scheme=input.getAttribute("data-md-color-scheme"),palette.color.primary=input.getAttribute("data-md-color-primary"),palette.color.accent=input.getAttribute("data-md-color-accent")}for(var[key,value]of Object.entries(palette.color))document.body.setAttribute("data-md-color-"+key,value)}</script>
    
    
    
      
      
        <label class="md-header__button md-icon" for="__search">
          
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M9.5 3A6.5 6.5 0 0 1 16 9.5c0 1.61-.59 3.09-1.56 4.23l.27.27h.79l5 5-1.5 1.5-5-5v-.79l-.27-.27A6.52 6.52 0 0 1 9.5 16 6.5 6.5 0 0 1 3 9.5 6.5 6.5 0 0 1 9.5 3m0 2C7 5 5 7 5 9.5S7 14 9.5 14 14 12 14 9.5 12 5 9.5 5"/></svg>
        </label>
        <div class="md-search" data-md-component="search" role="dialog">
  <label class="md-search__overlay" for="__search"></label>
  <div class="md-search__inner" role="search">
    <form class="md-search__form" name="search">
      <input type="text" class="md-search__input" name="query" aria-label="Search" placeholder="Search" autocapitalize="off" autocorrect="off" autocomplete="off" spellcheck="false" data-md-component="search-query" required>
      <label class="md-search__icon md-icon" for="__search">
        
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M9.5 3A6.5 6.5 0 0 1 16 9.5c0 1.61-.59 3.09-1.56 4.23l.27.27h.79l5 5-1.5 1.5-5-5v-.79l-.27-.27A6.52 6.52 0 0 1 9.5 16 6.5 6.5 0 0 1 3 9.5 6.5 6.5 0 0 1 9.5 3m0 2C7 5 5 7 5 9.5S7 14 9.5 14 14 12 14 9.5 12 5 9.5 5"/></svg>
        
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M20 11v2H8l5.5 5.5-1.42 1.42L4.16 12l7.92-7.92L13.5 5.5 8 11z"/></svg>
      </label>
      <nav class="md-search__options" aria-label="Search">
        
        <button type="reset" class="md-search__icon md-icon" title="Clear" aria-label="Clear" tabindex="-1">
          
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M19 6.41 17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/></svg>
        </button>
      </nav>
      
    </form>
    <div class="md-search__output">
      <div class="md-search__scrollwrap" tabindex="0" data-md-scrollfix>
        <div class="md-search-result" data-md-component="search-result">
          <div class="md-search-result__meta">
            Initializing search
          </div>
          <ol class="md-search-result__list" role="presentation"></ol>
        </div>
      </div>
    </div>
  </div>
</div>
      
    
    
      <div class="md-header__source">
        <a href="https://github.com/262dist/pagatu" title="Go to repository" class="md-source" data-md-component="source">
  <div class="md-source__icon md-icon">
    
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><!--! Font Awesome Free 7.1.0 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free (Icons: CC BY 4.0, Fonts: SIL OFL 1.1, Code: MIT License) Copyright 2025 Fonticons, Inc.--><path d="M439.6 236.1 244 40.5c-5.4-5.5-12.8-8.5-20.4-8.5s-15 3-20.4 8.4L162.5 81l51.5 51.5c27.1-9.1 52.7 16.8 43.4 43.7l49.7 49.7c34.2-11.8 61.2 31 35.5 56.7-26.5 26.5-70.2-2.9-56-37.3L240.3 199v121.9c25.3 12.5 22.3 41.8 9.1 55-6.4 6.4-15.2 10.1-24.3 10.1s-17.8-3.6-24.3-10.1c-17.6-17.6-11.1-46.9 11.2-56v-123c-20.8-8.5-24.6-30.7-18.6-45L142.6 101 8.5 235.1C3 240.6 0 247.9 0 255.5s3 15 8.5 20.4l195.6 195.7c5.4 5.4 12.7 8.4 20.4 8.4s15-3 20.4-8.4l194.7-194.7c5.4-5.4 8.4-12.8 8.4-20.4s-3-15-8.4-20.4"/></svg>
  </div>
  <div class="md-source__repository">
    262dist/pagatu
  </div>
</a>
      </div>
    
  </nav>
  
</header>
    
    <div class="md-container" data-md-component="container">
      
      
        
          
        
      
      <main class="md-main" data-md-component="main">
        <div class="md-main__inner md-grid">
          
            
              
              <div class="md-sidebar md-sidebar--primary" data-md-component="sidebar" data-md-type="navigation" >
                <div class="md-sidebar__scrollwrap">
                  <div class="md-sidebar__inner">
                    



<nav class="md-nav md-nav--primary" aria-label="Navigation" data-md-level="0">
  <label class="md-nav__title" for="__drawer">
    <a href="../.." title="Pagatu" class="md-nav__button md-logo" aria-label="Pagatu" data-md-component="logo">
      
  
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M12 8a3 3 0 0 0 3-3 3 3 0 0 0-3-3 3 3 0 0 0-3 3 3 3 0 0 0 3 3m0 3.54C9.64 9.35 6.5 8 3 8v11c3.5 0 6.64 1.35 9 3.54 2.36-2.19 5.5-3.54 9-3.54V8c-3.5 0-6.64 1.35-9 3.54"/></svg>

    </a>
    Pagatu
  </label>
  
    <div class="md-nav__source">
      <a href="https://github.com/262dist/pagatu" title="Go to repository" class="md-source" data-md-component="source">
  <div class="md-source__icon md-icon">
    
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><!--! Font Awesome Free 7.1.0 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free (Icons: CC BY 4.0, Fonts: SIL OFL 1.1, Code: MIT License) Copyright 2025 Fonticons, Inc.--><path d="M439.6 236.1 244 40.5c-5.4-5.5-12.8-8.5-20.4-8.5s-15 3-20.4 8.4L162.5 81l51.5 51.5c27.1-9.1 52.7 16.8 43.4 43.7l49.7 49.7c34.2-11.8 61.2 31 35.5 56.7-26.5 26.5-70.2-2.9-56-37.3L240.3 199v121.9c25.3 12.5 22.3 41.8 9.1 55-6.4 6.4-15.2 10.1-24.3 10.1s-17.8-3.6-24.3-10.1c-17.6-17.6-11.1-46.9 11.2-56v-123c-20.8-8.5-24.6-30.7-18.6-45L142.6 101 8.5 235.1C3 240.6 0 247.9 0 255.5s3 15 8.5 20.4l195.6 195.7c5.4 5.4 12.7 8.4 20.4 8.4s15-3 20.4-8.4l194.7-194.7c5.4-5.4 8.4-12.8 8.4-20.4s-3-15-8.4-20.4"/></svg>
  </div>
  <div class="md-source__repository">
    262dist/pagatu
  </div>
</a>
    </div>
  
  <ul class="md-nav__list" data-md-scrollfix>
    
      
      
  
  
  
  
    <li class="md-nav__item">
      <a href="../.." class="md-nav__link">
        
  
  
  <span class="md-ellipsis">
    
  
    Inicio
  

    
  </span>
  
  

      </a>
    </li>
  

    
      
      
  
  
  
  
    
    
    
    
    
    <li class="md-nav__item md-nav__item--nested">
      
        
        
        <input class="md-nav__toggle md-toggle " type="checkbox" id="__nav_2" >
        
          
          <label class="md-nav__link" for="__nav_2" id="__nav_2_label" tabindex="0">
            
  
  
  <span class="md-ellipsis">
    
  
    Guía de Proyecto Sello
  

    
  </span>
  
  

            <span class="md-nav__icon md-icon"></span>
          </label>
        
        <nav class="md-nav" data-md-level="1" aria-labelledby="__nav_2_label" aria-expanded="false">
          <label class="md-nav__title" for="__nav_2">
            <span class="md-nav__icon md-icon"></span>
            
  
    Guía de Proyecto Sello
  

          </label>
          <ul class="md-nav__list" data-md-scrollfix>
            
              
                
  
  
  
  
    <li class="md-nav__item">
      <a href="../../proyecto-sello/" class="md-nav__link">
        
  
  
  <span class="md-ellipsis">
    
  
    Guía del proyecto
  

    
  </span>
  
  

      </a>
    </li>
  

              
            
              
                
  
  
  
  
    <li class="md-nav__item">
      <a href="../../proyecto-sello/brief/" class="md-nav__link">
        
  
  
  <span class="md-ellipsis">
    
  
    Brief técnico (plantilla)
  

    
  </span>
  
  

      </a>
    </li>
  

              
            
              
                
  
  
  
  
    <li class="md-nav__item">
      <a href="../../proyecto-sello/alcance-microservicios/" class="md-nav__link">
        
  
  
  <span class="md-ellipsis">
    
  
    Alcance por microservicio
  

    
  </span>
  
  

      </a>
    </li>
  

              
            
              
                
  
  
  
  
    <li class="md-nav__item">
      <a href="../../proyecto-sello/acad/" class="md-nav__link">
        
  
  
  <span class="md-ellipsis">
    
  
    Sistema académico (referencia)
  

    
  </span>
  
  

      </a>
    </li>
  

              
            
              
                
  
  
  
  
    <li class="md-nav__item">
      <a href="../../proyecto-sello/produccion/" class="md-nav__link">
        
  
  
  <span class="md-ellipsis">
    
  
    Sistema de producción y comercialización (referencia)
  

    
  </span>
  
  

      </a>
    </li>
  

              
            
          </ul>
        </nav>
      
    </li>
  

    
      
      
  
  
  
  
    
    
    
    
    
    <li class="md-nav__item md-nav__item--nested">
      
        
        
        <input class="md-nav__toggle md-toggle " type="checkbox" id="__nav_3" >
        
          
          <label class="md-nav__link" for="__nav_3" id="__nav_3_label" tabindex="0">
            
  
  
  <span class="md-ellipsis">
    
  
    Silabos
  

    
  </span>
  
  

            <span class="md-nav__icon md-icon"></span>
          </label>
        
        <nav class="md-nav" data-md-level="1" aria-labelledby="__nav_3_label" aria-expanded="false">
          <label class="md-nav__title" for="__nav_3">
            <span class="md-nav__icon md-icon"></span>
            
  
    Silabos
  

          </label>
          <ul class="md-nav__list" data-md-scrollfix>
            
              
                
  
  
  
  
    <li class="md-nav__item">
      <a href="../../silabo_dist_2026_1/" class="md-nav__link">
        
  
  
  <span class="md-ellipsis">
    
  
    Silabo 2026-1
  

    
  </span>
  
  

      </a>
    </li>
  

              
            
              
                
  
  
  
  
    <li class="md-nav__item">
      <a href="../../silabo_dist_2026_2/" class="md-nav__link">
        
  
  
  <span class="md-ellipsis">
    
  
    Silabo 2026-2
  

    
  </span>
  
  

      </a>
    </li>
  

              
            
          </ul>
        </nav>
      
    </li>
  

    
      
      
  
  
    
  
  
  
    
    
    
    
    
    <li class="md-nav__item md-nav__item--active md-nav__item--nested">
      
        
        
        <input class="md-nav__toggle md-toggle " type="checkbox" id="__nav_4" checked>
        
          
          <label class="md-nav__link" for="__nav_4" id="__nav_4_label" tabindex="0">
            
  
  
  <span class="md-ellipsis">
    
  
    I. Sistema distribuido base orientado a producción
  

    
  </span>
  
  

            <span class="md-nav__icon md-icon"></span>
          </label>
        
        <nav class="md-nav" data-md-level="1" aria-labelledby="__nav_4_label" aria-expanded="true">
          <label class="md-nav__title" for="__nav_4">
            <span class="md-nav__icon md-icon"></span>
            
  
    I. Sistema distribuido base orientado a producción
  

          </label>
          <ul class="md-nav__list" data-md-scrollfix>
            
              
                
  
  
  
  
    <li class="md-nav__item">
      <a href="../S01_Construccion_Servicio_Base/" class="md-nav__link">
        
  
  
  <span class="md-ellipsis">
    
  
    S1 - Construcción de un servicio base para un sistema distribuido
  

    
  </span>
  
  

      </a>
    </li>
  

              
            
              
                
  
  
    
  
  
  
    <li class="md-nav__item md-nav__item--active">
      
      <input class="md-nav__toggle md-toggle" type="checkbox" id="__toc">
      
      
        
      
      
        <label class="md-nav__link md-nav__link--active" for="__toc">
          
  
  
  <span class="md-ellipsis">
    
  
    S2 - Gestión centralizada de configuración y ambientes
  

    
  </span>
  
  

          <span class="md-nav__icon md-icon"></span>
        </label>
      
      <a href="./" class="md-nav__link md-nav__link--active">
        
  
  
  <span class="md-ellipsis">
    
  
    S2 - Gestión centralizada de configuración y ambientes
  

    
  </span>
  
  

      </a>
      
        

<nav class="md-nav md-nav--secondary" aria-label="Table of contents">
  
  
  
    
  
  
    <label class="md-nav__title" for="__toc">
      <span class="md-nav__icon md-icon"></span>
      Table of contents
    </label>
    <ul class="md-nav__list" data-md-component="toc" data-md-scrollfix>
      
        <li class="md-nav__item">
  <a href="#1-introduccion" class="md-nav__link">
    <span class="md-ellipsis">
      
        1. Introducción
      
    </span>
  </a>
  
    <nav class="md-nav" aria-label="1. Introducción">
      <ul class="md-nav__list">
        
          <li class="md-nav__item">
  <a href="#11-presentacion-de-la-sesion" class="md-nav__link">
    <span class="md-ellipsis">
      
        1.1 Presentación de la sesión
      
    </span>
  </a>
  
</li>
        
          <li class="md-nav__item">
  <a href="#12-indice" class="md-nav__link">
    <span class="md-ellipsis">
      
        1.2 Índice
      
    </span>
  </a>
  
</li>
        
          <li class="md-nav__item">
  <a href="#13-proposito-de-aprendizaje" class="md-nav__link">
    <span class="md-ellipsis">
      
        1.3 Propósito de aprendizaje
      
    </span>
  </a>
  
</li>
        
          <li class="md-nav__item">
  <a href="#14-producto-de-sesion" class="md-nav__link">
    <span class="md-ellipsis">
      
        1.4 Producto de sesión
      
    </span>
  </a>
  
</li>
        
          <li class="md-nav__item">
  <a href="#15-metodologia" class="md-nav__link">
    <span class="md-ellipsis">
      
        1.5 Metodología
      
    </span>
  </a>
  
</li>
        
          <li class="md-nav__item">
  <a href="#16-motivacion-de-la-sesion" class="md-nav__link">
    <span class="md-ellipsis">
      
        1.6 Motivación de la sesión
      
    </span>
  </a>
  
    <nav class="md-nav" aria-label="1.6 Motivación de la sesión">
      <ul class="md-nav__list">
        
          <li class="md-nav__item">
  <a href="#161-caso-la-configuracion-que-no-crece-igual-que-el-sistema" class="md-nav__link">
    <span class="md-ellipsis">
      
        1.6.1 Caso: la configuración que no crece igual que el sistema
      
    </span>
  </a>
  
</li>
        
      </ul>
    </nav>
  
</li>
        
          <li class="md-nav__item">
  <a href="#17-ubicacion-en-el-curso" class="md-nav__link">
    <span class="md-ellipsis">
      
        1.7 Ubicación en el curso
      
    </span>
  </a>
  
</li>
        
      </ul>
    </nav>
  
</li>
      
        <li class="md-nav__item">
  <a href="#2-explica" class="md-nav__link">
    <span class="md-ellipsis">
      
        2. Explica
      
    </span>
  </a>
  
    <nav class="md-nav" aria-label="2. Explica">
      <ul class="md-nav__list">
        
          <li class="md-nav__item">
  <a href="#21-arquitectura-de-la-sesion" class="md-nav__link">
    <span class="md-ellipsis">
      
        2.1 Arquitectura de la sesión
      
    </span>
  </a>
  
</li>
        
          <li class="md-nav__item">
  <a href="#22-el-problema-de-la-configuracion-duplicada-entre-microservicios" class="md-nav__link">
    <span class="md-ellipsis">
      
        2.2 El problema de la configuración duplicada entre microservicios
      
    </span>
  </a>
  
</li>
        
          <li class="md-nav__item">
  <a href="#23-panorama-de-patrones-de-arquitectura-de-microservicios" class="md-nav__link">
    <span class="md-ellipsis">
      
        2.3 Panorama de patrones de arquitectura de microservicios
      
    </span>
  </a>
  
</li>
        
          <li class="md-nav__item">
  <a href="#24-config-server-y-config-repo-dos-responsabilidades-distintas" class="md-nav__link">
    <span class="md-ellipsis">
      
        2.4 Config Server y config-repo: dos responsabilidades distintas
      
    </span>
  </a>
  
    <nav class="md-nav" aria-label="2.4 Config Server y config-repo: dos responsabilidades distintas">
      <ul class="md-nav__list">
        
          <li class="md-nav__item">
  <a href="#241-que-es-el-patron-de-configuracion-centralizada" class="md-nav__link">
    <span class="md-ellipsis">
      
        2.4.1 Qué es el patrón de Configuración Centralizada
      
    </span>
  </a>
  
</li>
        
          <li class="md-nav__item">
  <a href="#242-configuracion-en-dev" class="md-nav__link">
    <span class="md-ellipsis">
      
        2.4.2 Configuración en DEV
      
    </span>
  </a>
  
</li>
        
          <li class="md-nav__item">
  <a href="#243-configuracion-en-prod-local" class="md-nav__link">
    <span class="md-ellipsis">
      
        2.4.3 Configuración en PROD local
      
    </span>
  </a>
  
</li>
        
      </ul>
    </nav>
  
</li>
        
          <li class="md-nav__item">
  <a href="#25-convencion-de-nombres-aplicacion-perfilyml" class="md-nav__link">
    <span class="md-ellipsis">
      
        2.5 Convención de nombres: {aplicación}-{perfil}.yml
      
    </span>
  </a>
  
</li>
        
          <li class="md-nav__item">
  <a href="#26-config-server-en-dev-y-en-produccion-local" class="md-nav__link">
    <span class="md-ellipsis">
      
        2.6 Config Server en DEV y en producción local
      
    </span>
  </a>
  
</li>
        
          <li class="md-nav__item">
  <a href="#27-observabilidad-diagnosticar-un-perfil-no-encontrado" class="md-nav__link">
    <span class="md-ellipsis">
      
        2.7 Observabilidad: diagnosticar un perfil no encontrado
      
    </span>
  </a>
  
</li>
        
      </ul>
    </nav>
  
</li>
      
        <li class="md-nav__item">
  <a href="#3-aplica-actividad-practica-guiada" class="md-nav__link">
    <span class="md-ellipsis">
      
        3. Aplica: actividad práctica guiada
      
    </span>
  </a>
  
    <nav class="md-nav" aria-label="3. Aplica: actividad práctica guiada">
      <ul class="md-nav__list">
        
          <li class="md-nav__item">
  <a href="#31-verificar-el-punto-de-partida" class="md-nav__link">
    <span class="md-ellipsis">
      
        3.1 Verificar el punto de partida
      
    </span>
  </a>
  
</li>
        
          <li class="md-nav__item">
  <a href="#32-crear-la-carpeta-infra" class="md-nav__link">
    <span class="md-ellipsis">
      
        3.2 Crear la carpeta infra
      
    </span>
  </a>
  
</li>
        
          <li class="md-nav__item">
  <a href="#33-crear-el-proyecto-pagatu-config" class="md-nav__link">
    <span class="md-ellipsis">
      
        3.3 Crear el proyecto pagatu-config
      
    </span>
  </a>
  
</li>
        
          <li class="md-nav__item">
  <a href="#34-habilitar-config-server" class="md-nav__link">
    <span class="md-ellipsis">
      
        3.4 Habilitar Config Server
      
    </span>
  </a>
  
</li>
        
          <li class="md-nav__item">
  <a href="#35-configurar-pagatu-config-para-leer-config-repo-en-dev" class="md-nav__link">
    <span class="md-ellipsis">
      
        3.5 Configurar pagatu-config para leer config-repo en DEV
      
    </span>
  </a>
  
</li>
        
          <li class="md-nav__item">
  <a href="#36-probar-pagatu-config-en-dev" class="md-nav__link">
    <span class="md-ellipsis">
      
        3.6 Probar pagatu-config en DEV
      
    </span>
  </a>
  
</li>
        
          <li class="md-nav__item">
  <a href="#37-mover-la-configuracion-de-pagatu-catalogo-ms-a-config-repo" class="md-nav__link">
    <span class="md-ellipsis">
      
        3.7 Mover la configuración de pagatu-catalogo-ms a config-repo
      
    </span>
  </a>
  
</li>
        
          <li class="md-nav__item">
  <a href="#38-consultar-los-perfiles-por-http" class="md-nav__link">
    <span class="md-ellipsis">
      
        3.8 Consultar los perfiles por HTTP
      
    </span>
  </a>
  
    <nav class="md-nav" aria-label="3.8 Consultar los perfiles por HTTP">
      <ul class="md-nav__list">
        
          <li class="md-nav__item">
  <a href="#381-probar-una-consulta-incorrecta-para-aprender-del-error" class="md-nav__link">
    <span class="md-ellipsis">
      
        3.8.1 Probar una consulta incorrecta para aprender del error
      
    </span>
  </a>
  
</li>
        
      </ul>
    </nav>
  
</li>
        
          <li class="md-nav__item">
  <a href="#39-conectar-pagatu-catalogo-ms-como-config-client" class="md-nav__link">
    <span class="md-ellipsis">
      
        3.9 Conectar pagatu-catalogo-ms como Config Client
      
    </span>
  </a>
  
</li>
        
          <li class="md-nav__item">
  <a href="#310-levantar-pagatu-catalogo-ms-en-dev-con-configuracion-externa" class="md-nav__link">
    <span class="md-ellipsis">
      
        3.10 Levantar pagatu-catalogo-ms en DEV con configuración externa
      
    </span>
  </a>
  
</li>
        
          <li class="md-nav__item">
  <a href="#311-dockerizar-pagatu-config-para-produccion-local-opcional" class="md-nav__link">
    <span class="md-ellipsis">
      
        3.11 Dockerizar pagatu-config para producción local (opcional)
      
    </span>
  </a>
  
</li>
        
          <li class="md-nav__item">
  <a href="#312-compartir-red-entre-pagatu-config-y-pagatu-catalogo-ms-en-produccion-local-opcional" class="md-nav__link">
    <span class="md-ellipsis">
      
        3.12 Compartir red entre pagatu-config y pagatu-catalogo-ms en producción local (opcional)
      
    </span>
  </a>
  
</li>
        
          <li class="md-nav__item">
  <a href="#313-probar-pagatu-config-y-pagatu-catalogo-ms-en-produccion-local-opcional" class="md-nav__link">
    <span class="md-ellipsis">
      
        3.13 Probar pagatu-config y pagatu-catalogo-ms en producción local (opcional)
      
    </span>
  </a>
  
</li>
        
          <li class="md-nav__item">
  <a href="#314-revisar-logs-y-bajar-el-entorno-opcional" class="md-nav__link">
    <span class="md-ellipsis">
      
        3.14 Revisar logs y bajar el entorno (opcional)
      
    </span>
  </a>
  
</li>
        
      </ul>
    </nav>
  
</li>
      
        <li class="md-nav__item">
  <a href="#4-crea-actividad-autonoma" class="md-nav__link">
    <span class="md-ellipsis">
      
        4. Crea: actividad autónoma
      
    </span>
  </a>
  
    <nav class="md-nav" aria-label="4. Crea: actividad autónoma">
      <ul class="md-nav__list">
        
          <li class="md-nav__item">
  <a href="#41-actividad" class="md-nav__link">
    <span class="md-ellipsis">
      
        4.1 Actividad
      
    </span>
  </a>
  
</li>
        
          <li class="md-nav__item">
  <a href="#42-proposito" class="md-nav__link">
    <span class="md-ellipsis">
      
        4.2 Propósito
      
    </span>
  </a>
  
</li>
        
          <li class="md-nav__item">
  <a href="#43-indicaciones" class="md-nav__link">
    <span class="md-ellipsis">
      
        4.3 Indicaciones
      
    </span>
  </a>
  
    <nav class="md-nav" aria-label="4.3 Indicaciones">
      <ul class="md-nav__list">
        
          <li class="md-nav__item">
  <a href="#431-estructura-del-informe" class="md-nav__link">
    <span class="md-ellipsis">
      
        4.3.1 Estructura del informe
      
    </span>
  </a>
  
</li>
        
      </ul>
    </nav>
  
</li>
        
          <li class="md-nav__item">
  <a href="#44-criterios-minimos-de-aceptacion" class="md-nav__link">
    <span class="md-ellipsis">
      
        4.4 Criterios mínimos de aceptación
      
    </span>
  </a>
  
</li>
        
          <li class="md-nav__item">
  <a href="#45-preguntas-de-defensa" class="md-nav__link">
    <span class="md-ellipsis">
      
        4.5 Preguntas de defensa
      
    </span>
  </a>
  
</li>
        
          <li class="md-nav__item">


