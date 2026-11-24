"""HW2 · club.py: the club and its chat bot. Practises Session 4 (each class has one job),
Session 5 (importing your own modules and the standard library) and Session 6 (catching only
the errors you expect)."""

from errors import SignupError, UnknownEventError
from event import Event


class Club:
    """A student club. It finds events by title; each Event looks after its own seats."""

    def __init__(self, name: str):
        """Provided: a club with no events yet."""
        self.name = name
        self.events: dict[str, Event] = {}

    def add_event(self, title: str, capacity: int) -> Event:
        """Make a new Event, store it under its title, and return it."""
        if title == "":
            raise ValueError("Event title can't be empty")
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        if title in self.events:
            raise ValueError("Event alreaydy exists")

        new_event = Event(title, capacity)
        self.events[title] = new_event
        return new_event
    def event(self, title: str) -> Event:
        """Return the event with this title, or raise UnknownEventError."""
        try:
            return self.events[title]
        except KeyError:
            raise UnknownEventError(title)
        
    
    def handle(self, line: str) -> str:
        """Answer one chat command with one sentence."""

        parts = line.split(",")

        if len(parts) != 3:
            return f"Sorry, I don't understand {line!r}."

        command = parts[0].strip().lower()
        title = parts[1].strip()
        member = parts[2].strip()

        try:
            current_event = self.event(title)

            if command == "join":
                result = current_event.sign_up(member)

                if result == "seat":
                    return f"{member} has a seat at {title}."

                return f"{member} is on the waitlist for {title}."

            if command == "leave":
                promoted_member = current_event.cancel(member)

                if promoted_member is not None:
                    return (
                        f"{member} left {title}. "
                        f"{promoted_member} gets the seat."
                    )

                return f"{member} left {title}."

            return f"Sorry, I don't understand {line!r}."

        except SignupError as error:
            return f"Sorry, {error}."

    def attendance(self) -> dict[str, int]:
        """How many events each member has a seat at. The waitlist does not count."""
        member_counts = {}

        for current_event in self.events.values():
            for member in current_event.seats:
                if member not in member_counts:
                    member_counts[member] = 0

                member_counts[member] += 1
        return member_counts

if __name__ == "__main__":
    # Provided: a short run of the chat bot. It runs only with `python club.py`, not on import.
    club = Club("Harbour.Space Bangkok club")
    club.add_event("Muay Thai basics", 2)
    for line in [
        "join, Muay Thai basics, Nino",
        "join, Muay Thai basics, Aung",
        "join, Muay Thai basics, Tashi",
        "leave, Muay Thai basics, Nino",
        "join, Chess night, Ploy",
    ]:
        print(club.handle(line))
