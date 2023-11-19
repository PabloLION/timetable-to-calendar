from typing import NamedTuple


class Names(NamedTuple):
    shortened: str
    full: str


EVENT_ID_TO_EVENT_NAME: dict[str, Names] = {
    "1": Names("SAGE", "Sustainability and Green Engineering"),
    "2": Names("AHPC", "Advanced High Performance Computing"),
    "3": Names("DTAS", "Data Transmission and Security"),
    "4": Names("CPS", "Cyberphysical Systems"),
    "5": Names("DAODM", "Data Analysis, Optimization and Decision Making"),
    "6": Names("ETIR", "Engineering Technology, Innovation and Research"),
    "7": Names("CADM", "Cloud App Development and Management"),
    "8": Names("DTAC", "Data Transmission and Cryptography"),
    "9": Names("SIND", "Smart Industry"),
    "10": Names("DLEA", "Deep Learning"),
}
