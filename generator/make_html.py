#!/usr/bin/env python

import html
import json


def get_categories(inv):
    categories = []
    for k, v in inv.items():
        for c in v["categories"]:
            if c not in categories:
                categories.append(c)
    return sorted(categories)


def get_category_inputs(categories):
    i = 2 * " "
    s = f'{i}<input type="radio" id="all" name="categories" value="all" checked>'
    for c in categories:
        cns = c.replace(" ", "")
        s += f'\n{i}<input type="radio" id="{cns}" name="categories" value="{cns}">'
    return s


def get_category_filters(categories):
    i = 4 * " "
    s = f'{i}<li><label for="all">all</label></li>'
    for c in categories:
        cns = c.replace(" ", "")
        s += f'\n{i}<li><label for="{cns}">{c}</label></li>'
    return s


def get_inventory_html(inv):
    s = ""
    for k, v in inv.items():
        figure = v["figure"]
        item = html.escape(k).encode("ascii", "xmlcharrefreplace").decode("utf-8")
        price = (
            html.escape(v["price"]).encode("ascii", "xmlcharrefreplace").decode("utf-8")
        )
        if v["notes"]:
            price += (
                "  ("
                + (
                    html.escape(v["notes"])
                    .encode("ascii", "xmlcharrefreplace")
                    .decode("utf-8")
                )
                + ")"
            )
        ingredients = (
            html.escape(". ".join(v["ingredients"]))
            .encode("ascii", "xmlcharrefreplace")
            .decode("utf-8")
        )

        s += f"""
    <li class="menuitem" data-category="MyCategories">
       {figure}
       <h2>{item}</h2>
       <p class="price">{price}</p>
       <p class="ingredients">{ingredients}</p>
    </li>
""".replace(
            "MyCategories", " ".join([i.replace(" ", "") for i in v["categories"]])
        )
    return s


