import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate} from 'react-router-dom';
import QuerySelector from './components/QuerySelector';
import DataDisplay from './components/DataDisplay';
import AddNew from './components/AddNew';
import Register from './components/Register';
import LogIn from './components/LogIn';
import './styles.css';

function App() {
  // State variables
  const [selectedQuery, setSelectedQuery] = useState(1);
  const [data, setData] = useState(null);
  const [startTime, setStartTime] = useState('');
  const [endTime, setEndTime] = useState('');
  const [dateRptdStart, setDateRptdStart] = useState('');
  const [dateRptdEnd, setDateRptdEnd] = useState('');
  const [crmCd1, setCrmCd1] = useState('');
  const [crmCd2, setCrmCd2] = useState('');
  const [dateOccStart, setDateOccStart] = useState('');
  const [dateOccEnd, setDateOccEnd] = useState('');
  const [latMin, setLatMin] = useState('');
  const [latMax, setLatMax] = useState('');
  const [lonMin, setLonMin] = useState('');
  const [lonMax, setLonMax] = useState('');
  const [flag, setFlag] = useState('');
  const [numOcc, setNumOcc] = useState('');
  const [areaId, setAreaId] = useState('');
  const [drNum, setDrNum] = useState('');
  const [shortYear, setShortYear] = useState('');
  const [isAuthenticated, setIsAuthenticated] = useState(!!localStorage.getItem('access_token'));

  // Logic for handling login, logout and token refresh
  const handleLogin = () => {
    setIsAuthenticated(true);
  };
  
  const handleLogout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    setIsAuthenticated(false);
  };

  const refreshAccessToken = async () => {
    const refreshToken = localStorage.getItem('refresh_token');
  
    try {
      const response = await fetch('http://localhost:8000/token/refresh/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ refresh: refreshToken }),
      });
  
      if (!response.ok) {
        handleLogout();
        return null;
      }
  
      const data = await response.json();
      localStorage.setItem('access_token', data.access);
      return data.access;
    } catch (error) {
      console.error('Error refreshing access token:', error);
      handleLogout();
      return null;
    }
  };

  // Logic for sending data to the API
  const handleSendData = (formData) => {
    if (shouldSendData(formData)) {
      sendData(formData);
    }
    if (!shouldSendData(formData)) {
      console.log("shouldSendData(): ", shouldSendData(formData));
    }
  };

  const shouldSendData = (formData) => {
    const latRegex = /^-?\d{1,2}\.\d{0,8}$/;
    const lonRegex = /^-?\d{1,3}\.\d{0,8}$/;
    const numRegex = /^\d+$/;
    const num5Regex = /^\d{5}$/;
    const mocodesRegex = /^(nan|\d{4}( \d{4})*)$/;
    const addressRegex = /^[a-zA-Z0-9\s.-]+$/;

    const latInRange =  formData.location.lat >= -90 && 
                        formData.location.lat <= 90
    const lonInRange =  formData.location.lon >= -180 &&
                        formData.location.lon <= 180

    if (formData.dr_no === '' || formData.area === '' || formData.rpt_dist_no === '' ||
        formData.weapon === '' || formData.status === '' || formData.premise === '' || formData.victim.vict_age === '' || 
        formData.victim.vict_sex === '' || formData.victim.vict_descent === '' || formData.location.street_address === '' ||
        formData.crimereportcode.crm_cd_1 === '' ||formData.crimedate.date_occ === '' || formData.crimedate.time_occ === '') {
      alert('Please fill in all required fields.');
      return false;
    }
    if (!num5Regex.test(formData.dr_no)) {
      alert('Please enter a valid 5 digit DR number.');
      return false;
    }
    if (formData.mocodes === '' || formData.mocodes === '0') {
      formData.mocodes = 'nan';
    }
    if (!mocodesRegex.test(formData.mocodes)) {
      alert('Please enter valid MO codes.');
      return false;
    }
    if (!numRegex.test(formData.victim.vict_age)) {
      alert('Please enter a valid age.');
      return false;
    }
    if (!addressRegex.test(formData.location.street_address)) {
      alert('Please enter a valid street address.');
      return false;
    }
    if (formData.location.cross_street !== '') {
      if (!addressRegex.test(formData.location.cross_street)) {
        alert('Please enter a valid cross street.');
        return false;
      }
    }
    if (formData.location.lat !== '' || formData.location.lon !== '') {
      if (!latRegex.test(formData.location.lat) || !lonRegex.test(formData.location.lon) || 
          !latInRange || !lonInRange) {
        alert('Please enter valid latitude and longitude values.');
        return false;
      }
    }
    return true;
  };

  // Send data to the API
  const sendData = async (formData) => {
    try {
      const url = `http://127.0.0.1:8000/addNewCrime/`;
      let token = localStorage.getItem('access_token');
  
      console.log("Sending data to:", url);
      console.log("Sending data:", formData);
  
      let response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify(formData),
      });
  
      if (response.status === 401) {
        token = await refreshAccessToken();
        if (token) {
          response = await fetch(url, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${token}`,
            },
            body: JSON.stringify(formData),
          });
        }
        if (!token) {
          handleLogout();
          return;
        }
      }
  
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
  
      const result = await response.json();
      console.log("Server response:", result);
      alert('Crime report added successfully!');
    } catch (error) {
      console.error("Error sending data:", error);
      alert('Failed to add crime report. Please try again.');
    }
  };
  

  // Logic for Fetching data from the API
  const handleFetchData = () => {
    if (shouldFetchData()) {
      fetchData(selectedQuery);
    } 
    if (!shouldFetchData()) {
      alert('Please fill in all required fields with valid values.');
    }
  };

  // Check if all required parameters are set
  const shouldFetchData = () => {
    if (selectedQuery === 1) {
      return startTime !== '' && endTime !== '' && startTime <= endTime;
    }
    if (selectedQuery === 2) {
      return dateRptdStart !== '' && startTime !== '' && endTime !== '' && crmCd1 !== '' && startTime <= endTime;
    }
    if (selectedQuery === 3) {
      return dateOccStart !== '';
    }
    if (selectedQuery === 4) {
      const dateStart = String(dateOccStart);
      const dateEnd = String(dateOccEnd);
      return dateOccStart !== '' && dateOccEnd !== '' && dateStart <= dateEnd;
    }
    if (selectedQuery === 5) {
      const latRegex = /^-?\d{1,2}\.\d{0,8}$/;
      const lonRegex = /^-?\d{1,3}\.\d{0,8}$/;
  
      const latInRange =  latMin >= -90 && 
                          latMin <= 90 && 
                          latMax >= -90 && 
                          latMax <= 90;
      const lonInRange =  lonMin >= -180 &&
                          lonMin <= 180 &&
                          lonMax >= -180 &&
                          lonMax <= 180;
          
  
      return (
        dateOccStart !== '' &&
        latMin !== '' &&
        latMax !== '' &&
        lonMin !== '' &&
        lonMax !== '' &&
        latRegex.test(latMin) &&
        latRegex.test(latMax) &&
        lonRegex.test(lonMin) &&
        lonRegex.test(lonMax) &&
        latInRange &&
        lonInRange &&
        latMin < latMax &&
        lonMin < lonMax
      );
    }
    if (selectedQuery === 6) {
      const dateStart = String(dateRptdStart);
      const dateEnd = String(dateRptdEnd);
      return dateRptdStart !== '' && dateRptdEnd !== '' && flag !== '' && dateStart <= dateEnd;
    }
    if (selectedQuery === 7) {
      const dateStart = String(dateRptdStart);
      const dateEnd = String(dateRptdEnd);
      const dateOccStarts = String(dateOccStart);
      const dateOccEnds = String(dateOccEnd);
      return (dateRptdStart !== '' && dateRptdEnd !== '' && dateOccStart !== '' && 
              dateOccEnd !== '' && dateStart <= dateEnd && dateOccStarts <= dateOccEnds
      );
    }
    if (selectedQuery === 8) {
      const dateStart = String(dateOccStart);
      const dateEnd = String(dateOccEnd);
      return crmCd1 !== '' && dateOccStart !== '' && dateOccEnd !== '' && dateStart <= dateEnd;
    }
    if (selectedQuery === 9) {
      return true;
    }
    if (selectedQuery === 10) {
      return crmCd1 !== '' && flag !== '';
    }
    if (selectedQuery === 11) {
      return crmCd1 !== '' && crmCd2 !== '';
    }
    if (selectedQuery === 12) {
      return startTime !== '' && endTime !== '' && startTime <= endTime;
    }
    if (selectedQuery === 13) {
      const numRegex = /^\d+$/;
      return startTime !== '' && endTime !== '' && numOcc !== '' && startTime <= endTime && numRegex.test(numOcc);
    }
    if (selectedQuery === 14) {
      return areaId !== '';
    }
    if (selectedQuery === 15) {
      const numRegex = /^\d{5}$/;
      return shortYear !== '' && areaId !== '' && drNum !== '' && numRegex.test(drNum);
    }
    return true;
  };

  // Fetch data from the API
  const fetchData = async (queryNumber) => {
    try {
      // Define query parameters
      const queryParams = {
        1: { start_time: startTime, end_time: endTime },
        2: { date_rptd: dateRptdStart, start_time: startTime, end_time: endTime, crm_cd_1: crmCd1 },
        3: { date_occ: dateOccStart },
        4: { date_occ_start: dateOccStart, date_occ_end: dateOccEnd },
        5: { date_occ: dateOccStart, lat_min: latMin, lat_max: latMax, lon_min: lonMin, lon_max: lonMax },
        6: { date_rptd_start: dateRptdStart, date_rptd_end: dateRptdEnd, flag: flag },
        7: { date_rptd_start: dateRptdStart, date_rptd_end: dateRptdEnd, date_occ_start: dateOccStart, date_occ_end: dateOccEnd },
        8: { crm_cd: crmCd1, date_occ_start: dateOccStart, date_occ_end: dateOccEnd },
        9: {null: null},
        10: {crm_cd: crmCd1, flag: flag},
        11: {crm_cd1: crmCd1, crm_cd2: crmCd2},
        12: {start_time: startTime, end_time: endTime},
        13: {start_time: startTime, end_time: endTime, num_occ: numOcc},
        14: {area_id: areaId},
        15: {dr_no: shortYear + areaId + drNum}
      };
  
      // Build query parameters
      const params = new URLSearchParams(queryParams[queryNumber]);
      const url = `http://127.0.0.1:8000/query${queryNumber}/?${params.toString()}`;
      const url2 = `http://127.0.0.1:8000/query${queryNumber}/${flag}/?${params.toString()}`;
      
      const urlToFetch = flag ? url2 : url;
      console.log("Fetching data from:", urlToFetch);
  
      // Fetch data from the API
      let token = localStorage.getItem('access_token');
      let response = await fetch(urlToFetch, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
      });
  
      if (response.status === 401) {
        token = await refreshAccessToken();
        if (token) {
          response = await fetch(urlToFetch, {
            headers: {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${token}`,
            },
          });
        } 
        if (!token) {
          handleLogout();
          return;
        }
      }
  
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
  
      const result = await response.json();
      setData(result);
    } catch (error) {
      console.error("Error fetching data:", error);
      setData({ error: error.message });
    }
  };
  
  // Event handlers
  const handleSelect = (queryNumber) => {
    setSelectedQuery(queryNumber);
    setData(null);
    if (queryNumber !== 1) {
      setStartTime('');
      setEndTime('');
    }
    if (queryNumber !== 2) {
      setDateRptdStart('');
      setStartTime('');
      setEndTime('');
      setCrmCd1('');
    }
    if (queryNumber !== 3) {
      setDateOccStart('');
    }
    if (queryNumber !== 4) {
      setDateOccStart('');
      setDateOccEnd('');
    }
    if (queryNumber !== 5) {
      setDateOccStart('');
      setLatMin('');
      setLatMax('');
      setLonMin('');
      setLonMax('');
    }
    if (queryNumber !== 6) {
      setDateRptdStart('');
      setDateRptdEnd('');
      setFlag('');
    }
    if (queryNumber !== 7) {
      setDateRptdStart('');
      setDateRptdEnd('');
      setDateOccStart('');
      setDateOccEnd('');
    }
    if (queryNumber !== 8) {
      setCrmCd1('');
      setDateOccStart('');
      setDateOccEnd('');
    }
    if (queryNumber !== 9) {
      // do nothing
    }
    if (queryNumber !== 10) {
      setCrmCd1('');
      setFlag('');
    }
    if (queryNumber !== 11) {
      setCrmCd1('');
      setCrmCd2('');
    }
    if (queryNumber !== 12) {
      setStartTime('');
      setEndTime('');
    }
    if (queryNumber !== 13) {
      setStartTime('');
      setEndTime('');
      setNumOcc('');
    }
    if (queryNumber !== 14) {
      setAreaId('');
    }
    if (queryNumber !== 15) {
      setAreaId('');
      setShortYear('');
      setDrNum('');
    }
  };

  const handleTimeChange = (field, value) => {
    if (field === 'startTime') {
      setStartTime(value);
    }
    if (field === 'endTime') {
      setEndTime(value);
    }
  };

  const handleDateChange = (field, value) => {
    if (field === 'dateRptdStart') {
      setDateRptdStart(value);
    }
    if (field === 'dateRptdEnd') {
      setDateRptdEnd(value);
    }
    if (field === 'dateOccStart') {
      setDateOccStart(value);
    }
    if (field === 'dateOccEnd') {
      setDateOccEnd(value);
    }
    if (field === 'shortYear') {
      setShortYear(value);
    }
  };

  const handleCrmCdChange = (field, value) => {
    if (field === 'crmCd1') {
      setCrmCd1(value);
    }
    if (field === 'crmCd2') {
      setCrmCd2(value);
    }
  };

  const handleLatLonChange = (field, value) => {
    if (field === 'latMin') {
      setLatMin(value);
    }
    if (field === 'latMax') {
      setLatMax(value);
    }
    if (field === 'lonMin') {
      setLonMin(value);
    }
    if (field === 'lonMax') {
      setLonMax(value);
    }
  };

  const handleFlagChange = (field, value) => {
    if (field === 'flag') {
      setFlag(value);
    }
  };

  const handleNumOccChange = (field, value) => {
    if (field === 'numOcc') {
      setNumOcc(value);
    }
  };

  const handleAreaIdChange = (field, value) => {
    if (field === 'areaId') {
      setAreaId(value);
    }
  }

  const handleDrNumChange = (field, value) => {
    if (field === 'drNum') {
      setDrNum(value);
    }
  }

  return (
    <Router>
      <div className="App">
        <nav>
          <ul>
            {isAuthenticated ? (
              <>
                <li>
                  <button onClick={handleLogout}>Logout</button>
                </li>
              </>
            ) : (
              <>
                <li>
                <button onClick={() => window.location.href ="/login"}>Login</button>
                </li>
                <br />
                <li>
                <button onClick={() => window.location.href = "/register"}>Register</button>
                </li>
              </>
            )}
          </ul>
        </nav>

        <Routes>
          {isAuthenticated ? (
            <>
              <Route
                path="/home"
                element={
                  <>
                <h1>Data Viewer</h1>
                  <QuerySelector
                    selectedQuery={selectedQuery}
                    onSelect={handleSelect}
                    startTime={startTime}
                    endTime={endTime}
                    onTimeChange={handleTimeChange}
                    dateOccStart={dateOccStart}
                    dateOccEnd={dateOccEnd}
                    dateRptdStart={dateRptdStart}
                    dateRptdEnd={dateRptdEnd}
                    onDateChange={handleDateChange}
                    crmCd1={crmCd1}
                    crmCd2={crmCd2}
                    onCrmCdChange={handleCrmCdChange}
                    latMin={latMin}
                    latMax={latMax}
                    lonMin={lonMin}
                    lonMax={lonMax}
                    onLatLonChange={handleLatLonChange}
                    flag={flag}
                    onFlagChange={handleFlagChange}
                    numOcc={numOcc}
                    onNumOccChange={handleNumOccChange}
                    areaId={areaId}
                    onAreaIdChange={handleAreaIdChange}
                    shortYear={shortYear}
                    drNum={drNum}
                    onDrNumChange={handleDrNumChange}
                  />
                  <button onClick={handleFetchData} style={{ marginTop: '20px' }} disabled={!shouldFetchData()}>Fetch Data</button>
                  <DataDisplay data={data} />
                  <AddNew onSendData={handleSendData}/>
                  </>
                }
              />
              <Route path="*" element={<Navigate to="/home" replace />} />
            </>
          ) : (
            <>
              <Route path="/login" element={<LogIn onLogin={handleLogin} />} />
              <Route path="/register" element={<Register />} />
              <Route path="*" element={<Navigate to="/login" replace />} />
            </>
          )}
        </Routes>
      </div>
    </Router>
  );
}

export default App;
