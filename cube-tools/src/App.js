import cardsData from './top100.json';
import {BrowserRouter, Routes, Route, NavLink, Navigate} from 'react-router-dom';
import './App.css';
import React from 'react';



function Home() {
  return (
    <div className="home-text">
      <p>Welcome to cube-tools.com!</p>
      <p>This website uses CubeCobra exports to compute top inclusions and recomendations for given cube ids.</p>
      <p>Made by Kalani Battson.</p>
    </div>
  );
}

function TopCards() {
  const [page, setPage] = React.useState(0);
  const pageSize = 20;
  const start = page * pageSize;
  const paginated = cardsData.slice(start, start + pageSize);
  
  return (
    <div className="card-list">
      {paginated.map((card, index) => (
      <div className="card-item" key = {card.name}>
        {start + index + 1}. {card.name} in {card.count} cubes
        <div className="card-preview">
          <img src={card.image.replace('/small/', '/normal/')} alt={card.name} />
        </div>
      </div>
      ))}
      <div className="pagination">
        <button onClick={() => setPage(p => p - 1)} disabled={page === 0}>Previous</button>
        <span>{page + 1} / {Math.ceil(cardsData.length / pageSize)}</span>
        <button onClick={() => setPage(p => p + 1)} disabled={start + pageSize >= cardsData.length}>Next</button>
      </div>
    </div>
  );
}

function Recommender() {
  const [cubeId, setCubeId] = React.useState('');
  const [recs, setRecs] = React.useState([]);
  const [loading, setLoading] = React.useState(false);
  const [page, setPage] = React.useState(0);
  const pageSize = 20;
  const start = page * pageSize;
  const paginated = recs.slice(start, start + pageSize);

  async function handleSubmit() {
    setLoading(true);
    const res = await fetch(`http://localhost:5000/recommend?cube_id=${cubeId}`);
    const data = await res.json();
    setRecs(data);
    setPage(0)
    setLoading(false);
  }

  return (
    <div className="card-list">
      <div className="recommender-input">
        <input
          type="text"
          placeholder="Enter cube ID..."
          value={cubeId}
          onChange={e => setCubeId(e.target.value)}
          className="recommender-text"
        />
        <button onClick={handleSubmit} className="recommender-button">
          {loading ? 'Loading...' : 'Get Recs'}
        </button>
      </div>
      {paginated.map(([card, score], index) => (
        <div className="card-item" key={card.name}>
          {start + index + 1}. {card.name} - {score.toFixed(2)}
          <div className="card-preview">
            <img src={card.image.replace('/small/', '/normal/')} alt={card.name} />
          </div>
        </div>
      ))}
      {recs.length > 0 && (
        <div className="pagination">
          <button onClick={() => setPage(p => p - 1)} disabled={page === 0}>Previous</button>
          <span>{page + 1} / {Math.ceil(recs.length / pageSize)}</span>
          <button onClick={() => setPage(p => p + 1)} disabled={start + pageSize >= recs.length}>Next</button>
        </div>
      )}
    </div>
  );
}

function App() {
  return (
    <BrowserRouter>
      <nav>
        <div className="nav-links">
          <NavLink to="/home">Home</NavLink>
          <NavLink to="/topcards">Top Cards</NavLink>
          <NavLink to="/recommender">Recommender</NavLink>
        </div>
      </nav>
      <Routes>
        <Route path="/" element={<Navigate to="/home" replace />} />
        <Route path="/home" element={<Home />} />        
        <Route path="/topcards" element={<TopCards />} />
        <Route path="/recommender" element={<Recommender />} />
      </Routes>
    </BrowserRouter>    
  );
}

export default App;
