interface GridCellProps {
  hand: string;
  row: number;
  col: number;
  isSelected: boolean;
  isHovered: boolean;
  onMouseEnter: () => void;
  onMouseLeave: () => void;
  onClick: () => void;
}

export default function GridCell({
  hand,
  isSelected,
  isHovered,
  onMouseEnter,
  onMouseLeave,
  onClick,
}: GridCellProps) {
  // Default color: light blueish gray
  const defaultColor = '#E0E7EF';  // light blueish gray

  // Build the style object
  const cellStyle: React.CSSProperties = {
    position: 'relative',
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    aspectRatio: '1',
    width: '50px',
    height: '50px',
    border: '1px solid #D1D5DB',
    cursor: 'pointer',
    userSelect: 'none',
    transition: 'all 150ms',
    backgroundColor: isSelected ? '#4ADE80' : defaultColor,
    borderColor: isSelected ? '#16A34A' : '#9CA3AF',
    fontWeight: isSelected ? 'bold' : 'normal',
    transform: isHovered ? 'scale(1.05)' : 'scale(1)',
    boxShadow: isHovered ? '0 10px 15px -3px rgba(0, 0, 0, 0.1)' : 'none',
    zIndex: isHovered ? 10 : 1,
  };

  const handLabelStyle: React.CSSProperties = {
    fontSize: '13px',
    fontWeight: 600,
    color: isSelected ? '#FFFFFF' : '#374151',
    marginBottom: '2px',
  };

  return (
    <div
      style={cellStyle}
      onMouseEnter={onMouseEnter}
      onMouseLeave={onMouseLeave}
      onClick={onClick}
    >
      <span style={handLabelStyle}>
        {hand}
      </span>
    </div>
  );
}
