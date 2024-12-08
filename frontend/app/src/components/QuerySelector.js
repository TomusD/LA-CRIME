import React, {useState, useEffect} from 'react';
import { Dropdown } from 'primereact/dropdown';

const QuerySelector = ({
  selectedQuery,
  onSelect,
  startTime,
  endTime,
  onTimeChange,
  dateRptdStart,
  dateRptdEnd,
  dateOccStart,
  dateOccEnd,
  onDateChange,
  crmCd1,
  crmCd2,
  onCrmCdChange,
  latMin,
  latMax,
  lonMin,
  lonMax,
  onLatLonChange,
  flag,
  onFlagChange,
  numOcc,
  onNumOccChange,
  areaId,
  onAreaIdChange,
  shortYear,
  drNum,
  onDrNumChange
}) => {
  
  // Array of query and dropdown options
  const queries = Array.from({ length: 15 }, (_, i) => `Query ${i + 1}`);
  const flags = ['area', 'dist'];
  const area_ids = ['01','02','03','04','05','06','07','08','09','10','11',
                    '12','13','14','15','16','17','18','19','20','21']
  const year = ['19','20','21', '22', '23', '24', '25', '26', '27', '28', '29', '30']
  const [crmCds, setCrmCds] = useState([]);

  // Data fetch for crime codes dropdown
  useEffect(() => {
    fetch('crm_cds.csv')
      .then(r => r.text())
      .then(crmCdsData => {
      const processFile = (text) => {
        const lines = text.split('\n').map(l => l.trim()).filter(l => l !== '');
        const dataLines = lines.slice(1);
        return dataLines.sort();
      };
      setCrmCds(processFile(crmCdsData));
    })
  }, [])

  return (
    <div>
      <label htmlFor="query-select">Choose a query:</label>
      <select
        id="query-select"
        value={selectedQuery}
        onChange={(e) => onSelect(Number(e.target.value))}
      >
        {queries.map((query, index) => (
          <option key={index} value={index + 1}>
            {query}
          </option>
        ))}
      </select>

      {selectedQuery === 1 && (
        <div style={{ marginTop: '10px' }}>
          <h3>Total Reports Per Crime Code Within a Time Range</h3>
          <label>
            Start Time:
            <input
              type="time"
              name="start_time"
              value={startTime}
              onChange={(e) => onTimeChange('startTime', e.target.value)}
            />
          </label>
          <label style={{ marginLeft: '10px' }}>
            End Time:
            <input
              type="time"
              name="end_time"
              value={endTime}
              onChange={(e) => onTimeChange('endTime', e.target.value)}
            />
          </label>
        </div>
      )}

      {selectedQuery === 2 && (
        <div style={{ marginTop: '10px' }}>
          <h3>Daily Reports Per Crime Code for a Specific Time Range</h3>
        <label>
          Date reported:
          <input
            type="date"
            name="date_rptd"
            value={dateRptdStart}
            onChange={(e) => onDateChange('dateRptdStart', e.target.value)}
          />
        </label>
        <label>
          Start Time:
          <input
            type="time"
            name="start_time"
            value={startTime}
            onChange={(e) => onTimeChange('startTime', e.target.value)}
          />
        </label>
        <label style={{ marginLeft: '10px' }}>
          End Time:
          <input
            type="time"
            name="end_time"
            value={endTime}
            onChange={(e) => onTimeChange('endTime', e.target.value)}
          />
        </label>
        <label style={{ border: '2px solid #000', padding: '5px', display: 'inline-block' }}>
            <Dropdown
              value={crmCd1}
              options={crmCds}
              onChange={(e) => onCrmCdChange('crmCd1', e.value)}
              placeholder="Select a Crime Code"
              checkmark={true}
            />
        </label>
      </div>
      )}

      {selectedQuery === 3 && (
        <div style={{ marginTop: '10px' }}>
          <h3>Most Common Crime Per Area on a Specific Day</h3>
          <label>
            Date occurred:
            <input
              type="date"
              name="date_occ"
              value={dateOccStart}
              onChange={(e) => onDateChange('dateOccStart', e.target.value)}
            />
          </label>
        </div>
      )}

      {selectedQuery === 4 && (
        <div style={{ marginTop: '10px' }}>
          <h3>Average Crimes Per Hour for a Date Range</h3>
          <label>
            Starting Date occurred:
            <input
              type="date"
              name="date_occ_start"
              value={dateOccStart}
              onChange={(e) => onDateChange('dateOccStart', e.target.value)}
            />
          </label>
          <label>
            Ending Date occurred:
            <input
              type="date"
              name="date_occ_end"
              value={dateOccEnd}
              onChange={(e) => onDateChange('dateOccEnd', e.target.value)}
            />
          </label>
        </div>
      )}

      {selectedQuery === 5 && (
        <div style={{ marginTop: '10px' }}>
          <h3>Most Common Crime Code in a GPS Bounding Box on a Specific Day</h3>
          <label>
            Date occurred:
            <input
              type="date"
              name="date_occ"
              value={dateOccStart}
              onChange={(e) => onDateChange('dateOccStart', e.target.value)}
            />
          </label>
          <label>
            Minimum Latitude (float):
            <input
              type="number"
              name="lat_min"
              value={latMin}
              onChange={(e) => onLatLonChange('latMin', e.target.value)}
            />
          </label>
          <label>
            Maximum Latitude (float):
            <input
              type="number"
              name="lat_max"
              value={latMax}
              onChange={(e) => onLatLonChange('latMax', e.target.value)}
            />
          </label>
          <label>
            Minimum Longitude (float):
            <input
              type="number"
              name="lon_min"
              value={lonMin}
              onChange={(e) => onLatLonChange('lonMin', e.target.value)}
            />
          </label>
          <label>
            Maximum Longitude (float):
            <input
              type="number"
              name="lon_max"
              value={lonMax}
              onChange={(e) => onLatLonChange('lonMax', e.target.value)}
            />
          </label>
        </div>
      )}

      {selectedQuery === 6 && (
        <div style={{ marginTop: '10px' }}>
          <h3>Top-5 Areas or Report District Numbers by Crimes Reported in a Date Range</h3>
          <label>
            Starting Date reported:
            <input
              type="date"
              name="date_rptd_start"
              value={dateRptdStart}
              onChange={(e) => onDateChange('dateRptdStart', e.target.value)}
            />
          </label>
          <label>
            Ending Date reported:
            <input
              type="date"
              name="date_rptd_end"
              value={dateRptdEnd}
              onChange={(e) => onDateChange('dateRptdEnd', e.target.value)}
            />
          </label>
          <label style={{ border: '2px solid #000', padding: '5px', display: 'inline-block' }}>
            <Dropdown
              value={flag}
              options={flags}
              onChange={(e) => onFlagChange('flag', e.value)}
              placeholder="Select Area or District"
              checkmark={true}
            />
        </label>
        </div>
      )}

      {selectedQuery === 7 && (
        <div style={{ marginTop: '10px' }}>
          <h3>Most Common Crime Pair in the Area with Most Reports</h3>
          <label>
            Starting Date reported:
            <input
              type="date"
              name="date_rptd_start"
              value={dateRptdStart}
              onChange={(e) => onDateChange('dateRptdStart', e.target.value)}
            />
          </label>
          <label>
            Ending Date reported:
            <input
              type="date"
              name="date_rptd_start"
              value={dateRptdEnd}
              onChange={(e) => onDateChange('dateRptdEnd', e.target.value)}
            />
          </label>
          <label>
            Starting Date occurred:
            <input
              type="date"
              name="date_occ_start"
              value={dateOccStart}
              onChange={(e) => onDateChange('dateOccStart', e.target.value)}
            />
          </label>
          <label>
            Ending Date occurred:
            <input
              type="date"
              name="date_occ_end"
              value={dateOccEnd}
              onChange={(e) => onDateChange('dateOccEnd', e.target.value)}
            />
          </label>
        </div>
      )}
      
      {selectedQuery === 8 && (
        <div style={{ marginTop: '10px' }}>
          <h3>Second Most Common Co-occurring Crime for a Specific Crime</h3>
          <label>
            Starting Date occurred:
            <input
              type="date"
              name="date_occ_start"
              value={dateOccStart}
              onChange={(e) => onDateChange('dateOccStart', e.target.value)}
            />
          </label>
          <label>
            Ending Date occurred:
            <input
              type="date"
              name="date_occ_end"
              value={dateOccEnd}
              onChange={(e) => onDateChange('dateOccEnd', e.target.value)}
            />
          </label>
          <label style={{ border: '2px solid #000', padding: '5px', display: 'inline-block' }}>
            <Dropdown
              value={crmCd1}
              options={crmCds}
              onChange={(e) => onCrmCdChange('crmCd1', e.value)}
              placeholder="Select a Crime Code"
              checkmark={true}
            />
        </label>
        </div>
      )}

      {selectedQuery === 9 && (
        <div style={{ marginTop: '10px' }}>
          <h3>Most Common Weapon Used by Victim Age Groups</h3>
          <label>
          Weapon used against victims depending on their age:
          </label>
        </div>
      )}

      {selectedQuery === 10 && (
        <div style={{ marginTop: '10px' }}>
          <h3>Longest Time Without a Specific Crime by Area or Report District Number</h3>
          <label style={{ border: '2px solid #000', padding: '5px', display: 'inline-block' }}>
            <Dropdown
              value={crmCd1}
              options={crmCds}
              onChange={(e) => onCrmCdChange('crmCd1', e.value)}
              placeholder="Select a Crime Code"
              checkmark={true}
            />
        </label>
        <label style={{ border: '2px solid #000', padding: '5px', display: 'inline-block' }}>
            <Dropdown
              value={flag}
              options={flags}
              onChange={(e) => onFlagChange('flag', e.value)}
              placeholder="Select Area or District"
              checkmark={true}
            />
        </label>
        </div>
      )}

      {selectedQuery === 11 && (
        <div style={{ marginTop: '10px' }}>
          <h3>Areas with More Than 1 Report for Two Specific Crimes on the Same Day</h3>
          <label style={{ border: '2px solid #000', padding: '5px', display: 'inline-block' }}>
            <Dropdown
              value={crmCd1}
              options={crmCds}
              onChange={(e) => onCrmCdChange('crmCd1', e.value)}
              placeholder="Select Crime Code 1"
              checkmark={true}
            />
        </label>
        <label style={{ border: '2px solid #000', padding: '5px', display: 'inline-block' }}>
            <Dropdown
              value={crmCd2}
              options={crmCds}
              onChange={(e) => onCrmCdChange('crmCd2', e.value)}
              placeholder="Select a Crime Code 2"
              checkmark={true}
            />
        </label>
        </div>
      )}

      {selectedQuery === 12 && (
        <div style={{ marginTop: '10px' }}>
          <h3>Divisions of Records for Same-Day Crimes in Different Areas with the Same Weapon</h3>
          <label>
            Start Time:
            <input
              type="time"
              name="start_time"
              value={startTime}
              onChange={(e) => onTimeChange('startTime', e.target.value)}
            />
          </label>
          <label style={{ marginLeft: '10px' }}>
            End Time:
            <input
              type="time"
              name="end_time"
              value={endTime}
              onChange={(e) => onTimeChange('endTime', e.target.value)}
            />
          </label>
        </div>
      )}

      {selectedQuery === 13 && (
        <div style={{ marginTop: '10px' }}>
          <h3>Crimes Occurring a Number of Times on the Same Day in the Same Area with the Same Weapon</h3>
          <label>
            Start Time:
            <input
              type="time"
              name="start_time"
              value={startTime}
              onChange={(e) => onTimeChange('startTime', e.target.value)}
            />
          </label>
          <label style={{ marginLeft: '10px' }}>
            End Time:
            <input
              type="time"
              name="end_time"
              value={endTime}
              onChange={(e) => onTimeChange('endTime', e.target.value)}
            />
          </label>
          <label style={{ padding: '5px', display: 'inline-block' }}>
            Number of times occurred (integer):
            <input
              type="number"
              name="num_occ"
              value={numOcc}
              onChange={(e) => onNumOccChange('numOcc', e.target.value)}
            />
          </label>
        </div>
      )}

      {selectedQuery === 14 && (
        <div style={{ marginTop: '10px' }}>
          <h3>Search For All Incidents That Took Place In An Area</h3>
          <label style={{ border: '2px solid #000', padding: '5px', display: 'inline-block' }}>
            <Dropdown
              value={areaId}
              options={area_ids}
              onChange={(e) => onAreaIdChange('areaId', e.value)}
              placeholder="Select Area ID"
              checkmark={true}
            />
        </label>
        </div>
      )}

      {selectedQuery === 15 && (
        <div style={{ marginTop: '10px' }}>
          <h3>Retrieve All Data Related to a Specific Division of Records Number</h3>
          <label style={{ border: '2px solid #000', padding: '5px', display: 'inline-block' }}>
            <Dropdown
              value={shortYear}
              options={year}
              onChange={(e) => onDateChange('shortYear', e.value)}
              placeholder="Select Year"
              checkmark={true}
            />
        </label>
          <label style={{ border: '2px solid #000', padding: '5px', display: 'inline-block' }}>
            <Dropdown
              value={areaId}
              options={area_ids}
              onChange={(e) => onAreaIdChange('areaId', e.value)}
              placeholder="Select Area ID"
              checkmark={true}
            />
        </label>
        <label>
            Specific Record 5 Digit Number:
            <input
              type="number"
              name="drNum"
              value={drNum}
              onChange={(e) => onDrNumChange('drNum', e.target.value)}
            />
          </label>
        </div>
      )}

    </div>
  );
};

export default QuerySelector;
