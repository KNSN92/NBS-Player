
export interface Note {
  instrument: number, // u8
  key: number, // u8
  volume: number, // u8
  panning: number, // u8
  pitch: number, // i16
}

export type Tick = number;
export type LayerId = number;

export type NotesInTick = [LayerId, Note][];

export type NoteBlocks = Record<Tick, NotesInTick>;
