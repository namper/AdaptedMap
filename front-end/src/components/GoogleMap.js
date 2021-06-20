import React, { Component, useEffect, useState, useRef, useMemo } from "react";
import { Map, Marker, GoogleApiWrapper, InfoWindow } from "google-maps-react";
import PlacesAutocomplete, {
  geocodeByAddress,
  getLatLng,
} from "react-places-autocomplete";
import MainIcon from "../assets/main-icon.png";
import axios from "axios";
import FormData, { from } from "form-data";
import { Camera } from "./Camera";

const apiUrl = "http://d16a8647b722.ngrok.io";

const MapCountainer = (props) => {
  const [currLocation, setCurrLocation] = useState(null);
  const [markers, setMarkers] = useState(null);

  const [currLocationAddress, setCurrLocationAddress] = useState("");

  const [placedMarker, setPlacedMarker] = useState(null);

  useEffect(async () => {
    console.log("------------------->");
    const response = await axios.get(`${apiUrl}/api/map/markers/`);
    setAllMarkers(response.data);
    console.log("reponse", response);
  }, []);

  const [allMarkers, setAllMarkers] = useState([]);
  const [placingMarker, setPlacingMarker] = useState(false);
  const [state, setState] = useState({
    // for google map places autocomplete
    address: "",

    showingInfoWindow: false,
    activeMarker: {},
    selectedPlace: {},

    takingPhoto: false,

    mapCenter: {
      lat: 0,
      lng: 0,
    },
  });

  useEffect(() => {
    if ("geolocation" in navigator) {
      navigator.geolocation.getCurrentPosition(function (position) {
        setState({
          ...state,
          mapCenter: {
            lat: position.coords.latitude,
            lng: position.coords.longitude,
          },
        });
        setCurrLocation({
          lat: position.coords.latitude,
          lng: position.coords.longitude,
        });
      });
    } else {
      window.alert("location not avaliable");
      console.log("Not Available");
    }
    function handlePermission() {
      navigator.permissions
        .query({ name: "geolocation" })
        .then(function (result) {
          if (result.state == "granted") {
            report(result.state);
            // geoBtn.style.display = "none";
          } else if (result.state == "prompt") {
            report(result.state);
            // geoBtn.style.display = "none";
            // navigator.geolocation.getCurrentPosition(
            //   revealPosition,
            //   positionDenied,
            //   geoSettings
            // );
          } else if (result.state == "denied") {
            report(result.state);
            // geoBtn.style.display = "inline";
          }
          result.onchange = function () {
            report(result.state);
          };
        });
    }

    function report(state) {
      console.log("Permission p[k[" + state);
    }

    handlePermission();
  }, []);

  const mapRef = useRef("");

  const takePhoto = (cb) => {
    const picture = cb();
    console.log("picture taken", picture);
    setState({ ...state, takingPhoto: false });
  };

  useEffect(() => {
    setState({
      ...state,
      mapCenter: {
        lat: props?.currLocation?.lat,
        lng: props?.currLocation?.lng,
      },
    });
  }, []);

  const onMarkerClick = (props, marker, e) => {
    setState({
      ...state,
      selectedPlace: props,
      activeMarker: marker,
      showingInfoWindow: true,
    });
    getLocationByLatLng({ lat: marker.position.lat, lng: marker.position.lng });
  };
  const onMapClicked = (props) => {
    if (state.showingInfoWindow) {
      setState({ ...state, showingInfoWindow: false, activeMarker: null });
    }
  };

  const addMarkerToMap = async (picture) => {
    try {
      const formData = new FormData();
      formData.append(
        "name",
        await getLocationByLatLng({
          lat: placedMarker.lat,
          lng: placedMarker.lng,
        })
      );
      formData.append("lat", placedMarker.lat);
      formData.append("lng", placedMarker.lng);

      const response = await axios.post(`${apiUrl}/api/map/markers/`, formData);
      const formData2 = new FormData();
      formData2.append("image", picture);
      formData2.append("marker", response.data.id);

      const response2 = await axios.post(
        `${apiUrl}/api/map/markerImages/`,
        formData2,
        { headers: { "Content-Type": "multipart/form-data" } }
      );
      console.log("response===>", response2);
    } catch (e) {
      console.log("error---->", Object.keys(e));
      console.log(e.toJSON());
      console.log(e.response);
      console.log(e.request);
    }
  };

  const placeMarker = (location) => {
    setAllMarkers((prev) => [
      ...prev,
      {
        name: "added marker",
        lat: location.lat(),
        lng: location.lng(),
      },
    ]);
    setPlacedMarker({
      name: "added marker",

      lat: location.lat(),
      lng: location.lng(),
    });
  };

  console.log("allmarkers", allMarkers);

  useEffect(() => {
    console.log("mapref", mapRef.current.map);
  }, []);

  const handleSelect = (address) => {
    setState({ ...state, address });
    geocodeByAddress(address)
      .then((results) => getLatLng(results[0]))
      .then((latLng) => {
        console.log("Success", latLng);

        // update center state
        setState({ ...state, mapCenter: latLng });
      })
      .catch((error) => console.error("Error", error));
  };

  const handleChange = (address) => {
    setState({ ...state, address });
  };

  const getLocationByLatLng = async (latLng) => {
    setCurrLocationAddress("loading", latLng);

    // const latLngstr = `latlng=${latLng.lat()},${latLng.lng()}`;

    // console.log("curr marker locaiton", latLngstr);
    const response = await axios.get(
      `https://maps.googleapis.com/maps/api/geocode/json?latlng=44,44&key=AIzaSyDQeimZ39H_n6iAHIa-QK5AcYZQ7B5FULg`
    );

    setCurrLocationAddress(response.data.results?.[0]?.formatted_address);
    return response.data.results?.[0]?.formatted_address;
  };

  // const currentMarkerLocationString =  useMemo(async () => {
  //   return await getLocationByLatLng(state?.activeMarker?.position);
  // }, [state?.activeMarker]);

  const addMarkerHandler = () => {
    alert("add marker in map");
    console.log(state.activeMarker);
    props.google.maps.event.addListener(
      mapRef.current.map,
      "click",
      function (event) {
        console.log("mapcileckedfiurew");
        placeMarker(event.latLng);
        // placeMarker(event.latLng);
      }
    );
    setPlacingMarker(true);
    //setState({ ...state, takingPhoto: true });
  };

  const checkCurrentMarkers = async () => {
    const response = await axios.post(`${apiUrl}/api/map/markers/`);
    console.log("----->", response);
    setAllMarkers(response.data);
    setState({ ...state, takingPhoto: true });
  };

  return (
    <div>
      <div>
        <div
          style={{
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
            width: "100vw",
            height: "100vh",
          }}
        >
          {state.takingPhoto ? (
            <Camera
              takePhoto={takePhoto}
              setState={setState}
              addMarkerToMap={addMarkerToMap}
            />
          ) : (
            <>
              <PlacesAutocomplete
                value={state.address}
                onChange={handleChange}
                onSelect={handleSelect}
              >
                {({
                  getInputProps,
                  suggestions,
                  getSuggestionItemProps,
                  loading,
                }) => (
                  <div>
                    <input
                      {...getInputProps({
                        placeholder: "Search Places ...",
                        className: "location-search-input",
                      })}
                    />
                    <div className="autocomplete-dropdown-container">
                      {loading && <div>Loading...</div>}
                      {suggestions.map((suggestion) => {
                        const className = suggestion.active
                          ? "suggestion-item--active"
                          : "suggestion-item";
                        // inline style for demonstration purpose
                        const style = suggestion.active
                          ? { backgroundColor: "#fafafa", cursor: "pointer" }
                          : { backgroundColor: "#ffffff", cursor: "pointer" };
                        return (
                          <div
                            {...getSuggestionItemProps(suggestion, {
                              className,
                              style,
                            })}
                          >
                            <span>{suggestion.description}</span>
                          </div>
                        );
                      })}
                    </div>
                  </div>
                )}
              </PlacesAutocomplete>
              <Map
                ref={mapRef}
                className={"map"}
                google={props.google}
                initialCenter={{
                  lat: state.mapCenter.lat,
                  lng: state.mapCenter.lng,
                }}
                center={{
                  lat: state.mapCenter.lat,
                  lng: state.mapCenter.lng,
                }}
              >
                {allMarkers?.map((marker) => {
                  console.log("m", marker);
                  return (
                    <Marker
                      key={Math.random()}
                      onClick={onMarkerClick}
                      name={marker.name}
                      position={{
                        lat: marker?.lat,
                        lng: marker?.lng,
                      }}
                    />
                  );
                })}
                <Marker
                  key={Math.random()}
                  onClick={onMarkerClick}
                  name={"Current Location"}
                  position={{
                    lat: state.mapCenter.lat,
                    lng: state.mapCenter.lng,
                  }}
                />
                {/* <InfoWindow
                      marker={state.activeMarker}
                      visible={state.showingInfoWindow}
                    >
                      <div>
                        <h1>{state.selectedPlace.name}</h1>
                      </div>
                    </InfoWindow> */}
              </Map>
              {state.showingInfoWindow ? (
                <div className={"details-wrapper"}>
                  {state.activeMarker?.photo ? (
                    <img src={state.activeMarker?.photo} />
                  ) : (
                    <div className="details-no-imgs">No images</div>
                  )}
                  <div>location - {currLocationAddress}</div>
                  <button
                    onClick={() =>
                      setState({ ...state, showingInfoWindow: false })
                    }
                  >
                    close
                  </button>
                  <button
                    className="upload-photo-details"
                    onClick={() => {
                      setState({ ...state, takingPhoto: true });
                    }}
                  >
                    <div className="upload-photo-text">ატვირთე ფოტო</div>
                  </button>
                </div>
              ) : (
                <>
                  <button
                    className="upload-photo-wrapper"
                    onClick={() => {
                      addMarkerHandler();
                    }}
                  >
                    <div className="upload-photo-text">+</div>
                  </button>

                  {placingMarker && (
                    <button
                      onClick={() => checkCurrentMarkers()}
                      className="upload-photo-wrapper-right"
                    >
                      add
                    </button>
                  )}
                </>
              )}
            </>
          )}
        </div>
      </div>
    </div>
  );
};

export default GoogleApiWrapper({
  apiKey: "AIzaSyDQeimZ39H_n6iAHIa-QK5AcYZQ7B5FULg",
})(MapCountainer);
