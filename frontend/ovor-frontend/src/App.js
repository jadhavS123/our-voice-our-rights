import React, { useState, useEffect } from 'react';
import axios from 'axios';
import About from './About';
import { EmploymentChart, ExpenditureChart } from './Charts';
import './App.css';

function App() {
  const [districts, setDistricts] = useState([]);
  const [selectedDistrict, setSelectedDistrict] = useState('');
  const [mgnregaData, setMgnregaData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [currentPage, setCurrentPage] = useState('dashboard'); // 'dashboard' or 'about'
  const [geolocationSupported, setGeolocationSupported] = useState(false);

  // Fetch districts on component mount
  useEffect(() => {
    fetchDistricts();
    // Check if geolocation is supported
    if (navigator.geolocation) {
      setGeolocationSupported(true);
    }
  }, []);

  const fetchDistricts = async () => {
    try {
      const response = await axios.get('http://localhost:8000/api/districts/');
      setDistricts(response.data);
    } catch (error) {
      console.error('Error fetching districts:', error);
    }
  };

  const fetchMGNREGAData = async () => {
    if (!selectedDistrict) return;
    
    setLoading(true);
    try {
      const response = await axios.get(`http://localhost:8000/api/performance/${selectedDistrict}/`);
      setMgnregaData(response.data);
    } catch (error) {
      console.error('Error fetching MGNREGA data:', error);
    } finally {
      setLoading(false);
    }
  };

  const detectUserLocation = () => {
    if (!navigator.geolocation) {
      alert('Geolocation is not supported by your browser');
      return;
    }
    
    setLoading(true);
    navigator.geolocation.getCurrentPosition(
      async (position) => {
        try {
          // In a real implementation, you would use a reverse geocoding service
          // to convert coordinates to district names
          // For demo purposes, we'll just show an alert
          alert(`Latitude: ${position.coords.latitude}, Longitude: ${position.coords.longitude}\n\nIn a production app, this would automatically detect your district.`);
          
          // Example of how you might implement this in a real app:
          /*
          const response = await axios.get(`http://localhost:8000/api/detect-district/`, {
            params: {
              lat: position.coords.latitude,
              lon: position.coords.longitude
            }
          });
          
          if (response.data.district) {
            setSelectedDistrict(response.data.district);
            fetchMGNREGAData();
          }
          */
        } catch (error) {
          console.error('Error detecting location:', error);
          alert('Could not detect your location. Please select your district manually.');
        } finally {
          setLoading(false);
        }
      },
      (error) => {
        console.error('Error getting location:', error);
        alert('Could not get your location. Please select your district manually.');
        setLoading(false);
      }
    );
  };

  const handleDistrictChange = (e) => {
    setSelectedDistrict(e.target.value);
  };

  const handleSearch = () => {
    fetchMGNREGAData();
  };

  const navigateTo = (page) => {
    setCurrentPage(page);
  };

  return (
    <div className="App">
      <nav className="navigation">
        <button 
          className={currentPage === 'dashboard' ? 'nav-button active' : 'nav-button'}
          onClick={() => navigateTo('dashboard')}
        >
          Dashboard
        </button>
        <button 
          className={currentPage === 'about' ? 'nav-button active' : 'nav-button'}
          onClick={() => navigateTo('about')}
        >
          About MGNREGA
        </button>
      </nav>

      {currentPage === 'dashboard' ? (
        <header className="App-header">
          <h1>Our Voice, Our Rights</h1>
          <h2>MGNREGA Performance Dashboard</h2>
          
          <div className="search-section">
            {geolocationSupported && (
              <button onClick={detectUserLocation} disabled={loading} className="location-button">
                📍 Detect My Location
              </button>
            )}
            <select value={selectedDistrict} onChange={handleDistrictChange}>
              <option value="">Select a District</option>
              {districts.map((district) => (
                <option key={district.id} value={district.district_name}>
                  {district.district_name}, {district.state_name}
                </option>
              ))}
            </select>
            <button onClick={handleSearch} disabled={!selectedDistrict || loading}>
              {loading ? 'Loading...' : 'Search'}
            </button>
          </div>

          {mgnregaData.length > 0 && (
            <div className="data-display">
              <h3>Performance Data for {selectedDistrict}</h3>
              
              {/* Charts Section */}
              <div className="charts-section">
                <div className="chart-container">
                  <EmploymentChart data={mgnregaData} />
                </div>
                <div className="chart-container">
                  <ExpenditureChart data={mgnregaData} />
                </div>
              </div>
              
              {/* Data Cards */}
              {mgnregaData.map((data, index) => (
                <div key={index} className="data-card">
                  <h4>{data.month} {data.fin_year}</h4>
                  <div className="data-grid">
                    <div className="data-item">
                      <strong>Total Households Worked:</strong> {data.total_households_worked?.toLocaleString()}
                    </div>
                    <div className="data-item">
                      <strong>Total Individuals Worked:</strong> {data.total_individuals_worked?.toLocaleString()}
                    </div>
                    <div className="data-item">
                      <strong>Total Expenditure:</strong> ₹{data.total_exp?.toLocaleString()} lakhs
                    </div>
                    <div className="data-item">
                      <strong>Wages:</strong> ₹{data.wages?.toLocaleString()} lakhs
                    </div>
                    <div className="data-item">
                      <strong>Women Persondays:</strong> {data.women_persondays?.toLocaleString()}
                    </div>
                    <div className="data-item">
                      <strong>Average Wage Rate:</strong> ₹{data.average_wage_rate} per day
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </header>
      ) : (
        <About />
      )}
    </div>
  );
}

export default App;