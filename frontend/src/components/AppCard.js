import './AppCard.css';

function AppCard({className, logo}) {
  return (
    <div className={`AppCard ${className}`}>
        <img src={logo} className="App-logo" alt="logo" />
    </div>
  )
}
export default AppCard;