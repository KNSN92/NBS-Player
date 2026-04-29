
export type Instrument = "Piano" |
  "DoubleBass" |
  "BassDrum" |
  "SnareDrum" |
  "Click" |
  "Guitar" |
  "Flute" |
  "Bell" |
  "Chime" |
  "Xylophone" |
  "IronXylophone" |
  "CowBell" |
  "Didgeridoo" |
  "Bit" |
  "Banjo" |
  "Pling" |
  number;

export interface Note {
  instrument: Instrument;
  key: number;
  volume: number;
  panning: number;
  pitch: number;
}

export type NotesInTick = {layer: number, note: Note}[];
