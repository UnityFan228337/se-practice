import { useEffect, useMemo, useState } from 'react';
import { checkRoom } from './booking';
import { filterRooms } from './filter';
import { ROOMS } from './rooms';

const equipmentOptions = ['projector', 'whiteboard', 'video', 'audio'];

const toMinutes = (value: string) => {
  const [hours, minutes] = value.split(':').map(Number);
  return hours * 60 + minutes;
};

const fmt = (minutes: number) => `${String(Math.floor(minutes / 60)).padStart(2, '0')}:${String(minutes % 60).padStart(2, '0')}`;

export default function App() {
  const [attendees, setAttendees] = useState(8);
  const [selectedEquipment, setSelectedEquipment] = useState<string[]>(['projector']);
  const [roomId, setRoomId] = useState('a101');
  const [now, setNow] = useState('09:00');
  const [start, setStart] = useState('10:00');
  const [end, setEnd] = useState('11:00');
  const [result, setResult] = useState<boolean | null>(null);
  const [error, setError] = useState('');

  const filteredRooms = useMemo(
    () => filterRooms(ROOMS, { attendees, equipment: selectedEquipment }),
    [attendees, selectedEquipment],
  );

  useEffect(() => {
    setResult(null);
    setError('');

    if (!filteredRooms.some((room) => room.id === roomId)) {
      if (filteredRooms[0]) {
        setRoomId(filteredRooms[0].id);
      }
    }
  }, [filteredRooms, roomId]);

  const selectedRoom = ROOMS.find((room) => room.id === roomId) ?? filteredRooms[0] ?? ROOMS[0];

  const toggleEquipment = (equipment: string) => {
    setSelectedEquipment((current) => {
      if (current.includes(equipment)) {
        return current.filter((item) => item !== equipment);
      }
      return [...current, equipment];
    });
  };

  function check() {
    if (!selectedRoom) {
      setError('No room matches the current filter.');
      setResult(null);
      return;
    }

    const s = toMinutes(start);
    const e = toMinutes(end);
    const n = toMinutes(now);

    const available = checkRoom(ROOMS, selectedRoom.id, { start: s, end: e, now: n });
    setError(available ? '' : 'The selected room is unavailable for that booking.');
    setResult(available);
  }

  return (
    <main className="page">
      <h1>Smart Campus Room Availability</h1>

      <div className="filters panel">
        <label>
          Attendees
          <input
            type="number"
            min="1"
            value={attendees}
            onChange={(event) => setAttendees(Number(event.target.value) || 1)}
          />
        </label>

        <div className="equipment-picker">
          <span>Equipment</span>
          {equipmentOptions.map((equipment) => (
            <label key={equipment} className="inline-check">
              <input
                type="checkbox"
                checked={selectedEquipment.includes(equipment)}
                onChange={() => toggleEquipment(equipment)}
              />
              {equipment}
            </label>
          ))}
        </div>
      </div>

      <div className="row panel">
        <label>
          Room
          <select value={roomId} onChange={(event) => setRoomId(event.target.value)}>
            {filteredRooms.length ? (
              filteredRooms.map((room) => (
                <option key={room.id} value={room.id}>
                  {room.name}
                </option>
              ))
            ) : (
              <option value={selectedRoom.id}>{selectedRoom.name}</option>
            )}
          </select>
        </label>

        <label>
          Current time
          <input type="time" value={now} onChange={(event) => setNow(event.target.value)} />
        </label>

        <label>
          Start
          <input type="time" value={start} onChange={(event) => setStart(event.target.value)} />
        </label>

        <label>
          End
          <input type="time" value={end} onChange={(event) => setEnd(event.target.value)} />
        </label>
      </div>

      <button type="button" onClick={check}>Check availability</button>

      {error && <p className="error">{error}</p>}

      {filteredRooms.length === 0 ? (
        <p className="empty-state">No rooms match the selected capacity and equipment.</p>
      ) : null}

      {result !== null && (
        <p className={`result ${result ? 'available' : 'unavailable'}`}>
          {result ? 'Available' : 'Unavailable'}
        </p>
      )}

      <section>
        <h2>Existing bookings for {selectedRoom.name}</h2>
        <ul>
          {selectedRoom.bookings.length ? (
            selectedRoom.bookings.map((booking, index) => (
              <li key={`${selectedRoom.id}-${index}`}>
                {fmt(booking.start)}–{fmt(booking.end)}
              </li>
            ))
          ) : (
            <li>none</li>
          )}
        </ul>
      </section>
    </main>
  );
}
