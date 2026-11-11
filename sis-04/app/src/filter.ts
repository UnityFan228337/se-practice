import type { Room } from './rooms';

export function filterRooms(
  rooms: Room[],
  criteria: { attendees: number; equipment: string[] },
): Room[] {
  const required = (criteria.equipment ?? []).map((item) => item.trim().toLowerCase());

  return rooms.filter((room) => {
    if (room.capacity < criteria.attendees) {
      return false;
    }

    return required.every((item) => room.equipment.some((has) => has.toLowerCase() === item));
  });
}