def generate_html(inv):

    template = r"""<!DOCTYPE html>
<html>
<head>
<title>minnie bakery</title>
<link rel="icon" href="https://minyoung-baker.github.io/stg/img/logo_print_sq.png">
</head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="css/w3mod.css">
<link rel="stylesheet" href="css/lato.css">
<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.2.0/css/all.css" integrity="sha384-hWVjflwFxL6sNzntih27bfxkr27PmbbK/iSvJ+a4+0owXq79v+lsFkW54bOGbiDQ" crossorigin="anonymous">
<link rel="stylesheet" href="css/minniebakery.css">
<link rel="stylesheet" href="css/filter.css">

<body id="#top">

<!-- Navbar (sit on top) -->
<div class="w3-top">
  <div class="w3-bar w3-text-white" id="myNavbar">
    <a class="w3-bar-item w3-button w3-hover-black w3-hide-medium w3-hide-large w3-right" href="javascript:void(0);" onclick="toggleFunction()" title="Toggle Navigation Menu">
      <i class="fa fa-bars"></i>
    </a>
    <a href="#top" class="w3-bar-item w3-button w3-hide-small"><i class="fa fa-long-arrow-alt-up"></i> TOP</a>
    <a href="#menu" class=" w3-bar-item w3-button w3-hide-small"><i class="fa fa-utensils"></i> MENU</a>
    <a href="#order" class=" w3-bar-item w3-button w3-hide-small"><i class="fa fa-shopping-cart"></i> ORDER</a>
  </div>

  <!-- Navbar on small screens -->
  <div id="menubar" class="w3-bar-block w3-white w3-hide w3-hide-large w3-hide-medium">
    <a href="#top" class="w3-text-black w3-bar-item w3-button" onclick="toggleFunction()">TOP</a>
    <a href="#menu" class="w3-text-black w3-bar-item w3-button" onclick="toggleFunction()">MENU</a>
    <a href="#order" class="w3-text-black w3-bar-item w3-button" onclick="toggleFunction()">ORDER</a>
  </div>
</div>

<!-- From: https://hibbard.eu/display-ui-blocking-overlay-on-page-load/ -->
<!-- To disable, comment out until ... -->
<!-- <div id="announcement"> -->
<!--   <h2>temporary closure.</h2> -->
<!--   <p>We're temporarily closed.</p> -->
<!--   <p>We will be back to baking on <b>August 12</b>, and we look forward to serving you then!</p> -->
<!--   <p>In the meantime, we apologize for any inconvenience this causes.</p> -->
<!--   <a id="close" href="#">Close</a> -->
<!-- </div> -->
<!-- <script src="https://code.jquery.com/jquery-latest.js"></script> -->
<!-- <script> -->
<!--   jQuery.fn.center = function () { -->
<!--     var w = $(window); -->
<!--     this.css("position","absolute"); -->
<!--     this.css("top", Math.max(0, ( -->
<!--       (w.height() - $(this).outerHeight()) / 2) + w.scrollTop() -->
<!--     ) + "px"); -->
<!--     this.css("left", Math.max(0, ( -->
<!--       (w.width() - $(this).outerWidth()) / 2) + w.scrollLeft() -->
<!--     ) + "px"); -->
<!--     return this; -->
<!--   } -->
<!--   $('<div>', {id : 'overlay'}).appendTo('body'); -->
<!--   $("#announcement").fadeIn('slow').center(); -->
<!--   $("#close").click(function(e){ -->
<!--     $("#announcement").remove(); -->
<!--     $("#overlay").remove(); -->
<!--     e.preventDefault(); -->
<!--   }); -->
<!-- </script> -->
<!-- ... here. -->

<!-- First Parallax Image with Logo -->
<div class="bgimg-1 w3-display-container w3-padding-64">
  <div class="w3-display-middle" style="white-space:nowrap;">
    <div class="transbox">
      <img style="width:100%" src="img/logo_print_sq.png">
    </div>
    <div class="w3-center w3-padding-32" >
      <a href="#menu">
        <i class="fa fa-4x fa-arrow-circle-down" style="color: #ffffffaa"></i>
      </a>
    </div>
  </div>
</div>

<!-- Gap between Logo and First Section -->
<div class="w3-white w3-display-container w3-padding-32">
</div>

<!-- Second Parallax Image with Menu Text -->
<div class="bgimg-2 w3-display-container w3-opacity-min" id="menu">
  <div class="w3-display-middle">
    <span class="w3-center w3-padding-large w3-white w3-xxlarge w3-wide w3-opacity-min">MENU</span>
  </div>
</div>

<div class="w3-white w3-display-container w3-padding-32 w3-center">
MyCategoryInputs

  <ol class="filters">
MyCategoryFilters
  </ol>

  <ol class="menuitems">
MyInventory
  </ol>
</div>

<div id="myModal" class="modal">
  <span class="close" onclick="document.getElementById('myModal').style.display='none'">&times;</span>
  <img class="modal-content" id="img01">
  <div id="caption"></div>
</div>

<!-- Third Parallax Image with Order Text -->
<div class="bgimg-3 w3-display-container w3-opacity-min" id="order">
  <div class="w3-display-middle">
    <span class="w3-center w3-padding-large w3-white w3-xxlarge w3-wide w3-opacity-min">ORDER</span>
  </div>
</div>

<!-- Container (Order Section) -->
<div class="w3-content w3-container w3-padding-32">
  <div class="w3-row w3-section">
    <div class="w3-col w3-half w3-panel">
      <h2 class="w3-center">order by reservation.</h2>
      <br>
      <div class="w3-center w3-large w3-margin-bottom">
        <i class="fa fa-phone fa-fw w3-hover-text-black w3-xlarge w3-margin-right"></i>505-663-6202<br><br>
        <i class="fa fa-envelope fa-fw w3-hover-text-black w3-xlarge w3-margin-right"></i><a href="mailto:minyoung.baker@gmail.com?Subject=Minnie%20Bakery%20Order%20Reservation" target="_top">minyoung.baker@gmail.com</a><br><br>
      </div>
      <h2 class="w3-center">receive by pickup.</h2>
      <br>
      <div class="w3-center w3-large w3-margin-bottom">
        <i class="fa fa-building fa-fw w3-hover-text-black w3-xlarge w3-margin-right"></i>54 Canyon View Los Alamos, NM 87544 <br>
      </div>
    </div>
    <div class="w3-col w3-half w3-container">
      <img style="width:100%;height:400px" src="img/map_static.png">
      <!-- <div id="googleMap" class="w3-round-large w3-greyscale-min" style="width:100%;height:400px;"></div> -->
    </div>
  </div>
</div>

<!-- Footer -->
<footer class="w3-center w3-black w3-padding-32 w3-opacity">
  <!-- <a href="#top" class="w3-button w3-light-grey"><i class="fa fa-arrow-up w3-margin-right"></i>To the top</a> -->
  <div class="w3-xlarge w3-section">
    <a href="https://www.facebook.com/minniebakeryLLC"><i class="fab fa-facebook w3-hover-opacity"></i></a>
    <a href="https://www.instagram.com/minniebakeryLLC/"><i class="fab fa-instagram w3-hover-opacity"></i></a>
    <!-- <i class="fa fa-snapchat w3-hover-opacity"></i> -->
    <!-- <i class="fa fa-pinterest-p w3-hover-opacity"></i> -->
    <!-- <i class="fa fa-twitter w3-hover-opacity"></i> -->
    <!-- <i class="fa fa-linkedin w3-hover-opacity"></i> -->
  </div>
  <div class="w3-text-white w3-small w3-lighter">
    Copyright <i class="far fa-copyright"></i> 2021 minnie bakery LLC.  All rights reserved.
    <br>
    Both our menu and our website are cookie free.
  </div>
</footer>

<!-- Google Maps -->
<script>
  function myMap() {
    myCenter=new google.maps.LatLng( 35.881884, -106.310765 );
    var mapOptions= {
      center:myCenter,
      zoom:15, scrollwheel: false, draggable: true,
      mapTypeId:google.maps.MapTypeId.ROADMAP
    };
    var map=new google.maps.Map(document.getElementById("googleMap"),mapOptions);

    var marker = new google.maps.Marker({
      position: myCenter,
    });
    marker.setMap(map);
  }

  // Modal Image Gallery
  function onClick(element) {
    document.getElementById("img01").src = element.src;
    document.getElementById("modal01").style.display = "block";
    var captionText = document.getElementById("caption");
    captionText.innerHTML = element.alt;
  }

  // Change style of navbar on scroll
  window.onscroll = function() { myFunction() };
  function myFunction() {
      var navbar = document.getElementById("myNavbar");
      if (document.body.scrollTop > 100 || document.documentElement.scrollTop > 100) {
          navbar.className = "w3-bar" + " w3-card" + " w3-animate-top" + " w3-white" + " w3-text-black";
      } else {
          navbar.className = navbar.className.replace(" w3-card w3-animate-top w3-white w3-text-black", " w3-text-white");
      }
  }

  // Used to toggle the menu on small screens when clicking on the menu button
  function toggleFunction() {
      var x = document.getElementById("menubar");
      if (x.className.indexOf("w3-show") == -1) {
          x.className += " w3-show";
      } else {
          x.className = x.className.replace(" w3-show", "");
      }
  }
</script>
<script src="https://maps.googleapis.com/maps/api/js?key=AIzaSyB9KoT_IA8yG7HO0Mh7bjM50QcUyYiU6tM&callback=myMap"></script>

<!-- Modal zooming -->
<script src="https://ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js"></script>

<script>
  // Get the modal
  var modal = document.getElementById('myModal');

  // Get the image and insert it inside the modal - use its "alt" text as a caption
  var img = $('.modal_img');
  var modalImg = $("#img01");
  var captionText = document.getElementById("caption");
  $('.modal_img').click( function() {
      modal.style.display = "block";
      var newSrc = this.src.replace("_th400","");
      modalImg.attr('src', newSrc);
      captionText.innerHTML = this.alt;
  });

  // Get the <span> element that closes the modal
  var span = document.getElementsByClassName("close")[0];

  // When the user clicks on <span> (x), close the modal
  span.onclick = function() {
    modal.style.display = "none";
  }

  // When the user clicks anywhere outside of the modal, close it
  window.onclick = function(event) {
    if (event.target == modal) {
      modal.style.display = "none";
    }
  }
</script>

<!-- Swap images on mouseover -->
<script>
  function hover(element) {
    var src = element.src;
    element.setAttribute('src', src.replace("_01", "_02"));
  }

  function unhover(element) {
    var src = element.src;
    element.setAttribute('src', src.replace("_02", "_01"));
  }
</script>

</body>
</html>
"""
    categories = get_categories(inv)
    s = template.replace("MyCategoryInputs", get_category_inputs(categories))
    s = s.replace("MyCategoryFilters", get_category_filters(categories))
    s = s.replace("MyInventory", get_inventory_html(inv))
    return s


