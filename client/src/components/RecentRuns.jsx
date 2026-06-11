import React from 'react';

const RecentRunsTable = () => {
    const data = [
        { id: 1, Date: 'Jun 1', Distance: '8 mi', AvgPace:'7:10', Time:'53:40' },
        { id: 2, Date: 'Jun 2', Distance: '8 mi', AvgPace:'7:50', Time:'46:40' },
        { id: 3, Date: 'Jun 3', Distance: '8 mi', AvgPace:'7:45', Time:'52:40' },
        { id: 4, Date: 'Jun 4', Distance: '8 mi', AvgPace:'7:05', Time:'40:50' },
        { id: 5, Date: 'Jun 5', Distance: '8 mi', AvgPace:'7:20', Time:'58:40' },
    ];
    return (
        <table>
            <thead>
                <tr>
                    <th>id</th>
                    <th>Date</th>
                    <th>Distance</th>
                    <th>AvgPace</th>
                    <th>Time</th>
                </tr>
            </thead>
            <tbody>
                {data.map(session => (
                    <tr key={session.id}>
                        <td>{session.id}</td>
                        <td>{session.Date}</td>
                        <td>{session.Distance}</td>
                        <td>{session.AvgPace}</td>
                        <td>{session.Time}</td>
                    </tr>
                ))}
            </tbody>
        </table>
    ); 
};

export default RecentRunsTable;