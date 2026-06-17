
export interface Header {
  song_meta: {
    vanilla_instruments: number;
    length: number;
    layers: number;
    tempo: number;
    looping: {
      enabled: boolean;
      count: number | null;
      start_tick: number;
    }
  },
  song_info: {
    name: string;
    author: string;
    original_author: string;
    description: string;
  },
  song_stats: {
    minutes_spent: number,
    left_clicks: number;
    right_clicks: number;
    note_blocks_added: number;
    note_blocks_removed: number;
  },
  editor_info: {
    time_signature: number;
    midi_schematic_file_name: string;
    auto_saving: {
      enabled: boolean;
      duration: number;
    }
  }
}
