import React, { useState, useEffect } from 'react';
import { Dropdown } from 'primereact/dropdown'

const AddNew = ({ onSendData}) => { 

    // State variables
    const [drNum, setDrNum] = useState('');
    const [areaId, setAreaId] = useState('');
    const [reportDistNo, setReportDistNo] = useState('');
    const [weapon, setWeapon] = useState('');
    const [status, setStatus] = useState('');
    const [premise, setPremise] = useState('');
    const [mocodes, setMocodes] = useState('');
    const [victAge, setVictAge] = useState('');
    const [victSex, setVictSex] = useState('');
    const [victDescent, setVictDescent] = useState('');
    const [streetAddress, setStreetAddress] = useState('');
    const [crossStreet, setCrossStreet] = useState('');
    const [lat, setLat] = useState('');
    const [lon, setLon] = useState('');
    const [crmCd1, setCrmCd1] = useState('');
    const [crmCd2, setCrmCd2] = useState('');
    const [crmCd3, setCrmCd3] = useState('');
    const [crmCd4, setCrmCd4] = useState('');
    const [dateOcc, setDateOcc] = useState('');
    const [TimeOcc, setTimeOcc] = useState('');

    // Dropdown options
    const area_ids = ['01','02','03','04','05','06','07','08','09','10','11',
                      '12','13','14','15','16','17','18','19','20','21']
    const statuses = ['AA', 'AO', 'IC', 'JA', 'JO' ,'CC']
    const sex_list = ['M', 'F', 'X']
    const descents = ['A', 'B', 'C', 'D', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'O', 'P', 'S', 'U', 'V', 'W', 'X', 'Z']
    
    // Fetch data from CSV files for dropdown options
    const [crmCds, setCrmCds] = useState([]);
    const [reportDistNos, setReportDistNos] = useState([]);
    const [weapons, setWeapons] = useState([]);
    const [premises, setPremises] = useState([]);

    useEffect(() => {
      Promise.all([
        fetch('crm_cds.csv').then(r => r.text()),
        fetch('report_dist_nos.csv').then(r => r.text()),
        fetch('weapons.csv').then(r => r.text()),
        fetch('premises.csv').then(r => r.text()),
      ])
      .then(([crmCdsData, reportDistNosData, weaponsData, premisesData]) => {
        const processFile = (text) => {
          const lines = text.split('\n').map(l => l.trim()).filter(l => l !== '');
          const dataLines = lines.slice(1);
          return dataLines.sort();
        };
        setCrmCds(processFile(crmCdsData));
        setReportDistNos(processFile(reportDistNosData));
        setWeapons(processFile(weaponsData));
        setPremises(processFile(premisesData));
      })
    }, [])

    const handleSubmit = (e) => {
      e.preventDefault();
      
      // JSON format for POST request
      const formData = {
        dr_no: String(drNum),
        area: areaId,
        rpt_dist_no: reportDistNo,
        weapon: weapon,
        status: status,
        premise: premise,
        mocodes: mocodes,
        victim: {
          vict_age: victAge,
          vict_sex: victSex,
          vict_descent: victDescent,
        },
        location: {
          street_address: streetAddress,
          cross_street: crossStreet,
          lat: lat,
          lon: lon,
        },
        crimereportcode: {
          crm_cd_1: crmCd1,
          crm_cd_2: crmCd2,
          crm_cd_3: crmCd3,
          crm_cd_4: crmCd4,
        },
        crimedate: {
          date_occ: dateOcc,
          time_occ: TimeOcc,
        },
      };
    
      onSendData(formData);
    };

    return (
        <div>
          <h2>Add New Crime Report</h2>
          <form onSubmit={handleSubmit} className="form-container" >
          <div>
          <label>
            Type Specific Record 5 Digit Number:
            <input
              type="number"
              name="dr_no"
              value={drNum}
              onChange={(e) => setDrNum(e.target.value)}
            />
          </label>
          <label style={{ border: '2px solid #000', padding: '5px', display: 'inline-block' }}>
            <Dropdown
              value={areaId}
              options={area_ids}
              onChange={(e) => setAreaId(e.value)}
              placeholder='Select Area ID'
              checkmark={true}
            />
          </label>
          <label style={{ border: '2px solid #000', padding: '5px', display: 'inline-block' }}>
            <Dropdown
              value={reportDistNo}
              options={reportDistNos}
              onChange={(e) => setReportDistNo(e.value)}
              placeholder='Select Report District Number'
              checkmark={true}
            />
          </label>
          <div style={{ display: 'flex', gap: '10px', alignItems: 'center' }}>
            <label style={{ border: '2px solid #000', padding: '5px', display: 'inline-block' }}>
              <Dropdown
                value={weapon}
                options={weapons}
                onChange={(e) => setWeapon(e.value)}
                placeholder="Select Weapon"
                checkmark={true}
              />
            </label>
            <label style={{ border: '2px solid #000', padding: '5px', display: 'inline-block' }}>
              <Dropdown
                value={status}
                options={statuses}
                onChange={(e) => setStatus(e.value)}
                placeholder="Select Status"
                checkmark={true}
              />
            </label>
            <label style={{ border: '2px solid #000', padding: '5px', display: 'inline-block' }}>
              <Dropdown
                value={premise}
                options={premises}
                onChange={(e) => setPremise(e.value)}
                placeholder="Select Premise"
                checkmark={true}
              />
            </label>
          </div>
          <label>
            Type Mocodes:
            <input
              type="text"
              name="mocodes"
              value={mocodes}
              onChange={(e) => setMocodes(e.target.value)}
            />
          </label>
          <label>
            Type Victim Age:
            <input
              type="number"
              name="vict_age"
              value={victAge}
              onChange={(e) => setVictAge(e.target.value)}
            />
          </label>
          <label style={{ border: '2px solid #000', padding: '5px', display: 'inline-block' }}>
            <Dropdown
              value={victSex}
              options = {sex_list}
              onChange={(e) => setVictSex(e.value)}
              placeholder='Select Victim Sex'
              checkmark={true}
            />
          </label>
          <label style={{ border: '2px solid #000', padding: '5px', display: 'inline-block' }}>
            <Dropdown
              value={victDescent}
              options={descents}
              onChange={(e) => setVictDescent(e.value)}
              placeholder='Select Victim Descent'
              checkmark={true}
            />
          </label>
          <label>
            Type Street Address:
            <input
              type="text"
              name="street_address"
              value={streetAddress}
              onChange={(e) => setStreetAddress(e.target.value)}
            />
          </label>
          <label>
            Type Cross Street:
            <input
              type="text"
              name="cross_street"
              value={crossStreet}
              onChange={(e) => setCrossStreet(e.target.value)}
            />
          </label>
          <label>
            Type Longitude (float):
            <input
              type="number"
              name="lon"
              value={lon}
              onChange={(e) => setLon(e.target.value)}
            />
          </label>
          <label>
            Type Latitude (float):
            <input
              type="number"
              name="lat"
              value={lat}
              onChange={(e) => setLat(e.target.value)}
            />
          </label>
          <label style={{ border: '2px solid #000', padding: '5px', display: 'inline-block' }}>
            <Dropdown
              value={crmCd1}
              options={crmCds}
              onChange={(e) => setCrmCd1(e.value)}
              placeholder="Select Primary Crime Code"
              checkmark={true}
            />
        </label>
        <label style={{ border: '2px solid #000', padding: '5px', display: 'inline-block' }}>
            <Dropdown
              value={crmCd2}
              options={crmCds}
              onChange={(e) => setCrmCd2(e.value)}
              placeholder="Select Secondary Crime Code"
              checkmark={true}
            />
        </label>
        <label style={{ border: '2px solid #000', padding: '5px', display: 'inline-block' }}>
            <Dropdown
              value={crmCd3}
              options={crmCds}
              onChange={(e) => setCrmCd3(e.value)}
              placeholder="Select Tertiary Crime Code"
              checkmark={true}
            />
        </label>
        <label style={{ border: '2px solid #000', padding: '5px', display: 'inline-block'}}>
            <Dropdown
              value={crmCd4}
              options={crmCds}
              onChange={(e) => setCrmCd4(e.value)}
              placeholder="Select Quaternary Crime Code"
              checkmark={true}
            />
        </label>
        <label>
            Time Occurred:
            <input
              type="time"
              name="time_occ"
              value={TimeOcc}
              onChange={(e) => setTimeOcc(e.target.value)}
            />
          </label>
          <label>
            Date Occurred:
            <input
              type="date"
              name="date_occ"
              value={dateOcc}
              onChange={(e) => setDateOcc(e.target.value)}
            />
          </label>
          <button type="submit">Add Crime Report</button>
          </div>
          </form>
        </div>
      );



};

export default AddNew;