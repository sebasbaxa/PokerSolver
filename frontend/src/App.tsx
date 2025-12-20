import RangePresets from './components/RangePresets'
import RangeBuilder from './components/RangeBuilder'
import './App.css'

function App() {
  return (
    <div className="min-h-screen bg-gray-100">
      <header className="bg-green-700 text-white p-6">
        <h1 className="text-3xl font-bold">Poker Solver</h1>
      </header>
      <main className="container mx-auto py-8">
        <RangeBuilder />
      </main>
    </div>
  )
}

export default App