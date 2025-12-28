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
  // Build the style object using CSS variables for dark theme
  const cellStyle: React.CSSProperties = {
    position: 'relative',
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    aspectRatio: '1',
    width: '50px',
    height: '50px',
    border: '1px solid var(--color-border)',
    borderRadius: 'var(--radius-sm)',
    cursor: 'pointer',
    userSelect: 'none',
    transition: 'all 150ms',
    backgroundColor: isSelected ? 'var(--color-accent-success)' : 'var(--color-bg-tertiary)',
    borderColor: isSelected ? '#20863a' : 'var(--color-border)',
    fontWeight: isSelected ? 'bold' : 'normal',
    transform: isHovered ? 'scale(1.05)' : 'scale(1)',
    boxShadow: isHovered ? 'var(--shadow-md)' : 'none',
    zIndex: isHovered ? 10 : 1,
  };

  const handLabelStyle: React.CSSProperties = {
    fontSize: '13px',
    fontWeight: 600,
    color: isSelected ? '#FFFFFF' : 'var(--color-text-primary)',
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