def get_checked_filters(categories):
    s = '[value="all"]:checked ~ .filters [for="all"]'
    for c in categories:
        cns = c.replace(" ", "")
        s += f',\n[value="{cns}"]:checked ~ .filters [for="{cns}"]'
    s += """ {
  background: var(--brown);
  color: #ffffff;
}"""
    return s


def get_checked_menu_items(categories):
    s = """[value="all"]:checked ~ .menuitems [data-category] {
  display: block;
}

"""
    for c in categories[:-1]:
        cns = c.replace(" ", "")
        s += f'[value="{cns}"]:checked ~ .menuitems .menuitem:not([data-category~="{cns}"]),\n'
    cns = categories[-1].replace(" ", "")
    s += f'[value="{cns}"]:checked ~ .menuitems .menuitem:not([data-category~="{cns}"])'
    s += """ {
  display: none;
}"""
    return s


def generate_css(inv):
    template = """
ol {
  list-style: none;
}

input[type="radio"] {
  position: absolute;
  left: -9999px;
}

.menuitems {
  display: grid;
  grid-gap: 1.5rem;
  grid-template-columns: repeat( auto-fill, minmax(400px, 1fr) );
}

.menuitems .menuitem {
  box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
  text-align: center;
  margin: 5%;
}

/* FILTERS
–––––––––––––––––––––––––––––––––––––––––––––––––– */
.filters {
  text-align: center;
  margin-bottom: 2rem;
}

.filters * {
  display: inline-block;
}

.filters label {
  padding: 0.5rem 1rem;
  margin-bottom: 0.25rem;
  border-radius: 2rem;
  min-width: 50px;
  line-height: normal;
  cursor: pointer;
  transition: all 0.1s;
  border-style: solid;
  border-width: 1px;
  border-color: var(--brown);
}

.filters label:hover {
  background: var(--brown);
  color: #ffffff;
}

/* FILTERING RULES
–––––––––––––––––––––––––––––––––––––––––––––––––– */

MyCheckedFilters

MyCheckedMenuItems
"""

    categories = get_categories(inv)
    s = template.replace("MyCheckedFilters", get_checked_filters(categories))
    s = s.replace("MyCheckedMenuItems", get_checked_menu_items(categories))
    return s


with open("website_items.json") as json_file:
    inv = json.load(json_file)

f = open("../index.html", "w")
f.write(generate_html(inv))
f.close()

f = open("../css/filter.css", "w")
f.write(generate_css(inv))
f.close()
