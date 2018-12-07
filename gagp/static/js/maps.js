function csrfSafeMethod(method) {
  return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}


$.ajaxSetup({
  beforeSend: function(xhr, settings) {
    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
      xhr.setRequestHeader('X-CSRFToken', csrftoken);
    }
  }
});

var geocoder;
var map;
var myLatLng = {lat:39.7285, lng:-121.8375};



function initMap() {
  //alert('You in the initMap()')
        geocoder =  new google.maps.Geocoder();
        map = new google.maps.Map(document.getElementById('map'), {
          zoom: 11,
          center: myLatLng
        });
        //get_locations();
        get_data();

}


function get_data() {
  $.post('/get_data/')
    .done(function(result) {
      drop(result[0], result[1])
      //drop(result);
    });
}
google.maps.event.addDomListener(window, 'load', initMap);

function fillmodal(event_id) {
    // var info = title.split(",")
    // $('.modal-header .modal-title').text(info[0])
    // $(".modal-body").text('Sport: ' + info[1] +
    //                       '\nDate of event: ' + info[2] +
    //                       '\nTime of event: ' + info[3] +
    //                       '\nCreated by: ' + info[4]);
    // $("#myModal").modal("toggle")
    //alert(event_id)
    // $.get('/events/view/' + event_id)
    $.ajax({
      url: '/events/view/' + event_id + '/',
      type: 'GET',
      data: {
        id: event_id
      },
      error: function (xhr, textStatus, thrownError){
        alert("failure: " + xhr.statusText);
      },
      success: function(response) {
        //alert('Success')
        window.location.href = '/events/view/' + event_id
      }
    })


}

function drop(locations, events) {
  for (var i = 0; i < locations.length; i++) {
    var event_list = ''
    for(var e = 0; e < events.length; e++)
    {
      if(events[e]['location']['name'] == locations[i]['name'])
      {
        //console.log(events)
        event_list +=  '<div class="container">' +
                         // '<button class="btn btn-primary" onclick="fillmodal(\''+ events[e]['name'] + ','
                         //                                + events[e]['activity'] + ','
                         //                                + events[e]['date_of_event'] + ','
                         //                                + events[e]['time_of_event'] + ','
                         //                                + events[e]['created_by'] + ','
                         //                                + events[e]['attendees'] + '\')"'  + '>'+
                         '<button class="btn btn-primary" onclick="fillmodal(\'' + events[e]['id'] + '\')"' + '>'+
                              events[e]['name'] +
                         '</button>' +
                        '</div><br>';
      }
    }
    if(event_list == '') {
      event_list = '<h6>No events posted.</h6>'
    }
    contentString = '<h3>' + locations[i]['name'] + '</h3>' +
                    '<h5> Events at this location: </h5>' +
                      event_list + '<br>' +
                    // '<input type="button" onclick="showForm()" value="Create Event here." />'
                    '<a href="#" data-toggle="modal" data-target="#eventForm">Create Event Here</a>'
    var infoWindow = new google.maps.InfoWindow({
      content: contentString,
      maxWidth:500,
      maxHeight:200
    })
  //  alert(locations[i]['address'] + locations[i]['city'])
    codeAddress(locations[i]['address'] + ' ' + locations[i]['city'], infoWindow, i*200);
  }
}

function codeAddress(address, infoWindow, timeout) {
    markers = [];
    geocoder.geocode( {'address':address}, function(results, status) {
        setTimeout(function() {
          if (status == 'OK') {
            var marker = new google.maps.Marker({
                map: map,
                animation: google.maps.Animation.DROP,
                position: results[0].geometry.location,
                infowindow: infoWindow
            });
            markers.push(marker)
            google.maps.event.addListener(marker, 'click', function() {
              closeMarkers(map,markers);
              map.panTo(marker.getPosition())
              infoWindow.open(map, marker);
            })
            google.maps.event.addListener(map, 'drag', function() {
              closeMarkers(map,markers);
            })
          }
        }, timeout)
    })
}

function closeMarkers(map,markers) {
  markers.forEach(function(marker) {
    marker.infowindow.close(map,marker);
  })
}
