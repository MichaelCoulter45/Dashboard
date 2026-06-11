import React from 'react';


function GoalProgressBar({ goal, progress }) {
    // Must be between 0 and 100
    const clampProgress = Math.min(100, Math.max(0, progress));

    // Bar styling
    const containerStyle = {
        height: '20px',
        width: '100%',
        backgroundColor: '#e0e0de',
        borderRadius: '50px',
        margin: '10px 0'
    };

    const fillerStyle = {
        height: '100%',
        width: `${clampProgress}%`,
        backgroundColor: '#2bdc40',
        borderRadius: 'inherit',
        transition: 'width 0.2s ease-in-out',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'flex-end'
    };

    const labelStyle = {
        padding: '5px',
        color: 'white',
        fontWeight: 'bold',
        fontSize: '12px'
    };

    return (
        <div>
            <p>{goal}</p>
            <div style={containerStyle}>
                <div style={fillerStyle}>
                    {clampProgress > 5 && <span style={labelStyle}>{`${clampProgress}%`}</span>}
                </div>
            </div>
        </div>
    )
};

export default GoalProgressBar;