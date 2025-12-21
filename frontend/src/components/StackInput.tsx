interface StackInputProps {
  label: string;
  value: number;
  onChange: (value: number) => void;
}

export default function StackInput({ label, value, onChange }: StackInputProps) {
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newValue = parseFloat(e.target.value);
    if (!isNaN(newValue) && newValue >= 0) {
      onChange(newValue);
    }
  };

  return (
    <div className="stack-input">
      <label>{label}</label>
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