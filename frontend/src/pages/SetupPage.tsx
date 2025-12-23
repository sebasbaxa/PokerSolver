import { useState } from 'react';
import StackInput from '../components/StackInput';
import PotInput from '../components/PotInput';
import FlopSelector from '../components/FlopSelector';
import PlayerRangeButton from '../components/PlayerRangeButton';
import { solverApi, type SolveResponse, type SolveRequest } from '../api/solver';

export default function SetupPage() {
  // game parameter states
  const [oopStack, setOopStack] = useState<number>(100);
  const [ipStack, setIpStack] = useState<number>(100);
  const [pot, setPot] = useState<number>(10);
  const [flop, setFlop] = useState<string[]>([]);
  const [oopRange, setOopRange] = useState<string[]>([]);
  const [ipRange, setIpRange] = useState<string[]>([]);

  // api states  
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<SolveResponse | null>(null);

  const handleSolve = async () => {
    console.log('Solving with:', {
      oopStack,
      ipStack,
      pot,
      flop,
      oopRange,
      ipRange
    });

    setLoading(true);
    setError(null);

    try { 
      const req: SolveRequest = {
        oop_range: oopRange,
        ip_range: ipRange,
        oop_stack: oopStack,
        ip_stack: ipStack,
        oop_contribution: 0,  // implementing this later
        ip_contribution: 0,   // implementing this later
        pot,
        flop
      }

      const response = await solverApi.solve(req);
      console.log('Solver response:', response);
      setResult(response);
    } catch (err: any) {
      setError('Failed to solve the game. Please try again.');
      setLoading(false);
    } finally {
      setLoading(false);
    }
    


    // TODO: Call solver API
  };

  return (
    <div className="setup-page">
      <h1>Poker Solver Setup</h1>
      
      <div className="setup-row">
        <div className="setup-section half-width">
          <h2>Stack Sizes</h2>
          <StackInput label="OOP Stack" value={oopStack} onChange={setOopStack} />
          <StackInput label="IP Stack" value={ipStack} onChange={setIpStack} />
        </div>

        <div className="setup-section half-width">
          <h2>Pot Size</h2>
          <PotInput value={pot} onChange={setPot} />
        </div>
      </div>

      <div className="setup-row">
        <div className="setup-section half-width">
          <h2>Flop</h2>
          <FlopSelector selectedCards={flop} onCardsChange={setFlop} />
        </div>

        <div className="setup-section half-width">
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
      </div>

      <button 
        className="solve-button" 
        onClick={handleSolve}
        disabled={loading || flop.length !== 3 || oopRange.length === 0 || ipRange.length === 0}
      >
        {loading ? 'Solving...' : 'Solve'}
      </button>

      <div className="solver-output">
        {/* Error Display */}
            {error && (
                <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-6">
                    {error}
                </div>
            )}

            {/* Results Display */}
            {result && (
                <div className="bg-white p-6 rounded-lg shadow-md">
                    <h2 className="text-xl font-semibold mb-4">Solver Results</h2>
                    <p className="text-gray-600 mb-4">{result.message}</p>
                    
                    {/* TODO: Add proper strategy visualization here */}
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div>
                            <h3 className="font-semibold mb-2">OOP Strategy ({result.oop_strategy.length} hands)</h3>
                            <pre className="bg-gray-100 p-2 rounded text-xs overflow-auto max-h-60">
                                {JSON.stringify(result.oop_strategy.slice(0, 5), null, 2)}
                            </pre>
                        </div>
                        
                        <div>
                            <h3 className="font-semibold mb-2">IP Strategy ({result.ip_strategy.length} hands)</h3>
                            <pre className="bg-gray-100 p-2 rounded text-xs overflow-auto max-h-60">
                                {JSON.stringify(result.ip_strategy.slice(0, 5), null, 2)}
                            </pre>
                        </div>
                    </div>
                </div>
            )}
      </div>
    </div>
  );
}