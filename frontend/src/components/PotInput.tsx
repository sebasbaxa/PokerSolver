interface PotInputProps {
  value: number;
  onChange: (value: number) => void;
}

export default function PotInput({ value, onChange }: PotInputProps) {
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newValue = parseFloat(e.target.value);
    if (!isNaN(newValue) && newValue >= 0) {
      onChange(newValue);
    }
  };

  return (
    <div className="pot-input">
      <label>Pot Size</label>
      <input
        type="number"
        value={value}
        onChange={handleChange}
        min="0"
        step="0.5"
        className="input-field"
      />
      <span className="unit">BB</span>
    </div>
  );
}