import { useState } from 'react';
import StackInput from '../components/StackInput';
import PotInput from '../components/PotInput';
import FlopSelector from '../components/FlopSelector';
import PlayerRangeButton from '../components/PlayerRangeButton';

export default function SetupPage() {
  const [oopStack, setOopStack] = useState<number>(100);
  const [ipStack, setIpStack] = useState<number>(100);
  const [pot, setPot] = useState<number>(10);
  const [flop, setFlop] = useState<string[]>([]);
  const [oopRange, setOopRange] = useState<string[]>([]);
  const [ipRange, setIpRange] = useState<string[]>([]);

  const handleSolve = () => {
    console.log('Solving with:', {
      oopStack,
      ipStack,
      pot,
      flop,
      oopRange,
      ipRange
    });
    // TODO: Call solver API
  };

  return (
    <div className="setup-page">
      <h1>Poker Solver Setup</h1>
      
      <div className="setup-section">
        <h2>Stack Sizes</h2>
        <StackInput label="OOP Stack" value={oopStack} onChange={setOopStack} />
        <StackInput label="IP Stack" value={ipStack} onChange={setIpStack} />
      </div>

      <div className="setup-section">
        <h2>Pot Size</h2>
        <PotInput value={pot} onChange={setPot} />
      </div>

      <div className="setup-section">
        <h2>Flop</h2>
        <FlopSelector selectedCards={flop} onCardsChange={setFlop} />
      </div>

      <div className="setup-section">
        <h2>Player Ranges</h2>
        <div className="range-buttons">
          <PlayerRangeButton
            player="OOP"
            selectedHands={oopRange}
            onRangeChange={setOopRange}
          />
          <PlayerRangeButton
            player="IP"
            selectedHands={ipRange}
            onRangeChange={setIpRange}
          />
        </div>
      </div>

      <button 
        className="solve-button" 
        onClick={handleSolve}
        disabled={flop.length !== 3 || oopRange.length === 0 || ipRange.length === 0}
      >
        Solve
      </button>
    </div>
  );
}