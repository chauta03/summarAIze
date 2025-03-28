import './LiveTranscription.css';
import ggMeet from '../assets/ggMeet.svg';
import microsoftTeams from '../assets/microsoftTeams.svg';
import zoom from '../assets/zoom.svg';
import AppCard from '../components/AppCard';

function App() {
  const logos = [ggMeet, microsoftTeams, zoom];

  return (
    <div className="LiveTranscription" id="transcription">
      <header className="LiveTranscription-header">
        <h1>live transcription</h1>
        <h2>connect with</h2>
      </header>
      <div className="LiveTranscription-body">
        {logos.map((logo, index) => (
          <AppCard key={index} className={`card ${index % 2 === 0 ? "odd" : "middle"}`} logo={logo} />
        ))}
      </div>
    </div>
  );
}

export default App;
