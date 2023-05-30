function getLocation() {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(sendLocationToServer);
    } else {
      //default location of New York, NY if geolocation is not supported
      sendLocationToServer({
        coords: {
          latitude: 27.9506,
          longitude: -82.4572,
        },
      });
    }
  }
  
function sendLocationToServer(position) {
    fetch(`/set-location?lat=${position.coords.latitude}&lon=${position.coords.longitude}`);
    
}

//call the function when the script is loaded
getLocation();