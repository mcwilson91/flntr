var LatLng = {lat: parseFloat("{{flat.latitude}}"), lng: parseFloat("{{flat.longitude}}")};

var map;

function initMap() {
  map = new google.maps.Map(document.getElementById('flat-view-map'), {
  zoom: 16,
  center: LatLng
});

var marker = new google.maps.Marker({
  position:  LatLng,
  map: map,
  title: "{{flat.title}}"
});

}


$(document).ready(function() {

var foodmarker1 = new google.maps.Marker({
  position:  {lat : 55.877671, lng : -4.289873},

  title: "Oran Mor",
  icon: '{% static "map_pins/food-pin.png" %}',
  animation: google.maps.Animation.DROP
});

var foodmarker2 = new google.maps.Marker({
  position:  {lat : 55.874955, lng : -4.293167},

  title: "Ubiquitous Chip",
  icon: '{% static "map_pins/food-pin.png" %}',
  animation: google.maps.Animation.DROP
});

var foodmarker3 = new google.maps.Marker({
  position:  {lat : 55.866972, lng : -4.289219},

  title: "Butchershop Bar & Grill",
  icon: '{% static "map_pins/food-pin.png" %}',
  animation: google.maps.Animation.DROP
});

var foodmarker4 = new google.maps.Marker({
  position:  {lat : 55.864569, lng : -4.283339},

  title: "Fanny Trollopes",
  icon: '{% static "map_pins/food-pin.png" %}',
  animation: google.maps.Animation.DROP
});

var foodmarker5 = new google.maps.Marker({
  position:  {lat : 55.870842, lng : -4.298903},

  title: "No. 16",
  icon: '{% static "map_pins/food-pin.png" %}',
  animation: google.maps.Animation.DROP
});

var foodmarker6 = new google.maps.Marker({
  position:  {lat : 55.874940, lng : -4.280578},

  title: "Inn Deep",
  icon: '{% static "map_pins/food-pin.png" %}',
  animation: google.maps.Animation.DROP
});

var foodmarker7 = new google.maps.Marker({
  position:  {lat : 55.878051, lng : -4.322470},

  title: "Wee Lochan",
  icon: '{% static "map_pins/food-pin.png" %}',
  animation: google.maps.Animation.DROP
});

var foodmarker8 = new google.maps.Marker({
  position:  {lat : 55.877003, lng : -4.290612},

  title: "Hillhead Bookclub",
  icon: '{% static "map_pins/food-pin.png" %}',
  animation: google.maps.Animation.DROP
});





var entmarker1 = new google.maps.Marker({
  position:  {lat : 55.874567, lng : -4.293186},

  title: "Grosvenor Cinema",
  icon: '{% static "map_pins/ent-pin.png" %}',
  animation: google.maps.Animation.DROP
});

var entmarker2 = new google.maps.Marker({
  position:  {lat : 55.8685891, lng : -4.2906039},

  title: "Kelvingrove Art Gallery and Museum",
  icon: '{% static "map_pins/ent-pin.png" %}',
  animation: google.maps.Animation.DROP
});

var entmarker3 = new google.maps.Marker({
  position:  {lat : 55.858743, lng : -4.294550},

  title: "Glasgow Science Centre",
  icon: '{% static "map_pins/ent-pin.png" %}',
  animation: google.maps.Animation.DROP
});

var entmarker4 = new google.maps.Marker({
  position:  {lat : 55.879456, lng : -4.291471},

  title: "Glasgow Botanic Gardens",
  icon: '{% static "map_pins/ent-pin.png" %}',
  animation: google.maps.Animation.DROP
});

var entmarker5 = new google.maps.Marker({
  position:  {lat : 55.860129, lng : -4.285279},

  title: "The Hydro",
  icon: '{% static "map_pins/ent-pin.png" %}',
  animation: google.maps.Animation.DROP
});



var sportmarker1 = new google.maps.Marker({
  position:  {lat : 55.872911, lng : -4.285293},

  title: "Glasgow University Stevenson Building",
  icon: '{% static "map_pins/gym-pin.png" %}',
  animation: google.maps.Animation.DROP
});

var sportmarker2 = new google.maps.Marker({
  position:  {lat : 55.850685, lng : -4.305372},

  title: "Glasgow Climbing Centre",
  icon: '{% static "map_pins/gym-pin.png" %}',
  animation: google.maps.Animation.DROP
});

var sportmarker3 = new google.maps.Marker({
  position:  {lat : 55.860129, lng : -4.285279},

  title: "Kelvin Hall",
  icon: '{% static "map_pins/gym-pin.png" %}',
  animation: google.maps.Animation.DROP
});




var shopmarker1 = new google.maps.Marker({
  position:  {lat : 55.875464, lng : -4.294590},

  title: "Ruthven Mews Arcade",
  icon: '{% static "map_pins/shop-pin.png" %}',
  animation: google.maps.Animation.DROP
});

var shopmarker2 = new google.maps.Marker({
  position:  {lat : 55.864518, lng : -4.283165},

  title: "The Shop of Interest",
  icon: '{% static "map_pins/shop-pin.png" %}',
  animation: google.maps.Animation.DROP
});

var shopmarker3 = new google.maps.Marker({
  position:  {lat : 55.875019, lng : -4.281039},

  title: "The Glasgow Vintage Co.",
  icon: '{% static "map_pins/shop-pin.png" %}',
  animation: google.maps.Animation.DROP
});

var shopmarker4 = new google.maps.Marker({
  position:  {lat : 55.872185, lng : -4.312336},

  title: "West End Retail Park",
  icon: '{% static "map_pins/shop-pin.png" %}',
  animation: google.maps.Animation.DROP
});


$('#food_check').change(function() {
    if(this.checked) {
        foodmarker1.setMap(map);
        foodmarker2.setMap(map);
        foodmarker3.setMap(map);
        foodmarker4.setMap(map);
        foodmarker5.setMap(map);
        foodmarker6.setMap(map);
        foodmarker7.setMap(map);
        foodmarker8.setMap(map);
    } else {
        foodmarker1.setMap(null);
        foodmarker2.setMap(null);
        foodmarker3.setMap(null);
        foodmarker4.setMap(null);
        foodmarker5.setMap(null);
        foodmarker6.setMap(null);
        foodmarker7.setMap(null);
        foodmarker8.setMap(null);
    }
});

$('#ent_check').change(function() {
    if(this.checked) {
        entmarker1.setMap(map);
        entmarker2.setMap(map);
        entmarker3.setMap(map);
        entmarker4.setMap(map);
        entmarker5.setMap(map);
    } else {
        entmarker1.setMap(null);
        entmarker2.setMap(null);
        entmarker3.setMap(null);
        entmarker4.setMap(null);
        entmarker5.setMap(null);
    }
});


$('#sport_check').change(function() {
    if(this.checked) {
        sportmarker1.setMap(map);
        sportmarker2.setMap(map);
        sportmarker3.setMap(map);
    } else {
        sportmarker1.setMap(null);
        sportmarker2.setMap(null);
        sportmarker3.setMap(null);
    }
});

$('#shop_check').change(function() {
    if(this.checked) {
        shopmarker1.setMap(map);
        shopmarker2.setMap(map);
        shopmarker3.setMap(map);
        shopmarker4.setMap(map);
    } else {
        shopmarker1.setMap(null);
        shopmarker2.setMap(null);
        shopmarker3.setMap(null);
        shopmarker4.setMap(null);
    }
});

});
