function getLocation() {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(sendLocationToServer);
    } else {
      // If geolocation is not supported, send the location of New York
      sendLocationToServer({
        coords: {
          latitude: 40.7128,
          longitude: -74.0060,
        },
      });
    }
  }
  
  function sendLocationToServer(position) {
    fetch(`/set-location?lat=${position.coords.latitude}&long=${position.coords.longitude}`);
  }
  