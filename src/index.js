import 'bootstrap/dist/css/bootstrap.css';
import 'leaflet/dist/leaflet.css'
import './index.css';

import React from 'react';
import ReactDOM from 'react-dom';

import FlightDashboard from './components/Dashboard/FlightDashboard';
import Header from './components/Header/Header';
import FooterPage from './components/Footer/Footer';

import * as serviceWorker from './serviceWorker';

import USAFlights from './assets/USAFlights';

import Airports from './assets/Airports';
import FlightPathStats from './assets/FlightPathStats';
import States from './assets/States';
import StatesToAirports from './assets/StatesToAirports';
import Years from './assets/Years';


// ReactDOM.render(<App />, document.getElementById('root'));
// ReactDOM.render(<Controller />, document.getElementById('flight-select'));
ReactDOM.render(
    <Header />,
    document.getElementById('header')
);
ReactDOM.render(
    <FlightDashboard
        flightData={USAFlights}
        airportsData={Airports}
        flightPathStats={FlightPathStats}
        statesData={States}
        statesToAirportsData={StatesToAirports}
        yearsData={Years.sort().reverse()} />,
    document.getElementById('flight-dashboard')
);
ReactDOM.render(
    <FooterPage/>,
    document.getElementById('footer')
);



// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: http://bit.ly/CRA-PWA
serviceWorker.unregister();
