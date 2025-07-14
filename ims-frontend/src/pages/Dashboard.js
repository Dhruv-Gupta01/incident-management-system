import React, { useEffect, useState } from 'react';
import API from '../api';
import '../App.css';
import Navbar from '../components/Navbar';


export default function Dashboard() {
  const [incidents, setIncidents] = useState([]);
  const [form, setForm] = useState({
    reporter_name: '',
    details: '',
    priority: 'Medium',
    status: 'Open',
    is_enterprise: false,
  });

  const fetchIncidents = async () => {
    try {
      const res = await API.get('/incidents/');
      setIncidents(res.data);
    } catch (err) {
      console.error('Error fetching incidents', err);
    }
  };

  const createIncident = async () => {
    try {
      await API.post('/incidents/', form);
      fetchIncidents();
    } catch (err) {
      alert('Failed to create incident');
    }
  };

  useEffect(() => {
    fetchIncidents();
  }, []);

  return (
    <>
        <Navbar />
        <div className="container">
        <h2>Incident Dashboard</h2>

        <h3>Create Incident</h3>
        <input name="reporter_name" onChange={(e) => setForm({ ...form, reporter_name: e.target.value })} placeholder="Reporter Name" />
        <input name="details" onChange={(e) => setForm({ ...form, details: e.target.value })} placeholder="Details" />
        <select onChange={(e) => setForm({ ...form, priority: e.target.value })}>
            <option value="High">High</option>
            <option value="Medium">Medium</option>
            <option value="Low">Low</option>
        </select>
        <select onChange={(e) => setForm({ ...form, status: e.target.value })}>
            <option value="Open">Open</option>
            <option value="In progress">In progress</option>
            <option value="Closed">Closed</option>
        </select>
        <label>
            <input type="checkbox" onChange={(e) => setForm({ ...form, is_enterprise: e.target.checked })} />
            Enterprise
        </label>
        <button onClick={createIncident}>Submit</button>

        <h3 style={{ marginTop: '2rem' }}>Your Incidents</h3>
        {incidents.map((item) => (
            <div className="incident" key={item.id}>
            <b>{item.incident_id}</b><br />
            {item.details} - <i>{item.status}</i><br />
            <small>{item.priority} Priority</small>
            </div>
        ))}
        </div>
    </>
  );
}
